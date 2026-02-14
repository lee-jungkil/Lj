@echo off
title Upbit AutoProfit Bot v6.30.25 - Setup
color 0E

echo.
echo ========================================
echo  Upbit AutoProfit Bot v6.30.25
echo  Initial Setup
echo ========================================
echo.

REM Change to script directory
cd /d "%~dp0"
echo [1/7] Current directory: %cd%
echo.

echo [2/7] Checking Python installation...
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
    echo Press any key to exit...
    pause > nul
    goto :END
)

python --version
echo [OK] Python installation confirmed
echo.

echo [3/7] Creating virtual environment...
if exist "venv\" (
    echo [OK] Virtual environment already exists
) else (
    python -m venv venv
    if errorlevel 1 (
        echo [WARN] Failed to create virtual environment!
        echo [INFO] This is not critical. Continuing with system Python...
    ) else (
        echo [OK] Virtual environment created
    )
)
echo.

echo [4/7] Activating virtual environment...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat 2>nul
    if errorlevel 1 (
        echo [WARN] Failed to activate virtual environment
        echo [INFO] Continuing with system Python...
    ) else (
        echo [OK] Virtual environment activated
    )
) else (
    echo [INFO] Virtual environment not found, using system Python
)
echo.

echo [5/7] Upgrading pip and installing build tools...
python -m pip install --upgrade pip setuptools wheel > nul 2>&1
if errorlevel 1 (
    echo [WARN] Failed to upgrade pip, continuing...
) else (
    echo [OK] Build tools ready
)
echo.

echo [6/7] Installing required packages...
echo This may take a few minutes...
echo.

if exist "requirements.txt" (
    echo Installing from requirements.txt...
    pip install --no-cache-dir -r requirements.txt
    if errorlevel 1 (
        echo.
        echo [WARN] Some packages failed to install
        echo [INFO] Trying essential packages only...
        echo.
        pip install pyupbit pandas numpy requests python-dotenv
        if errorlevel 1 (
            echo [ERROR] Installation failed!
            echo [INFO] You may need to install packages manually
        ) else (
            echo [OK] Essential packages installed
        )
    ) else (
        echo [OK] All packages installed successfully
    )
) else (
    echo [WARN] requirements.txt not found
    echo [INFO] Installing essential packages...
    pip install pyupbit pandas numpy requests python-dotenv
    if errorlevel 1 (
        echo [WARN] Some packages failed to install
    ) else (
        echo [OK] Essential packages installed
    )
)
echo.

echo [7/7] Creating config file...
if exist ".env" (
    echo [INFO] .env file already exists
) else (
    if exist ".env.example" (
        copy .env.example .env > nul 2>&1
        echo [OK] .env file created from .env.example
    ) else if exist ".env.test" (
        copy .env.test .env > nul 2>&1
        echo [OK] .env file created from .env.test
    ) else (
        echo [INFO] Creating basic .env file...
        (
            echo # Upbit AutoProfit Bot v6.30.25
            echo.
            echo TRADING_MODE=paper
            echo INITIAL_CAPITAL=100000
            echo MAX_DAILY_LOSS=10000
            echo MAX_CUMULATIVE_LOSS=20000
            echo MAX_POSITIONS=5
            echo MAX_POSITION_RATIO=0.2
            echo.
            echo # AI System
            echo ENABLE_ADVANCED_AI=true
            echo ENABLE_ORDERBOOK_ANALYSIS=true
            echo ENABLE_SCENARIO_DETECTION=true
            echo ENABLE_SMART_SPLIT=true
            echo ENABLE_HOLDING_TIME_AI=true
            echo ENABLE_DYNAMIC_EXIT=true
            echo EXIT_MODE=aggressive
            echo.
            echo # Logging
            echo LOG_LEVEL=INFO
            echo ENABLE_TRADING_LOG=true
            echo ENABLE_ERROR_LOG=true
            echo.
            echo # Sentiment Analysis
            echo ENABLE_SENTIMENT=false
            echo.
            echo # Upbit API Keys
            echo UPBIT_ACCESS_KEY=
            echo UPBIT_SECRET_KEY=
            echo.
            echo # Notifications
            echo TELEGRAM_BOT_TOKEN=
            echo TELEGRAM_CHAT_ID=
            echo GMAIL_SENDER=
            echo GMAIL_PASSWORD=
            echo GMAIL_RECEIVER=
            echo NEWS_API_KEY=
        ) > .env
        echo [OK] Basic .env file created
    )
)
echo.

echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo You can now run:
echo   RUN_PAPER_CLEAN.bat  - Paper trading
echo   RUN_LIVE_CLEAN.bat   - Live trading
echo.
echo Next steps:
echo   1. Review .env file settings
echo   2. For live trading: Add Upbit API keys to .env
echo   3. Run RUN_PAPER_CLEAN.bat to start
echo.

REM CRITICAL: Always pause at the end
echo.
echo Press any key to exit...
pause > nul

:END

