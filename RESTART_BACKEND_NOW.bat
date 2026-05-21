@echo off
cls
echo ========================================
echo IMPORTANT: RESTART YOUR BACKEND SERVER
echo ========================================
echo.
echo Your backend is running OLD code!
echo.
echo Current status shows:
echo   "features": {
echo     "self_learning": true,
echo     "feedback_api": true,
echo     "code_analysis": true
echo   }
echo.
echo It should show:
echo   "features": {
echo     "enhanced_features": true,
echo     "gemini_ai": true,
echo     "oauth": true
echo   }
echo.
echo ========================================
echo HOW TO FIX:
echo ========================================
echo.
echo 1. Go to your backend terminal window
echo 2. Press Ctrl+C to stop the server
echo 3. Run these commands:
echo.
echo    cd backend\src
echo    python api.py
echo.
echo 4. Look for this message:
echo    "Enhanced features enabled (OAuth, Gemini AI, User Management)"
echo.
echo 5. Then refresh your browser
echo.
echo ========================================
pause
