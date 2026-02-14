@echo off
REM Continue cleanup and start bot
chcp 65001 >nul
cls
echo.
echo ========================================================================
echo    Continuing cleanup and starting bot...
echo ========================================================================
echo.

REM Delete .pyc files
echo [1/3] Deleting .pyc files...
del /s /q *.pyc 2>nul
echo OK
echo.

REM Verify cache deleted
echo [2/3] Verifying cache deletion...
dir /s /b __pycache__ 2>nul
if %errorlevel% neq 0 (
    echo [OK] All cache deleted
) else (
    echo [WARNING] Some cache may remain
)
echo.

REM Start bot
echo [3/3] Starting bot...
echo.
echo Expected logs every 3 seconds:
echo   [HH:MM:SS] Position liquidation check #1
echo   [HH:MM:SS] KRW-XPL profit/loss: +31.93%%
echo   [HH:MM:SS] Take-profit trigger!
echo.
echo ========================================================================
echo.
pause

if exist RUN_PAPER_CLEAN.bat (
    call RUN_PAPER_CLEAN.bat
) else (
    echo ERROR: RUN_PAPER_CLEAN.bat not found!
    pause
)
