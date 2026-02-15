@echo off
chcp 65001 > nul
title Quick No-Debug Update

echo ============================================================
echo Quick No-Debug Update v6.30.71
echo ============================================================
echo.
echo Downloads and applies latest code without debug outputs
echo.
pause

echo.
echo [1/4] Stopping bot...
taskkill /F /IM python.exe /T 2>nul
timeout /t 2 /nobreak > nul

echo.
echo [2/4] Downloading scripts...
curl -L -o REMOVE_ALL_DEBUG.py https://raw.githubusercontent.com/lee-jungkil/Lj/main/REMOVE_ALL_DEBUG.py 2>nul
if %errorlevel% equ 0 (
    echo [OK] Downloaded REMOVE_ALL_DEBUG.py
) else (
    echo [ERROR] Download failed
    pause
    exit /b 1
)

curl -L -o main.py.tmp https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py 2>nul
if %errorlevel% equ 0 (
    move /y main.py.tmp src\main.py >nul
    echo [OK] Downloaded main.py
)

curl -L -o VERSION.txt https://raw.githubusercontent.com/lee-jungkil/Lj/main/VERSION.txt 2>nul
if %errorlevel% equ 0 (
    echo [OK] Downloaded VERSION.txt
)

echo.
echo [3/4] Clearing cache...
del /s /q *.pyc 2>nul
for /d /r %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
echo [OK] Cache cleared

echo.
echo [4/4] Version:
type VERSION.txt
echo.

echo ============================================================
echo Update complete! Press any key to start bot...
echo ============================================================
pause

python -B -u -m src.main --mode paper
