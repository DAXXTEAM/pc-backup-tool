@echo off
echo ========================================
echo    PC AUTO BACKUP TOOL
echo ========================================
echo.
echo Starting backup...
echo.

python backup.py %~d0

echo.
echo ========================================
echo    BACKUP COMPLETE!
echo ========================================
echo.
pause
