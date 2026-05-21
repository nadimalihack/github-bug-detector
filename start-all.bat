@echo off
echo ========================================
echo Starting Github Bug Detection System
echo ========================================
echo.
echo Your current stats:
echo - Total Analyses: 1
echo - Repositories: 1
echo - Average Risk: 55%%
echo.
echo Starting servers...
echo.

echo Opening Backend in new window...
start "Backend Server" cmd /k "cd backend && python -m uvicorn src.api:app --reload"

timeout /t 3 /nobreak > nul

echo Opening Frontend in new window...
start "Frontend Server" cmd /k "cd frontend && npm run dev"

timeout /t 5 /nobreak > nul

echo.
echo ========================================
echo Servers are starting!
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Wait for both servers to start, then open:
echo http://localhost:5173
echo.
echo Your stats should appear automatically!
echo.
echo Press any key to open browser...
pause > nul

start http://localhost:5173

echo.
echo ========================================
echo To stop servers:
echo - Close the Backend Server window
echo - Close the Frontend Server window
echo ========================================
