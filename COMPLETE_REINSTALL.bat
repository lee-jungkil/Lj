@echo off
title Upbit AutoProfit Bot v6.30.62 - COMPLETE REINSTALL
color 0E

echo.
echo ========================================
echo  Upbit AutoProfit Bot v6.30.62
echo  COMPLETE REINSTALL
echo ========================================
echo.
echo This script will:
echo   1. Backup your .env file
echo   2. Stop all Python processes
echo   3. Delete ALL Python cache files
echo   4. Download latest code from GitHub
echo   5. Install all dependencies
echo   6. Restore your .env file
echo   7. Verify installation
echo   8. Start the bot
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
echo  STEP 1/9: Backup Configuration
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
    echo [OK] .env backed up
) else (
    echo [WARN] No .env file found
)
echo.

echo ========================================
echo  STEP 2/9: Stop Running Processes
echo ========================================
echo.

echo Stopping Python processes...
taskkill /F /IM python.exe /T > nul 2>&1
if errorlevel 1 (
    echo [INFO] No Python processes running
) else (
    echo [OK] Python stopped
    timeout /t 2 /nobreak > nul
)

taskkill /F /IM pythonw.exe /T > nul 2>&1
echo.

echo ========================================
echo  STEP 3/9: Delete Python Cache
echo ========================================
echo.

echo Deleting .pyc files...
del /s /q *.pyc > nul 2>&1
echo [OK] .pyc deleted
echo.

echo Deleting __pycache__ folders...
for /d /r . %%d in (__pycache__) do @if exist "%%d" (
    rd /s /q "%%d" 2>nul
)
echo [OK] __pycache__ deleted
echo.

echo Deleting specific caches...
if exist "src\__pycache__" rd /s /q "src\__pycache__" 2>nul
if exist "src\ai\__pycache__" rd /s /q "src\ai\__pycache__" 2>nul
if exist "src\strategies\__pycache__" rd /s /q "src\strategies\__pycache__" 2>nul
if exist "src\utils\__pycache__" rd /s /q "src\utils\__pycache__" 2>nul
echo [OK] Specific caches deleted
echo.

echo ========================================
echo  STEP 4/9: Check Python
echo ========================================
echo.

python --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not installed!
    echo.
    echo Install from: https://www.python.org/
    echo Check "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

python --version
echo [OK] Python found
echo.

echo ========================================
echo  STEP 5/9: Download Code
echo ========================================
echo.

git --version > nul 2>&1
if errorlevel 1 (
    echo [WARN] Git not found
    echo.
    echo Downloading with PowerShell...
    powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py' -OutFile 'src\main.py' -UseBasicParsing"
    
    if errorlevel 1 (
        echo [ERROR] Download failed!
        echo.
        echo Download from:
        echo https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
        echo.
        pause
        exit /b 1
    )
) else (
    echo [OK] Git found
    git --version
    echo.
    
    if not exist ".git" git init
    git remote remove origin > nul 2>&1
    git remote add origin https://github.com/lee-jungkil/Lj.git
    
    echo Fetching code...
    git fetch origin main
    if errorlevel 1 (
        echo [ERROR] Fetch failed!
        pause
        exit /b 1
    )
    
    git reset --hard origin/main
    echo [OK] Code updated
)
echo.

echo ========================================
echo  STEP 6/9: Verify Code
echo ========================================
echo.

if not exist "src\main.py" (
    echo [ERROR] main.py not found!
    pause
    exit /b 1
)

findstr /C:"class AutoProfitBot" src\main.py > nul
if errorlevel 1 (
    echo [ERROR] AutoProfitBot not found!
    pause
    exit /b 1
)
echo [OK] AutoProfitBot found
echo.

findstr /C:"[EXECUTE-SELL]" src\main.py > nul
if errorlevel 1 (
    echo [WARN] Debug logs not found
) else (
    echo [OK] Debug logs found
)
echo.

if exist "VERSION.txt" (
    echo Version:
    type VERSION.txt
    echo.
)
echo.

echo ========================================
echo  STEP 7/9: Install Packages
echo ========================================
echo.

echo Upgrading pip...
python -m pip install --upgrade pip > nul 2>&1
echo [OK] pip upgraded
echo.

echo Installing packages...
if exist "requirements.txt" (
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        python -m pip install pyupbit pandas numpy requests python-dotenv colorlog ta
    )
) else (
    python -m pip install pyupbit pandas numpy requests python-dotenv colorlog ta
)

if errorlevel 1 (
    echo [ERROR] Install failed!
    pause
    exit /b 1
)
echo [OK] Packages installed
echo.

echo ========================================
echo  STEP 8/9: Restore Config
echo ========================================
echo.

if exist ".env.backup" (
    copy /Y .env.backup .env > nul
    echo [OK] Config restored
) else if exist ".env" (
    echo [OK] Config exists
) else (
    echo Creating .env...
    (
        echo # Upbit Bot v6.30.62
        echo TRADING_MODE=paper
        echo INITIAL_CAPITAL=5000000
        echo MAX_DAILY_LOSS=500000
        echo MAX_CUMULATIVE_LOSS=1000000
        echo MAX_POSITIONS=5
        echo ENABLE_ADVANCED_AI=true
        echo LOG_LEVEL=INFO
    ) > .env
    echo [OK] Config created
)
echo.

echo ========================================
echo  STEP 9/9: Verify
echo ========================================
echo.

if exist "src\__pycache__" (
    echo [WARN] Cache exists
) else (
    echo [OK] Cache deleted
)

findstr /C:"[EXECUTE-SELL]" src\main.py > nul
if errorlevel 1 (
    echo [WARN] Old code
) else (
    echo [OK] Latest code
)
echo.

echo ========================================
echo  COMPLETE!
echo ========================================
echo.
echo Version: v6.30.62
echo Repo: https://github.com/lee-jungkil/Lj
echo.
echo Changes:
echo   - Cache deleted
echo   - Latest code
echo   - Packages updated
echo   - Sell debugging enhanced
echo.
echo Expected logs:
echo   [EXECUTE-SELL] called
echo   [EXECUTE-SELL] cleanup start
echo   [EXECUTE-SELL] protector called
echo.
set /p START="Start bot? (Y/N): "
if /i "%START%"=="Y" (
    echo.
    echo Starting bot...
    echo.
    timeout /t 2 /nobreak > nul
    python -B -u -m src.main --mode paper
) else (
    echo.
    echo Run manually:
    echo   python -B -u -m src.main --mode paper
    echo.
)

pause
exit /b 0
