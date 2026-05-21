import joblib
import numpy as np
from typing import Dict, List
from .utils import calculate_file_risk
from .code_analyzer import CodeAnalyzer

class BugPredictor:
    def __init__(self, model_path: str = "../models/bug_predictor.pkl"):
        try:
            self.model = joblib.load(model_path)
            print("[SUCCESS] ML model loaded successfully")
        except FileNotFoundError:
            self.model = None
            print("[WARNING] Model not found. Using rule-based prediction.")
            print("  Train a model with: python train_from_github.py")
        
        self.code_analyzer = CodeAnalyzer()
    
    def predict_repository_risk(self, repo_data: Dict) -> Dict:
        """Predict bug risk for all modules in a repository"""
        try:
            print(f"Predicting risk for repository: {repo_data.get('repository_name', 'Unknown')}")
            
            commits = repo_data.get('commits', [])
            print(f"Processing {len(commits)} commits")
            
            if not commits:
                print("Warning: No commits found in repository data")
                return {
                    "repository_name": repo_data.get('repository_name', 'Unknown'),
                    "modules": [],
                    "overall_repository_risk": 0.0
                }
            
            issues = {issue.get('commit_hash'): issue.get('type') for issue in repo_data.get('issues', [])}
            
            # Aggregate commits by file
            file_commits = {}
            for commit in commits:
                files = commit.get('files_changed', [])
                for file in files:
                    if file not in file_commits:
                        file_commits[file] = []
                    file_commits[file].append(commit)
            
            print(f"Analyzing {len(file_commits)} unique files")
            
            # Calculate risk for each file
            modules = []
            total_commits = len(commits)
            
            for file, commits_list in file_commits.items():
                try:
                    risk_score, reason = calculate_file_risk(commits_list, total_commits)
                    
                    # Analyze code quality issues in this file
                    code_quality_issues = []
                    critical_issues = 0
                    high_issues = 0
                    
                    for commit in commits_list:
                        for issue_data in commit.get('code_issues', []):
                            if issue_data['file'] == file:
                                code_quality_issues.append(issue_data)
                                critical_issues += issue_data['severity_counts'].get('critical', 0)
                                high_issues += issue_data['severity_counts'].get('high', 0)
                    
                    # Adjust risk score based on code quality issues
                    if critical_issues > 0:
                        risk_score = min(risk_score + 0.2, 1.0)
                        reason += f" | {critical_issues} critical code issues detected"
                    elif high_issues > 0:
                        risk_score = min(risk_score + 0.1, 1.0)
                        reason += f" | {high_issues} high-severity code issues"
                    
                    # Collect detailed issues for display
                    detailed_issues = []
                    for commit in commits_list:
                        for issue_data in commit.get('code_issues', []):
                            if issue_data['file'] == file:
                                detailed_issues.extend(issue_data.get('detailed_issues', []))
                    
                    modules.append({
                        "file": file,
                        "risk_score": round(risk_score, 2),
                        "reason": reason,
                        "code_quality_issues": len(code_quality_issues),
                        "critical_issues": critical_issues,
                        "high_issues": high_issues,
                        "detailed_issues": detailed_issues[:10]  # Limit to 10 most important
                    })
                except Exception as e:
                    print(f"Warning: Error calculating risk for {file}: {str(e)}")
                    continue
            
            # Sort by risk score
            modules.sort(key=lambda x: x['risk_score'], reverse=True)
            
            # Calculate overall repository risk
            overall_risk = np.mean([m['risk_score'] for m in modules]) if modules else 0.0
            
            print(f"✓ Risk prediction complete: {len(modules)} modules analyzed")
            
            return {
                "repository_name": repo_data.get('repository_name', 'Unknown'),
                "modules": modules,
                "overall_repository_risk": round(overall_risk, 2)
            }
        except Exception as e:
            print(f"✗ Error in predict_repository_risk: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
