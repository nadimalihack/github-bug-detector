@echo off
echo ========================================
echo Github Bug Detection System - Setup
echo ========================================
echo.

echo [1/4] Installing Backend Dependencies...
cd backend
pip install -r requirements.txt
cd ..

echo.
echo [2/4] Installing Frontend Dependencies...
cd frontend
call npm install
cd ..

echo.
echo [3/4] Testing GitHub Integration...
cd backend
python test_github.py
cd ..

echo.
echo [4/4] Setup Complete!
echo.
echo ========================================
echo Next Steps:
echo ========================================
echo.
echo 1. Start Backend:  start_backend.bat
echo 2. Start Frontend: start_frontend.bat
echo 3. Open Browser:   http://localhost:3000
echo.
echo Or read QUICKSTART.md for detailed instructions
echo.

pause
