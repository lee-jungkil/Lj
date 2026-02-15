@echo off
title Upbit AutoProfit Bot v6.30.62 - Paper Trading Mode
color 0A

echo.
echo ========================================
echo  Upbit AutoProfit Bot v6.30.62
echo  PAPER TRADING MODE (Safe Testing)
echo ========================================
echo.

REM Change to script directory
cd /d "%~dp0"
echo Current directory: %cd%
echo.

echo ========================================
echo  Checking Requirements
echo ========================================
echo.

echo Checking Python installation...
python --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo.
    echo Please install Python 3.8+ from https://www.python.org/
    echo Make sure to check "Add Python to PATH"
    echo.
    pause
    exit /b 1
)
python --version
echo [OK] Python found
echo.

echo Checking project files...
if not exist "src\main.py" (
    echo [ERROR] src\main.py not found!
    echo.
    echo Please run COMPLETE_REINSTALL.bat first
    echo.
    pause
    exit /b 1
)

findstr /C:"class AutoProfitBot" src\main.py > nul
if errorlevel 1 (
    echo [ERROR] AutoProfitBot class not found!
    echo.
    echo Please run COMPLETE_REINSTALL.bat to fix
    echo.
    pause
    exit /b 1
)
echo [OK] Project files found
echo.

echo Checking Python packages...
python -c "import pyupbit, pandas, requests, dotenv" > nul 2>&1
if errorlevel 1 (
    echo [WARN] Some packages missing
    echo Installing required packages...
    python -m pip install pyupbit pandas numpy requests python-dotenv colorlog ta
    if errorlevel 1 (
        echo [ERROR] Package installation failed!
        pause
        exit /b 1
    )
) else (
    echo [OK] All packages found
)
echo.

echo ========================================
echo  Cleaning Python Cache
echo ========================================
echo.

echo Deleting .pyc files...
del /s /q *.pyc > nul 2>&1
echo [OK] Cache cleaned

echo Deleting __pycache__ folders...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
echo [OK] Cache folders cleaned
echo.

echo ========================================
echo  Checking Configuration
echo ========================================
echo.

if not exist ".env" (
    echo [WARN] .env file not found
    echo Creating default .env file...
    (
        echo # Upbit AutoProfit Bot v6.30.62
        echo TRADING_MODE=paper
        echo INITIAL_CAPITAL=5000000
        echo MAX_DAILY_LOSS=500000
        echo MAX_CUMULATIVE_LOSS=1000000
        echo MAX_POSITIONS=5
        echo ENABLE_ADVANCED_AI=true
        echo LOG_LEVEL=INFO
    ) > .env
    echo [OK] Default .env created
) else (
    echo [OK] .env file found
)
echo.

echo ========================================
echo  STARTING BOT IN PAPER MODE
echo ========================================
echo.
echo Mode: PAPER TRADING (Safe - No Real Money)
echo Version: v6.30.62 (Enhanced Sell Debugging)
echo Repository: https://github.com/lee-jungkil/Lj
echo.
echo Starting with flags:
echo   -B : Disable bytecode (.pyc) generation
echo   -u : Unbuffered output (real-time logs)
echo.
echo Expected logs:
echo   [DEBUG-LOOP] Main loop messages
echo   [EXECUTE-SELL] Sell execution logs
echo   Position updates every 3-5 seconds
echo.
echo To stop: Press Ctrl+C
echo.
timeout /t 3 /nobreak > nul

python -B -u -m src.main --mode paper

echo.
echo ========================================
echo  BOT STOPPED
echo ========================================
echo.
if errorlevel 1 (
    echo [ERROR] Bot exited with error
    echo.
    echo Troubleshooting:
    echo   1. Run COMPLETE_REINSTALL.bat
    echo   2. Check .env file settings
    echo   3. Verify Python packages installed
    echo   4. Check internet connection
    echo.
) else (
    echo [INFO] Bot stopped normally
)
echo.
pause
