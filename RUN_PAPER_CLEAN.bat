@echo off
title Upbit AutoProfit Bot v6.30.28 - Paper Trading (Clean Start)
color 0A

echo.
echo ========================================
echo  Upbit AutoProfit Bot v6.30.28
echo  Paper Trading Mode
echo ========================================
echo.

REM Change to script directory
cd /d "%~dp0"

echo [1/6] Checking current directory...
echo [OK] %cd%
echo.

echo [2/6] Checking Python installation...
python --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo Visit: https://www.python.org/
    echo.
    echo Press any key to exit...
    pause > nul
    goto :END
)
python --version
echo.

echo [3/6] Checking required packages...
python -c "import dotenv, pyupbit, pandas, requests" > nul 2>&1
if errorlevel 1 (
    echo [WARNING] Some packages are missing!
    echo.
    echo Running setup.bat to install packages...
    echo This may take a few minutes...
    echo.
    call setup.bat
    echo.
    echo Setup completed. Continuing...
    echo.
)
echo [OK] All packages available
echo.

echo [4/6] Cleaning Python cache (Important!)
echo Removing old .pyc files...
if exist "src\__pycache__" rmdir /s /q src\__pycache__ 2>nul
if exist "src\strategies\__pycache__" rmdir /s /q src\strategies\__pycache__ 2>nul
if exist "src\utils\__pycache__" rmdir /s /q src\utils\__pycache__ 2>nul
if exist "src\ai\__pycache__" rmdir /s /q src\ai\__pycache__ 2>nul
del /s /q *.pyc 2>nul
echo [OK] Cache cleaned!
echo.

echo [5/6] Checking .env file...
if not exist ".env" (
    echo [WARNING] .env file not found
    if exist ".env.test" (
        echo Copying from .env.test...
        copy .env.test .env > nul 2>&1
        echo [OK] .env file created!
    ) else if exist ".env.example" (
        echo Copying from .env.example...
        copy .env.example .env > nul 2>&1
        echo [OK] .env file created!
    ) else (
        echo [ERROR] No .env template found!
        echo Please create .env file manually
        echo.
        echo Press any key to exit...
        pause > nul
        goto :END
    )
)
echo [OK] .env file exists
echo.

echo [6/6] Starting bot...
echo.
echo ========================================
echo  Paper Trading Mode
echo ========================================
echo.
echo Stop: Ctrl+C
echo Logs folder: trading_logs\
echo Version: v6.30.28
echo.
echo Check for these logs:
echo   - "Position liquidation check"
echo   - "Profit/Loss ratio"
echo   - "Sell trigger"
echo.

REM Run bot with cache disabled
python -B -m src.main --mode paper

REM Check exit code
if errorlevel 1 (
    echo.
    echo ========================================
    echo [ERROR] Bot execution error!
    echo ========================================
    echo.
    echo Possible causes:
    echo   1. Missing packages - Run setup.bat
    echo   2. Configuration error - Check .env file
    echo   3. Network error - Check internet connection
    echo.
    echo Check logs in trading_logs\ folder for details
) else (
    echo.
    echo ========================================
    echo [INFO] Bot stopped normally
    echo ========================================
)

echo.
echo Press any key to exit...
pause > nul

:END
