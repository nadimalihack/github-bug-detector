"""
Test analysis with user ID to verify data is saved
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"
USER_ID = "60312089"  # Your actual user ID

def test_analysis_with_user():
    print("=== Testing Analysis with User ID ===\n")
    
    print(f"Using User ID: {USER_ID}")
    
    # Step 1: Check initial stats
    print("\n1. Checking initial stats...")
    try:
        response = requests.get(f"{BASE_URL}/user/{USER_ID}/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"   Total Analyses: {stats.get('total_analyses', 0)}")
            print(f"   Repositories: {stats.get('repositories_analyzed', 0)}")
            print(f"   Average Risk: {(stats.get('average_risk', 0) * 100):.0f}%")
        else:
            print(f"   Status: {response.status_code}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Step 2: Run demo analysis (which should save data)
    print("\n2. Running demo analysis...")
    try:
        response = requests.get(f"{BASE_URL}/demo")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✓ Demo analysis complete")
            print(f"   Repository: {result.get('repository_name')}")
            print(f"   Risk: {(result.get('overall_repository_risk', 0) * 100):.0f}%")
            print(f"   Record ID: {result.get('record_id')}")
        else:
            print(f"   ✗ Failed: {response.status_code}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Step 3: Manually save analysis for user
    print("\n3. Manually saving analysis for user...")
    try:
        # Use the Python API directly
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        
        from user_manager import UserManager
        
        user_manager = UserManager()
        
        # Create test analysis
        test_analysis = {
            'repository_name': 'test/manual-repo',
            'overall_repository_risk': 0.55,
            'modules': [
                {'name': 'test.js', 'risk_score': 0.6},
                {'name': 'app.js', 'risk_score': 0.5}
            ]
        }
        
        # Save it
        if user_manager.mongodb.is_connected():
            user_manager.mongodb.save_analysis(USER_ID, test_analysis)
            print(f"   ✓ Saved to MongoDB")
        else:
            user_manager.save_analysis_local(USER_ID, test_analysis)
            print(f"   ✓ Saved locally")
            
    except Exception as e:
        print(f"   Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Step 4: Wait and check stats again
    print("\n4. Waiting 2 seconds...")
    time.sleep(2)
    
    print("\n5. Checking updated stats...")
    try:
        response = requests.get(f"{BASE_URL}/user/{USER_ID}/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"   Total Analyses: {stats.get('total_analyses', 0)}")
            print(f"   Repositories: {stats.get('repositories_analyzed', 0)}")
            print(f"   Average Risk: {(stats.get('average_risk', 0) * 100):.0f}%")
            
            if stats.get('total_analyses', 0) > 0:
                print("\n   ✓✓✓ SUCCESS! Stats are updating! ✓✓✓")
            else:
                print("\n   ✗✗✗ PROBLEM: Stats still showing 0 ✗✗✗")
        else:
            print(f"   Status: {response.status_code}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Step 6: Check trends
    print("\n6. Checking analytics trends...")
    try:
        response = requests.get(f"{BASE_URL}/analytics/trends?user_id={USER_ID}")
        if response.status_code == 200:
            trends = response.json()
            print(f"   Data points: {len(trends.get('labels', []))}")
            print(f"   Repositories: {trends.get('repository_names', [])}")
        else:
            print(f"   Status: {response.status_code}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n=== Test Complete ===")
    print("\nNext steps:")
    print("1. If stats are still 0, check backend console for error messages")
    print("2. Run: python backend/check_user_stats.py")
    print("3. Check if MongoDB is saving data correctly")

if __name__ == "__main__":
    test_analysis_with_user()
