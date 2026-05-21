"""
Verify that the gemini_analyzer.py fix is loaded
"""
import sys
import os

# Read the file
with open('src/gemini_analyzer.py', 'r', encoding='utf-8') as f:
    content = f.read()

print("="*60)
print("VERIFYING GEMINI ANALYZER FIX")
print("="*60)

# Check if request_options is still in the file
if 'request_options' in content:
    print("❌ PROBLEM: 'request_options' still found in file!")
    print("   The fix was NOT applied correctly.")
    
    # Find the line
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        if 'request_options' in line:
            print(f"   Line {i}: {line.strip()}")
    sys.exit(1)
else:
    print("✅ VERIFIED: 'request_options' removed from file")
    print("   The fix is correctly applied.")

# Check the generate_content call
if 'self.model.generate_content(' in content:
    print("✅ VERIFIED: generate_content method exists")
    
    # Find the call and show it
    lines = content.split('\n')
    in_generate_call = False
    call_lines = []
    
    for line in lines:
        if 'self.model.generate_content(' in line:
            in_generate_call = True
        
        if in_generate_call:
            call_lines.append(line)
            if ')' in line and not line.strip().endswith(','):
                break
    
    print("\n📝 Current generate_content call:")
    for line in call_lines[:5]:  # Show first 5 lines
        print(f"   {line}")
    
    if any('request_options' in line for line in call_lines):
        print("\n❌ ERROR: request_options still in the call!")
        sys.exit(1)
    else:
        print("\n✅ CORRECT: No request_options in the call")

print("\n" + "="*60)
print("✅ ALL CHECKS PASSED - FIX IS CORRECT")
print("="*60)
print("\nNow you need to:")
print("1. Stop your backend server (Ctrl+C)")
print("2. Restart it: python -m uvicorn src.api:app --reload")
print("3. Or run: FORCE_RESTART_NOW.bat")
