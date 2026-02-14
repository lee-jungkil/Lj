@echo off
chcp 65001 > nul
title Upbit AutoProfit Bot v6.30.55 - Setup
color 0E

echo.
echo ========================================
echo  Upbit AutoProfit Bot v6.30.55
echo  Initial Setup
echo ========================================
echo.

REM Change to script directory
cd /d "%~dp0"
echo [1/9] Current directory: %cd%
echo.

echo [2/9] Checking Python installation...
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

echo [3/9] Cleaning Python cache...
echo Deleting .pyc files...
del /s /q *.pyc > nul 2>&1
echo Deleting __pycache__ folders...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
echo [OK] Cache cleaned
echo.

echo [4/9] Checking Git installation...
git --version > nul 2>&1
if errorlevel 1 (
    echo [WARN] Git not installed
    echo [INFO] Git is recommended but not required
    echo.
    echo To install Git: https://git-scm.com/
    echo.
) else (
    git --version
    echo [OK] Git installation confirmed
)
echo.

echo [5/9] Verifying project structure...
if not exist "src" (
    echo [ERROR] src directory not found!
    echo.
    echo Please make sure you are in the correct directory.
    echo Current: %cd%
    echo.
    pause
    exit /b 1
)

if not exist "src\main.py" (
    echo [ERROR] src\main.py not found!
    echo.
    echo This may indicate an incomplete installation.
    echo Please download the complete project from:
    echo https://github.com/lee-jungkil/Lj
    echo.
    pause
    exit /b 1
)

echo [OK] Project structure verified
echo.

echo [6/9] Upgrading pip and build tools...
python -m pip install --upgrade pip setuptools wheel > nul 2>&1
if errorlevel 1 (
    echo [WARN] Failed to upgrade pip
    echo [INFO] Continuing with current version...
) else (
    echo [OK] Build tools ready
)
echo.

echo [7/9] Installing required packages...
echo This may take a few minutes, please wait...
echo.

REM Check if requirements.txt exists
if exist "requirements.txt" (
    echo Installing from requirements.txt...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo [WARN] Some packages failed to install from requirements.txt
        echo [INFO] Trying essential packages individually...
        echo.
        goto :INSTALL_ESSENTIALS
    ) else (
        echo [OK] All packages installed successfully
        goto :CONFIG_SETUP
    )
) else (
    echo [INFO] requirements.txt not found
    echo [INFO] Installing essential packages...
    goto :INSTALL_ESSENTIALS
)

:INSTALL_ESSENTIALS
echo.
echo Installing essential packages one by one...
echo.

echo Installing pyupbit...
python -m pip install pyupbit
if errorlevel 1 echo [WARN] pyupbit installation failed

echo Installing pandas...
python -m pip install pandas
if errorlevel 1 echo [WARN] pandas installation failed

echo Installing numpy...
python -m pip install numpy
if errorlevel 1 echo [WARN] numpy installation failed

echo Installing requests...
python -m pip install requests
if errorlevel 1 echo [WARN] requests installation failed

echo Installing python-dotenv...
python -m pip install python-dotenv
if errorlevel 1 echo [WARN] python-dotenv installation failed

echo Installing colorlog...
python -m pip install colorlog
if errorlevel 1 echo [WARN] colorlog installation failed

echo Installing ta...
python -m pip install ta
if errorlevel 1 echo [WARN] ta installation failed

echo.
echo [OK] Essential packages installation completed
echo.

:CONFIG_SETUP
echo [8/9] Setting up configuration file...
if exist ".env" (
    echo [INFO] .env file already exists
    echo [INFO] Keeping existing configuration
) else (
    if exist ".env.example" (
        copy .env.example .env > nul 2>&1
        echo [OK] .env file created from .env.example
    ) else if exist ".env.test" (
        copy .env.test .env > nul 2>&1
        echo [OK] .env file created from .env.test
    ) else (
        echo [INFO] Creating default .env file...
        (
            echo # Upbit AutoProfit Bot v6.30.38
            echo.
            echo # Trading Mode
            echo TRADING_MODE=paper
            echo.
            echo # Risk Management
            echo INITIAL_CAPITAL=5000000
            echo MAX_DAILY_LOSS=500000
            echo MAX_CUMULATIVE_LOSS=1000000
            echo MAX_POSITIONS=5
            echo MAX_POSITION_RATIO=0.3
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
            echo # Coin Selection
            echo COIN_SELECTION_METHOD=ai_composite
            echo TOP_COINS_COUNT=35
            echo.
            echo # Logging
            echo LOG_LEVEL=INFO
            echo ENABLE_TRADING_LOG=true
            echo ENABLE_ERROR_LOG=true
            echo.
            echo # Advanced Features
            echo ENABLE_SENTIMENT=false
            echo.
            echo # Upbit API Keys ^(Required for live trading^)
            echo UPBIT_ACCESS_KEY=
            echo UPBIT_SECRET_KEY=
            echo.
            echo # Notifications ^(Optional^)
            echo TELEGRAM_BOT_TOKEN=
            echo TELEGRAM_CHAT_ID=
            echo GMAIL_SENDER=
            echo GMAIL_PASSWORD=
            echo GMAIL_RECEIVER=
            echo NEWS_API_KEY=
        ) > .env
        echo [OK] Default .env file created
    )
)
echo.

echo [9/9] Verifying installation...
echo.
echo Checking TradingBot class...
findstr /C:"class TradingBot" src\main.py > nul
if errorlevel 1 (
    echo [ERROR] TradingBot class not found!
    echo [INFO] main.py may be corrupted or outdated
    echo.
    echo Please run COMPLETE_REINSTALL.bat to fix this issue
    echo.
    pause
    exit /b 1
) else (
    echo [OK] TradingBot class found
)

echo Checking DEBUG code...
findstr /C:"DEBUG-LOOP" src\main.py > nul
if errorlevel 1 (
    echo [WARN] DEBUG code not found (you may have an older version)
    echo [INFO] Consider running COMPLETE_REINSTALL.bat for the latest version
) else (
    echo [OK] DEBUG code found (v6.30.37+)
)
echo.

echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo Installation Summary:
echo   - Python: Ready
echo   - Dependencies: Installed
echo   - Configuration: .env file ready
echo   - Code verification: Passed
echo.
echo You can now run:
echo   RUN_PAPER_CLEAN.bat  - Paper trading (recommended for testing)
echo   RUN_LIVE_CLEAN.bat   - Live trading (requires API keys)
echo.
echo Next steps:
echo   1. Review .env file settings (especially INITIAL_CAPITAL)
echo   2. For live trading: Add Upbit API keys to .env
echo   3. Run RUN_PAPER_CLEAN.bat to start testing
echo.
echo Troubleshooting:
echo   - If bot doesn't start: Run COMPLETE_REINSTALL.bat
echo   - If no DEBUG logs appear: Run COMPLETE_REINSTALL.bat
echo   - For help: Check GitHub issues or documentation
echo.
echo Repository: https://github.com/lee-jungkil/Lj
echo Current version: v6.30.38
echo.

echo.
echo Press any key to exit...
pause > nul
exit /b 0
