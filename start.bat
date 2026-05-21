@echo off
echo ========================================
echo Github Bug Detection System - Starting...
echo ========================================
echo.

echo Starting Backend Server...
start "Backend Server" cmd /k "cd backend\src && python api.py"
timeout /t 3 /nobreak > nul

echo Starting Frontend Server...
start "Frontend Server" cmd /k "cd frontend && npm run dev"
timeout /t 3 /nobreak > nul

echo.
echo ========================================
echo Servers Started!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to open browser...
pause > nul

start http://localhost:3000

echo.
echo To stop servers, close the terminal windows
echo.
