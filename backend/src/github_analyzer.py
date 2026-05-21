"""GitHub Repository Analyzer - Fetches commits, diffs, and issues"""
import os
from github import Github, GithubException
from typing import Dict, List, Optional
from dotenv import load_dotenv
from .code_analyzer import CodeAnalyzer

load_dotenv()

class GitHubAnalyzer:
    def __init__(self, access_token: Optional[str] = None, 
                 progress_tracker=None, session_id: str = None):
        """Initialize GitHub client with access token"""
        token = access_token or os.getenv('GITHUB_TOKEN')
        self.github = Github(token) if token else Github()
        self.rate_limit_checked = False
        self.code_analyzer = CodeAnalyzer()
        self.progress_tracker = progress_tracker
        self.session_id = session_id
    
    def check_rate_limit(self):
        """Check GitHub API rate limit"""
        rate_limit = self.github.get_rate_limit()
        core = rate_limit.core
        print(f"Rate limit: {core.remaining}/{core.limit} (resets at {core.reset})")
        return core.remaining > 0
    
    def parse_repo_url(self, url: str) -> tuple:
        """Extract owner and repo name from GitHub URL"""
        # Handle various URL formats
        url = url.strip().rstrip('/')
        
        if 'github.com' in url:
            parts = url.split('github.com/')[-1].split('/')
            if len(parts) >= 2:
                return parts[0], parts[1].replace('.git', '')
        else:
            # Assume format: owner/repo
            parts = url.split('/')
            if len(parts) == 2:
                return parts[0], parts[1]
        
        raise ValueError("Invalid GitHub URL format. Use: https://github.com/owner/repo or owner/repo")
    
    def analyze_repository(self, repo_url: str, max_commits: int = 100) -> Dict:
        """Analyze a GitHub repository and extract bug prediction data"""
        try:
            owner, repo_name = self.parse_repo_url(repo_url)
            print(f"Analyzing repository: {owner}/{repo_name}")
            
            try:
                repo = self.github.get_repo(f"{owner}/{repo_name}")
            except GithubException as e:
                if e.status == 401:
                    raise ValueError("GitHub authentication failed. Please check your access token or log in again.")
                elif e.status == 404:
                    raise ValueError(f"Repository '{owner}/{repo_name}' not found. Please check:\n"
                                   f"1. The repository name is correct\n"
                                   f"2. The repository is public, or you have access to it\n"
                                   f"3. You're logged in with the correct GitHub account")
                elif e.status == 403:
                    raise ValueError("GitHub API rate limit exceeded. Please wait a few minutes or use a GitHub token.")
                else:
                    raise ValueError(f"GitHub API error: {e.data.get('message', str(e))}")
            
            # Fetch commits
            commits_data = []
            issues_data = []
            
            print(f"Fetching up to {max_commits} commits...")
            if self.progress_tracker and self.session_id:
                import asyncio
                asyncio.create_task(self.progress_tracker.update(
                    self.session_id, "fetching", 
                    f"Fetching commits from {owner}/{repo_name}...", 30
                ))
            
            # Fetch commits with empty repository handling
            try:
                commits_paginated = repo.get_commits()
                commits_list = []
                
                for idx, commit in enumerate(commits_paginated, 1):
                    if idx > max_commits:
                        break
                    commits_list.append(commit)
                    if idx % 10 == 0:
                        print(f"  Fetched {idx} commits...")
                        if self.progress_tracker and self.session_id:
                            progress = 30 + int((idx / max_commits) * 30)
                            asyncio.create_task(self.progress_tracker.update(
                                self.session_id, "fetching",
                                f"Fetched {idx} commits...", progress,
                                f"Processing commit {idx}/{max_commits}"
                            ))
            except Exception as e:
                if "empty" in str(e).lower() or "409" in str(e):
                    print(f"✗ Repository is empty")
                    return {
                        "repository_name": f"{owner}/{repo_name}",
                        "commits": [],
                        "issues": [],
                        "metadata": {
                            "stars": repo.stargazers_count,
                            "forks": repo.forks_count,
                            "language": repo.language,
                            "description": repo.description,
                            "error": "Repository is empty - no commits found"
                        }
                    }
                raise
            
            print(f"Found {len(commits_list)} commits")
            
            for idx, commit in enumerate(commits_list, 1):
                if idx % 10 == 0:
                    print(f"  Processed {idx} commits...")
                
                try:
                    # Get commit details
                    files_changed = [f.filename for f in commit.files]
                    
                    # Get diff (limited to avoid huge responses)
                    diff_text = ""
                    code_issues = []
                    
                    for file in commit.files[:5]:  # Limit to first 5 files
                        if file.patch:
                            patch = file.patch[:1000]  # Limit patch size
                            diff_text += patch + "\n"
                            
                            # Analyze code quality in the diff
                            analysis = self.code_analyzer.analyze_diff(patch, file.filename)
                            
                            # Debug: Always log analysis results
                            if analysis['total_issues'] > 0:
                                print(f"    Found {analysis['total_issues']} issues in {file.filename}")
                                if self.progress_tracker and self.session_id:
                                    import asyncio
                                    asyncio.create_task(self.progress_tracker.update(
                                        self.session_id, "analyzing",
                                        f"Analyzing code quality...", None,
                                        f"Found {analysis['total_issues']} issues in {file.filename}"
                                    ))
                                code_issues.append({
                                    'file': file.filename,
                                    'issues': analysis['total_issues'],
                                    'severity_counts': analysis['severity_counts'],
                                    'detailed_issues': analysis['issues']  # Include full issue details
                                })
                    
                    commits_data.append({
                        "hash": commit.sha[:7],
                        "message": commit.commit.message.split('\n')[0][:200],  # First line only
                        "diff": diff_text,
                        "files_changed": files_changed[:10],  # Limit files
                        "code_issues": code_issues  # Add code quality issues
                    })
                    
                except Exception as e:
                    print(f"  Warning: Skipped commit {commit.sha[:7]}: {str(e)}")
                    continue
            
            # Fetch issues (bugs)
            print("Fetching issues...")
            try:
                issues_paginated = repo.get_issues(state='all', labels=['bug'])
                issues_list = []
                for idx, issue in enumerate(issues_paginated, 1):
                    if idx > 50:
                        break
                    issues_list.append(issue)
                print(f"Found {len(issues_list)} bug issues")
            except Exception as e:
                print(f"Warning: Could not fetch issues: {str(e)}")
                issues_list = []
            
            for issue in issues_list:
                # Try to find related commits
                if issue.pull_request:
                    try:
                        pr = repo.get_pull(issue.number)
                        for commit in pr.get_commits():
                            issues_data.append({
                                "commit_hash": commit.sha[:7],
                                "type": "bug"
                            })
                    except:
                        pass
            
            result = {
                "repository_name": f"{owner}/{repo_name}",
                "commits": commits_data,
                "issues": issues_data,
                "metadata": {
                    "stars": repo.stargazers_count,
                    "forks": repo.forks_count,
                    "open_issues": repo.open_issues_count,
                    "language": repo.language,
                    "description": repo.description
                }
            }
            
            print(f"✓ Analysis complete: {len(commits_data)} commits, {len(issues_data)} bug issues")
            return result
            
        except GithubException as e:
            error_msg = str(e)
            if hasattr(e, 'data') and isinstance(e.data, dict):
                error_msg = e.data.get('message', str(e))
            print(f"✗ GitHub API error: {error_msg}")
            import traceback
            traceback.print_exc()
            raise Exception(f"GitHub API error: {error_msg}")
        except ValueError as e:
            print(f"✗ Validation error: {str(e)}")
            import traceback
            traceback.print_exc()
            raise Exception(str(e))
        except Exception as e:
            print(f"✗ Analysis failed: {str(e)}")
            import traceback
            traceback.print_exc()
            raise Exception(f"Analysis failed: {str(e)}")
    
    def get_user_repos(self, username: Optional[str] = None) -> List[Dict]:
        """Get list of repositories for a user"""
        try:
            if username:
                user = self.github.get_user(username)
            else:
                user = self.github.get_user()  # Authenticated user
            
            repos = []
            for repo in user.get_repos()[:20]:  # Limit to 20 repos
                repos.append({
                    "name": repo.full_name,
                    "url": repo.html_url,
                    "description": repo.description,
                    "language": repo.language,
                    "stars": repo.stargazers_count
                })
            
            return repos
        except Exception as e:
            raise Exception(f"Failed to fetch repositories: {str(e)}")
