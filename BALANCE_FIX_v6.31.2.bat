@echo off
chcp 65001 > nul
title Balance Fix Update v6.31.2

echo ============================================================
echo Balance Fix Update v6.31.2
echo ============================================================
echo.
echo This update fixes balance calculation after sell orders:
echo - Before: Total balance did not reflect profit/loss correctly
echo - After: Balance now correctly shows gains/losses with fees
echo.
echo Example:
echo - Start: 5,000,000 KRW
echo - Buy:  -1,000,000 KRW (balance: 4,000,000)
echo - Sell: +997,501 KRW with -0.05%% fee (balance: 4,997,501)
echo - Loss correctly reflected: -2,499 KRW
echo.
pause

echo.
echo [1/5] Stopping bot...
taskkill /F /IM python.exe /T 2>nul
timeout /t 2 /nobreak > nul

echo.
echo [2/5] Clearing cache...
del /s /q *.pyc 2>nul
for /d /r %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
echo [OK] Cache cleared

echo.
echo [3/5] Downloading fixed code...
curl -L -o risk_manager.py.tmp https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/utils/risk_manager.py 2>nul
if %errorlevel% equ 0 (
    move /y risk_manager.py.tmp src\utils\risk_manager.py >nul
    echo [OK] risk_manager.py updated
) else (
    echo [ERROR] Download failed
    pause
    exit /b 1
)

curl -L -o VERSION.txt https://raw.githubusercontent.com/lee-jungkil/Lj/main/VERSION.txt 2>nul
if %errorlevel% equ 0 (
    echo [OK] VERSION.txt updated
)

echo.
echo [4/5] Version:
type VERSION.txt
echo.

echo.
echo [5/5] Starting bot...
echo.
echo ============================================================
echo Balance calculation fixed! Bot starting...
echo ============================================================
echo.
echo Now your total balance will correctly reflect:
echo - Profits: Balance increases
echo - Losses:  Balance decreases
echo - All transactions include 0.05%% trading fees
echo.
timeout /t 3 /nobreak > nul

python -B -u -m src.main --mode paper
