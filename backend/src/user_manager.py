"""
User Management System with MongoDB Integration
"""
import json
import os
from datetime import datetime
from typing import Optional
from .mongodb_manager import MongoDBManager

class UserManager:
    def __init__(self, data_dir: str = "data/users"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        self.mongodb = MongoDBManager()
    
    def create_or_update_user(self, user_data: dict) -> dict:
        """Create or update user profile in MongoDB and local file"""
        user_id = str(user_data['id'])
        
        # Save to MongoDB
        if self.mongodb.is_connected():
            print(f"✓ Saving user {user_id} to MongoDB")
            result = self.mongodb.create_or_update_user(user_data)
            print(f"✓ User saved: {result.get('username')}")
            return result
        
        # Fallback to local file
        user_file = os.path.join(self.data_dir, f"{user_id}.json")
        
        # Load existing data if available
        existing_data = {}
        if os.path.exists(user_file):
            with open(user_file, 'r') as f:
                existing_data = json.load(f)
        
        # Merge data
        profile = {
            'id': user_id,
            'username': user_data.get('login'),
            'email': user_data.get('email'),
            'name': user_data.get('name'),
            'avatar_url': user_data.get('avatar_url'),
            'github_url': user_data.get('html_url'),
            'bio': user_data.get('bio'),
            'company': user_data.get('company'),
            'location': user_data.get('location'),
            'created_at': existing_data.get('created_at', datetime.utcnow().isoformat()),
            'updated_at': datetime.utcnow().isoformat(),
            'last_login': datetime.utcnow().isoformat(),
            'analysis_count': existing_data.get('analysis_count', 0),
            'repositories': existing_data.get('repositories', [])
        }
        
        # Save to file
        with open(user_file, 'w') as f:
            json.dump(profile, f, indent=2)
        
        return profile
    
    def get_user(self, user_id: str) -> Optional[dict]:
        """Get user profile from MongoDB or local file"""
        # Try MongoDB first
        if self.mongodb.is_connected():
            return self.mongodb.get_user(user_id)
        
        # Fallback to local file
        user_file = os.path.join(self.data_dir, f"{user_id}.json")
        if os.path.exists(user_file):
            with open(user_file, 'r') as f:
                return json.load(f)
        return None
    
    def update_analysis_count(self, user_id: str):
        """Increment user's analysis count"""
        # Try MongoDB first
        if self.mongodb.is_connected():
            self.mongodb.update_analysis_count(user_id)
        
        # Also update local file
        user = self.get_user(user_id)
        if user:
            user['analysis_count'] = user.get('analysis_count', 0) + 1
            user['updated_at'] = datetime.utcnow().isoformat()
            
            user_file = os.path.join(self.data_dir, f"{user_id}.json")
            with open(user_file, 'w') as f:
                json.dump(user, f, indent=2)
            print(f"✓ Updated analysis count for user {user_id}: {user['analysis_count']}")
    
    def add_repository_to_user(self, user_id: str, repo_data: dict):
        """Add analyzed repository to user's history"""
        user = self.get_user(user_id)
        if user:
            repos = user.get('repositories', [])
            
            # Add new repo
            repos.append({
                'name': repo_data.get('name'),
                'url': repo_data.get('url'),
                'risk_score': repo_data.get('risk_score'),
                'analyzed_at': datetime.utcnow().isoformat()
            })
            
            # Keep only last 50
            user['repositories'] = repos[-50:]
            user['updated_at'] = datetime.utcnow().isoformat()
            
            user_file = os.path.join(self.data_dir, f"{user_id}.json")
            with open(user_file, 'w') as f:
                json.dump(user, f, indent=2)
            print(f"✓ Added repository to user {user_id}: {repo_data.get('name')}")
    
    def save_analysis_local(self, user_id: str, analysis_data: dict):
        """Save analysis to local file (fallback when MongoDB is not available)"""
        try:
            # Update analysis count
            self.update_analysis_count(user_id)
            
            # Add repository to history
            self.add_repository_to_user(user_id, {
                'name': analysis_data.get('repository_name'),
                'url': analysis_data.get('repository_name'),
                'risk_score': analysis_data.get('overall_repository_risk', 0)
            })
            
            print(f"✓ Analysis saved locally for user {user_id}")
        except Exception as e:
            print(f"✗ Error saving analysis locally: {e}")
    
    def get_user_stats(self, user_id: str) -> dict:
        """Get user statistics from MongoDB or local file"""
        # Try MongoDB first
        if self.mongodb.is_connected():
            return self.mongodb.get_user_stats(user_id)
        
        # Fallback to local file
        user = self.get_user(user_id)
        if not user:
            return {}
        
        repos = user.get('repositories', [])
        
        return {
            'total_analyses': user.get('analysis_count', 0),
            'repositories_analyzed': len(repos),
            'average_risk': sum(r.get('risk_score', 0) for r in repos) / len(repos) if repos else 0,
            'last_analysis': repos[-1].get('analyzed_at') if repos else None,
            'member_since': user.get('created_at')
        }
