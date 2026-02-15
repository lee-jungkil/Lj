@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ========================================
echo  Remove DEBUG Logs v6.30.70
echo ========================================
echo.
echo This will remove all [DEBUG] log lines
echo from the bot for cleaner console output.
echo.
echo ========================================
echo.
set /p confirm="Remove DEBUG logs? (Y/N): "
if /i not "%confirm%"=="Y" goto cancel

echo.
echo Running cleanup script...
python remove_debug_logs.py

if errorlevel 1 (
    echo.
    echo ❌ Failed to remove DEBUG logs
    pause
    goto end
)

echo.
echo ========================================
echo  Cleanup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Stop the bot (Ctrl+C in bot window)
echo   2. Clear cache: del /s /q *.pyc
echo   3. Restart: python -B -u -m src.main --mode paper
echo.
echo Or run: MINIMAL_UPDATE.bat
echo.
pause
goto end

:cancel
echo.
echo Cancelled.
timeout /t 2 /nobreak >nul

:end
