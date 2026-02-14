@echo off
chcp 65001 > nul
title Upbit AutoProfit Bot v6.30.55 - Paper Trading (Clean Start)
color 0A

echo.
echo ========================================
echo  Upbit AutoProfit Bot v6.30.55
echo  Paper Trading Mode (Clean Start)
echo ========================================
echo.

REM Change to script directory
cd /d "%~dp0"

echo [1/7] Checking current directory...
echo [OK] %cd%
echo.

echo [2/7] Checking Python installation...
python --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo.
    echo Please install Python 3.8+ from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)
python --version
echo [OK] Python found
echo.

echo [3/7] Verifying project files...
if not exist "src\main.py" (
    echo [ERROR] src\main.py not found!
    echo.
    echo Please run COMPLETE_REINSTALL.bat to fix this issue
    echo.
    pause
    exit /b 1
)

findstr /C:"class TradingBot" src\main.py > nul
if errorlevel 1 (
    echo [ERROR] TradingBot class not found in main.py!
    echo.
    echo Your code may be corrupted or outdated.
    echo Please run COMPLETE_REINSTALL.bat to fix this issue
    echo.
    pause
    exit /b 1
)
echo [OK] TradingBot class verified
echo.

echo [4/7] Checking required packages...
python -c "import dotenv, pyupbit, pandas, requests, colorlog" > nul 2>&1
if errorlevel 1 (
    echo [WARN] Some packages are missing!
    echo.
    set /p INSTALL="Install missing packages now? (Y/N): "
    if /i "!INSTALL!"=="Y" (
        echo.
        echo Installing packages...
        python -m pip install python-dotenv pyupbit pandas requests colorlog ta numpy
        echo.
    ) else (
        echo.
        echo Please run setup.bat to install packages
        echo.
        pause
        exit /b 1
    )
)
echo [OK] All required packages available
echo.

echo [5/7] Cleaning Python cache (Critical!)
echo.
echo Deleting all .pyc files...
del /s /q *.pyc > nul 2>&1
echo [OK] .pyc files deleted
echo.

echo Deleting all __pycache__ folders...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
if exist "src\__pycache__" rd /s /q "src\__pycache__" 2>nul
if exist "src\ai\__pycache__" rd /s /q "src\ai\__pycache__" 2>nul
if exist "src\strategies\__pycache__" rd /s /q "src\strategies\__pycache__" 2>nul
if exist "src\utils\__pycache__" rd /s /q "src\utils\__pycache__" 2>nul
echo [OK] All cache directories deleted
echo.

echo [6/7] Checking configuration...
if not exist ".env" (
    echo [WARN] .env file not found
    echo.
    if exist ".env.test" (
        echo Copying from .env.test...
        copy .env.test .env > nul 2>&1
        echo [OK] .env file created
    ) else if exist ".env.example" (
        echo Copying from .env.example...
        copy .env.example .env > nul 2>&1
        echo [OK] .env file created
    ) else (
        echo Creating default .env file...
        (
            echo # Upbit AutoProfit Bot v6.30.55
            echo TRADING_MODE=paper
            echo INITIAL_CAPITAL=5000000
            echo MAX_DAILY_LOSS=500000
            echo MAX_CUMULATIVE_LOSS=1000000
            echo MAX_POSITIONS=5
            echo MAX_POSITION_RATIO=0.3
            echo ENABLE_ADVANCED_AI=true
            echo LOG_LEVEL=INFO
        ) > .env
        echo [OK] Default .env file created
    )
    echo.
)
echo [OK] Configuration file ready
echo.

echo [7/7] Starting bot...
echo.
echo ========================================
echo  Bot Starting...
echo ========================================
echo.
echo Mode: Paper Trading (Simulation)
echo Version: v6.30.55
echo Repository: https://github.com/lee-jungkil/Lj
echo.
echo Expected logs (every 3-5 seconds):
echo   [DEBUG-LOOP] Main loop #N starting...
echo   [DEBUG] Phase 3 check...
echo   [DEBUG-SLEEP] Waiting N seconds...
echo.
echo Position check logs (when holding):
echo   "Position liquidation check #N"
echo   "KRW-XXX Profit/Loss: +X.XX%"
echo   "Take-profit/Stop-loss trigger"
echo.
echo Stop bot: Press Ctrl+C
echo Logs folder: trading_logs\
echo.
echo ========================================
echo.

REM Run with -B (no .pyc) and -u (unbuffered output)
python -B -u -m src.main --mode paper

REM Check exit code
if errorlevel 1 (
    echo.
    echo ========================================
    echo [ERROR] Bot execution error!
    echo ========================================
    echo.
    echo Possible causes:
    echo   1. Code integrity issue - Run COMPLETE_REINSTALL.bat
    echo   2. Missing packages - Run setup.bat
    echo   3. Configuration error - Check .env file
    echo   4. Network error - Check internet connection
    echo.
    echo Troubleshooting:
    echo   1. Run COMPLETE_REINSTALL.bat (most reliable)
    echo   2. Check trading_logs\ for error details
    echo   3. Verify .env file settings
    echo.
) else (
    echo.
    echo ========================================
    echo [INFO] Bot stopped normally
    echo ========================================
    echo.
)

echo.
echo Press any key to exit...
pause > nul
exit /b 0
