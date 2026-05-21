"""Test full analysis with code issues"""
import sys
sys.path.append('src')

from github_analyzer import GitHubAnalyzer
from predictor import BugPredictor

# Test with a small repo
test_repo = "octocat/Hello-World"

print("=" * 70)
print("Testing Full Analysis Pipeline")
print("=" * 70)

try:
    print(f"\n1. Analyzing GitHub repository: {test_repo}")
    analyzer = GitHubAnalyzer()
    repo_data = analyzer.analyze_repository(test_repo, max_commits=5)
    
    print(f"\n2. Repository data collected:")
    print(f"   - Commits: {len(repo_data['commits'])}")
    print(f"   - Issues: {len(repo_data['issues'])}")
    
    # Check if code issues are present
    total_code_issues = 0
    for commit in repo_data['commits']:
        code_issues = commit.get('code_issues', [])
        total_code_issues += len(code_issues)
        if code_issues:
            print(f"\n   Commit {commit['hash']} has {len(code_issues)} code issues")
            for issue in code_issues:
                print(f"     - {issue['file']}: {issue['issues']} issues")
    
    print(f"\n   Total code issues found: {total_code_issues}")
    
    print(f"\n3. Running bug prediction...")
    predictor = BugPredictor()
    result = predictor.predict_repository_risk(repo_data)
    
    print(f"\n4. Results:")
    print(f"   - Repository: {result['repository_name']}")
    print(f"   - Overall Risk: {result['overall_repository_risk']}")
    print(f"   - Modules analyzed: {len(result['modules'])}")
    
    # Check detailed issues
    for module in result['modules'][:3]:
        print(f"\n   File: {module['file']}")
        print(f"   - Risk Score: {module['risk_score']}")
        print(f"   - Critical Issues: {module.get('critical_issues', 0)}")
        print(f"   - High Issues: {module.get('high_issues', 0)}")
        print(f"   - Detailed Issues: {len(module.get('detailed_issues', []))}")
        
        if module.get('detailed_issues'):
            print(f"   - Sample issue:")
            issue = module['detailed_issues'][0]
            print(f"     * {issue['severity']}: {issue['message']}")
            print(f"     * Line: {issue['line']}")
            print(f"     * Fix: {issue.get('fix', 'N/A')}")
    
    print("\n" + "=" * 70)
    print("✓ Full analysis pipeline working!")
    print("=" * 70)
    
except Exception as e:
    print(f"\n✗ Error: {str(e)}")
    import traceback
    traceback.print_exc()
