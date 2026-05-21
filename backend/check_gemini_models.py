import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key: {api_key[:20]}...")

genai.configure(api_key=api_key)

print("\n📋 Available Gemini Models:")
print("-" * 50)

try:
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✓ {model.name}")
            print(f"  Display Name: {model.display_name}")
            print(f"  Description: {model.description[:100] if model.description else 'N/A'}")
            print()
except Exception as e:
    print(f"❌ Error listing models: {e}")
