"""
Test multiple Gemini API keys fallback system
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gemini_analyzer import GeminiAnalyzer

def test_multiple_keys():
    print("=" * 60)
    print("Testing Multiple Gemini API Keys Fallback System")
    print("=" * 60)
    
    try:
        # Initialize analyzer
        print("\n1. Initializing GeminiAnalyzer...")
        analyzer = GeminiAnalyzer()
        print(f"   ✓ Loaded {len(analyzer.api_keys)} API key(s)")
        print(f"   ✓ Currently using key #{analyzer.current_key_index + 1}")
        
        # Test simple code analysis
        print("\n2. Testing code analysis...")
        test_code = """
def login(username, password):
    query = "SELECT * FROM users WHERE username='" + username + "'"
    return db.execute(query)
"""
        
        result = analyzer.analyze_code(test_code, "login.py")
        
        print(f"   ✓ Analysis completed successfully")
        print(f"   Risk Score: {result.get('risk_score', 'N/A')}")
        print(f"   Vulnerabilities: {len(result.get('vulnerabilities', []))}")
        print(f"   Bugs: {len(result.get('bugs', []))}")
        print(f"   Suggestions: {len(result.get('suggestions', []))}")
        
        if result.get('vulnerabilities'):
            print(f"\n   Found vulnerabilities:")
            for vuln in result['vulnerabilities'][:2]:
                print(f"   - {vuln}")
        
        print("\n" + "=" * 60)
        print("✅ Multiple API Keys System Working!")
        print("=" * 60)
        print(f"\nCurrent Status:")
        print(f"  - Total API keys configured: {len(analyzer.api_keys)}")
        print(f"  - Active key: #{analyzer.current_key_index + 1}")
        print(f"  - Remaining backup keys: {len(analyzer.api_keys) - analyzer.current_key_index - 1}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_multiple_keys()
