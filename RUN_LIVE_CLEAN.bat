@echo off
title Upbit AutoProfit Bot v6.30.25 - Live Trading (Clean Start)
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
    echo Cancelled.
    echo.
    echo Press any key to exit...
    pause > nul
    goto :END
)

echo.
echo ========================================
echo  Upbit AutoProfit Bot v6.30.25
echo  BATCH-FILE-ENCODING-FIX
echo ========================================
echo.
echo [1/6] Checking current directory...
cd /d "%~dp0"
echo [OK] %cd%
echo.

echo [2/6] Checking Python installation...
python --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo.
    echo Press any key to exit...
    pause > nul
    goto :END
)
python --version
echo.

echo [3/6] Cleaning Python cache (Important!)
if exist "src\__pycache__" rmdir /s /q src\__pycache__
if exist "src\strategies\__pycache__" rmdir /s /q src\strategies\__pycache__
if exist "src\utils\__pycache__" rmdir /s /q src\utils\__pycache__
if exist "src\ai\__pycache__" rmdir /s /q src\ai\__pycache__
del /s /q *.pyc 2>nul
echo [OK] Cache cleaned!
echo.

echo [4/6] Checking .env file...
if not exist ".env" (
    echo [ERROR] .env file not found!
    echo Please copy .env.example and configure your API keys
    echo.
    echo Press any key to exit...
    pause > nul
    goto :END
)
echo [OK] .env file exists
echo.

echo [5/6] Checking Upbit API keys...
findstr /C:"UPBIT_ACCESS_KEY=" .env | findstr /V /C:"UPBIT_ACCESS_KEY=$" | findstr /V /C:"UPBIT_ACCESS_KEY= " > nul
if errorlevel 1 (
    echo [ERROR] Upbit API keys are not configured!
    echo Please set UPBIT_ACCESS_KEY and UPBIT_SECRET_KEY in .env file
    echo.
    echo Press any key to exit...
    pause > nul
    goto :END
)
echo [OK] API keys configured
echo.

echo [6/6] Starting bot...
echo.
echo ========================================
echo  Live Trading Mode
echo ========================================
echo.
echo Stop: Ctrl+C
echo Logs folder: trading_logs\
echo Version: v6.30.25
echo.
echo Profit/Loss sell system enabled
echo Position check: every 3 seconds
echo.

REM Run bot with cache disabled
python -B -m src.main --mode live

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

:END
