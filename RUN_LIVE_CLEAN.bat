@echo off
title Upbit AutoProfit Bot v6.30.30 - Live Trading (Clean Start)
color 0C

echo.
echo ======================================================================
echo.
echo                    WARNING: LIVE TRADING MODE
echo.
echo  Real money will be used and losses can occur!
echo.
echo ======================================================================
echo.
set /p confirm="Do you really want to proceed with live trading? (yes to confirm): "
if not "%confirm%"=="yes" (
    echo.
    echo Cancelled by user.
    echo.
    echo Press any key to exit...
    pause > nul
    goto :END
)

echo.
echo ========================================
echo  Upbit AutoProfit Bot v6.30.30
echo  Live Trading Mode
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
    echo Visit: https://www.python.org/
    echo.
    echo Press any key to exit...
    pause > nul
    goto :END
)
python --version
echo.

echo [3/7] Checking required packages...
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

echo [4/7] Cleaning Python cache (Important!)
echo Removing old .pyc files...
if exist "src\__pycache__" rmdir /s /q src\__pycache__ 2>nul
if exist "src\strategies\__pycache__" rmdir /s /q src\strategies\__pycache__ 2>nul
if exist "src\utils\__pycache__" rmdir /s /q src\utils\__pycache__ 2>nul
if exist "src\ai\__pycache__" rmdir /s /q src\ai\__pycache__ 2>nul
del /s /q *.pyc 2>nul
echo [OK] Cache cleaned!
echo.

echo [5/7] Checking .env file...
if not exist ".env" (
    echo [ERROR] .env file not found!
    echo Please create .env file with your Upbit API keys
    echo.
    echo Press any key to exit...
    pause > nul
    goto :END
)
echo [OK] .env file exists
echo.

echo [6/7] Checking Upbit API keys...
findstr /C:"UPBIT_ACCESS_KEY=" .env | findstr /V /C:"UPBIT_ACCESS_KEY=$" | findstr /V /C:"UPBIT_ACCESS_KEY= " > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Upbit API keys are not configured!
    echo.
    echo Please set UPBIT_ACCESS_KEY and UPBIT_SECRET_KEY in .env file
    echo.
    echo Press any key to exit...
    pause > nul
    goto :END
)
echo [OK] API keys configured
echo.

echo [7/7] Starting bot...
echo.
echo ========================================
echo  Live Trading Mode
echo ========================================
echo.
echo Stop: Ctrl+C
echo Logs folder: trading_logs\
echo Version: v6.30.30
echo.
echo System Status:
echo   - Profit/Loss sell system: ENABLED
echo   - Position check: every 3 seconds
echo   - Auto liquidation: ACTIVE
echo.

REM Run bot with cache disabled
python -B -m src.main --mode live

REM Check exit code
if errorlevel 1 (
    echo.
    echo ========================================
    echo [ERROR] Bot execution error!
    echo ========================================
    echo.
    echo Possible causes:
    echo   1. Missing packages - Run setup.bat
    echo   2. Invalid API keys - Check .env file
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
