@echo off
echo ========================================
echo FORCE RESTARTING BACKEND
echo ========================================
echo.

echo Step 1: Killing ALL Python processes...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Step 2: Killing processes on port 8000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do (
    echo Killing PID: %%a
    taskkill /F /PID %%a 2>nul
)

echo.
echo Step 3: Waiting 3 seconds...
timeout /t 3 /nobreak >nul

echo.
echo Step 4: Starting fresh backend...
cd src
start cmd /k "python api.py"

echo.
echo ========================================
echo Backend restarted in new window!
echo ========================================
echo.
echo Wait 5 seconds, then refresh your browser
echo.
pause
