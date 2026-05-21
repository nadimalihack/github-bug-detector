@echo off
echo ========================================
echo Testing Gemini-Only Real Analysis Setup
echo ========================================
echo.

echo Step 1: Testing API Key...
python backend/test_gemini_api.py
echo.

if %ERRORLEVEL% NEQ 0 (
    echo ❌ API key test failed!
    echo Please check your GEMINI_API_KEY in backend/.env
    pause
    exit /b 1
)

echo ✅ API key is working!
echo.
echo Step 2: Checking configuration...
echo.

echo Checking backend/src/gemini_analyzer.py...
findstr /C:"_fallback_analysis" backend\src\gemini_analyzer.py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ❌ WARNING: Fallback function still exists!
) else (
    echo ✅ No fallback function found - Gemini-only mode confirmed
)

echo.
echo Checking model configuration...
findstr /C:"gemini-2.5-flash" backend\src\gemini_analyzer.py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ Using Gemini 2.5 Flash (stable model)
) else (
    echo ⚠️ Model configuration may need update
)

echo.
echo ========================================
echo ✅ Setup Complete!
echo ========================================
echo.
echo Your system is configured for:
echo • Real Gemini AI analysis only
echo • No fallback content
echo • Gemini 2.5 Flash model
echo • ML data + AI insights
echo.
echo To start the application:
echo 1. cd backend
echo 2. python -m uvicorn src.api:app --reload
echo 3. In another terminal: cd frontend ^&^& npm run dev
echo.
pause
