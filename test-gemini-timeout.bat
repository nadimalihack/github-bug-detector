@echo off
echo ========================================
echo Testing Gemini API with Timeout Handling
echo ========================================
echo.

cd backend
python test_gemini_timeout.py

echo.
echo ========================================
echo Test Complete
echo ========================================
pause
