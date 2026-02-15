@echo off
title Emergency Cache Clear v6.30.62
color 0C

echo.
echo ========================================
echo  EMERGENCY CACHE CLEAR
echo ========================================
echo.
echo This will:
echo   1. Stop Python
echo   2. Delete ALL cache
echo   3. Restart bot
echo.
pause

cd /d "%~dp0"
echo.

echo Step 1: Stop Python
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM pythonw.exe /T 2>nul
timeout /t 2 /nobreak >nul
echo [OK] Stopped
echo.

echo Step 2: Delete cache
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
del /s /q *.pyc 2>nul
if exist "src\__pycache__" rd /s /q "src\__pycache__" 2>nul
if exist "src\strategies\__pycache__" rd /s /q "src\strategies\__pycache__" 2>nul
if exist "src\ai\__pycache__" rd /s /q "src\ai\__pycache__" 2>nul
echo [OK] Deleted
echo.

echo Step 3: Verify
if exist "VERSION.txt" type VERSION.txt
echo.

findstr /C:"[EXECUTE-SELL]" src\main.py >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Old code!
    echo Download: https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
    pause
    exit /b 1
) else (
    echo [OK] Latest code
)
echo.

echo ========================================
echo  CACHE CLEARED
echo ========================================
echo.
echo Starting bot...
pause

python -B -u -m src.main --mode paper

pause
