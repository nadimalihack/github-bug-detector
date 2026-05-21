"""Test the self-learning system"""
import sys
sys.path.append('src')

from incremental_learner import IncrementalLearner

print("=" * 70)
print("Testing Self-Learning System")
print("=" * 70)

# Initialize learner
learner = IncrementalLearner()

# Simulate some analyses and feedback
print("\n1. Simulating user analyses and feedback...")

# Mock analysis data
mock_analyses = [
    {
        'repository_name': 'test/repo1',
        'modules': [
            {'file': 'auth.js', 'risk_score': 0.85, 'critical_issues': 2, 'high_issues': 1},
            {'file': 'db.js', 'risk_score': 0.45, 'critical_issues': 0, 'high_issues': 1},
        ]
    },
    {
        'repository_name': 'test/repo2',
        'modules': [
            {'file': 'api.js', 'risk_score': 0.65, 'critical_issues': 1, 'high_issues': 0},
            {'file': 'utils.js', 'risk_score': 0.25, 'critical_issues': 0, 'high_issues': 0},
        ]
    }
]

# Record analyses
for analysis in mock_analyses:
    record_id = learner.record_analysis(
        {'repository_name': analysis['repository_name']},
        {'modules': analysis['modules'], 'overall_repository_risk': 0.5}
    )
    print(f"  Recorded analysis #{record_id}: {analysis['repository_name']}")

# Add feedback
print("\n2. Adding user feedback...")
feedback_data = [
    (0, 'auth.js', True),   # High risk, actually had bugs
    (0, 'db.js', False),    # Medium risk, no bugs
    (1, 'api.js', True),    # Medium risk, had bugs
    (1, 'utils.js', False), # Low risk, no bugs
]

for record_id, file_name, had_bugs in feedback_data:
    success = learner.add_user_feedback(record_id, file_name, had_bugs)
    status = "✓" if success else "✗"
    print(f"  {status} Feedback: {file_name} -> {'Had bugs' if had_bugs else 'No bugs'}")

# Get stats
print("\n3. Learning Statistics:")
stats = learner.get_learning_stats()
for key, value in stats.items():
    print(f"  {key}: {value}")

# Try retraining (will fail - not enough data)
print("\n4. Attempting to retrain...")
success = learner.retrain_model(min_feedback_samples=3)

if success:
    print("  ✓ Model retrained successfully!")
else:
    print("  ⚠ Not enough feedback yet (need 10+ samples)")
    print("  💡 In production, collect feedback from real analyses")

print("\n" + "=" * 70)
print("Self-Learning System Test Complete!")
print("=" * 70)

print("\n📚 Next Steps:")
print("  1. Restart backend: cd backend/src && python api.py")
print("  2. Analyze repositories in the UI")
print("  3. Click '✅ Had Bugs' or '❌ No Bugs' for each file")
print("  4. System auto-retrains after 20 feedback items")
print("  5. Model improves over time!")
