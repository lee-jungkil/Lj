@echo off
chcp 65001 > nul
title Clean Update v6.30.71

echo ============================================================
echo Clean Update v6.30.71 - No Debug Outputs
echo ============================================================
echo.
echo This script will:
echo 1. Stop Python processes
echo 2. Download latest code from GitHub
echo 3. Remove all debug outputs
echo 4. Clear cache
echo 5. Restart bot
echo.
set /p confirm="Continue? (Y/N): "
if /i not "%confirm%"=="Y" exit /b

echo.
echo [1/6] Stopping Python...
taskkill /F /IM python.exe /T 2>nul
if %errorlevel% equ 0 (
    echo [OK] Stopped
) else (
    echo [INFO] No process found
)
timeout /t 2 /nobreak > nul

echo.
echo [2/6] Clearing cache...
del /s /q *.pyc 2>nul
for /d /r %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
echo [OK] Cache cleared

echo.
echo [3/6] Downloading latest code...
curl -L -o main.py.tmp https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py 2>nul
if %errorlevel% equ 0 (
    move /y main.py.tmp src\main.py >nul
    echo [OK] main.py updated
) else (
    echo [ERROR] Download failed
    del main.py.tmp 2>nul
    pause
    exit /b 1
)

curl -L -o VERSION.txt https://raw.githubusercontent.com/lee-jungkil/Lj/main/VERSION.txt 2>nul
if %errorlevel% equ 0 (
    echo [OK] VERSION.txt updated
) else (
    echo [WARNING] VERSION.txt download failed
)

echo.
echo [4/6] Removing debug outputs...
if exist REMOVE_ALL_DEBUG.py (
    python REMOVE_ALL_DEBUG.py
    echo [OK] Debug outputs removed
) else (
    echo [INFO] Debug removal script not found, skipping
)

echo.
echo [5/6] Checking version...
type VERSION.txt
echo.

echo.
echo [6/6] Starting bot...
echo.
echo ============================================================
echo Bot is starting with clean output!
echo ============================================================
echo.
timeout /t 3 /nobreak > nul

python -B -u -m src.main --mode paper
