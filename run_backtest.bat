@echo off
chcp 65001 > nul
title Upbit AutoProfit Bot v5.2 - Backtest Mode
color 0B

echo.
echo ========================================
echo  Upbit AutoProfit Bot v5.2
echo  Backtest Mode (Historical Data)
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

REM Activate virtual environment (if exists)
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

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
echo  Starting Backtest Mode
echo ========================================
echo.

REM Run the bot
python -m src.main --mode backtest

if errorlevel 1 (
    echo.
    echo [ERROR] Backtest encountered an error!
    echo Check logs in: trading_logs/
    pause
    exit /b 1
)

pause
