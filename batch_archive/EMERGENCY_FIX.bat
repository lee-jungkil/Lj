@echo off
chcp 65001 >nul
cls
echo.
echo ========================================================================
echo    EMERGENCY FIX - Force Python to reload modules
echo ========================================================================
echo.

REM Step 1: Kill ALL Python processes
echo [1/5] Killing ALL Python processes...
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM pythonw.exe /T 2>nul
timeout /t 3 >nul
echo [OK] All Python processes terminated
echo.

REM Step 2: Delete ALL cache again
echo [2/5] Deleting ALL cache again...
rd /s /q src\__pycache__ 2>nul
rd /s /q src\ai\__pycache__ 2>nul
rd /s /q src\strategies\__pycache__ 2>nul
rd /s /q src\utils\__pycache__ 2>nul
del /s /q *.pyc 2>nul
echo [OK] Cache deleted
echo.

REM Step 3: Verify no cache
echo [3/5] Verifying cache deletion...
dir /s /b src\__pycache__ 2>nul
if %errorlevel% neq 0 (
    echo [OK] No cache found
) else (
    echo [ERROR] Cache still exists!
    pause
    exit /b 1
)
echo.

REM Step 4: Set Python environment variable to ignore .pyc
echo [4/5] Setting Python to ignore bytecode...
set PYTHONDONTWRITEBYTECODE=1
echo [OK] PYTHONDONTWRITEBYTECODE=1
echo.

REM Step 5: Run bot with -B flag (no bytecode)
echo [5/5] Starting bot with -B flag (no bytecode)...
echo.
echo ========================================================================
echo Expected logs every 3 seconds:
echo   [HH:MM:SS] Position liquidation check #1
echo   [HH:MM:SS] KRW-OM profit/loss: +0.10%%
echo ========================================================================
echo.
pause

python -B -m src.main --mode paper
