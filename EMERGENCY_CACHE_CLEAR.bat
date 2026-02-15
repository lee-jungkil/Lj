@echo off
title Upbit AutoProfit Bot v6.30.62 - EMERGENCY CACHE CLEAR
color 0C

echo.
echo ========================================
echo  EMERGENCY CACHE CLEAR v6.30.62
echo ========================================
echo.
echo This script will:
echo   1. Stop all Python processes
echo   2. Delete ALL Python cache files
echo   3. Verify deletion
echo   4. Restart the bot
echo.
echo Use this when:
echo   - Sell orders not executing
echo   - Old code still running
echo   - [EXECUTE-SELL] logs missing
echo.
pause

REM Change to script directory
cd /d "%~dp0"
echo.
echo Current directory: %cd%
echo.

echo ========================================
echo  Step 1: Stop Python Processes
echo ========================================
echo.
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM pythonw.exe /T 2>nul
timeout /t 2 /nobreak >nul
echo [OK] Python processes stopped
echo.

echo ========================================
echo  Step 2: Delete __pycache__ Folders
echo ========================================
echo.
for /d /r . %%d in (__pycache__) do (
    if exist "%%d" (
        echo Deleting: %%d
        rd /s /q "%%d" 2>nul
    )
)
echo [OK] __pycache__ folders deleted
echo.

echo ========================================
echo  Step 3: Delete .pyc Files
echo ========================================
echo.
del /s /q *.pyc 2>nul
echo [OK] .pyc files deleted
echo.

echo ========================================
echo  Step 4: Delete Specific Caches
echo ========================================
echo.
if exist "src\__pycache__" (
    rd /s /q "src\__pycache__" 2>nul
    echo [OK] src\__pycache__ deleted
) else (
    echo [INFO] src\__pycache__ not found
)

if exist "src\strategies\__pycache__" (
    rd /s /q "src\strategies\__pycache__" 2>nul
    echo [OK] src\strategies\__pycache__ deleted
) else (
    echo [INFO] src\strategies\__pycache__ not found
)

if exist "src\ai\__pycache__" (
    rd /s /q "src\ai\__pycache__" 2>nul
    echo [OK] src\ai\__pycache__ deleted
) else (
    echo [INFO] src\ai\__pycache__ not found
)

if exist "src\utils\__pycache__" (
    rd /s /q "src\utils\__pycache__" 2>nul
    echo [OK] src\utils\__pycache__ deleted
) else (
    echo [INFO] src\utils\__pycache__ not found
)
echo.

echo ========================================
echo  Step 5: Verify VERSION
echo ========================================
echo.
if exist "VERSION.txt" (
    type VERSION.txt
    echo.
) else (
    echo [WARN] VERSION.txt not found
)
echo.

echo ========================================
echo  Step 6: Verify Debug Logs
echo ========================================
echo.
findstr /C:"[EXECUTE-SELL]" src\main.py >nul 2>&1
if errorlevel 1 (
    echo [ERROR] [EXECUTE-SELL] logs not found in main.py!
    echo.
    echo Please download latest code:
    echo https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
    echo.
    pause
    exit /b 1
) else (
    echo [OK] [EXECUTE-SELL] debug logs present
)
echo.

echo ========================================
echo  Cache Deletion Complete!
echo ========================================
echo.
echo Now starting the bot...
echo.
echo Expected logs after cache clear:
echo   [EXECUTE-SELL] execute_sell called
echo   [EXECUTE-SELL] Position cleanup start
echo   [EXECUTE-SELL] holding_protector called
echo   [EXECUTE-SELL] risk_manager called
echo.
echo If you DON'T see [EXECUTE-SELL] logs:
echo   1. Run this script again
echo   2. Download fresh ZIP:
echo      https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
echo.
pause

echo.
echo ========================================
echo  Starting Bot (Paper Mode)
echo ========================================
echo.

python -B -u -m src.main --mode paper

echo.
echo ========================================
echo  Bot Stopped
echo ========================================
echo.
pause
