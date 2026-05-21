@echo off
echo Killing all Python processes...
taskkill /F /IM python.exe /T 2>nul
timeout /t 3 /nobreak >nul

echo.
echo Starting fresh backend server...
echo.
cd backend\src
python api.py
