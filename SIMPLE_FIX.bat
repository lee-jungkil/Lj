@echo off
REM ============================================================================
REM SIMPLE FIX - No Git Required
REM Just delete cache and restart bot
REM ============================================================================

if "%1" neq "NESTED" (
    cmd /k "%~f0" NESTED
    exit
)

chcp 65001
cls
echo.
echo ========================================================================
echo.
echo    SIMPLE FIX - Cache Cleanup Only (No Git)
echo.
echo ========================================================================
echo.
echo This will:
echo   1. Stop Python
echo   2. Delete all cache files
echo   3. Restart the bot
echo.
echo No git commands - just cache cleanup!
echo.
echo ========================================================================
echo.
echo Press ENTER to start...
pause >nul
echo.

REM Step 1: Stop Python
echo [Step 1/4] Stopping Python processes...
taskkill /F /IM python.exe >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python stopped
) else (
    echo [INFO] No Python processes running
)
echo.
timeout /t 2 >nul

REM Step 2: Delete cache
echo [Step 2/4] Deleting Python cache...
echo This will take a moment...
echo.

set count=0
for /d /r . %%d in (__pycache__) do (
    if exist "%%d" (
        echo Deleting: %%d
        rd /s /q "%%d" >nul 2>&1
        set /a count+=1
    )
)

echo.
echo Deleting .pyc files...
del /s /q *.pyc >nul 2>&1
echo.
echo [OK] Deleted %count% cache folders
echo.
timeout /t 2 >nul

REM Step 3: Verify
echo [Step 3/4] Verifying cache deletion...
dir /s /b __pycache__ >nul 2>&1
if %errorlevel% neq 0 (
    echo [OK] All cache deleted
) else (
    echo [WARNING] Some cache may remain - but should be OK
)
echo.
timeout /t 2 >nul

REM Step 4: Check version
echo [Step 4/4] Checking current version...
if exist VERSION.txt (
    type VERSION.txt | findstr /B "v"
    echo.
) else (
    echo [WARNING] VERSION.txt not found
)
echo.
timeout /t 2 >nul

echo ========================================================================
echo                        CACHE CLEANUP COMPLETE
echo ========================================================================
echo.
echo Next: Starting bot...
echo.
echo Expected logs every 3 seconds:
echo   [HH:MM:SS] Position liquidation check #1
echo   [HH:MM:SS] KRW-XXX profit/loss: X.XX%%
echo.
echo If logs don't appear, you may need to update code manually.
echo.
echo ========================================================================
echo.
echo Press ENTER to start bot now...
pause >nul

REM Start bot
echo.
echo Starting bot...
echo.
if exist RUN_PAPER_CLEAN.bat (
    call RUN_PAPER_CLEAN.bat
) else (
    echo [ERROR] RUN_PAPER_CLEAN.bat not found!
    echo Make sure you are in the correct directory.
    echo.
    pause
)
