@echo off
echo ========================================
echo Applying All Fixes
echo ========================================
echo.
echo This will:
echo 1. Test Gemini recommendations structure
echo 2. Restart backend server
echo 3. Open test helper for OAuth
echo.
pause

echo.
echo ========================================
echo Step 1: Testing Gemini Structure
echo ========================================
python test-gemini-recommendations.py
if errorlevel 1 (
    echo.
    echo ❌ Gemini test failed!
    echo Check your GEMINI_API_KEY in backend/.env
    pause
    exit /b 1
)

echo.
echo ========================================
echo Step 2: Restarting Backend
echo ========================================
echo Stopping existing backend...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Backend*" 2>nul
timeout /t 2 /nobreak >nul

echo Starting backend server...
cd backend
start "Backend Server" cmd /k "python -m uvicorn src.api:app --reload --host 0.0.0.0 --port 8000"
cd ..

echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

echo.
echo ========================================
echo Step 3: Opening Test Helper
echo ========================================
start test-oauth-flow.html

echo.
echo ========================================
echo ✅ All Fixes Applied!
echo ========================================
echo.
echo Next Steps:
echo 1. Use the test helper to clear browser storage
echo 2. Go to http://localhost:3000
echo 3. Test OAuth login
echo 4. Verify Gemini recommendations appear
echo.
echo Backend running at: http://localhost:8000
echo Frontend should be at: http://localhost:3000
echo.
echo Press any key to exit...
pause >nul
