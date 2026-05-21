@echo off
echo Killing process on port 8000...

for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do (
    echo Found process: %%a
    taskkill /F /PID %%a 2>nul
)

echo.
echo Waiting 2 seconds...
timeout /t 2 /nobreak >nul

echo.
echo Starting backend server...
cd src
python api.py
