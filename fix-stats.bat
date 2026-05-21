@echo off
echo ========================================
echo Fixing Real-Time Stats Issue
echo ========================================
echo.

cd backend

echo Step 1: Checking current user stats...
echo.
python check_user_stats.py
echo.

echo ========================================
echo.
echo Step 2: Testing stats flow...
echo.
python test_stats_flow.py
echo.

echo ========================================
echo.
echo IMPORTANT: To fix your stats, you need to:
echo.
echo 1. Make sure the backend is running:
echo    cd backend
echo    python -m uvicorn src.api:app --reload
echo.
echo 2. In your browser, open the console (F12)
echo    and check what user ID is being used:
echo    localStorage.getItem('user')
echo.
echo 3. When you analyze a repository, check the
echo    browser console for messages like:
echo    "Analyzing repository: ... for user: ..."
echo.
echo 4. After analysis, check if data was saved:
echo    python backend/check_user_stats.py
echo.
echo 5. If stats still show 0, the issue might be:
echo    - User ID not being sent with analysis request
echo    - MongoDB not connected (check .env file)
echo    - Analysis failing silently
echo.
echo ========================================
pause
