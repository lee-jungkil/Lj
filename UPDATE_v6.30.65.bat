@echo off
chcp 65001 > nul
title Upbit AutoProfit Bot - Update to v6.30.65-PAPER-MODE-FIX
color 0A

echo ========================================
echo  Upbit AutoProfit Bot v6.30.65 Update
echo  Critical Fix: Paper-Mode Sell Bug
echo ========================================
echo.

cd /d "%~dp0"

echo [STEP 1/6] Stopping Python processes...
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM pythonw.exe /T 2>nul
timeout /t 2 /nobreak > nul
echo Done.
echo.

echo [STEP 2/6] Deleting all cache files...
del /s /q *.pyc 2>nul
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
echo Done.
echo.

echo [STEP 3/6] Downloading latest code (v6.30.65)...
powershell -Command "try { Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py' -OutFile 'src\main.py' -UseBasicParsing; Write-Host 'main.py downloaded' } catch { Write-Host 'Failed to download main.py'; exit 1 }"
if %errorlevel% NEQ 0 (
    echo [ERROR] Failed to download main.py
    pause
    exit /b 1
)

powershell -Command "try { Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/lee-jungkil/Lj/main/VERSION.txt' -OutFile 'VERSION.txt' -UseBasicParsing; Write-Host 'VERSION.txt downloaded' } catch { Write-Host 'Failed to download VERSION.txt'; exit 1 }"
if %errorlevel% NEQ 0 (
    echo [ERROR] Failed to download VERSION.txt
    pause
    exit /b 1
)
echo Done.
echo.

echo [STEP 4/6] Verifying version...
type VERSION.txt
echo.

echo [STEP 5/6] Verifying code fix...
findstr /C:"모의거래 모드: 포지션 전체 매도 허용" src\main.py >nul
if %errorlevel% EQU 0 (
    echo [SUCCESS] v6.30.65 code verified!
    echo.
) else (
    echo [ERROR] Code verification failed!
    echo Please download manually from: https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
    pause
    exit /b 1
)

echo [STEP 6/6] Cache verification...
dir /s /b src\__pycache__ 2>nul | findstr /R "." >nul
if %errorlevel% EQU 0 (
    echo [WARNING] Cache files still exist. Deleting again...
    for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
    echo Done.
) else (
    echo [SUCCESS] All cache cleared!
)
echo.

echo ========================================
echo  Update Complete!
echo ========================================
echo.
echo Version: v6.30.65-PAPER-MODE-FIX
echo Status: READY TO RUN
echo.
echo WHAT WAS FIXED:
echo - Paper-mode sell execution now works correctly
echo - holding_protector check bypassed in paper mode
echo - Position cleanup always executes after sell
echo.
echo EXPECTED LOGS AFTER SELL:
echo - [EXECUTE-SELL] 모의거래 모드: 포지션 전체 매도 허용
echo - [EXECUTE-SELL] ========== Position cleanup start ==========
echo - [EXECUTE-SELL] holding_protector.close_bot_position^(^) called...
echo - [EXECUTE-SELL] risk_manager.close_position^(^) called...
echo - [EXECUTE-SELL] Position removed from UI
echo.
echo ========================================
echo.

set /p start="Start bot now? (Y/N): "
if /i "%start%"=="Y" (
    echo.
    echo Starting bot in paper-trading mode with -B flag...
    echo Press Ctrl+C to stop.
    echo.
    python -B -u -m src.main --mode paper
) else (
    echo.
    echo To start manually, run:
    echo python -B -u -m src.main --mode paper
    echo.
)

pause
