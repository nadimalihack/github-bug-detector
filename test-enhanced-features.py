"""
Test Enhanced Features
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_root():
    """Test root endpoint"""
    print("Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    data = response.json()
    print(f"✓ Status: {data['status']}")
    print(f"✓ Enhanced Features: {data['features']['enhanced_features']}")
    print(f"✓ Gemini AI: {data['features']['gemini_ai']}")
    print(f"✓ OAuth: {data['features']['oauth']}")
    return data['features']['enhanced_features']

def test_auth_github():
    """Test GitHub OAuth endpoint"""
    print("\nTesting GitHub OAuth endpoint...")
    response = requests.get(f"{BASE_URL}/auth/github")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ OAuth URL: {data['authorization_url'][:50]}...")
        return True
    elif response.status_code == 503:
        print("✗ Enhanced features not enabled")
        return False
    else:
        print(f"✗ Error: {response.status_code}")
        return False

def main():
    print("=" * 50)
    print("Testing Enhanced Features")
    print("=" * 50)
    
    try:
        enhanced = test_root()
        
        if enhanced:
            test_auth_github()
            print("\n" + "=" * 50)
            print("✓ All enhanced features working!")
            print("=" * 50)
        else:
            print("\n" + "=" * 50)
            print("⚠ Enhanced features not enabled")
            print("Run: pip install google-generativeai authlib python-jose httpx")
            print("Then restart backend server")
            print("=" * 50)
    except requests.exceptions.ConnectionError:
        print("\n✗ Backend server not running!")
        print("Start it with: cd backend/src && python api.py")

if __name__ == "__main__":
    main()
