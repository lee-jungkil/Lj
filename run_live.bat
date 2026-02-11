@echo off
chcp 65001 > nul
title Upbit AutoProfit Bot v5.2 - Live Trading
color 0C

echo.
echo ========================================
echo  WARNING: LIVE TRADING MODE
echo ========================================
echo.
echo This mode trades with REAL MONEY!
echo.
echo Please confirm:
echo   1. Upbit API keys are configured in .env
echo   2. Tested thoroughly with backtest and paper trading
echo   3. Risk management settings are verified
echo.
echo Press any key to continue...
pause > nul

echo.
echo [INFO] Preparing environment...

REM Change to script directory
cd /d "%~dp0"

REM Check Python installation
python --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo Please install Python 3.8 or higher: https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python installation confirmed

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Check .env file
if not exist ".env" (
    echo.
    echo [ERROR] .env file not found!
    echo Please create .env and configure UPBIT API keys
    pause
    exit /b 1
)

REM Check API key configuration (simple check)
findstr /C:"UPBIT_ACCESS_KEY=" .env | findstr /V /C:"UPBIT_ACCESS_KEY=$" | findstr /V /C:"UPBIT_ACCESS_KEY= " > nul
if errorlevel 1 (
    echo.
    echo [ERROR] Upbit API keys are not configured!
    echo Please set UPBIT_ACCESS_KEY and UPBIT_SECRET_KEY in .env
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Starting Live Trading Mode
echo ========================================
echo.
echo TIPS:
echo   - Press Ctrl+C to stop safely
echo   - All trades are logged in trading_logs/
echo   - AI learning data is saved in learning_data/
echo.

REM Run the bot
python src/main.py --mode live

if errorlevel 1 (
    echo.
    echo [ERROR] Bot encountered an error!
    echo Check logs in: trading_logs/
    pause
    exit /b 1
)

pause
