"""Test if progress endpoint works"""
import requests
import time

BASE_URL = "http://localhost:8000"

print("Testing Progress Endpoint...")
print("=" * 70)

# Test 1: Check if endpoint exists
print("\n1. Testing progress endpoint...")
try:
    response = requests.get(f"{BASE_URL}/progress/test_session", stream=True, timeout=5)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        print("   ✓ Progress endpoint exists!")
        print("   Receiving events...")
        
        # Read a few events
        for i, line in enumerate(response.iter_lines()):
            if i >= 5:  # Just read first 5 lines
                break
            if line:
                print(f"   Event: {line.decode()}")
        
        response.close()
    else:
        print(f"   ✗ Unexpected status: {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("   ✗ Backend not running!")
    print("   Start it with: cd backend/src && python api.py")
except Exception as e:
    print(f"   ✗ Error: {str(e)}")

print("\n" + "=" * 70)
print("If you see 404, restart the backend to load new endpoints!")
