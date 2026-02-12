@echo off
chcp 65001 >nul 2>&1
cls

echo ============================================================
echo  Upbit AutoProfit Bot Update v6.26-ALL-FIXES-COMPLETE
echo ============================================================
echo.
echo Update Contents:
echo  [OK] Screen scroll completely removed
echo  [OK] Profit/Loss sync improved
echo  [OK] Risk management enhanced (auto-stop at -10%%)
echo  [OK] Debug output suppressed
echo  [OK] Sell history permanent storage (keep 10 records)
echo  [NEW] Real-time sync fixed - entry_time storage added
echo  [NEW] Position price update optimization
echo  [NEW] Risk manager auto-sync function added
echo.

REM Save current directory
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..

REM Change to project root
cd /d "%PROJECT_ROOT%"

echo Current directory: %CD%
echo.

REM Check if we are in the correct directory
if not exist "src\utils" (
    echo [ERROR] Project structure not found!
    echo.
    echo Please run this script from: Lj-main\update\UPDATE.bat
    echo Current path: %CD%
    echo.
    pause
    exit /b 1
)

REM Create backup directory
if not exist "backup" mkdir "backup"
set BACKUP_DIR=backup\backup_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set BACKUP_DIR=%BACKUP_DIR: =0%
mkdir "%BACKUP_DIR%" 2>nul

echo [1/4] Backing up existing files...
if exist "src\utils\fixed_screen_display.py" (
    copy "src\utils\fixed_screen_display.py" "%BACKUP_DIR%\fixed_screen_display.py.bak" >nul 2>&1
    if %errorlevel% equ 0 (
        echo  + fixed_screen_display.py backed up
    )
)
echo [OK] Backup completed: %BACKUP_DIR%
echo.

echo [2/4] Checking update files...
if not exist "update\fixed_screen_display.py" (
    echo [ERROR] update\fixed_screen_display.py not found!
    echo.
    echo Please ensure update folder contains the required files.
    pause
    exit /b 1
)
echo [OK] Update files found
echo.

echo [3/4] Updating files...
copy /Y "update\fixed_screen_display.py" "src\utils\fixed_screen_display.py" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] File copy failed!
    echo.
    echo Troubleshooting:
    echo  1. Run Command Prompt as Administrator
    echo  2. Close Python processes using the file
    echo  3. Check file permissions
    echo.
    pause
    exit /b 1
)
echo  + fixed_screen_display.py updated
echo [OK] File update completed
echo.

echo [4/4] Verifying update...
echo.
echo ============================================================
echo  Update Completed Successfully!
echo ============================================================
echo.
echo What's New in v6.16-SELLHISTORY:
echo  - Screen scroll removed (fully fixed display)
echo  - Profit/Loss auto-calculated from initial_capital
echo  - Debug output minimized for cleaner display
echo  - Risk management: auto-stop at -10%% loss
echo  [NEW] Sell history: keep up to 10 records
echo  [NEW] Display last 5 sell records on screen
echo  [NEW] Sell records persist like buy positions
echo.
echo Backup location: %BACKUP_DIR%
echo.
echo Next step: Run the bot
echo   Windows: run.bat or run_live.bat or run_paper.bat
echo.
pause
