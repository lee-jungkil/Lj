@echo off
REM ============================================================================
REM URGENT FIX - Position Check Not Working
REM This batch file will NOT close automatically - you must close it manually
REM ============================================================================

REM Force window to stay open even on error
if "%1" neq "NESTED" (
    cmd /k "%~f0" NESTED
    exit
)

chcp 65001
cls
echo.
echo ========================================================================
echo.
echo    URGENT FIX: Position Check Log Not Showing (v6.30.31)
echo.
echo ========================================================================
echo.
echo Current Problem:
echo   - Position exists but no liquidation check logs
echo   - Take-profit and stop-loss not executing
echo.
echo Root Cause: Python cached .pyc files from old version
echo.
echo Solution: Delete all cache + Force update + Restart
echo.
echo ========================================================================
echo.
echo Press ENTER to start fixing...
pause >nul
echo.

REM Step 1: Stop Python
echo [Step 1/7] Stopping all Python processes...
taskkill /F /IM python.exe >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python processes stopped
) else (
    echo [INFO] No Python processes found
)
echo.
echo Press ENTER to continue...
pause >nul

REM Step 2: Delete cache
echo.
echo [Step 2/7] Deleting Python cache...
echo This may take a moment...
for /d /r . %%d in (__pycache__) do @if exist "%%d" (
    echo Deleting: %%d
    rd /s /q "%%d" >nul 2>&1
)
del /s /q *.pyc >nul 2>&1
echo [OK] Cache deleted
echo.
echo Press ENTER to continue...
pause >nul

REM Step 3: Verify cache deleted
echo.
echo [Step 3/7] Verifying cache deletion...
dir /s /b __pycache__ >nul 2>&1
if %errorlevel% neq 0 (
    echo [OK] No __pycache__ folders found
) else (
    echo [WARNING] Some __pycache__ folders still exist
)
echo.
echo Press ENTER to continue...
pause >nul

REM Step 4: Git reset
echo.
echo [Step 4/7] Resetting git repository...
git reset --hard HEAD
if %errorlevel% neq 0 (
    echo [ERROR] Git reset failed!
    echo Make sure you are in the correct directory.
    echo.
    echo Press ENTER to exit...
    pause >nul
    exit /b 1
)
echo [OK] Git reset complete
echo.
echo Press ENTER to continue...
pause >nul

REM Step 5: Git pull
echo.
echo [Step 5/7] Pulling latest code...
git pull origin main
if %errorlevel% neq 0 (
    echo [ERROR] Git pull failed!
    echo Check your internet connection.
    echo.
    echo Press ENTER to exit...
    pause >nul
    exit /b 1
)
echo [OK] Code updated
echo.
echo Press ENTER to continue...
pause >nul

REM Step 6: Verify version
echo.
echo [Step 6/7] Verifying version...
type VERSION.txt | findstr "v6.30"
if %errorlevel% neq 0 (
    echo [WARNING] Version check uncertain
) else (
    echo [OK] Version verified
)
echo.
echo Current version:
type VERSION.txt | findstr /B "v"
echo.
echo Press ENTER to continue...
pause >nul

REM Step 7: Verify code
echo.
echo [Step 7/7] Verifying Phase 3 code...
findstr /N "if current_time - self.last_position_check_time" src\main.py | findstr "2143:"
if %errorlevel% neq 0 (
    echo [WARNING] Phase 3 code not found at line 2143
    echo This may be normal if line numbers changed
) else (
    echo [OK] Phase 3 code verified
)
echo.
echo Press ENTER to continue...
pause >nul

REM Final step
echo.
echo ========================================================================
echo                        ALL STEPS COMPLETE
echo ========================================================================
echo.
echo Next: Run RUN_PAPER_CLEAN.bat to start the bot
echo.
echo Expected logs every 3 seconds:
echo   [HH:MM:SS] Position liquidation check #1
echo   [HH:MM:SS] KRW-XXX profit/loss: X.XX%%
echo.
echo ========================================================================
echo.
echo Do you want to start the bot now? (Y/N)
set /p choice=Enter Y or N: 
if /i "%choice%"=="Y" (
    echo.
    echo Starting bot...
    echo.
    call RUN_PAPER_CLEAN.bat
) else (
    echo.
    echo OK - Run RUN_PAPER_CLEAN.bat when ready
    echo.
)

echo.
echo ========================================================================
echo This window will stay open - close it manually when done
echo ========================================================================
echo.
pause
