@echo off
echo ========================================
echo Bug Prediction Model Trainer
echo ========================================
echo.

cd src
python trainer.py

echo.
echo Press any key to exit...
pause > nul
