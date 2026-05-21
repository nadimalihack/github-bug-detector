"""
List all repositories for a GitHub user
"""
import requests

def list_user_repos(username):
    """List all public repositories for a user"""
    url = f"https://api.github.com/users/{username}/repos"
    
    print(f"Fetching repositories for: {username}")
    print(f"URL: {url}\n")
    
    response = requests.get(url, params={'per_page': 100})
    
    if response.status_code == 200:
        repos = response.json()
        print(f"✅ Found {len(repos)} repositories:\n")
        
        for i, repo in enumerate(repos, 1):
            private_badge = "🔒 PRIVATE" if repo['private'] else "🌐 PUBLIC"
            print(f"{i}. {repo['full_name']} {private_badge}")
            if repo.get('description'):
                print(f"   Description: {repo['description']}")
            print(f"   URL: {repo['html_url']}")
            print()
        
        return repos
    elif response.status_code == 404:
        print(f"❌ User '{username}' not found")
        return []
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"   Response: {response.text}")
        return []

if __name__ == "__main__":
    print("=" * 70)
    print("GitHub User Repositories")
    print("=" * 70)
    print()
    
    username = "gryffindowr"
    repos = list_user_repos(username)
    
    if repos:
        print("=" * 70)
        print("\nYou can analyze any of these repositories!")
        print("Just copy the full name (e.g., 'gryffindowr/repo-name')")
    else:
        print("\n⚠️ No public repositories found or user doesn't exist")
        print("\nIf you have private repositories:")
        print("1. Log in to the dashboard")
        print("2. Your repositories will appear in the 'Repositories' tab")
