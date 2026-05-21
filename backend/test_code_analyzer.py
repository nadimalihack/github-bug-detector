"""Test the code analyzer"""
import sys
sys.path.append('src')

from code_analyzer import CodeAnalyzer

# Test code samples with various issues
test_samples = {
    "SQL Injection": """
def get_user(username):
    query = "SELECT * FROM users WHERE name = '" + username + "'"
    return db.execute(query)
""",
    "Hardcoded Password": """
const config = {
    password: "admin123",
    apiKey: "secret-key-here"
}
""",
    "Empty Catch Block": """
try {
    riskyOperation()
} catch (error) {
}
""",
    "Eval Usage": """
function executeCode(code) {
    return eval(code)
}
""",
    "Console Logs": """
function processData(data) {
    console.log("Processing:", data)
    return data.map(x => x * 2)
}
""",
    "Clean Code": """
function calculateTotal(items) {
    return items.reduce((sum, item) => sum + item.price, 0)
}
"""
}

analyzer = CodeAnalyzer()

print("=" * 70)
print("CODE ANALYZER TEST")
print("=" * 70)

for name, code in test_samples.items():
    print(f"\n{name}:")
    print("-" * 70)
    
    result = analyzer.analyze_code(code, "test.js")
    
    print(f"Total Issues: {result['total_issues']}")
    print(f"Severity Breakdown: {result['severity_counts']}")
    
    if result['issues']:
        print("\nIssues Found:")
        for issue in result['issues']:
            severity_emoji = {
                'critical': '🔴',
                'high': '🟠',
                'medium': '🟡',
                'low': '🟢'
            }.get(issue['severity'], '⚪')
            
            print(f"  {severity_emoji} Line {issue['line']}: {issue['message']}")
            print(f"     Code: {issue['code_snippet']}")
    else:
        print("✓ No issues found!")
    
    quality_score = analyzer.calculate_code_quality_score(result)
    print(f"\nCode Quality Score: {quality_score * 100:.0f}%")

print("\n" + "=" * 70)
print("✓ Code Analyzer is working!")
print("=" * 70)
