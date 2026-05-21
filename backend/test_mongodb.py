"""
Test MongoDB Integration and Populate Sample Data
"""
import sys
sys.path.append('src')

from mongodb_manager import MongoDBManager
from datetime import datetime, timedelta

def test_mongodb():
    print("=" * 50)
    print("Testing MongoDB Integration")
    print("=" * 50)
    
    db = MongoDBManager()
    
    if not db.is_connected():
        print("✗ MongoDB not connected!")
        return
    
    print("✓ MongoDB connected")
    
    # Create test user
    test_user = {
        'id': '60312089',  # Your GitHub user ID
        'login': 'gryffindowr',
        'email': 'test@example.com',
        'name': 'Test User',
        'avatar_url': 'https://avatars.githubusercontent.com/u/60312089',
        'html_url': 'https://github.com/gryffindowr',
        'bio': 'Test bio',
        'company': 'Test Company',
        'location': 'Test Location'
    }
    
    print("\nCreating test user...")
    user = db.create_or_update_user(test_user)
    print(f"✓ User created: {user.get('username')}")
    
    # Create sample analyses
    print("\nCreating sample analyses...")
    for i in range(5):
        analysis_data = {
            'repository_name': f'test/repo-{i+1}',
            'overall_repository_risk': 0.3 + (i * 0.1),
            'modules': [
                {
                    'file': f'src/file{i+1}.js',
                    'risk_score': 0.5 + (i * 0.05),
                    'reason': f'Test reason {i+1}'
                }
            ],
            'metadata': {
                'stars': 100 + i,
                'forks': 50 + i,
                'language': 'JavaScript'
            }
        }
        
        analysis_id = db.save_analysis('60312089', analysis_data)
        print(f"  ✓ Analysis {i+1} saved: {analysis_id}")
    
    # Get stats
    print("\nFetching user stats...")
    stats = db.get_user_stats('60312089')
    print(f"  Total Analyses: {stats['total_analyses']}")
    print(f"  Repositories: {stats['repositories_analyzed']}")
    print(f"  Average Risk: {stats['average_risk']:.2%}")
    
    # Get trends
    print("\nFetching trends...")
    trends = db.get_analytics_trends('60312089')
    print(f"  Data points: {len(trends['labels'])}")
    print(f"  Risk scores: {trends['risk_scores']}")
    
    print("\n" + "=" * 50)
    print("✓ MongoDB test complete!")
    print("=" * 50)
    print("\nNow refresh your browser to see the data!")

if __name__ == "__main__":
    test_mongodb()
