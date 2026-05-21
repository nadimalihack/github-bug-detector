@echo off
echo ========================================
echo Testing Real-Time Data Features
echo ========================================
echo.

cd backend

echo Checking if backend is running...
curl -s http://localhost:8000/ > nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Backend is not running!
    echo Please start the backend first:
    echo   cd backend
    echo   python -m uvicorn src.api:app --reload
    echo.
    pause
    exit /b 1
)

echo Backend is running!
echo.
echo Running real-time data tests...
echo.

python test_realtime_data.py

echo.
echo ========================================
echo Test Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Open http://localhost:5173 in your browser
echo 2. Login with GitHub OAuth
echo 3. Analyze a repository
echo 4. Watch the stats update in real-time!
echo.
echo Check these sections:
echo - Dashboard sidebar (updates every 5 seconds)
echo - Analytics tab (updates every 10 seconds)
echo - Profile tab (updates every 10 seconds)
echo.
pause
