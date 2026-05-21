@echo off
echo ========================================
echo Starting Backend Server
echo ========================================
echo.
echo IMPORTANT: Do NOT run "python api.py" directly!
echo This script uses the correct command.
echo.
cd backend
echo Running: python -m uvicorn src.api:app --reload
echo.
python -m uvicorn src.api:app --reload
