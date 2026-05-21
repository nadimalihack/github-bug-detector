@echo off
echo ========================================
echo Testing Live Stats Update
echo ========================================
echo.

echo Current stats for user 60312089:
python backend/check_user_stats.py
echo.

echo ========================================
echo.
echo Now:
echo 1. Go to your browser (http://localhost:3000)
echo 2. Click "Analyze" on any repository
echo 3. Wait for analysis to complete
echo 4. Watch the sidebar stats update!
echo.
echo The stats should update within 5-10 seconds.
echo.
echo After analyzing, press any key to check if data was saved...
pause

echo.
echo Checking updated stats...
python backend/check_user_stats.py
echo.

echo ========================================
echo.
echo If the analysis count increased, it's working!
echo If not, check:
echo - Backend console for "💾 Saving analysis for user" message
echo - Browser console for "✅ Analysis complete" message
echo.
pause
