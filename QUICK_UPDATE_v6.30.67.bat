@echo off
chcp 65001 > nul
title Upbit Bot - Quick Update v6.30.67
color 0A

echo ========================================
echo  QUICK UPDATE v6.30.67
echo ========================================
echo.

cd /d "%~dp0"
echo Working in: %CD%
echo.

echo [1/4] Stopping Python...
taskkill /F /IM python.exe /T 2>nul
timeout /t 2 /nobreak > nul
echo Done.
echo.

echo [2/4] Clearing cache...
del /s /q *.pyc 2>nul
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
echo Done.
echo.

echo [3/4] Downloading v6.30.67...
powershell -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py' -OutFile 'src\main.py' -UseBasicParsing" 2>nul
if errorlevel 1 (
    echo ERROR: Download failed!
    echo Please check internet connection.
    pause
    exit /b 1
)
powershell -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/lee-jungkil/Lj/main/VERSION.txt' -OutFile 'VERSION.txt' -UseBasicParsing" 2>nul
echo Done.
echo.

echo [4/4] Verifying...
type VERSION.txt 2>nul
if errorlevel 1 (
    echo ERROR: VERSION.txt not found!
    pause
    exit /b 1
)
echo.

echo ========================================
echo UPDATE COMPLETE!
echo ========================================
echo.
echo Version: v6.30.67-DEBUG-LOGGING
echo.
echo When you start the bot, watch for these logs:
echo   [EXECUTE-SELL] 현재가 조회 시작...
echo   [EXECUTE-SELL] 가격 조회 시도 1/3...
echo   [EXECUTE-SELL] 손익률 계산 중...
echo   [EXECUTE-SELL] 스프레드 분석 중...
echo.
echo Start command:
echo   python -B -u -m src.main --mode paper
echo.

pause
