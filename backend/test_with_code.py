"""Test with actual code containing issues"""
import sys
sys.path.append('src')

from predictor import BugPredictor

# Create test data with code issues
test_data = {
    "repository_name": "test/repo",
    "commits": [
        {
            "hash": "abc123",
            "message": "Fixed SQL injection bug",
            "diff": """
+ const query = "SELECT * FROM users WHERE id = '" + userId + "'";
+ db.execute(query);
""",
            "files_changed": ["database.js"],
            "code_issues": [
                {
                    "file": "database.js",
                    "issues": 1,
                    "severity_counts": {"critical": 1, "high": 0, "medium": 0, "low": 0},
                    "detailed_issues": [
                        {
                            "type": "sql_injection",
                            "severity": "critical",
                            "message": "Potential SQL injection vulnerability",
                            "line": 1,
                            "code_snippet": "const query = \"SELECT * FROM users WHERE id = '\" + userId + \"'\";",
                            "fix": "Use parameterized queries or prepared statements",
                            "impact": "Attackers can execute arbitrary SQL, steal or delete data"
                        }
                    ]
                }
            ]
        },
        {
            "hash": "def456",
            "message": "Added logging",
            "diff": """
+ console.log("User data:", userData);
+ console.log("Processing...");
""",
            "files_changed": ["app.js"],
            "code_issues": [
                {
                    "file": "app.js",
                    "issues": 2,
                    "severity_counts": {"critical": 0, "high": 0, "medium": 0, "low": 2},
                    "detailed_issues": [
                        {
                            "type": "console_log",
                            "severity": "low",
                            "message": "Console statements left in code",
                            "line": 1,
                            "code_snippet": "console.log(\"User data:\", userData);",
                            "fix": "Remove console statements or use proper logging",
                            "impact": "Can expose sensitive data and clutter production logs"
                        },
                        {
                            "type": "console_log",
                            "severity": "low",
                            "message": "Console statements left in code",
                            "line": 2,
                            "code_snippet": "console.log(\"Processing...\");",
                            "fix": "Remove console statements or use proper logging",
                            "impact": "Can expose sensitive data and clutter production logs"
                        }
                    ]
                }
            ]
        }
    ],
    "issues": []
}

print("=" * 70)
print("Testing Predictor with Code Issues")
print("=" * 70)

predictor = BugPredictor()
result = predictor.predict_repository_risk(test_data)

print(f"\nRepository: {result['repository_name']}")
print(f"Overall Risk: {result['overall_repository_risk']}")
print(f"\nModules:")

for module in result['modules']:
    print(f"\n  {module['file']}:")
    print(f"    Risk Score: {module['risk_score']}")
    print(f"    Reason: {module['reason']}")
    print(f"    Critical Issues: {module.get('critical_issues', 0)}")
    print(f"    High Issues: {module.get('high_issues', 0)}")
    print(f"    Detailed Issues Count: {len(module.get('detailed_issues', []))}")
    
    if module.get('detailed_issues'):
        print(f"\n    Detailed Issues:")
        for issue in module['detailed_issues']:
            print(f"      - [{issue['severity']}] {issue['message']}")
            print(f"        Line {issue['line']}: {issue['code_snippet']}")
            print(f"        Fix: {issue['fix']}")

print("\n" + "=" * 70)
print("✓ Test complete!")
print("=" * 70)
