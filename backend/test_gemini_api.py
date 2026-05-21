"""
Test Gemini API connection with stable model
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key found: {api_key[:20]}..." if api_key else "❌ No API key found")

if not api_key:
    print("\n⚠️ Please add GEMINI_API_KEY to backend/.env file")
    exit(1)

try:
    genai.configure(api_key=api_key)
    
    print("\n🧪 Testing Gemini 2.5 Flash (stable model for free tier)...")
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    response = model.generate_content("Say 'Hello, Gemini is working!' in one sentence.")
    print(f"\n✅ Gemini Response: {response.text}")
    print("\n✅ SUCCESS! Your API key is working with Gemini 2.5 Flash!")
    print("✅ You can now use real Gemini AI analysis in your application.")
    
except Exception as e:
    print(f"\n❌ Gemini API Error: {e}")
    print("\n⚠️ Possible issues:")
    print("1. API key quota exceeded - Free tier has limits:")
    print("   • 15 requests per minute")
    print("   • 1 million tokens per minute")
    print("   • 1,500 requests per day")
    print("   Wait 1 hour or get a new API key")
    print("\n2. Get new API key from: https://makersuite.google.com/app/apikey")
    print("\n3. Check your quota at: https://ai.dev/usage")
