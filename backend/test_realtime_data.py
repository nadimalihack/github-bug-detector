"""
Test script to verify real-time data flow
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_realtime_data():
    print("=== Testing Real-Time Data Flow ===\n")
    
    # Test 1: Check if MongoDB is connected
    print("1. Checking MongoDB connection...")
    try:
        response = requests.get(f"{BASE_URL}/")
        data = response.json()
        print(f"   Enhanced features: {data['features']['enhanced_features']}")
        print(f"   User management: {data['features']['user_management']}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Test 2: Create a test user
    print("\n2. Creating test user...")
    test_user_id = "test_user_123"
    
    # Test 3: Get user stats (should be 0)
    print("\n3. Getting initial user stats...")
    try:
        response = requests.get(f"{BASE_URL}/user/{test_user_id}/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"   Total analyses: {stats.get('total_analyses', 0)}")
            print(f"   Repositories: {stats.get('repositories_analyzed', 0)}")
            print(f"   Average risk: {stats.get('average_risk', 0)}")
        else:
            print(f"   User not found (expected for new user)")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Test 4: Simulate an analysis
    print("\n4. Simulating repository analysis...")
    try:
        response = requests.post(
            f"{BASE_URL}/analyze-github-url",
            json={
                "repo_url": "test/demo-repo",
                "user_id": test_user_id,
                "max_commits": 10
            }
        )
        if response.status_code == 200:
            result = response.json()
            print(f"   ✓ Analysis complete: {result.get('repository_name')}")
            print(f"   Risk score: {result.get('overall_repository_risk', 0)}")
        else:
            print(f"   ✗ Analysis failed: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Test 5: Get updated stats
    print("\n5. Getting updated user stats...")
    time.sleep(1)  # Wait for data to be saved
    try:
        response = requests.get(f"{BASE_URL}/user/{test_user_id}/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"   Total analyses: {stats.get('total_analyses', 0)}")
            print(f"   Repositories: {stats.get('repositories_analyzed', 0)}")
            print(f"   Average risk: {stats.get('average_risk', 0)}")
        else:
            print(f"   ✗ Failed to get stats: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Test 6: Get analytics trends
    print("\n6. Getting analytics trends...")
    try:
        response = requests.get(f"{BASE_URL}/analytics/trends?user_id={test_user_id}")
        if response.status_code == 200:
            trends = response.json()
            print(f"   Data points: {len(trends.get('labels', []))}")
            print(f"   Repositories: {trends.get('repository_names', [])}")
        else:
            print(f"   ✗ Failed to get trends: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_realtime_data()
