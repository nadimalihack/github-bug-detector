@echo off
echo ========================================
echo Checking Backend Status
echo ========================================
echo.

echo Testing if backend is running...
curl -s http://localhost:8000/ > nul 2>&1
if %errorlevel% neq 0 (
    echo Backend is NOT running!
    echo Starting backend...
    cd src
    start cmd /k python api.py
    timeout /t 3 /nobreak >nul
    cd ..
) else (
    echo Backend is running
)

echo.
echo Testing progress endpoint...
curl -s http://localhost:8000/progress/test 2>&1 | findstr "404" > nul
if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo ERROR: Progress endpoint not found!
    echo ========================================
    echo.
    echo The backend is running OLD code.
    echo You MUST restart it to load new features.
    echo.
    echo Steps:
    echo 1. Find terminal running "python api.py"
    echo 2. Press Ctrl+C to stop it
    echo 3. Run: cd backend\src
    echo 4. Run: python api.py
    echo.
    pause
) else (
    echo Progress endpoint exists!
    echo Backend is ready.
)
