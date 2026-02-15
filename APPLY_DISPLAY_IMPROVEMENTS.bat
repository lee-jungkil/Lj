@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ========================================
echo  Display Improvements v6.30.69
echo ========================================
echo.
echo This will apply:
echo   1. Remove DEBUG and verbose logs
echo   2. Add 10-minute screen clear
echo   3. Expand work status to 5 lines
echo   4. Increase sell history to 10
echo   5. Add real-time position update
echo.
echo ========================================
echo.
set /p confirm="Apply improvements? (Y/N): "
if /i not "%confirm%"=="Y" goto cancel

echo.
echo Running Python script...
python apply_display_improvements.py

if errorlevel 1 (
    echo.
    echo ❌ Failed to apply improvements
    pause
    goto end
)

echo.
echo ========================================
echo  Improvements Applied Successfully!
echo ========================================
echo.
echo Next steps:
echo   1. Stop the bot (Ctrl+C in bot window)
echo   2. Run MINIMAL_UPDATE.bat to restart
echo.
pause
goto end

:cancel
echo.
echo Cancelled.
timeout /t 2 /nobreak >nul

:end
