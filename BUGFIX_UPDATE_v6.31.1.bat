@echo off
chcp 65001 > nul
title Bugfix Update v6.31.1

echo ============================================================
echo Bugfix Update v6.31.1 - IndentationError Fixed
echo ============================================================
echo.
echo This update fixes Python syntax errors (IndentationError)
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
curl -L -o main.py.tmp https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py 2>nul
if %errorlevel% equ 0 (
    move /y main.py.tmp src\main.py >nul
    echo [OK] main.py updated
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
echo Bugfix applied! Bot starting...
echo ============================================================
echo.
timeout /t 3 /nobreak > nul

python -B -u -m src.main --mode paper
