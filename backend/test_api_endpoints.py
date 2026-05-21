"""Test if all API endpoints are working"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 70)
print("Testing API Endpoints")
print("=" * 70)

# Test 1: Root endpoint
print("\n1. Testing root endpoint...")
try:
    response = requests.get(f"{BASE_URL}/")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    if response.status_code == 200:
        print("   ✓ Root endpoint working")
except Exception as e:
    print(f"   ✗ Error: {str(e)}")

# Test 2: Learning stats endpoint
print("\n2. Testing learning stats endpoint...")
try:
    response = requests.get(f"{BASE_URL}/api/learning/learning-stats")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   Response: {response.json()}")
        print("   ✓ Learning stats endpoint working")
    else:
        print(f"   ✗ Failed: {response.text}")
except Exception as e:
    print(f"   ✗ Error: {str(e)}")

# Test 3: Feedback endpoint (will fail without data, but should not 404)
print("\n3. Testing feedback endpoint...")
try:
    test_feedback = {
        "record_id": 0,
        "file_name": "test.js",
        "actual_had_bugs": True
    }
    response = requests.post(
        f"{BASE_URL}/api/learning/feedback",
        json=test_feedback
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 404:
        print("   ✗ Endpoint not found - RESTART BACKEND!")
    elif response.status_code in [200, 400]:
        print("   ✓ Feedback endpoint exists (may fail due to no data)")
        print(f"   Response: {response.json()}")
    else:
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"   ✗ Error: {str(e)}")

# Test 4: Demo endpoint
print("\n4. Testing demo endpoint...")
try:
    response = requests.get(f"{BASE_URL}/demo")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Repository: {result.get('repository_name')}")
        print(f"   Modules: {len(result.get('modules', []))}")
        print(f"   Record ID: {result.get('record_id')}")
        print("   ✓ Demo endpoint working")
    else:
        print(f"   ✗ Failed: {response.text}")
except Exception as e:
    print(f"   ✗ Error: {str(e)}")

print("\n" + "=" * 70)
print("Endpoint Test Complete")
print("=" * 70)

print("\n📝 Summary:")
print("   If any endpoint shows 404, you need to restart the backend:")
print("   1. Stop backend (Ctrl+C)")
print("   2. Run: cd backend/src && python api.py")
print("   3. Or use: backend/restart_backend.bat")
