@echo off
chcp 65001 > nul
title Upbit AutoProfit Bot v5.2 - Paper Trading
color 0A

echo.
echo ========================================
echo  Upbit AutoProfit Bot v5.2
echo  Initial Capital: 100,000 KRW
echo  Max Daily Loss: 10%%
echo  Max Cumulative Loss: 20%%
echo ========================================
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

REM Check virtual environment
if not exist "venv\" (
    echo.
    echo [INFO] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo [INFO] Installing required packages...
pip install -q --upgrade pip
pip install -q -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install packages!
    pause
    exit /b 1
)
echo [OK] Packages installed

REM Check .env file
if not exist ".env" (
    echo.
    echo [ERROR] .env file not found!
    echo Please copy .env.example to .env
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Starting Paper Trading Mode
echo ========================================
echo.
echo TIP: Press Ctrl+C to stop
echo.

REM Run the bot
python -m src.main --mode paper

if errorlevel 1 (
    echo.
    echo [ERROR] Bot encountered an error!
    echo Check logs in: trading_logs/
    pause
    exit /b 1
)

pause
