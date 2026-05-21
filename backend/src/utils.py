import re
from typing import List, Dict

BUG_KEYWORDS = ['fix', 'bug', 'error', 'issue', 'resolve', 'patch', 'hotfix', 'crash']

def extract_features(commit_data: Dict) -> Dict:
    """Extract features from commit data for ML model"""
    message = commit_data.get('message', '').lower()
    diff = commit_data.get('diff', '')
    
    # Bug-related keywords count
    bug_keyword_count = sum(1 for keyword in BUG_KEYWORDS if keyword in message)
    
    # Diff complexity (lines changed)
    lines_changed = len(diff.split('\n')) if diff else 0
    
    return {
        'bug_keyword_count': bug_keyword_count,
        'lines_changed': lines_changed,
        'has_bug_keyword': int(bug_keyword_count > 0)
    }

def calculate_file_risk(file_commits: List[Dict], total_commits: int) -> tuple:
    """Calculate risk score for a file based on its commit history"""
    if not file_commits:
        return 0.0, "No commit history"
    
    bug_commits = sum(1 for c in file_commits if any(kw in c.get('message', '').lower() for kw in BUG_KEYWORDS))
    avg_lines_changed = sum(len(c.get('diff', '').split('\n')) for c in file_commits) / len(file_commits)
    
    # Risk calculation
    bug_ratio = bug_commits / len(file_commits) if file_commits else 0
    frequency_factor = min(len(file_commits) / max(total_commits, 1), 1.0)
    complexity_factor = min(avg_lines_changed / 100, 1.0)
    
    risk_score = (bug_ratio * 0.5 + frequency_factor * 0.3 + complexity_factor * 0.2)
    
    # Generate reason
    if risk_score > 0.7:
        reason = f"High bug frequency ({bug_commits}/{len(file_commits)} commits) and complex changes"
    elif risk_score > 0.4:
        reason = f"Moderate bug-related commits ({bug_commits}) with average complexity"
    else:
        reason = "Low bug frequency and stable changes"
    
    return min(risk_score, 1.0), reason
