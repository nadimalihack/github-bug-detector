@echo off
echo ========================================
echo Github Bug Detection System - Installation
echo ========================================
echo.

echo [1/4] Installing Backend Dependencies...
cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Backend installation failed!
    pause
    exit /b 1
)
echo ✓ Backend dependencies installed
echo.

echo [2/4] Installing Frontend Dependencies...
cd ..\frontend
call npm install
if %errorlevel% neq 0 (
    echo ERROR: Frontend installation failed!
    pause
    exit /b 1
)
echo ✓ Frontend dependencies installed
echo.

echo [3/4] Checking Configuration...
cd ..\backend
if exist .env (
    echo ✓ .env file found
) else (
    echo WARNING: .env file not found!
    echo Please create .env file with your API keys
)
echo.

echo [4/4] Installation Complete!
echo.
echo ========================================
echo Next Steps:
echo ========================================
echo.
echo 1. Start Backend:
echo    cd backend\src
echo    python api.py
echo.
echo 2. Start Frontend (in new terminal):
echo    cd frontend
echo    npm run dev
echo.
echo 3. Open Browser:
echo    http://localhost:3000
echo.
echo ========================================
echo Documentation:
echo ========================================
echo - INSTALLATION_GUIDE.md
echo - NEW_FEATURES.md
echo - QUICKSTART.md
echo.
pause
