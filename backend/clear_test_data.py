"""
Clear test data from MongoDB
"""
import sys
sys.path.append('src')

from mongodb_manager import MongoDBManager

def clear_test_data():
    print("Clearing test data from MongoDB...")
    
    db = MongoDBManager()
    
    if not db.is_connected():
        print("✗ MongoDB not connected!")
        return
    
    # Delete test analyses
    result = db.db.analyses.delete_many({'repository_name': {'$regex': '^test/'}})
    print(f"✓ Deleted {result.deleted_count} test analyses")
    
    # Keep your real user but reset analysis count
    db.db.users.update_one(
        {'user_id': '60312089'},
        {'$set': {'analysis_count': 0}}
    )
    print("✓ Reset analysis count")
    
    # Count real analyses
    real_analyses = db.db.analyses.count_documents({'user_id': '60312089'})
    print(f"✓ Real analyses in DB: {real_analyses}")
    
    print("\nDone! Refresh your browser to see updated stats.")

if __name__ == "__main__":
    clear_test_data()
