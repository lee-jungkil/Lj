@echo off
REM ============================================================================
REM COMPLETE REINSTALL - Download fresh copy from GitHub
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
echo    COMPLETE REINSTALL - Fresh Download from GitHub
echo.
echo ========================================================================
echo.
echo WARNING: This will:
echo   1. Backup current folder to Lj-main-backup
echo   2. Download completely fresh copy
echo   3. Copy your .env file back
echo   4. Install dependencies
echo   5. Start the bot
echo.
echo This is the MOST RELIABLE fix!
echo.
echo ========================================================================
echo.
echo Press ENTER to continue or close this window to cancel...
pause >nul
echo.

REM Step 1: Check current location
echo [Step 1/8] Checking current location...
cd
echo.
timeout /t 2 >nul

REM Step 2: Stop Python
echo [Step 2/8] Stopping all Python processes...
taskkill /F /IM python.exe >nul 2>&1
echo [OK] Python stopped
echo.
timeout /t 2 >nul

REM Step 3: Go to Downloads
echo [Step 3/8] Moving to Downloads folder...
cd C:\Users\admin\Downloads
if %errorlevel% neq 0 (
    echo [ERROR] Cannot access Downloads folder
    pause
    exit /b 1
)
echo [OK] In Downloads folder
echo.
timeout /t 2 >nul

REM Step 4: Backup .env file
echo [Step 4/8] Backing up .env file...
if exist Lj-main\Lj-main\.env (
    copy Lj-main\Lj-main\.env env_backup.txt >nul
    echo [OK] .env file backed up
) else (
    echo [WARNING] No .env file found
)
echo.
timeout /t 2 >nul

REM Step 5: Backup old folder
echo [Step 5/8] Backing up old folder...
if exist Lj-main-backup (
    echo Removing old backup...
    rd /s /q Lj-main-backup
)
if exist Lj-main (
    rename Lj-main Lj-main-backup
    echo [OK] Old folder backed up as Lj-main-backup
) else (
    echo [WARNING] No existing Lj-main folder
)
echo.
timeout /t 2 >nul

REM Step 6: Clone fresh copy
echo [Step 6/8] Downloading fresh copy from GitHub...
echo This may take a minute...
echo.
git clone https://github.com/lee-jungkil/Lj.git Lj-main
if %errorlevel% neq 0 (
    echo [ERROR] Git clone failed!
    echo.
    echo Possible reasons:
    echo   - No internet connection
    echo   - Git not installed
    echo   - GitHub repository not accessible
    echo.
    echo Restoring backup...
    if exist Lj-main-backup (
        rename Lj-main-backup Lj-main
    )
    pause
    exit /b 1
)
echo [OK] Fresh copy downloaded
echo.
timeout /t 2 >nul

REM Step 7: Restore .env file
echo [Step 7/8] Restoring .env file...
if exist env_backup.txt (
    copy env_backup.txt Lj-main\Lj-main\.env >nul
    del env_backup.txt >nul
    echo [OK] .env file restored
) else (
    echo [WARNING] No .env backup found
    echo You will need to configure .env manually
)
echo.
timeout /t 2 >nul

REM Step 8: Move to new folder
echo [Step 8/8] Moving to new folder...
cd Lj-main\Lj-main
echo [OK] Ready to start
echo.
timeout /t 2 >nul

REM Check version
echo ========================================================================
echo Checking version...
type VERSION.txt | findstr /B "v"
echo.

echo ========================================================================
echo                    REINSTALL COMPLETE
echo ========================================================================
echo.
echo Fresh installation ready!
echo.
echo Old folder backed up at: C:\Users\admin\Downloads\Lj-main-backup
echo.
echo ========================================================================
echo.
echo Do you want to:
echo   1. Run setup.bat (first time install)
echo   2. Run RUN_PAPER_CLEAN.bat (if already set up)
echo   3. Exit (set up manually later)
echo.
set /p choice=Enter 1, 2, or 3: 

if "%choice%"=="1" (
    echo.
    echo Running setup...
    call setup.bat
    echo.
    echo Setup complete! Now run RUN_PAPER_CLEAN.bat
    pause
) else if "%choice%"=="2" (
    echo.
    echo Starting bot...
    call RUN_PAPER_CLEAN.bat
) else (
    echo.
    echo OK - Set up manually when ready
    echo.
    echo Next steps:
    echo   1. Check .env file has correct settings
    echo   2. Run setup.bat if first time
    echo   3. Run RUN_PAPER_CLEAN.bat to start bot
    echo.
    pause
)
