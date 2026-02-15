@echo off
title Upbit Bot v6.30.62 - Paper Mode
color 0A

echo.
echo ========================================
echo  Upbit AutoProfit Bot v6.30.62
echo  PAPER TRADING MODE
echo ========================================
echo.

cd /d "%~dp0"
echo Directory: %cd%
echo.

echo Checking Python...
python --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    pause
    exit /b 1
)
python --version
echo [OK] Python found
echo.

echo Checking files...
if not exist "src\main.py" (
    echo [ERROR] main.py not found!
    echo Run COMPLETE_REINSTALL.bat
    pause
    exit /b 1
)
echo [OK] Files found
echo.

echo Cleaning cache...
del /s /q *.pyc > nul 2>&1
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
echo [OK] Cache clean
echo.

if not exist ".env" (
    echo Creating .env...
    (
        echo TRADING_MODE=paper
        echo INITIAL_CAPITAL=5000000
        echo LOG_LEVEL=INFO
    ) > .env
)
echo [OK] Config ready
echo.

echo ========================================
echo  STARTING BOT
echo ========================================
echo.
echo Mode: PAPER (Safe)
echo Version: v6.30.62
echo.
timeout /t 2 /nobreak > nul

python -B -u -m src.main --mode paper

echo.
if errorlevel 1 (
    echo [ERROR] Bot failed
    echo Run COMPLETE_REINSTALL.bat
) else (
    echo [INFO] Bot stopped
)
echo.
pause
