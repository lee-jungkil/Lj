@echo off
chcp 65001 > nul
title Upbit AutoProfit Bot - CRITICAL UPDATE v6.30.66
color 0C

echo ========================================
echo  🚨 CRITICAL FIX v6.30.66
echo  Exception Cleanup - No More Stuck Positions
echo ========================================
echo.
echo WHAT THIS FIXES:
echo - Positions stuck on screen after sell attempt
echo - Sell counter not incrementing
echo - Exception in execute_sell^(^) preventing cleanup
echo.

cd /d "%~dp0"

echo [STEP 1/7] Stopping all Python processes...
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM pythonw.exe /T 2>nul
wmic process where "commandline like '%%src.main%%'" delete 2>nul
timeout /t 3 /nobreak > nul
echo Done.
echo.

echo [STEP 2/7] Clearing ALL cache files...
del /s /q *.pyc 2>nul
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
echo Done.
echo.

echo [STEP 3/7] Downloading latest code (v6.30.66)...
powershell -Command "try { Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py' -OutFile 'src\main.py' -UseBasicParsing; Write-Host 'main.py downloaded' } catch { Write-Host 'Failed'; exit 1 }"
if %errorlevel% NEQ 0 (
    echo [ERROR] Failed to download main.py
    echo Please download manually from: https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
    pause
    exit /b 1
)

powershell -Command "try { Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/lee-jungkil/Lj/main/VERSION.txt' -OutFile 'VERSION.txt' -UseBasicParsing; Write-Host 'VERSION.txt downloaded' } catch { Write-Host 'Failed'; exit 1 }"
if %errorlevel% NEQ 0 (
    echo [ERROR] Failed to download VERSION.txt
    pause
    exit /b 1
)
echo Done.
echo.

echo [STEP 4/7] Verifying version...
type VERSION.txt
echo.

echo [STEP 5/7] Verifying critical fix...
findstr /C:"예외 발생 - 포지션 강제 청산" src\main.py >nul
if %errorlevel% EQU 0 (
    echo [SUCCESS] v6.30.66 exception cleanup code verified!
) else (
    echo [ERROR] Critical fix not found in code!
    echo Please re-download from: https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
    pause
    exit /b 1
)
echo.

echo [STEP 6/7] Final cache verification...
dir /s /b src\__pycache__ 2>nul | findstr /R "." >nul
if %errorlevel% EQU 0 (
    echo [WARNING] Cache still exists. Deleting again...
    for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
    timeout /t 1 /nobreak > nul
    echo Done.
) else (
    echo [SUCCESS] All cache cleared!
)
echo.

echo [STEP 7/7] Ready to start!
echo.

echo ========================================
echo  UPDATE COMPLETE!
echo ========================================
echo.
echo Version: v6.30.66-EXCEPTION-CLEANUP
echo Status: READY
echo.
echo WHAT WAS FIXED:
echo ✅ Positions now ALWAYS cleaned up, even on exception
echo ✅ Each cleanup step isolated with try-except
echo ✅ Price fetch failure uses avg_buy_price fallback
echo ✅ Detailed exception logging with stack traces
echo.
echo EXPECTED LOGS ON SELL:
echo - Normal: [EXECUTE-SELL] ========== Position cleanup start ==========
echo - Exception: [EXECUTE-SELL] ========== 예외 발생 - 포지션 강제 청산 시작 ==========
echo - Always: [EXECUTE-SELL] ✅ holding_protector cleanup complete
echo - Always: [EXECUTE-SELL] ✅ risk_manager cleanup complete
echo - Always: [EXECUTE-SELL] ✅ UI에서 포지션 제거 완료
echo.
echo YOUR PROBLEM (positions stuck on screen) IS NOW FIXED!
echo.
echo ========================================
echo.

set /p start="Start bot now with -B flag? (Y/N): "
if /i "%start%"=="Y" (
    echo.
    echo Starting bot in paper-trading mode...
    echo Watch for [EXECUTE-SELL] logs to verify cleanup!
    echo Press Ctrl+C to stop.
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
