@echo off
title Upbit AutoProfit Bot v6.30.25 - Paper Trading (Clean Start)
color 0A

echo.
echo ========================================
echo  Upbit AutoProfit Bot v6.30.25
echo  BATCH-FILE-ENCODING-FIX
echo ========================================
echo.
echo [1/5] Checking current directory...
cd /d "%~dp0"
echo [OK] %cd%
echo.

echo [2/5] Checking Python installation...
python --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo https://www.python.org/
    pause
    exit /b 1
)
python --version
echo.

echo [3/5] Cleaning Python cache (Important!)
echo Removing old .pyc files...
if exist "src\__pycache__" rmdir /s /q src\__pycache__
if exist "src\strategies\__pycache__" rmdir /s /q src\strategies\__pycache__
if exist "src\utils\__pycache__" rmdir /s /q src\utils\__pycache__
if exist "src\ai\__pycache__" rmdir /s /q src\ai\__pycache__
del /s /q *.pyc 2>nul
echo [OK] Cache cleaned!
echo.

echo [4/5] Checking .env file...
if not exist ".env" (
    echo [WARNING] .env file not found. Copying from .env.test...
    copy .env.test .env
    echo [OK] .env file created!
)
echo.

echo [5/5] Starting bot...
echo.
echo ========================================
echo  Paper Trading Mode
echo ========================================
echo.
echo Stop: Ctrl+C
echo Logs folder: trading_logs\
echo Version: v6.30.25
echo.
echo Check for these logs:
echo     "Position liquidation check"
echo     "Profit/Loss ratio"
echo     "Sell trigger"
echo.

REM Run bot with cache disabled
python -B -m src.main --mode paper

REM Always pause to keep window open
if errorlevel 1 (
    echo.
    echo [ERROR] Bot execution error!
    echo Check logs in trading_logs\ folder
) else (
    echo.
    echo [INFO] Bot stopped normally.
)

echo.
pause
