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

cd /d "%~dp0"

echo [1/6] Stopping Python...
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM pythonw.exe /T 2>nul
timeout /t 2 /nobreak > nul
echo Done.
echo.

echo [2/6] Clearing cache...
del /s /q *.pyc 2>nul
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
echo Done.
echo.

echo [3/6] Downloading v6.30.67...
powershell -Command "try { Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py' -OutFile 'src\main.py' -UseBasicParsing; Write-Host 'main.py OK' } catch { Write-Host 'FAILED'; exit 1 }"
if %errorlevel% NEQ 0 (
    echo [ERROR] Download failed!
    pause
    exit /b 1
)

powershell -Command "try { Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/lee-jungkil/Lj/main/VERSION.txt' -OutFile 'VERSION.txt' -UseBasicParsing; Write-Host 'VERSION.txt OK' } catch { Write-Host 'FAILED'; exit 1 }"
if %errorlevel% NEQ 0 (
    echo [ERROR] Download failed!
    pause
    exit /b 1
)
echo Done.
echo.

echo [4/6] Verifying version...
type VERSION.txt
echo.

echo [5/6] Verifying debug logs...
findstr /C:"현재가 조회 시작" src\main.py >nul
if %errorlevel% EQU 0 (
    findstr /C:"손익률 계산 중" src\main.py >nul
    if %errorlevel% EQU 0 (
        findstr /C:"스프레드 분석 중" src\main.py >nul
        if %errorlevel% EQU 0 (
            echo [SUCCESS] All debug logs verified!
        ) else (
            echo [ERROR] Missing debug logs!
            pause
            exit /b 1
        )
    ) else (
        echo [ERROR] Missing debug logs!
        pause
        exit /b 1
    )
) else (
    echo [ERROR] Debug code not found!
    pause
    exit /b 1
)
echo.

echo [6/6] Cache verification...
dir /s /b src\__pycache__ 2>nul | findstr /R "." >nul
if %errorlevel% EQU 0 (
    echo [WARNING] Cache exists, deleting again...
    for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
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
echo NEW LOGS TO WATCH FOR:
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
echo If logs STOP at any step, that's the problem!
echo.
echo IMPORTANT:
echo   - When sell happens, CAPTURE THE FULL LOG!
echo   - Screenshot or copy the entire [EXECUTE-SELL] section
echo   - This will tell us EXACTLY where it fails
echo.
echo ========================================
echo.

set /p start="Start bot now? (Y/N): "
if /i "%start%"=="Y" (
    echo.
    echo Starting bot with debug logging...
    echo Watch for [EXECUTE-SELL] messages!
    echo.
    timeout /t 2 /nobreak > nul
    python -B -u -m src.main --mode paper
) else (
    echo.
    echo To start manually:
    echo python -B -u -m src.main --mode paper
    echo.
)

pause
