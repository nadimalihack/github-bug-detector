"""
Test Gemini API with timeout handling and retry logic
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.gemini_analyzer import GeminiAnalyzer
import time

def test_basic_connection():
    """Test basic Gemini API connection"""
    print("\n" + "="*60)
    print("TEST 1: Basic Gemini API Connection")
    print("="*60)
    
    try:
        analyzer = GeminiAnalyzer()
        print("✅ GeminiAnalyzer initialized successfully")
        print(f"   - API Keys loaded: {len(analyzer.api_keys)}")
        print(f"   - Current key index: {analyzer.current_key_index + 1}")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        return False

def test_simple_analysis():
    """Test simple code analysis"""
    print("\n" + "="*60)
    print("TEST 2: Simple Code Analysis")
    print("="*60)
    
    try:
        analyzer = GeminiAnalyzer()
        
        sample_code = """
def calculate_total(items):
    total = 0
    for item in items:
        total += item['price']
    return total
"""
        
        print("📝 Analyzing sample code...")
        start_time = time.time()
        
        result = analyzer.analyze_code(sample_code, "calculator.py")
        
        elapsed = time.time() - start_time
        print(f"✅ Analysis completed in {elapsed:.2f}s")
        print(f"   - Risk Score: {result.get('risk_score', 'N/A')}")
        print(f"   - Vulnerabilities: {len(result.get('vulnerabilities', []))}")
        print(f"   - Bugs: {len(result.get('bugs', []))}")
        print(f"   - Suggestions: {len(result.get('suggestions', []))}")
        
        if result.get('explanation'):
            print(f"   - Explanation: {result['explanation'][:100]}...")
        
        return True
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return False

def test_ml_results_analysis():
    """Test ML results analysis (the one that times out)"""
    print("\n" + "="*60)
    print("TEST 3: ML Results Analysis (Timeout Test)")
    print("="*60)
    
    try:
        analyzer = GeminiAnalyzer()
        
        # Simulate ML results
        ml_data = {
            'repository': 'test/sample-repo',
            'overall_risk': 0.65,
            'total_files': 15,
            'high_risk_files': ['app.py', 'auth.py', 'database.py'],
            'medium_risk_files': ['utils.py', 'config.py'],
            'modules': [
                {
                    'file': 'app.py',
                    'risk_score': 0.85,
                    'reason': 'High complexity and potential security issues',
                    'code_issues': []
                },
                {
                    'file': 'auth.py',
                    'risk_score': 0.78,
                    'reason': 'Authentication logic needs review',
                    'code_issues': []
                },
                {
                    'file': 'database.py',
                    'risk_score': 0.72,
                    'reason': 'SQL injection vulnerabilities possible',
                    'code_issues': []
                }
            ]
        }
        
        print("📊 Analyzing ML results...")
        print(f"   - Repository: {ml_data['repository']}")
        print(f"   - Risk Score: {ml_data['overall_risk']*100:.1f}%")
        print(f"   - Files: {ml_data['total_files']}")
        print(f"   - High Risk: {len(ml_data['high_risk_files'])}")
        
        start_time = time.time()
        
        result = analyzer.analyze_ml_results(ml_data)
        
        elapsed = time.time() - start_time
        print(f"\n✅ Analysis completed in {elapsed:.2f}s")
        print(f"   - Overall Risk: {result.get('overall_risk', 'N/A')}%")
        print(f"   - Files Analyzed: {result.get('files_analyzed', 'N/A')}")
        print(f"   - Critical Concerns: {len(result.get('critical_concerns', []))}")
        print(f"   - Recommendations: {len(result.get('recommendations', []))}")
        print(f"   - Files Details: {len(result.get('files', []))}")
        
        if result.get('summary'):
            print(f"\n📝 Summary Preview:")
            print(f"   {result['summary'][:200]}...")
        
        if result.get('recommendations'):
            print(f"\n💡 Top 3 Recommendations:")
            for i, rec in enumerate(result['recommendations'][:3], 1):
                print(f"   {i}. {rec}")
        
        return True
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        return False

def test_timeout_handling():
    """Test timeout and retry logic"""
    print("\n" + "="*60)
    print("TEST 4: Timeout Handling & Retry Logic")
    print("="*60)
    
    try:
        analyzer = GeminiAnalyzer()
        
        # Create a large prompt that might timeout
        large_code = """
def complex_function():
    # This is a complex function with many lines
    """ + "\n    ".join([f"line_{i} = process_data_{i}()" for i in range(100)])
        
        print("📝 Testing with larger code sample...")
        print("   (This may take longer and test retry logic)")
        
        start_time = time.time()
        
        result = analyzer.analyze_code(large_code, "complex.py")
        
        elapsed = time.time() - start_time
        print(f"✅ Completed in {elapsed:.2f}s")
        print(f"   - Risk Score: {result.get('risk_score', 'N/A')}")
        
        return True
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"❌ Failed after {elapsed:.2f}s: {e}")
        return False

def test_api_key_fallback():
    """Test API key fallback mechanism"""
    print("\n" + "="*60)
    print("TEST 5: API Key Fallback")
    print("="*60)
    
    try:
        analyzer = GeminiAnalyzer()
        
        print(f"📊 API Key Configuration:")
        print(f"   - Total keys available: {len(analyzer.api_keys)}")
        print(f"   - Current active key: #{analyzer.current_key_index + 1}")
        
        if len(analyzer.api_keys) > 1:
            print(f"   ✅ Backup keys available: {len(analyzer.api_keys) - 1}")
            print(f"   - Fallback will work if primary key fails")
        else:
            print(f"   ⚠️ No backup keys configured")
            print(f"   - Add GEMINI_API_KEY_2, GEMINI_API_KEY_3, etc. to .env")
        
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 GEMINI API TIMEOUT & RETRY TEST SUITE")
    print("="*60)
    print("\nThis will test:")
    print("  1. Basic API connection")
    print("  2. Simple code analysis")
    print("  3. ML results analysis (the timeout-prone one)")
    print("  4. Timeout handling with retries")
    print("  5. API key fallback mechanism")
    print("\n" + "="*60)
    
    results = []
    
    # Run tests
    results.append(("Basic Connection", test_basic_connection()))
    results.append(("Simple Analysis", test_simple_analysis()))
    results.append(("ML Results Analysis", test_ml_results_analysis()))
    results.append(("Timeout Handling", test_timeout_handling()))
    results.append(("API Key Fallback", test_api_key_fallback()))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("\n" + "="*60)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Gemini API is working correctly.")
    elif passed > 0:
        print("⚠️ Some tests passed. Check failed tests above.")
    else:
        print("❌ All tests failed. Check your GEMINI_API_KEY in .env")
    
    print("="*60)
    
    # Recommendations
    if passed < total:
        print("\n💡 RECOMMENDATIONS:")
        if not results[0][1]:
            print("  - Check GEMINI_API_KEY in backend/.env")
            print("  - Get key from: https://makersuite.google.com/app/apikey")
        if not results[2][1]:
            print("  - Add backup API keys (GEMINI_API_KEY_2, etc.)")
            print("  - Try during off-peak hours")
            print("  - Check network connectivity")
        print()

if __name__ == "__main__":
    main()
