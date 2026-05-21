"""
Test script to verify stats are being saved and retrieved correctly
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from user_manager import UserManager
from datetime import datetime

def test_stats_flow():
    print("=== Testing Stats Flow ===\n")
    
    # Initialize user manager
    user_manager = UserManager()
    
    # Test user ID
    test_user_id = "123456789"
    
    print(f"1. Testing with user ID: {test_user_id}")
    
    # Create test user
    print("\n2. Creating test user...")
    test_user_data = {
        'id': test_user_id,
        'login': 'testuser',
        'name': 'Test User',
        'email': 'test@example.com',
        'avatar_url': 'https://example.com/avatar.jpg',
        'html_url': 'https://github.com/testuser',
        'bio': 'Test bio',
        'company': 'Test Company',
        'location': 'Test Location'
    }
    
    user = user_manager.create_or_update_user(test_user_data)
    print(f"   ✓ User created: {user.get('username')}")
    
    # Get initial stats
    print("\n3. Getting initial stats...")
    stats = user_manager.get_user_stats(test_user_id)
    print(f"   Total Analyses: {stats.get('total_analyses', 0)}")
    print(f"   Repositories: {stats.get('repositories_analyzed', 0)}")
    print(f"   Average Risk: {stats.get('average_risk', 0)}")
    
    # Simulate analysis
    print("\n4. Simulating analysis...")
    analysis_data = {
        'repository_name': 'test/repo1',
        'overall_repository_risk': 0.65,
        'modules': [
            {'name': 'file1.js', 'risk_score': 0.7},
            {'name': 'file2.js', 'risk_score': 0.6}
        ]
    }
    
    user_manager.save_analysis_local(test_user_id, analysis_data)
    print("   ✓ Analysis saved")
    
    # Get updated stats
    print("\n5. Getting updated stats...")
    stats = user_manager.get_user_stats(test_user_id)
    print(f"   Total Analyses: {stats.get('total_analyses', 0)}")
    print(f"   Repositories: {stats.get('repositories_analyzed', 0)}")
    print(f"   Average Risk: {(stats.get('average_risk', 0) * 100):.0f}%")
    
    # Add another analysis
    print("\n6. Adding second analysis...")
    analysis_data2 = {
        'repository_name': 'test/repo2',
        'overall_repository_risk': 0.35,
        'modules': [
            {'name': 'file3.js', 'risk_score': 0.4},
            {'name': 'file4.js', 'risk_score': 0.3}
        ]
    }
    
    user_manager.save_analysis_local(test_user_id, analysis_data2)
    print("   ✓ Second analysis saved")
    
    # Get final stats
    print("\n7. Getting final stats...")
    stats = user_manager.get_user_stats(test_user_id)
    print(f"   Total Analyses: {stats.get('total_analyses', 0)}")
    print(f"   Repositories: {stats.get('repositories_analyzed', 0)}")
    print(f"   Average Risk: {(stats.get('average_risk', 0) * 100):.0f}%")
    
    # Check MongoDB connection
    print("\n8. Checking MongoDB connection...")
    if user_manager.mongodb.is_connected():
        print("   ✓ MongoDB is connected")
        mongo_stats = user_manager.mongodb.get_user_stats(test_user_id)
        print(f"   MongoDB Total Analyses: {mongo_stats.get('total_analyses', 0)}")
        print(f"   MongoDB Repositories: {mongo_stats.get('repositories_analyzed', 0)}")
    else:
        print("   ⚠ MongoDB is not connected (using local files)")
    
    print("\n=== Test Complete ===")
    print(f"\nUser data file: backend/data/users/{test_user_id}.json")
    print("Check this file to verify data is being saved correctly.")

if __name__ == "__main__":
    test_stats_flow()
