@echo off
echo ========================================
echo Restarting Bug Prediction Backend
echo ========================================
echo.

echo Stopping old backend process...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
    echo Killing process %%a
    taskkill /F /PID %%a 2>nul
)

timeout /t 2 /nobreak >nul

echo.
echo Starting backend...
cd backend\src
start "Bug Prediction Backend" cmd /k python api.py

echo.
echo ========================================
echo Backend restarted!
echo ========================================
echo.
echo Check the new window for backend logs
echo API available at: http://localhost:8000
echo.

pause
