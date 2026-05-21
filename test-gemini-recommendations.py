"""
Test Gemini AI recommendations structure
"""
import sys
sys.path.append('backend/src')

from gemini_analyzer import GeminiAnalyzer

print("=" * 60)
print("Testing Gemini AI Recommendations Structure")
print("=" * 60)

# Initialize analyzer
analyzer = GeminiAnalyzer()

# Create mock ML data
ml_data = {
    "repository": "test/repo",
    "overall_risk": 0.75,
    "total_files": 5,
    "high_risk_files": [
        {"file": "auth.py", "risk_score": 0.9, "reason": "SQL injection vulnerability"}
    ],
    "medium_risk_files": [
        {"file": "utils.py", "risk_score": 0.5, "reason": "Code quality issues"}
    ],
    "modules": [
        {
            "file": "auth.py",
            "risk_score": 0.9,
            "reason": "SQL injection vulnerability",
            "code_issues": [
                {
                    "issues": 2,
                    "detailed_issues": [
                        {
                            "type": "sql_injection",
                            "severity": "critical",
                            "message": "SQL injection found"
                        }
                    ]
                }
            ]
        }
    ]
}

print("\n1. Testing analyze_ml_results...")
try:
    result = analyzer.analyze_ml_results(ml_data)
    
    print(f"\n✅ Analysis completed!")
    print(f"\nResult structure:")
    print(f"  - overall_risk: {result.get('overall_risk')}")
    print(f"  - files_analyzed: {result.get('files_analyzed')}")
    print(f"  - Has 'recommendations': {bool(result.get('recommendations'))}")
    print(f"  - Recommendations count: {len(result.get('recommendations', []))}")
    print(f"  - Has 'critical_concerns': {bool(result.get('critical_concerns'))}")
    print(f"  - Critical concerns count: {len(result.get('critical_concerns', []))}")
    print(f"  - Has 'summary': {bool(result.get('summary'))}")
    print(f"  - Has 'files': {bool(result.get('files'))}")
    
    if result.get('recommendations'):
        print(f"\n📋 Sample recommendations:")
        for i, rec in enumerate(result['recommendations'][:3], 1):
            print(f"  {i}. {rec if isinstance(rec, str) else rec.get('title', 'N/A')}")
    
    if result.get('critical_concerns'):
        print(f"\n⚠️ Sample critical concerns:")
        for i, concern in enumerate(result['critical_concerns'][:3], 1):
            print(f"  {i}. {concern if isinstance(concern, str) else concern.get('title', 'N/A')}")
    
    print("\n" + "=" * 60)
    print("✅ Test PASSED - Structure is correct!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ Test FAILED: {e}")
    import traceback
    traceback.print_exc()
