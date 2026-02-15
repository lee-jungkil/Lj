@echo off
title Upbit AutoProfit Bot v6.30.64 - COMPLETE REINSTALL
color 0E

echo.
echo ========================================
echo  Upbit AutoProfit Bot v6.30.64
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

REM Delete existing .git folder to avoid conflicts
if exist ".git" (
    echo Removing old git repository...
    rd /s /q ".git" 2>nul
    echo [OK] Old git removed
)

git --version > nul 2>&1
if errorlevel 1 (
    echo [WARN] Git not found, using PowerShell...
    echo.
    
    REM Create src directory if not exists
    if not exist "src" mkdir src
    
    REM Download main files using PowerShell
    echo Downloading src/main.py...
    powershell -Command "try { Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py' -OutFile 'src\main.py' -UseBasicParsing; exit 0 } catch { exit 1 }"
    
    if errorlevel 1 (
        echo [ERROR] PowerShell download failed!
        echo.
        echo Please download manually:
        echo https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
        echo.
        echo Extract the ZIP and copy contents to:
        echo %cd%
        echo.
        pause
        exit /b 1
    )
    
    echo Downloading VERSION.txt...
    powershell -Command "try { Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/lee-jungkil/Lj/main/VERSION.txt' -OutFile 'VERSION.txt' -UseBasicParsing; exit 0 } catch { exit 1 }"
    
    echo Downloading requirements.txt...
    powershell -Command "try { Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/lee-jungkil/Lj/main/requirements.txt' -OutFile 'requirements.txt' -UseBasicParsing; exit 0 } catch { exit 1 }"
    
    echo [OK] Files downloaded via PowerShell
    
) else (
    echo [OK] Git found
    git --version
    echo.
    
    REM Initialize fresh git repository
    echo Initializing Git repository...
    git init
    
    echo Adding remote...
    git remote add origin https://github.com/lee-jungkil/Lj.git
    
    echo Fetching code...
    git fetch origin main 2>&1
    if errorlevel 1 (
        echo [ERROR] Git fetch failed!
        echo.
        echo Trying alternative method...
        echo.
        
        REM Fallback to PowerShell
        if not exist "src" mkdir src
        
        echo Downloading with PowerShell...
        powershell -Command "try { Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py' -OutFile 'src\main.py' -UseBasicParsing; exit 0 } catch { exit 1 }"
        
        if errorlevel 1 (
            echo [ERROR] All download methods failed!
            echo.
            echo Please download manually:
            echo https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
            echo.
            pause
            exit /b 1
        )
        
        powershell -Command "try { Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/lee-jungkil/Lj/main/VERSION.txt' -OutFile 'VERSION.txt' -UseBasicParsing; exit 0 } catch { exit 1 }"
        powershell -Command "try { Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/lee-jungkil/Lj/main/requirements.txt' -OutFile 'requirements.txt' -UseBasicParsing; exit 0 } catch { exit 1 }"
        
        echo [OK] Downloaded via PowerShell fallback
    ) else (
        echo Resetting to latest...
        git reset --hard origin/main
        echo [OK] Code updated via Git
    )
)
echo.

echo ========================================
echo  STEP 6/9: Verify Code
echo ========================================
echo.

if not exist "src\main.py" (
    echo [ERROR] main.py not found!
    echo.
    echo Please download manually:
    echo https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
    echo.
    pause
    exit /b 1
)

findstr /C:"class AutoProfitBot" src\main.py > nul
if errorlevel 1 (
    echo [ERROR] AutoProfitBot not found in main.py!
    pause
    exit /b 1
)
echo [OK] AutoProfitBot found
echo.

findstr /C:"[EXECUTE-SELL]" src\main.py > nul
if errorlevel 1 (
    echo [WARN] Debug logs not found (might be old version)
) else (
    echo [OK] Debug logs found
)
echo.

if exist "VERSION.txt" (
    echo Version:
    type VERSION.txt
    echo.
) else (
    echo [WARN] VERSION.txt not found
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
    echo Found requirements.txt, installing...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [WARN] requirements.txt install failed, trying manual...
        python -m pip install pyupbit pandas numpy requests python-dotenv colorlog ta colorama schedule
    )
) else (
    echo No requirements.txt, installing manually...
    python -m pip install pyupbit pandas numpy requests python-dotenv colorlog ta colorama schedule
)

if errorlevel 1 (
    echo [ERROR] Package install failed!
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
    echo [OK] Config restored from backup
) else if exist ".env" (
    echo [OK] Config already exists
) else (
    echo Creating default .env...
    (
        echo # Upbit Bot v6.30.64
        echo TRADING_MODE=paper
        echo INITIAL_CAPITAL=5000000
        echo MAX_DAILY_LOSS=500000
        echo MAX_CUMULATIVE_LOSS=1000000
        echo MAX_POSITIONS=5
        echo ENABLE_ADVANCED_AI=false
        echo LOG_LEVEL=INFO
    ) > .env
    echo [OK] Default config created
)
echo.

echo ========================================
echo  STEP 9/9: Final Verification
echo ========================================
echo.

if exist "src\__pycache__" (
    echo [WARN] Cache still exists
) else (
    echo [OK] Cache deleted
)

findstr /C:"[EXECUTE-SELL]" src\main.py > nul
if errorlevel 1 (
    echo [WARN] Old code (no debug logs)
) else (
    echo [OK] Latest code detected
)

if exist "VERSION.txt" (
    echo [OK] VERSION.txt exists
) else (
    echo [WARN] VERSION.txt missing
)

echo.

echo ========================================
echo  INSTALLATION COMPLETE!
echo ========================================
echo.
echo Version: v6.30.64-CRITICAL-SELL-FIX
echo Repo: https://github.com/lee-jungkil/Lj
echo.
echo Critical Fix Applied:
echo   - Position cleanup continues even if order fails
echo   - Enhanced debugging logs
echo   - Cache handling improved
echo.
echo Expected logs when bot runs:
echo   [EXECUTE-SELL] execute_sell called
echo   [EXECUTE-SELL] cleanup start
echo   [EXECUTE-SELL] holding_protector complete
echo   [EXECUTE-SELL] risk_manager complete
echo.
set /p START="Start bot now? (Y/N): "
if /i "%START%"=="Y" (
    echo.
    echo Starting bot in paper trading mode...
    echo.
    timeout /t 2 /nobreak > nul
    python -B -u -m src.main --mode paper
) else (
    echo.
    echo To start manually:
    echo   python -B -u -m src.main --mode paper
    echo.
    echo To use live trading:
    echo   1. Edit .env file
    echo   2. Set TRADING_MODE=live
    echo   3. Add your Upbit API keys
    echo   4. Run: python -B -u -m src.main --mode live
    echo.
)

pause
exit /b 0
