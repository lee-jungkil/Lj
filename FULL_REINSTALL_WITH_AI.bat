@echo off
chcp 65001 > nul
setlocal EnableDelayedExpansion

echo ======================================================
echo   AI Learning Data Backup + Full Reinstall
echo ======================================================
echo.
echo Current Path: C:\Users\admin\Downloads\Lj-main\Lj-main
echo.
pause

set "BOT_DIR=%CD%"
set "TIMESTAMP=%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%"
set "TIMESTAMP=!TIMESTAMP: =0!"

echo.
echo ======================================================
echo   Step 1: Backup AI Learning Data
echo ======================================================
echo.

if not exist "%BOT_DIR%\AI_BACKUP" mkdir "%BOT_DIR%\AI_BACKUP"

:: Backup AI files
if exist "%BOT_DIR%\ai_learning_data.json" (
    copy "%BOT_DIR%\ai_learning_data.json" "%BOT_DIR%\AI_BACKUP\ai_learning_data_!TIMESTAMP!.json" > nul 2>&1
    echo [OK] ai_learning_data.json backed up
)

if exist "%BOT_DIR%\trade_history.json" (
    copy "%BOT_DIR%\trade_history.json" "%BOT_DIR%\AI_BACKUP\trade_history_!TIMESTAMP!.json" > nul 2>&1
    echo [OK] trade_history.json backed up
)

if exist "%BOT_DIR%\ai_learning.db" (
    copy "%BOT_DIR%\ai_learning.db" "%BOT_DIR%\AI_BACKUP\ai_learning_!TIMESTAMP!.db" > nul 2>&1
    echo [OK] ai_learning.db backed up
)

if exist "%BOT_DIR%\.env" (
    copy "%BOT_DIR%\.env" "%BOT_DIR%\AI_BACKUP\.env_!TIMESTAMP!" > nul 2>&1
    echo [OK] .env backed up
)

if exist "%BOT_DIR%\logs" (
    xcopy "%BOT_DIR%\logs" "%BOT_DIR%\AI_BACKUP\logs_!TIMESTAMP!\" /E /I /Q > nul 2>&1
    echo [OK] logs/ backed up
)

if exist "%BOT_DIR%\data" (
    xcopy "%BOT_DIR%\data" "%BOT_DIR%\AI_BACKUP\data_!TIMESTAMP!\" /E /I /Q > nul 2>&1
    echo [OK] data/ backed up
)

echo.
echo [OK] Backup complete: AI_BACKUP\
echo.

echo ======================================================
echo   Step 2: Download Latest Files
echo ======================================================
echo.

curl -# -L -o "%BOT_DIR%\src\config.py" "https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/config.py"
if !errorlevel! equ 0 (echo [OK] config.py) else (echo [ERROR] config.py)

curl -# -L -o "%BOT_DIR%\src\main.py" "https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py"
if !errorlevel! equ 0 (echo [OK] main.py) else (echo [ERROR] main.py)

if not exist "%BOT_DIR%\src\utils" mkdir "%BOT_DIR%\src\utils"
curl -# -L -o "%BOT_DIR%\src\utils\smart_investment_manager.py" "https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/utils/smart_investment_manager.py"
if !errorlevel! equ 0 (echo [OK] smart_investment_manager.py) else (echo [ERROR] smart_investment_manager.py)

curl -# -L -o "%BOT_DIR%\src\utils\surge_detector.py" "https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/utils/surge_detector.py"
if !errorlevel! equ 0 (echo [OK] surge_detector.py) else (echo [ERROR] surge_detector.py)

curl -# -L -o "%BOT_DIR%\VERSION.txt" "https://raw.githubusercontent.com/lee-jungkil/Lj/main/VERSION.txt"
if !errorlevel! equ 0 (echo [OK] VERSION.txt) else (echo [ERROR] VERSION.txt)

curl -# -L -o "%BOT_DIR%\test_smart_investment.py" "https://raw.githubusercontent.com/lee-jungkil/Lj/main/test_smart_investment.py"
if !errorlevel! equ 0 (echo [OK] test_smart_investment.py) else (echo [ERROR] test_smart_investment.py)

echo.
echo [OK] Download complete
echo.

echo ======================================================
echo   Step 3: Clear Cache
echo ======================================================
echo.

if exist "%BOT_DIR%\__pycache__" (
    rmdir /s /q "%BOT_DIR%\__pycache__" 2>nul
    echo [OK] __pycache__ cleared
)

if exist "%BOT_DIR%\src\__pycache__" (
    rmdir /s /q "%BOT_DIR%\src\__pycache__" 2>nul
    echo [OK] src\__pycache__ cleared
)

if exist "%BOT_DIR%\src\utils\__pycache__" (
    rmdir /s /q "%BOT_DIR%\src\utils\__pycache__" 2>nul
    echo [OK] src\utils\__pycache__ cleared
)

if exist "%BOT_DIR%\src\api\__pycache__" (
    rmdir /s /q "%BOT_DIR%\src\api\__pycache__" 2>nul
    echo [OK] src\api\__pycache__ cleared
)

if exist "%BOT_DIR%\src\strategies\__pycache__" (
    rmdir /s /q "%BOT_DIR%\src\strategies\__pycache__" 2>nul
    echo [OK] src\strategies\__pycache__ cleared
)

if exist "%BOT_DIR%\src\ai\__pycache__" (
    rmdir /s /q "%BOT_DIR%\src\ai\__pycache__" 2>nul
    echo [OK] src\ai\__pycache__ cleared
)

echo.
echo [OK] Cache cleared
echo.

echo ======================================================
echo   Step 4: Verify Installation
echo ======================================================
echo.

echo Version:
type "%BOT_DIR%\VERSION.txt"
echo.

echo Files:
if exist "%BOT_DIR%\src\config.py" (echo [OK] config.py) else (echo [ERROR] config.py)
if exist "%BOT_DIR%\src\main.py" (echo [OK] main.py) else (echo [ERROR] main.py)
if exist "%BOT_DIR%\src\utils\smart_investment_manager.py" (echo [OK] smart_investment_manager.py) else (echo [ERROR] smart_investment_manager.py)

echo.
echo ======================================================
echo   Full Reinstall Complete!
echo ======================================================
echo.
echo [Backup Location]
echo   AI_BACKUP\
echo   - Timestamp: !TIMESTAMP!
echo   - AI learning data preserved
echo.
echo [Next Steps]
echo.
echo 1. Test:
echo    python test_smart_investment.py
echo.
echo 2. Start Bot:
echo    python -B -u -m src.main --mode paper
echo.
echo 3. Restore AI Data (if needed):
echo    Copy files from AI_BACKUP\*_!TIMESTAMP!.* to original locations
echo.
echo ======================================================
pause
