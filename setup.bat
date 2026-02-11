@echo off
chcp 65001 > nul
title Upbit AutoProfit Bot v5.2 - Setup
color 0E

echo.
echo ========================================
echo  Upbit AutoProfit Bot v5.2
echo  Initial Setup
echo ========================================
echo.

REM Change to script directory
cd /d "%~dp0"

echo [1/5] Checking Python installation...
python --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo.
    echo Please follow these steps:
    echo   1. Visit https://www.python.org/
    echo   2. Download Python 3.8 or higher
    echo   3. Check "Add Python to PATH" during installation
    echo   4. Run this script again after installation
    echo.
    pause
    exit /b 1
)

python --version
echo [OK] Python installation confirmed
echo.

echo [2/5] Creating virtual environment...
if exist "venv\" (
    echo [OK] Virtual environment already exists
) else (
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)
echo.

echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment!
    pause
    exit /b 1
)
echo [OK] Virtual environment activated
echo.

echo [4/5] Upgrading pip and installing build tools...
python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo [WARN] Failed to upgrade pip, continuing...
)
echo [OK] Build tools ready
echo.

echo [5/5] Installing required packages...
echo This may take a few minutes...
pip install --no-cache-dir -r requirements.txt
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install some packages!
    echo.
    echo Trying alternative installation method...
    echo.
    pip install --no-cache-dir pyupbit pandas numpy requests python-dotenv schedule colorlog pytest typing-extensions
    if errorlevel 1 (
        echo [ERROR] Installation failed!
        echo.
        echo Please try manual installation:
        echo   1. Open command prompt as Administrator
        echo   2. Run: pip install --upgrade pip
        echo   3. Run: pip install pyupbit pandas numpy
        echo   4. Run this script again
        pause
        exit /b 1
    )
)
echo [OK] Packages installed successfully
echo.

echo [6/6] Creating config file...
if exist ".env" (
    echo [WARN] .env file already exists (skipping)
) else (
    if exist ".env.example" (
        copy .env.example .env > nul
        echo [OK] .env file created
    ) else (
        echo [WARN] .env.example not found, creating basic .env
        echo TRADING_MODE=paper > .env
        echo INITIAL_CAPITAL=100000 >> .env
        echo MAX_DAILY_LOSS=10000 >> .env
        echo MAX_CUMULATIVE_LOSS=20000 >> .env
        echo [OK] Basic .env file created
    )
    echo.
    echo Next steps:
    echo   1. Open .env file with text editor
    echo   2. Check TRADING_MODE (default: paper)
    echo   3. For live trading: Enter UPBIT_ACCESS_KEY and UPBIT_SECRET_KEY
    echo   4. Optional: Configure TELEGRAM and GMAIL settings
)
echo.

echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo You can now run:
echo.
echo   run_backtest.bat  - Backtest (historical data)
echo   run_paper.bat     - Paper trading (real-time + virtual)
echo   run_live.bat      - Live trading (real money)
echo.
echo Recommended order: Backtest -^> Paper -^> Live
echo.
echo If you encountered errors, check:
echo   - Python version (must be 3.8+)
echo   - Internet connection
echo   - Antivirus software (may block installation)
echo.
pause
