@echo off
chcp 65001 > nul
title Upbit Bot - DEBUG UPDATE v6.30.67
color 0E

echo ========================================
echo  DEBUG VERSION v6.30.67
echo  Extensive Logging for Sell Diagnosis
echo ========================================
echo.
echo This version adds 15+ debug logs to find
echo EXACTLY where sell execution stops!
echo.
echo Press any key to continue...
pause > nul
echo.

cd /d "%~dp0"

echo Current directory: %CD%
echo.

echo [1/6] Stopping Python...
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM pythonw.exe /T 2>nul
timeout /t 2 /nobreak > nul
echo Done.
echo.

echo [2/6] Clearing cache...
if exist "*.pyc" (
    del /s /q *.pyc 2>nul
    echo Deleted .pyc files
)
for /d /r . %%d in (__pycache__) do @if exist "%%d" (
    rd /s /q "%%d" 2>nul
    echo Deleted %%d
)
echo Cache clearing done.
echo.

echo [3/6] Downloading v6.30.67...
echo Downloading main.py...
powershell -ExecutionPolicy Bypass -Command "try { Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py' -OutFile 'src\main.py' -UseBasicParsing; Write-Host 'main.py downloaded successfully' } catch { Write-Host 'ERROR: Failed to download main.py'; Write-Host $_.Exception.Message; exit 1 }"
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to download main.py!
    echo Please check your internet connection.
    echo.
    goto :error_exit
)

echo Downloading VERSION.txt...
powershell -ExecutionPolicy Bypass -Command "try { Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/lee-jungkil/Lj/main/VERSION.txt' -OutFile 'VERSION.txt' -UseBasicParsing; Write-Host 'VERSION.txt downloaded successfully' } catch { Write-Host 'ERROR: Failed to download VERSION.txt'; Write-Host $_.Exception.Message; exit 1 }"
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to download VERSION.txt!
    echo Please check your internet connection.
    echo.
    goto :error_exit
)
echo Download complete.
echo.

echo [4/6] Verifying version...
if exist VERSION.txt (
    type VERSION.txt
    echo.
) else (
    echo [ERROR] VERSION.txt not found!
    goto :error_exit
)

echo [5/6] Verifying debug logs...
if not exist src\main.py (
    echo [ERROR] src\main.py not found!
    goto :error_exit
)

findstr /C:"현재가 조회 시작" src\main.py >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Debug log marker 1 not found!
    echo Code may not be v6.30.67
    goto :error_exit
)

findstr /C:"손익률 계산 중" src\main.py >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Debug log marker 2 not found!
    echo Code may not be v6.30.67
    goto :error_exit
)

findstr /C:"스프레드 분석 중" src\main.py >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Debug log marker 3 not found!
    echo Code may not be v6.30.67
    goto :error_exit
)

echo [SUCCESS] All debug logs verified!
echo v6.30.67 code confirmed.
echo.

echo [6/6] Final cache verification...
dir /s /b src\__pycache__ 2>nul | findstr /R "." >nul 2>&1
if not errorlevel 1 (
    echo [WARNING] Cache still exists, deleting again...
    for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
    echo Done.
) else (
    echo [SUCCESS] All cache cleared!
)
echo.

echo ========================================
echo  UPDATE COMPLETE!
echo ========================================
echo.
echo Version: v6.30.67-DEBUG-LOGGING
echo Status: DIAGNOSTIC VERSION
echo.
echo ----------------------------------------
echo NEW LOGS TO WATCH FOR:
echo ----------------------------------------
echo.
echo During sell, you will now see:
echo   [EXECUTE-SELL] 현재가 조회 시작...
echo   [EXECUTE-SELL] 가격 조회 시도 1/3...
echo   [EXECUTE-SELL] 가격 조회 결과: XXXXX
echo   [EXECUTE-SELL] 손익률 계산 중...
echo   [EXECUTE-SELL] 손익률: +X.XX%%
echo   [EXECUTE-SELL] ExitReason 파싱 중...
echo   [EXECUTE-SELL] ExitReason: XXXX
echo   [EXECUTE-SELL] 스프레드 분석 중...
echo   [EXECUTE-SELL] 스프레드: X.XX%%
echo   [EXECUTE-SELL] 시장 조건 분석 중...
echo   [EXECUTE-SELL] 시장 조건: {...}
echo   [EXECUTE-SELL] 주문 방법 선택 중...
echo   [EXECUTE-SELL] 주문 방법: XXXX
echo.
echo ----------------------------------------
echo IMPORTANT:
echo ----------------------------------------
echo.
echo If logs STOP at any step, that's where the problem is!
echo.
echo When sell happens:
echo   1. CAPTURE THE FULL LOG (screenshot or copy)
echo   2. Find the LAST [EXECUTE-SELL] message
echo   3. That tells us EXACTLY where it fails
echo.
echo ========================================
echo.
echo.

:ask_start
set /p start="Start bot now? (Y/N): "
if /i "%start%"=="Y" goto :start_bot
if /i "%start%"=="N" goto :manual_instructions
echo Invalid input. Please enter Y or N.
goto :ask_start

:start_bot
echo.
echo ========================================
echo  Starting Bot with Debug Logging
echo ========================================
echo.
echo Watch for [EXECUTE-SELL] messages!
echo Press Ctrl+C to stop the bot.
echo.
timeout /t 3 /nobreak > nul
python -B -u -m src.main --mode paper
echo.
echo Bot stopped.
goto :final_pause

:manual_instructions
echo.
echo ========================================
echo  Manual Start Instructions
echo ========================================
echo.
echo To start the bot manually, run:
echo   python -B -u -m src.main --mode paper
echo.
echo Make sure to use the -B flag to prevent cache!
echo.
goto :final_pause

:error_exit
echo.
echo ========================================
echo  UPDATE FAILED
echo ========================================
echo.
echo Please try one of these:
echo.
echo 1. Manual download:
echo    - Go to: https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
echo    - Extract to a new folder
echo    - Copy your .env file
echo    - Run: pip install -r requirements.txt
echo.
echo 2. Manual file download:
echo    - main.py: https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py
echo    - VERSION.txt: https://raw.githubusercontent.com/lee-jungkil/Lj/main/VERSION.txt
echo    - Save to current directory
echo.
echo ========================================
echo.
goto :final_pause

:final_pause
echo.
echo Press any key to exit...
pause > nul
exit /b 0
