@echo off
chcp 65001 > nul
title Upbit Bot Update v6.30.67
color 0A

echo ========================================
echo  UPBIT BOT UPDATE v6.30.67
echo  Debug Version - No Korean Characters
echo ========================================
echo.

cd /d "%~dp0"
echo Working directory: %CD%
echo.

echo [Step 1/4] Stopping Python processes...
taskkill /F /IM python.exe /T 2>nul
timeout /t 2 /nobreak > nul
echo Done.
echo.

echo [Step 2/4] Clearing cache files...
del /s /q *.pyc 2>nul
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
echo Done.
echo.

echo [Step 3/4] Downloading v6.30.67 code...
powershell -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py' -OutFile 'src\main.py' -UseBasicParsing" 2>nul
if errorlevel 1 (
    echo ERROR: Download failed! Check internet connection.
    echo.
    echo Manual download:
    echo https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
    echo.
    pause
    exit /b 1
)

powershell -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/lee-jungkil/Lj/main/VERSION.txt' -OutFile 'VERSION.txt' -UseBasicParsing" 2>nul
echo Done.
echo.

echo [Step 4/4] Verifying installation...
if exist VERSION.txt (
    type VERSION.txt
    echo.
) else (
    echo ERROR: VERSION.txt not found!
    pause
    exit /b 1
)

echo ========================================
echo  UPDATE COMPLETE
echo ========================================
echo.
echo Version: v6.30.67-DEBUG-LOGGING
echo.
echo Start command:
echo   python -B -u -m src.main --mode paper
echo.
echo IMPORTANT: Watch for these logs when selling:
echo   [EXECUTE-SELL] Price fetch starting...
echo   [EXECUTE-SELL] Price attempt 1/3...
echo   [EXECUTE-SELL] Price result: XXXXX
echo   [EXECUTE-SELL] Profit calculation...
echo   [EXECUTE-SELL] Spread analysis...
echo   [EXECUTE-SELL] Market condition...
echo.
echo If logs STOP at any step, screenshot it!
echo.

pause
