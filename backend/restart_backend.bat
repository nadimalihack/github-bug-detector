@echo off
echo ========================================
echo Restarting Backend Server
echo ========================================
echo.

echo Killing existing Python processes on port 8000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do (
    taskkill /F /PID %%a 2>nul
)

echo.
echo Waiting 2 seconds...
timeout /t 2 /nobreak >nul

echo.
echo Starting backend with new features...
cd src
python api.py
