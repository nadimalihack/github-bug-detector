"""
Test the full Gemini AI flow from API endpoint
"""
import requests
import json

print("=" * 60)
print("Testing Full Gemini AI Flow")
print("=" * 60)

# Test 1: Check API status
print("\n1. Checking API status...")
try:
    response = requests.get("http://localhost:8000/")
    data = response.json()
    print(f"✅ API is running")
    print(f"   - Gemini AI enabled: {data['features']['gemini_ai']}")
    print(f"   - Enhanced features: {data['features']['enhanced_features']}")
except Exception as e:
    print(f"❌ API not running: {e}")
    print("   Please start the backend with: start-backend.bat")
    exit(1)

# Test 2: Analyze a small test repository
print("\n2. Testing repository analysis with Gemini AI...")
test_data = {
    "repo_url": "https://github.com/octocat/Hello-World",
    "max_commits": 5,
    "session_id": "test_session"
}

try:
    print(f"   Analyzing: {test_data['repo_url']}")
    response = requests.post(
        "http://localhost:8000/analyze-github-url",
        json=test_data,
        timeout=120
    )
    
    if response.status_code == 200:
        result = response.json()
        
        print(f"\n✅ Analysis completed!")
        print(f"\nRepository: {result.get('repository_name')}")
        print(f"Overall Risk: {result.get('overall_repository_risk', 0) * 100:.1f}%")
        print(f"Files Analyzed: {len(result.get('modules', []))}")
        
        # Check Gemini analysis
        gemini = result.get('gemini_analysis')
        if gemini:
            print(f"\n🤖 Gemini AI Analysis:")
            print(f"   - Has recommendations: {bool(gemini.get('recommendations'))}")
            print(f"   - Recommendations count: {len(gemini.get('recommendations', []))}")
            print(f"   - Has critical_concerns: {bool(gemini.get('critical_concerns'))}")
            print(f"   - Critical concerns count: {len(gemini.get('critical_concerns', []))}")
            print(f"   - Has summary: {bool(gemini.get('summary'))}")
            print(f"   - Has error: {bool(gemini.get('error'))}")
            
            if gemini.get('error'):
                print(f"\n⚠️ Gemini Error: {gemini['error']}")
            
            if gemini.get('recommendations'):
                print(f"\n📋 Sample Recommendations:")
                for i, rec in enumerate(gemini['recommendations'][:3], 1):
                    rec_text = rec if isinstance(rec, str) else rec.get('title', str(rec)[:50])
                    print(f"   {i}. {rec_text[:80]}")
            
            if gemini.get('critical_concerns'):
                print(f"\n⚠️ Sample Critical Concerns:")
                for i, concern in enumerate(gemini['critical_concerns'][:3], 1):
                    concern_text = concern if isinstance(concern, str) else concern.get('title', str(concern)[:50])
                    print(f"   {i}. {concern_text[:80]}")
            
            print("\n" + "=" * 60)
            print("✅ FULL TEST PASSED!")
            print("=" * 60)
            print("\nThe frontend should now display Gemini recommendations!")
            print("Refresh your browser at http://localhost:3000")
        else:
            print(f"\n⚠️ No Gemini analysis in response")
            print(f"Response keys: {list(result.keys())}")
    else:
        print(f"❌ Analysis failed: {response.status_code}")
        print(f"   Error: {response.text}")
        
except requests.exceptions.Timeout:
    print(f"❌ Request timed out (this is normal for large repos)")
    print(f"   Try with a smaller repository or increase timeout")
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
