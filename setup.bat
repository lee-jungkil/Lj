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
    pause
    exit /b 1
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
        echo [ERROR] Failed to create virtual environment!
        echo.
        echo This is not critical. You can still use system Python.
        echo Continue with system Python? (Y/N)
        set /p continue="Enter Y to continue: "
        if /i not "%continue%"=="Y" (
            pause
            exit /b 1
        )
    ) else (
        echo [OK] Virtual environment created
    )
)
echo.

echo [4/7] Activating virtual environment...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
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
python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo [WARN] Failed to upgrade pip, continuing...
)
echo [OK] Build tools ready
echo.

echo [6/7] Installing required packages...
echo This may take a few minutes...
if exist "requirements.txt" (
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
) else (
    echo [WARN] requirements.txt not found
    echo [INFO] Installing essential packages...
    pip install pyupbit pandas numpy requests python-dotenv schedule colorlog pytest typing-extensions
    if errorlevel 1 (
        echo [ERROR] Installation failed!
        pause
        exit /b 1
    )
    echo [OK] Essential packages installed
)
echo.

echo [7/7] Creating config file...
if exist ".env" (
    echo [INFO] .env file already exists (keeping existing file)
) else (
    if exist ".env.example" (
        copy .env.example .env > nul
        echo [OK] .env file created from .env.example
    ) else if exist ".env.test" (
        copy .env.test .env > nul
        echo [OK] .env file created from .env.test
    ) else (
        echo [WARN] .env.example and .env.test not found, creating basic .env
        (
            echo # Upbit AutoProfit Bot v6.30.24
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
            echo # Upbit API Keys (for live trading)
            echo UPBIT_ACCESS_KEY=
            echo UPBIT_SECRET_KEY=
            echo.
            echo # Notifications (optional)
            echo TELEGRAM_BOT_TOKEN=
            echo TELEGRAM_CHAT_ID=
            echo GMAIL_SENDER=
            echo GMAIL_PASSWORD=
            echo GMAIL_RECEIVER=
            echo NEWS_API_KEY=
        ) > .env
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
echo   RUN_PAPER_CLEAN.bat  - Paper trading (recommended)
echo   RUN_LIVE_CLEAN.bat   - Live trading (real money)
echo.
echo Important Notes:
echo   - Always use RUN_*_CLEAN.bat files (not old run_*.bat)
echo   - Paper trading mode is safe and recommended for testing
echo   - For live trading, configure Upbit API keys in .env file
echo.
echo Documentation:
echo   - VERSION.txt - Current version info
echo   - BATCH_FILE_FIX_USER_GUIDE_v6.30.23.md - User guide
echo.
echo If you encountered errors, check:
echo   - Python version (must be 3.8+)
echo   - Internet connection
echo   - Antivirus software (may block installation)
echo.

REM Always pause so window stays open
pause
