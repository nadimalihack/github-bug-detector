"""Test GitHub analyzer with a real repository"""
import sys
sys.path.append('src')

from github_analyzer import GitHubAnalyzer

# Test with a small public repo
test_repo = "octocat/Hello-World"  # GitHub's test repo

print("=" * 60)
print("Testing GitHub Analyzer")
print("=" * 60)
print(f"\nAnalyzing repository: {test_repo}")
print("This may take a moment...\n")

try:
    analyzer = GitHubAnalyzer()  # No token needed for public repos
    result = analyzer.analyze_repository(test_repo, max_commits=10)
    
    print("\n" + "=" * 60)
    print("✓ Analysis Complete!")
    print("=" * 60)
    print(f"\nRepository: {result['repository_name']}")
    print(f"Commits analyzed: {len(result['commits'])}")
    print(f"Issues found: {len(result['issues'])}")
    
    if result.get('metadata'):
        meta = result['metadata']
        print(f"\nMetadata:")
        print(f"  Language: {meta.get('language')}")
        print(f"  Stars: {meta.get('stars')}")
        print(f"  Forks: {meta.get('forks')}")
    
    print(f"\nSample commits:")
    for commit in result['commits'][:3]:
        print(f"  - {commit['hash']}: {commit['message'][:60]}...")
    
    print("\n✓ GitHub integration is working!")
    
except Exception as e:
    print(f"\n✗ Error: {str(e)}")
    print("\nTroubleshooting:")
    print("1. Check your internet connection")
    print("2. GitHub API might be rate-limited (60 requests/hour without token)")
    print("3. Try with a GitHub token for higher limits")
