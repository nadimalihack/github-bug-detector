"""
Check user stats for debugging
"""
import sys
import os
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from user_manager import UserManager

def check_user_stats():
    print("=== Checking User Stats ===\n")
    
    user_manager = UserManager()
    
    # Check if MongoDB is connected
    print("1. MongoDB Status:")
    if user_manager.mongodb.is_connected():
        print("   ✓ MongoDB is CONNECTED")
    else:
        print("   ✗ MongoDB is NOT connected")
    
    # List all users in local storage
    print("\n2. Local Users:")
    users_dir = "data/users"
    if os.path.exists(users_dir):
        user_files = [f for f in os.listdir(users_dir) if f.endswith('.json')]
        print(f"   Found {len(user_files)} user(s)")
        
        for user_file in user_files:
            user_id = user_file.replace('.json', '')
            print(f"\n   User ID: {user_id}")
            
            # Load user data
            with open(os.path.join(users_dir, user_file), 'r') as f:
                user_data = json.load(f)
            
            print(f"   Username: {user_data.get('username', 'N/A')}")
            print(f"   Analysis Count: {user_data.get('analysis_count', 0)}")
            print(f"   Repositories: {len(user_data.get('repositories', []))}")
            
            # Get stats
            stats = user_manager.get_user_stats(user_id)
            print(f"   Stats - Total Analyses: {stats.get('total_analyses', 0)}")
            print(f"   Stats - Repositories Analyzed: {stats.get('repositories_analyzed', 0)}")
            print(f"   Stats - Average Risk: {(stats.get('average_risk', 0) * 100):.0f}%")
            
            # Show recent repositories
            repos = user_data.get('repositories', [])
            if repos:
                print(f"   Recent Repositories:")
                for repo in repos[-3:]:
                    print(f"     - {repo.get('name')}: {(repo.get('risk_score', 0) * 100):.0f}% risk")
    else:
        print("   No local users found")
    
    # Check MongoDB users
    if user_manager.mongodb.is_connected():
        print("\n3. MongoDB Users:")
        try:
            users = user_manager.mongodb.db.users.find()
            count = 0
            for user in users:
                count += 1
                print(f"\n   User ID: {user.get('user_id')}")
                print(f"   Username: {user.get('username')}")
                print(f"   Analysis Count: {user.get('analysis_count', 0)}")
                
                # Get MongoDB stats
                stats = user_manager.mongodb.get_user_stats(user.get('user_id'))
                print(f"   Stats - Total Analyses: {stats.get('total_analyses', 0)}")
                print(f"   Stats - Repositories: {stats.get('repositories_analyzed', 0)}")
                print(f"   Stats - Average Risk: {(stats.get('average_risk', 0) * 100):.0f}%")
            
            if count == 0:
                print("   No MongoDB users found")
        except Exception as e:
            print(f"   Error reading MongoDB: {e}")
    
    print("\n=== Check Complete ===")

if __name__ == "__main__":
    check_user_stats()
