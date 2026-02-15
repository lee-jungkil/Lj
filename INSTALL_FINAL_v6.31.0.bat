@echo off
chcp 65001 > nul
title Final Release v6.31.0 Installation

echo ============================================================
echo Trading Bot v6.31.0 FINAL RELEASE
echo ============================================================
echo.
echo This is the final stable version with:
echo - AI Learning System (Buy/Sell Decision Support)
echo - Surge Detection Scanner (30-second cycle)
echo - Ultra-Scalping Strategy (Max 2 positions, 500K KRW)
echo - Multiple Trading Strategies (Aggressive, Conservative, etc.)
echo - Clean Console Output (No debug messages)
echo - Real-time Position Monitoring
echo - 10-minute Auto Screen Clear
echo - 5-line Work Status Display
echo - 10 Sell History Records
echo.
echo ============================================================
pause

echo.
echo [1/8] Stopping existing bot...
taskkill /F /IM python.exe /T 2>nul
if %errorlevel% equ 0 (
    echo [OK] Stopped
) else (
    echo [INFO] No running process
)
timeout /t 2 /nobreak > nul

echo.
echo [2/8] Clearing cache...
del /s /q *.pyc 2>nul
for /d /r %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
echo [OK] Cache cleared

echo.
echo [3/8] Downloading main.py...
curl -L -o main.py.tmp https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py 2>nul
if %errorlevel% equ 0 (
    move /y main.py.tmp src\main.py >nul
    echo [OK] main.py downloaded
) else (
    echo [ERROR] Failed to download main.py
    del main.py.tmp 2>nul
    pause
    exit /b 1
)

echo.
echo [4/8] Downloading config.py...
curl -L -o config.py.tmp https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/config.py 2>nul
if %errorlevel% equ 0 (
    move /y config.py.tmp src\config.py >nul
    echo [OK] config.py downloaded
) else (
    echo [WARNING] Failed to download config.py
    del config.py.tmp 2>nul
)

echo.
echo [5/8] Downloading display manager...
curl -L -o display.py.tmp https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/utils/fixed_screen_display.py 2>nul
if %errorlevel% equ 0 (
    move /y display.py.tmp src\utils\fixed_screen_display.py >nul
    echo [OK] display manager downloaded
) else (
    echo [WARNING] Failed to download display manager
    del display.py.tmp 2>nul
)

echo.
echo [6/8] Downloading VERSION.txt...
curl -L -o VERSION.txt https://raw.githubusercontent.com/lee-jungkil/Lj/main/VERSION.txt 2>nul
if %errorlevel% equ 0 (
    echo [OK] VERSION.txt downloaded
) else (
    echo [WARNING] Failed to download VERSION.txt
)

echo.
echo [7/8] Checking version...
type VERSION.txt
echo.

echo.
echo [8/8] Verifying installation...
if exist src\main.py (
    echo [OK] main.py exists
) else (
    echo [ERROR] main.py missing!
    pause
    exit /b 1
)

if exist src\config.py (
    echo [OK] config.py exists
) else (
    echo [ERROR] config.py missing!
    pause
    exit /b 1
)

if exist src\utils\fixed_screen_display.py (
    echo [OK] display manager exists
) else (
    echo [ERROR] display manager missing!
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Installation Complete!
echo ============================================================
echo.
echo Final Version: v6.31.0
echo.
echo Key Features:
echo - Max 2 ultra-scalping positions
echo - Daily limit: Unlimited
echo - Max investment: 500,000 KRW per trade
echo - Balance ratio: 15%%
echo - AI learning enabled
echo - Surge detection: 30-second cycle
echo - Screen auto-clear: Every 10 minutes
echo.
echo ============================================================
echo Press any key to start the bot...
echo ============================================================
pause

python -B -u -m src.main --mode paper
