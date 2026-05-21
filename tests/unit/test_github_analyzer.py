"""
Unit tests for GitHub analyzer module
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

backend_path = Path(__file__).parent.parent.parent / "backend" / "src"
sys.path.insert(0, str(backend_path))


class TestGitHubAnalyzer:
    """Test cases for GitHubAnalyzer class"""
    
    @patch('github.Github')
    def test_init_with_token(self, mock_github):
        """Test initialization with GitHub token"""
        from github_analyzer import GitHubAnalyzer
        
        analyzer = GitHubAnalyzer(token="test_token")
        
        assert analyzer.token == "test_token"
        mock_github.assert_called_once_with("test_token")
        
    @patch('github.Github')
    def test_init_without_token(self, mock_github):
        """Test initialization without GitHub token"""
        from github_analyzer import GitHubAnalyzer
        
        analyzer = GitHubAnalyzer()
        
        assert analyzer.token is None
        mock_github.assert_called_once_with()
        
    def test_parse_github_url_full_url(self):
        """Test parsing full GitHub URL"""
        from github_analyzer import GitHubAnalyzer
        
        analyzer = GitHubAnalyzer()
        owner, repo = analyzer.parse_github_url("https://github.com/facebook/react")
        
        assert owner == "facebook"
        assert repo == "react"
        
    def test_parse_github_url_short_format(self):
        """Test parsing short format GitHub URL"""
        from github_analyzer import GitHubAnalyzer
        
        analyzer = GitHubAnalyzer()
        owner, repo = analyzer.parse_github_url("facebook/react")
        
        assert owner == "facebook"
        assert repo == "react"
        
    def test_parse_github_url_with_trailing_slash(self):
        """Test parsing URL with trailing slash"""
        from github_analyzer import GitHubAnalyzer
        
        analyzer = GitHubAnalyzer()
        owner, repo = analyzer.parse_github_url("https://github.com/facebook/react/")
        
        assert owner == "facebook"
        assert repo == "react"
        
    def test_parse_github_url_invalid(self):
        """Test parsing invalid GitHub URL"""
        from github_analyzer import GitHubAnalyzer
        
        analyzer = GitHubAnalyzer()
        
        with pytest.raises(ValueError):
            analyzer.parse_github_url("invalid_url")
            
    @patch('github.Github')
    def test_get_repository_success(self, mock_github):
        """Test successful repository retrieval"""
        from github_analyzer import GitHubAnalyzer
        
        mock_repo = Mock()
        mock_github.return_value.get_repo.return_value = mock_repo
        
        analyzer = GitHubAnalyzer()
        repo = analyzer.get_repository("facebook/react")
        
        assert repo == mock_repo
        
    @patch('github.Github')
    def test_get_repository_not_found(self, mock_github):
        """Test repository not found error"""
        from github_analyzer import GitHubAnalyzer
        from github import GithubException
        
        mock_github.return_value.get_repo.side_effect = GithubException(404, "Not Found")
        
        analyzer = GitHubAnalyzer()
        
        with pytest.raises(Exception):
            analyzer.get_repository("invalid/repo")
            
    @patch('github.Github')
    def test_fetch_commits(self, mock_github):
        """Test fetching commits from repository"""
        from github_analyzer import GitHubAnalyzer
        
        mock_commit = Mock()
        mock_commit.sha = "abc123"
        mock_commit.commit.message = "Test commit"
        mock_commit.commit.author.name = "Test User"
        mock_commit.commit.author.date = "2024-01-15"
        
        mock_repo = Mock()
        mock_repo.get_commits.return_value = [mock_commit]
        mock_github.return_value.get_repo.return_value = mock_repo
        
        analyzer = GitHubAnalyzer()
        commits = analyzer.fetch_commits("test/repo", max_commits=10)
        
        assert len(commits) > 0
        assert commits[0]["sha"] == "abc123"
        
    @patch('github.Github')
    def test_fetch_commits_with_limit(self, mock_github):
        """Test fetching commits with limit"""
        from github_analyzer import GitHubAnalyzer
        
        mock_commits = [Mock() for _ in range(20)]
        for i, commit in enumerate(mock_commits):
            commit.sha = f"sha{i}"
            commit.commit.message = f"Commit {i}"
            
        mock_repo = Mock()
        mock_repo.get_commits.return_value = mock_commits
        mock_github.return_value.get_repo.return_value = mock_repo
        
        analyzer = GitHubAnalyzer()
        commits = analyzer.fetch_commits("test/repo", max_commits=10)
        
        assert len(commits) <= 10
        
    @patch('github.Github')
    def test_fetch_issues(self, mock_github):
        """Test fetching issues from repository"""
        from github_analyzer import GitHubAnalyzer
        
        mock_issue = Mock()
        mock_issue.number = 1
        mock_issue.title = "Test Issue"
        mock_issue.state = "open"
        mock_issue.labels = []
        
        mock_repo = Mock()
        mock_repo.get_issues.return_value = [mock_issue]
        mock_github.return_value.get_repo.return_value = mock_repo
        
        analyzer = GitHubAnalyzer()
        issues = analyzer.fetch_issues("test/repo")
        
        assert len(issues) > 0
        assert issues[0]["number"] == 1
        
    @patch('github.Github')
    def test_fetch_pull_requests(self, mock_github):
        """Test fetching pull requests"""
        from github_analyzer import GitHubAnalyzer
        
        mock_pr = Mock()
        mock_pr.number = 1
        mock_pr.title = "Test PR"
        mock_pr.state = "open"
        
        mock_repo = Mock()
        mock_repo.get_pulls.return_value = [mock_pr]
        mock_github.return_value.get_repo.return_value = mock_repo
        
        analyzer = GitHubAnalyzer()
        prs = analyzer.fetch_pull_requests("test/repo")
        
        assert len(prs) > 0
        assert prs[0]["number"] == 1
        
    @patch('github.Github')
    def test_get_repository_stats(self, mock_github):
        """Test getting repository statistics"""
        from github_analyzer import GitHubAnalyzer
        
        mock_repo = Mock()
        mock_repo.name = "test-repo"
        mock_repo.description = "Test repository"
        mock_repo.language = "Python"
        mock_repo.stargazers_count = 100
        mock_repo.forks_count = 20
        mock_repo.open_issues_count = 5
        
        mock_github.return_value.get_repo.return_value = mock_repo
        
        analyzer = GitHubAnalyzer()
        stats = analyzer.get_repository_stats("test/repo")
        
        assert stats["name"] == "test-repo"
        assert stats["stars"] == 100
        assert stats["forks"] == 20
        
    @patch('github.Github')
    def test_analyze_repository_complete(self, mock_github):
        """Test complete repository analysis"""
        from github_analyzer import GitHubAnalyzer
        
        mock_repo = Mock()
        mock_repo.name = "test-repo"
        mock_repo.get_commits.return_value = []
        mock_repo.get_issues.return_value = []
        
        mock_github.return_value.get_repo.return_value = mock_repo
        
        analyzer = GitHubAnalyzer()
        result = analyzer.analyze_repository("test/repo")
        
        assert "repository" in result
        assert "commits" in result
        assert "issues" in result
        
    def test_extract_file_changes(self):
        """Test extracting file changes from commit"""
        from github_analyzer import GitHubAnalyzer
        
        mock_file = Mock()
        mock_file.filename = "test.py"
        mock_file.additions = 10
        mock_file.deletions = 5
        mock_file.changes = 15
        mock_file.status = "modified"
        
        mock_commit = Mock()
        mock_commit.files = [mock_file]
        
        analyzer = GitHubAnalyzer()
        files = analyzer.extract_file_changes(mock_commit)
        
        assert len(files) == 1
        assert files[0]["filename"] == "test.py"
        assert files[0]["additions"] == 10
        
    def test_calculate_commit_frequency(self):
        """Test calculating commit frequency"""
        from github_analyzer import GitHubAnalyzer
        from datetime import datetime, timedelta
        
        commits = [
            {"date": (datetime.now() - timedelta(days=i)).isoformat()}
            for i in range(10)
        ]
        
        analyzer = GitHubAnalyzer()
        frequency = analyzer.calculate_commit_frequency(commits)
        
        assert isinstance(frequency, (int, float))
        assert frequency > 0
        
    def test_identify_bug_related_commits(self):
        """Test identifying bug-related commits"""
        from github_analyzer import GitHubAnalyzer
        
        commits = [
            {"message": "fix: critical bug in authentication"},
            {"message": "feat: add new feature"},
            {"message": "hotfix: patch security issue"},
            {"message": "docs: update README"}
        ]
        
        analyzer = GitHubAnalyzer()
        bug_commits = analyzer.identify_bug_commits(commits)
        
        assert len(bug_commits) >= 2
        
    def test_get_rate_limit_info(self):
        """Test getting rate limit information"""
        from github_analyzer import GitHubAnalyzer
        
        with patch('github.Github') as mock_github:
            mock_rate_limit = Mock()
            mock_rate_limit.core.remaining = 5000
            mock_rate_limit.core.limit = 5000
            mock_github.return_value.get_rate_limit.return_value = mock_rate_limit
            
            analyzer = GitHubAnalyzer()
            rate_limit = analyzer.get_rate_limit()
            
            assert rate_limit["remaining"] == 5000
            assert rate_limit["limit"] == 5000
