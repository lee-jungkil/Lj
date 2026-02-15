@echo off
chcp 65001 > nul
title Remove All Debug Output v6.30.71

echo ============================================================
echo Remove All Debug Output Update v6.30.71
echo ============================================================
echo.
echo This script will:
echo 1. Stop the bot
echo 2. Remove all DEBUG/CHECK/verification outputs
echo 3. Clear cache files
echo 4. Restart the bot
echo.
echo ============================================================
pause

echo.
echo [1/5] Stopping bot...
taskkill /F /IM python.exe /T 2>nul
if %errorlevel% equ 0 (
    echo [OK] Python process stopped
) else (
    echo [INFO] No running Python process found
)
timeout /t 2 /nobreak > nul

echo.
echo [2/5] Removing debug outputs...
python REMOVE_ALL_DEBUG.py
if %errorlevel% equ 0 (
    echo [OK] Debug outputs removed successfully
) else (
    echo [ERROR] Failed to remove debug outputs
    pause
    exit /b 1
)

echo.
echo [3/5] Clearing cache...
del /s /q *.pyc 2>nul
for /d /r %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
echo [OK] Cache cleared

echo.
echo [4/5] Checking version...
type VERSION.txt
echo.

echo.
echo [5/5] Restarting bot...
echo.
echo ============================================================
echo Bot is starting. No more DEBUG outputs will be displayed!
echo ============================================================
echo.
timeout /t 3 /nobreak > nul

python -B -u -m src.main --mode paper
