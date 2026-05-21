"""
MongoDB Manager for User Data and Analysis Results
"""
import os
from datetime import datetime
from typing import Optional, List, Dict
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class MongoDBManager:
    def __init__(self):
        self.uri = os.getenv('MONGODB_URI')
        self.db_name = os.getenv('MONGODB_DB_NAME', 'githubbug')
        self.client = None
        self.db = None
        self.connect()
    
    def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
            # Test connection
            self.client.server_info()
            print(f"[SUCCESS] Connected to MongoDB: {self.db_name}")
        except Exception as e:
            print(f"[WARNING] MongoDB connection failed: {e}")
            self.client = None
            self.db = None
    
    def is_connected(self):
        """Check if MongoDB is connected"""
        return self.client is not None and self.db is not None
    
    # User Management
    def create_or_update_user(self, user_data: dict) -> dict:
        """Create or update user in MongoDB"""
        if not self.is_connected():
            return user_data
        
        try:
            users = self.db.users
            user_id = str(user_data['id'])
            
            existing_user = users.find_one({'user_id': user_id})
            
            if existing_user:
                # Update existing user
                users.update_one(
                    {'user_id': user_id},
                    {'$set': {
                        'username': user_data.get('login'),
                        'email': user_data.get('email'),
                        'name': user_data.get('name'),
                        'avatar_url': user_data.get('avatar_url'),
                        'github_url': user_data.get('html_url'),
                        'bio': user_data.get('bio'),
                        'company': user_data.get('company'),
                        'location': user_data.get('location'),
                        'updated_at': datetime.utcnow(),
                        'last_login': datetime.utcnow()
                    }}
                )
                return self.get_user(user_id)
            else:
                # Create new user
                user_doc = {
                    'user_id': user_id,
                    'username': user_data.get('login'),
                    'email': user_data.get('email'),
                    'name': user_data.get('name'),
                    'avatar_url': user_data.get('avatar_url'),
                    'github_url': user_data.get('html_url'),
                    'bio': user_data.get('bio'),
                    'company': user_data.get('company'),
                    'location': user_data.get('location'),
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow(),
                    'last_login': datetime.utcnow(),
                    'analysis_count': 0
                }
                users.insert_one(user_doc)
                return self.get_user(user_id)
        except Exception as e:
            print(f"Error creating/updating user: {e}")
            return user_data
    
    def get_user(self, user_id: str) -> Optional[dict]:
        """Get user from MongoDB"""
        if not self.is_connected():
            return None
        
        try:
            users = self.db.users
            user = users.find_one({'user_id': user_id})
            if user:
                user['id'] = user['user_id']
                user.pop('_id', None)
                return user
            return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def update_analysis_count(self, user_id: str):
        """Increment user's analysis count"""
        if not self.is_connected():
            return
        
        try:
            users = self.db.users
            users.update_one(
                {'user_id': user_id},
                {
                    '$inc': {'analysis_count': 1},
                    '$set': {'updated_at': datetime.utcnow()}
                }
            )
        except Exception as e:
            print(f"Error updating analysis count: {e}")
    
    # Analysis Management
    def save_analysis(self, user_id: str, analysis_data: dict) -> str:
        """Save analysis result to MongoDB"""
        if not self.is_connected():
            print(f"[WARNING] MongoDB not connected, skipping save for user {user_id}")
            return "local"
        
        try:
            analyses = self.db.analyses
            analysis_doc = {
                'user_id': user_id,
                'repository_name': analysis_data.get('repository_name'),
                'overall_risk': analysis_data.get('overall_repository_risk'),
                'modules_count': len(analysis_data.get('modules', [])),
                'modules': analysis_data.get('modules', []),
                'metadata': analysis_data.get('metadata', {}),
                'gemini_analysis': analysis_data.get('gemini_analysis'),
                'analyzed_at': datetime.utcnow()
            }
            result = analyses.insert_one(analysis_doc)
            
            # Update user's analysis count
            self.update_analysis_count(user_id)
            
            print(f"[SUCCESS] Analysis saved to MongoDB: {analysis_data.get('repository_name')} for user {user_id}")
            return str(result.inserted_id)
        except Exception as e:
            print(f"[WARNING] Error saving analysis: {e}")
            import traceback
            traceback.print_exc()
            return "error"
    
    def get_user_analyses(self, user_id: str, limit: int = 50) -> List[dict]:
        """Get user's analysis history"""
        if not self.is_connected():
            return []
        
        try:
            analyses = self.db.analyses
            results = analyses.find(
                {'user_id': user_id}
            ).sort('analyzed_at', -1).limit(limit)
            
            analysis_list = []
            for doc in results:
                doc.pop('_id', None)
                analysis_list.append(doc)
            
            return analysis_list
        except Exception as e:
            print(f"Error getting analyses: {e}")
            return []
    
    def get_user_stats(self, user_id: str) -> dict:
        """Get user statistics from MongoDB"""
        if not self.is_connected():
            return {
                'total_analyses': 0,
                'repositories_analyzed': 0,
                'average_risk': 0,
                'last_analysis': None,
                'member_since': None
            }
        
        try:
            user = self.get_user(user_id)
            if not user:
                return {
                    'total_analyses': 0,
                    'repositories_analyzed': 0,
                    'average_risk': 0,
                    'last_analysis': None,
                    'member_since': None
                }
            
            analyses = self.get_user_analyses(user_id)
            
            total_analyses = user.get('analysis_count', 0)
            repositories_analyzed = len(analyses)
            
            # Calculate average risk
            if analyses:
                total_risk = sum(a.get('overall_risk', 0) for a in analyses)
                average_risk = total_risk / len(analyses)
                last_analysis = analyses[0].get('analyzed_at') if analyses else None
            else:
                average_risk = 0
                last_analysis = None
            
            return {
                'total_analyses': total_analyses,
                'repositories_analyzed': repositories_analyzed,
                'average_risk': average_risk,
                'last_analysis': last_analysis.isoformat() if last_analysis else None,
                'member_since': user.get('created_at').isoformat() if user.get('created_at') else None
            }
        except Exception as e:
            print(f"Error getting user stats: {e}")
            return {
                'total_analyses': 0,
                'repositories_analyzed': 0,
                'average_risk': 0,
                'last_analysis': None,
                'member_since': None
            }
    
    def get_analytics_trends(self, user_id: str) -> dict:
        """Get trend data for charts"""
        if not self.is_connected():
            return {'labels': [], 'risk_scores': [], 'repository_names': []}
        
        try:
            analyses = self.get_user_analyses(user_id, limit=10)
            analyses.reverse()  # Oldest first for timeline
            
            return {
                'labels': [a.get('analyzed_at').strftime('%Y-%m-%d') if a.get('analyzed_at') else '' for a in analyses],
                'risk_scores': [a.get('overall_risk', 0) for a in analyses],
                'repository_names': [a.get('repository_name', '') for a in analyses]
            }
        except Exception as e:
            print(f"Error getting trends: {e}")
            return {'labels': [], 'risk_scores': [], 'repository_names': []}
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            print("[SUCCESS] MongoDB connection closed")
