@echo off
echo ========================================
echo Installing Enhanced Features
echo ========================================
echo.

echo Installing backend dependencies...
cd backend
pip install google-generativeai authlib python-jose[cryptography] httpx

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Installation failed!
    echo.
    echo Try installing individually:
    echo   pip install google-generativeai
    echo   pip install authlib
    echo   pip install python-jose[cryptography]
    echo   pip install httpx
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✓ Enhanced features installed!
echo ========================================
echo.
echo You can now use:
echo - Gemini AI Analysis
echo - GitHub OAuth
echo - User Management
echo - Analytics Dashboard
echo.
echo Restart your backend server to enable features.
echo.
pause
