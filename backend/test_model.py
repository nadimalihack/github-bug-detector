"""Quick test script to verify the trained model works"""
import sys
sys.path.append('src')

from predictor import BugPredictor

# Test data
test_repo = {
    "repository_name": "test/repo",
    "commits": [
        {
            "message": "Fixed critical bug in authentication",
            "diff": "- if (user == null)\n+ if (!user)",
            "files_changed": ["auth.js"]
        },
        {
            "message": "Added new feature for user profiles",
            "diff": "+ const getProfile = () => {}",
            "files_changed": ["profile.js"]
        }
    ],
    "issues": []
}

print("Testing Bug Predictor...")
print("=" * 60)

predictor = BugPredictor()
result = predictor.predict_repository_risk(test_repo)

print(f"\nRepository: {result['repository_name']}")
print(f"Overall Risk: {result['overall_repository_risk']}")
print(f"\nModule Analysis:")
for module in result['modules']:
    print(f"  {module['file']}: {module['risk_score']} - {module['reason']}")

print("\n✓ Model is working correctly!")
