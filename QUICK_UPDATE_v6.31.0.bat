@echo off
chcp 65001 > nul
title Quick Update to v6.31.0

echo ============================================================
echo Quick Update to v6.31.0 FINAL
echo ============================================================
echo.
echo This will update your bot to the final stable version.
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
echo [3/5] Downloading latest code...
curl -L -o main.py.tmp https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py 2>nul
if %errorlevel% equ 0 (
    move /y main.py.tmp src\main.py >nul
    echo [OK] main.py updated
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
echo Update complete! Starting v6.31.0...
echo ============================================================
echo.
timeout /t 3 /nobreak > nul

python -B -u -m src.main --mode paper
