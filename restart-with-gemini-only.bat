@echo off
echo ========================================
echo Restarting with Gemini-Only Mode
echo ========================================
echo.

echo Step 1: Testing Gemini API Key...
python backend/test_gemini_api.py
echo.

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Gemini API test failed!
    echo.
    echo Please fix the API key issue before continuing.
    echo Get a new key from: https://makersuite.google.com/app/apikey
    echo.
    pause
    exit /b 1
)

echo ✅ Gemini API is working!
echo.

echo Step 2: Stopping any running servers...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM node.exe 2>nul
timeout /t 2 /nobreak >nul
echo.

echo Step 3: Starting Backend Server...
start "Backend Server" cmd /k "cd backend && python -m uvicorn src.api:app --reload"
timeout /t 3 /nobreak >nul
echo ✅ Backend started
echo.

echo Step 4: Starting Frontend Server...
start "Frontend Server" cmd /k "cd frontend && npm run dev"
timeout /t 3 /nobreak >nul
echo ✅ Frontend started
echo.

echo ========================================
echo ✅ Servers Started Successfully!
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo What to expect:
echo • Badge shows "⚡ Powered by Gemini 2.5 Flash"
echo • AI Solutions shows real Gemini recommendations
echo • Detailed analysis shows 400+ word AI summary
echo • If Gemini fails, you'll see clear error message
echo • NO fallback content - only real AI analysis
echo.
echo Press any key to open the application...
pause >nul
start http://localhost:5173
