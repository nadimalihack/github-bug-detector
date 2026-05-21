@echo off
echo ========================================
echo Restarting Backend Server
echo ========================================

echo.
echo Stopping any running backend processes...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Backend*" 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Starting backend server...
cd backend
start "Backend Server" cmd /k "python -m uvicorn src.api:app --reload --host 0.0.0.0 --port 8000"

echo.
echo ========================================
echo Backend server restarted!
echo ========================================
echo.
echo Backend running at: http://localhost:8000
echo.
echo Press any key to exit...
pause >nul
