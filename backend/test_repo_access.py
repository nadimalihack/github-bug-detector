"""
Test if a repository exists and is accessible
"""
import requests

def check_repo(owner, repo):
    """Check if a GitHub repository exists and is accessible"""
    url = f"https://api.github.com/repos/{owner}/{repo}"
    
    print(f"Checking: {owner}/{repo}")
    print(f"URL: {url}\n")
    
    # Try without authentication first
    response = requests.get(url)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Repository EXISTS and is PUBLIC")
        print(f"   Name: {data['full_name']}")
        print(f"   Private: {data['private']}")
        print(f"   Description: {data.get('description', 'No description')}")
        return True
    elif response.status_code == 404:
        print(f"❌ Repository NOT FOUND")
        print(f"   This means:")
        print(f"   1. Repository doesn't exist")
        print(f"   2. Repository is private (and you're not authenticated)")
        print(f"   3. Repository name is misspelled")
        return False
    elif response.status_code == 403:
        print(f"⚠️ Access FORBIDDEN (Rate limit or private)")
        return False
    else:
        print(f"❓ Unexpected status: {response.status_code}")
        print(f"   Response: {response.text}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("GitHub Repository Access Test")
    print("=" * 60)
    print()
    
    # Test the repository you're trying to access
    print("Testing your repository:")
    print("-" * 60)
    check_repo("gryffindowr", "Three60onward")
    
    print("\n" + "=" * 60)
    print("\nTesting a known public repository for comparison:")
    print("-" * 60)
    check_repo("facebook", "react")
    
    print("\n" + "=" * 60)
    print("\nRECOMMENDATIONS:")
    print("-" * 60)
    print("1. If your repo is PRIVATE:")
    print("   → Log in to the dashboard")
    print("   → Your GitHub token will be used automatically")
    print()
    print("2. If your repo DOESN'T EXIST:")
    print("   → Check the repository name spelling")
    print("   → Verify it exists at: https://github.com/gryffindowr/Three60onward")
    print()
    print("3. Try a PUBLIC repository first:")
    print("   → facebook/react")
    print("   → microsoft/vscode")
    print("   → nodejs/node")
