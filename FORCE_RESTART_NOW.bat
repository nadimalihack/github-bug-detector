@echo off
echo ========================================
echo FORCE RESTARTING BACKEND
echo ========================================
echo.

echo Step 1: Killing all Python processes...
taskkill /F /IM python.exe 2>nul
timeout /t 3 /nobreak >nul

echo.
echo Step 2: Clearing Python cache...
cd backend
if exist __pycache__ rmdir /s /q __pycache__
if exist src\__pycache__ rmdir /s /q src\__pycache__

echo.
echo Step 3: Starting fresh backend server...
start "Backend Server - FIXED" cmd /k "python -m uvicorn src.api:app --reload --host 0.0.0.0 --port 8000"

echo.
echo ========================================
echo Backend restarted with FIXED code!
echo ========================================
echo.
echo Wait 5 seconds, then refresh your browser
echo.
timeout /t 5 /nobreak
echo Ready! Try your analysis again.
pause
