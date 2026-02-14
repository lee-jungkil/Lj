@echo off
chcp 65001 > nul
title Upbit AutoProfit Bot v6.30.38 - COMPLETE REINSTALL
color 0E

echo.
echo ========================================
echo  Upbit AutoProfit Bot v6.30.38
echo  COMPLETE REINSTALL
echo ========================================
echo.
echo This script will:
echo   1. Backup your .env file
echo   2. Delete all Python cache files
echo   3. Download fresh code from GitHub
echo   4. Install all dependencies
echo   5. Restore your .env file
echo   6. Start the bot
echo.
echo WARNING: This will delete ALL local changes!
echo.
set /p CONFIRM="Continue? (Y/N): "
if /i not "%CONFIRM%"=="Y" (
    echo.
    echo Cancelled by user.
    echo.
    pause
    exit /b 0
)

echo.
echo ========================================
echo  STEP 1/8: Backup Configuration
echo ========================================
echo.

REM Change to script directory
cd /d "%~dp0"
echo Current directory: %cd%
echo.

REM Backup .env file
if exist ".env" (
    echo Backing up .env file...
    copy /Y .env .env.backup > nul
    if errorlevel 1 (
        echo [ERROR] Failed to backup .env file!
        pause
        exit /b 1
    )
    echo [OK] .env backed up to .env.backup
) else (
    echo [WARN] No .env file found to backup
)
echo.

echo ========================================
echo  STEP 2/8: Stop Running Processes
echo ========================================
echo.

echo Stopping all Python processes...
taskkill /F /IM python.exe /T > nul 2>&1
if errorlevel 1 (
    echo [INFO] No Python processes running
) else (
    echo [OK] Python processes stopped
    timeout /t 2 /nobreak > nul
)
echo.

echo ========================================
echo  STEP 3/8: Delete Python Cache
echo ========================================
echo.

echo Deleting all .pyc files...
del /s /q *.pyc > nul 2>&1
echo [OK] .pyc files deleted
echo.

echo Deleting all __pycache__ folders...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
echo [OK] __pycache__ folders deleted
echo.

echo Deleting specific cache directories...
if exist "src\__pycache__" rd /s /q "src\__pycache__" 2>nul
if exist "src\ai\__pycache__" rd /s /q "src\ai\__pycache__" 2>nul
if exist "src\strategies\__pycache__" rd /s /q "src\strategies\__pycache__" 2>nul
if exist "src\utils\__pycache__" rd /s /q "src\utils\__pycache__" 2>nul
echo [OK] Specific cache directories deleted
echo.

echo ========================================
echo  STEP 4/8: Check Python Installation
echo ========================================
echo.

python --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo.
    echo Please install Python 3.8+ from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

python --version
echo [OK] Python installation confirmed
echo.

echo ========================================
echo  STEP 5/8: Download Fresh Code
echo ========================================
echo.

echo Checking Git installation...
git --version > nul 2>&1
if errorlevel 1 (
    echo [WARN] Git not found. Using alternative download method...
    echo.
    
    echo Downloading main.py using PowerShell...
    powershell -Command "try { Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py' -OutFile 'src\main.py' -UseBasicParsing; Write-Host '[OK] main.py downloaded'; exit 0 } catch { Write-Host '[ERROR] Download failed'; exit 1 }"
    
    if errorlevel 1 (
        echo.
        echo [ERROR] Failed to download code!
        echo.
        echo Please try one of these methods:
        echo   1. Install Git and run this script again
        echo   2. Download manually from: https://github.com/lee-jungkil/Lj
        echo   3. Use curl: curl -o src\main.py https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py
        echo.
        pause
        exit /b 1
    )
) else (
    echo [OK] Git found: 
    git --version
    echo.
    
    echo Initializing Git repository...
    if not exist ".git" (
        git init
    )
    echo.
    
    echo Adding remote repository...
    git remote remove origin > nul 2>&1
    git remote add origin https://github.com/lee-jungkil/Lj.git
    echo.
    
    echo Fetching latest code...
    git fetch origin main
    if errorlevel 1 (
        echo [ERROR] Failed to fetch code from GitHub!
        echo.
        echo Please check your internet connection and try again.
        echo.
        pause
        exit /b 1
    )
    echo.
    
    echo Resetting to latest version...
    git reset --hard origin/main
    if errorlevel 1 (
        echo [WARN] Reset failed, trying clean checkout...
        git checkout -f main
    )
    echo [OK] Code updated to latest version
)
echo.

echo ========================================
echo  STEP 6/8: Verify Code Integrity
echo ========================================
echo.

echo Checking main.py...
if not exist "src\main.py" (
    echo [ERROR] src\main.py not found!
    pause
    exit /b 1
)

findstr /C:"class TradingBot" src\main.py > nul
if errorlevel 1 (
    echo [ERROR] TradingBot class not found in main.py!
    echo The downloaded file may be corrupted.
    pause
    exit /b 1
)
echo [OK] TradingBot class found
echo.

findstr /C:"DEBUG-LOOP" src\main.py > nul
if errorlevel 1 (
    echo [WARN] DEBUG-LOOP not found (old version?)
) else (
    echo [OK] DEBUG-LOOP code found (v6.30.37+)
)
echo.

echo Checking file size...
for %%A in ("src\main.py") do (
    set size=%%~zA
    echo File size: %%~zA bytes
    if %%~zA LSS 50000 (
        echo [WARN] File seems too small, may be incomplete
    ) else (
        echo [OK] File size looks good
    )
)
echo.

echo ========================================
echo  STEP 7/8: Install Dependencies
echo ========================================
echo.

echo Upgrading pip...
python -m pip install --upgrade pip > nul 2>&1
echo [OK] pip upgraded
echo.

echo Installing required packages...
echo This may take a few minutes, please wait...
echo.

if exist "requirements.txt" (
    echo Installing from requirements.txt...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo [WARN] Some packages failed, trying essentials...
        python -m pip install pyupbit pandas numpy requests python-dotenv colorlog ta
    )
) else (
    echo Installing essential packages...
    python -m pip install pyupbit pandas numpy requests python-dotenv colorlog ta
)

if errorlevel 1 (
    echo.
    echo [ERROR] Package installation failed!
    echo.
    echo Please try installing manually:
    echo   pip install pyupbit pandas numpy requests python-dotenv colorlog ta
    echo.
    pause
    exit /b 1
)
echo.
echo [OK] All packages installed successfully
echo.

echo ========================================
echo  STEP 8/8: Restore Configuration
echo ========================================
echo.

if exist ".env.backup" (
    echo Restoring .env file...
    copy /Y .env.backup .env > nul
    echo [OK] .env file restored from backup
) else if exist ".env" (
    echo [OK] .env file already exists
) else (
    echo Creating new .env file...
    (
        echo # Upbit AutoProfit Bot v6.30.38
        echo.
        echo TRADING_MODE=paper
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
        echo # Logging
        echo LOG_LEVEL=INFO
        echo ENABLE_TRADING_LOG=true
        echo ENABLE_ERROR_LOG=true
        echo.
        echo # Upbit API Keys ^(for live trading^)
        echo UPBIT_ACCESS_KEY=
        echo UPBIT_SECRET_KEY=
    ) > .env
    echo [OK] Default .env file created
)
echo.

echo ========================================
echo  REINSTALL COMPLETE!
echo ========================================
echo.
echo Current version: v6.30.38
echo Repository: https://github.com/lee-jungkil/Lj
echo.
echo Next steps:
echo   1. Review your .env file settings
echo   2. For live trading: Add Upbit API keys to .env
echo   3. Press any key to start the bot in paper mode
echo.
echo.
set /p START="Start bot now? (Y/N): "
if /i "%START%"=="Y" (
    echo.
    echo ========================================
    echo  STARTING BOT...
    echo ========================================
    echo.
    echo Starting with -u flag for unbuffered output...
    echo You should see DEBUG logs every 3-5 seconds
    echo.
    timeout /t 2 /nobreak > nul
    python -B -u -m src.main --mode paper
) else (
    echo.
    echo To start the bot manually, run:
    echo   python -B -u -m src.main --mode paper
    echo.
    echo Or use:
    echo   RUN_PAPER_CLEAN.bat
    echo.
)

echo.
echo Press any key to exit...
pause > nul
exit /b 0
