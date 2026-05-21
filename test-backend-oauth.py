"""
Quick test to verify backend OAuth endpoints are working
"""
import requests

BACKEND_URL = "http://localhost:8000"

print("🔍 Testing Backend OAuth Endpoints\n")

# Test 1: Check if backend is running
print("1. Testing backend connection...")
try:
    response = requests.get(f"{BACKEND_URL}/")
    print(f"   ✅ Backend is running: {response.json()}")
except Exception as e:
    print(f"   ❌ Backend connection failed: {e}")
    print("   💡 Make sure backend is running: cd backend && python run.py")
    exit(1)

# Test 2: Check OAuth GitHub endpoint
print("\n2. Testing /auth/github endpoint...")
try:
    response = requests.get(f"{BACKEND_URL}/auth/github")
    if response.status_code == 503:
        print("   ⚠️  Enhanced features not available (503)")
        print("   💡 Install dependencies: pip install google-generativeai authlib python-jose[cryptography] httpx")
        exit(1)
    elif response.status_code == 200:
        data = response.json()
        print(f"   ✅ OAuth endpoint working")
        print(f"   Authorization URL: {data.get('authorization_url', 'N/A')[:80]}...")
    else:
        print(f"   ❌ Unexpected status: {response.status_code}")
except Exception as e:
    print(f"   ❌ Request failed: {e}")

# Test 3: Check if OAuth callback endpoint exists
print("\n3. Testing /auth/callback endpoint (without code)...")
try:
    response = requests.post(f"{BACKEND_URL}/auth/callback?code=test")
    print(f"   Status: {response.status_code}")
    if response.status_code == 400:
        print("   ✅ Endpoint exists (returns 400 for invalid code, which is expected)")
    elif response.status_code == 503:
        print("   ⚠️  Enhanced features not available")
    else:
        print(f"   Response: {response.text[:200]}")
except Exception as e:
    print(f"   ❌ Request failed: {e}")

print("\n" + "="*60)
print("Summary:")
print("- If all tests pass, backend OAuth is configured correctly")
print("- If you see 503 errors, install enhanced dependencies")
print("- If tests fail, check backend is running on port 8000")
print("="*60)
