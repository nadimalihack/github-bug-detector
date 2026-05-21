@echo off
echo ========================================
echo Force Restarting Backend Server
echo ========================================
echo.

echo Stopping any running Python processes...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Starting backend with new code...
cd backend\src
start "Bug Predictor Backend" cmd /k "python api.py"

echo.
echo ========================================
echo Backend server restarting...
echo ========================================
echo.
echo Wait 5 seconds, then test:
timeout /t 5 /nobreak

echo.
echo Testing endpoint...
curl http://localhost:8000/auth/github

echo.
echo.
echo If you see JSON with "authorization_url", it works!
echo If you see 404, wait a few more seconds and try again.
echo.
pause
