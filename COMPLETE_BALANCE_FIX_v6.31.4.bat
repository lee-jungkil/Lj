@echo off
chcp 65001 > nul
title Complete Balance Fix v6.31.4

echo ============================================================
echo Complete Balance Fix v6.31.4
echo ============================================================
echo.
echo This is the COMPLETE fix for balance calculation!
echo.
echo Previous fix (v6.31.2) missed the buy fee deduction.
echo This update fixes BOTH buy and sell fee calculations.
echo.
echo What was wrong:
echo - v6.31.2: Only sell fee was deducted
echo - Buy fee was NOT deducted from balance
echo - Balance appeared higher than actual value
echo.
echo Complete fix now:
echo - Buy:  Deduct amount + 0.05%% buy fee
echo - Sell: Add amount - 0.05%% sell fee
echo - Balance now 100%% accurate!
echo.
echo Example:
echo - Start: 5,000,000 KRW
echo - Buy 1M + 500 fee:  Balance = 4,999,500
echo - Sell 998K - 499 fee: Balance = 4,997,001
echo - Loss: -2,999 (fully reflected!)
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
echo [3/5] Downloading complete fix...
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
echo Complete balance fix applied! Bot starting...
echo ============================================================
echo.
echo Balance calculation is now 100%% accurate:
echo.
echo Buy transaction:
echo   - Amount paid: Investment + 0.05%% fee
echo   - Balance: Correctly decreased
echo.
echo Sell transaction:
echo   - Amount received: Sale value - 0.05%% fee
echo   - Balance: Correctly increased
echo.
echo Result:
echo   - Profit: Total balance increases
echo   - Loss:   Total balance decreases
echo   - All fees properly accounted for
echo.
timeout /t 3 /nobreak > nul

python -B -u -m src.main --mode paper
