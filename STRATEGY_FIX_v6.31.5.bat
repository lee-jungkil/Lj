@echo off
chcp 65001 > nul
setlocal EnableDelayedExpansion

echo ============================================================
echo    Trading Strategy Fix Update v6.31.5
echo ============================================================
echo.
echo [INFO] This update includes critical trading improvements:
echo   1. Minimum hold time enforcement (5 minutes)
echo   2. Relaxed sudden drop threshold (-1.5%% -^> -2.5%%)
echo   3. AI learning fee correction (0.1%% total fees)
echo   4. Raised take-profit target (1.0%% -^> 1.5%%)
echo.

REM Step 1: Check if bot is running
echo [1/6] Checking bot status...
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [WARNING] Python bot detected. Attempting to stop...
    taskkill /IM python.exe /F 2>NUL
    timeout /t 2 /nobreak > nul
    echo [OK] Bot stopped
) else (
    echo [OK] No bot running
)
echo.

REM Step 2: Backup current files
echo [2/6] Creating backup...
if not exist "backup" mkdir backup
set TIMESTAMP=%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%
copy src\main.py backup\main_%TIMESTAMP%.py > nul 2>&1
copy src\config.py backup\config_%TIMESTAMP%.py > nul 2>&1
copy src\ai\learning_engine.py backup\learning_engine_%TIMESTAMP%.py > nul 2>&1
echo [OK] Backup created: backup\*_%TIMESTAMP%.py
echo.

REM Step 3: Download updated files
echo [3/6] Downloading updated files...
curl -L -s -o src\main.py https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to download src\main.py
    goto :error
)
echo [OK] Updated src\main.py

curl -L -s -o src\config.py https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/config.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to download src\config.py
    goto :error
)
echo [OK] Updated src\config.py

curl -L -s -o src\ai\learning_engine.py https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/ai/learning_engine.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to download src\ai\learning_engine.py
    goto :error
)
echo [OK] Updated src\ai\learning_engine.py

curl -L -s -o VERSION.txt https://raw.githubusercontent.com/lee-jungkil/Lj/main/VERSION.txt
echo [OK] Updated VERSION.txt
echo.

REM Step 4: Clean cache
echo [4/6] Cleaning Python cache...
del /s /q *.pyc > nul 2>&1
for /d /r %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
echo [OK] Cache cleared
echo.

REM Step 5: Verify version
echo [5/6] Verifying version...
type VERSION.txt
echo.

REM Step 6: Complete
echo [6/6] Update complete!
echo.
echo ============================================================
echo    What Changed in v6.31.5?
echo ============================================================
echo.
echo [FIX 1] Minimum Hold Time (5 minutes)
echo   - Prevents premature exits during normal market swings
echo   - Gives trades time to recover from minor dips
echo   - Reduces emotional/panic selling
echo.
echo [FIX 2] Relaxed Sudden Drop Threshold
echo   - Old: -1.5%% triggered panic sell
echo   - New: -2.5%% allows normal crypto volatility
echo   - Reduces false positive exits
echo.
echo [FIX 3] AI Learning Fee Correction
echo   - Now includes 0.1%% total trading fees (0.05%% buy + 0.05%% sell)
echo   - Prevents AI from learning overly-optimistic profit expectations
echo   - More accurate profit/loss recording
echo.
echo [FIX 4] Raised Take-Profit Target
echo   - Old: 1.0%% quick exit
echo   - New: 1.5%% lets winners run
echo   - Increases average profit per winning trade
echo.
echo ============================================================
echo    Expected Improvements
echo ============================================================
echo.
echo   - Win rate stabilization (prevent decline)
echo   - Higher average profit per trade
echo   - Fewer premature exits
echo   - More accurate AI learning
echo   - Better handling of normal volatility
echo.
echo ============================================================
echo    Next Steps
echo ============================================================
echo.
echo   1. Start bot: python -B -u -m src.main --mode paper
echo   2. Monitor for 100-200 trades
echo   3. Compare results with previous performance
echo   4. Check trading_logs for improved patterns
echo.
echo [READY] You can now start the bot.
echo.
pause
goto :eof

:error
echo.
echo [FAILED] Update failed. Restoring from backup...
copy backup\main_%TIMESTAMP%.py src\main.py > nul 2>&1
copy backup\config_%TIMESTAMP%.py src\config.py > nul 2>&1
copy backup\learning_engine_%TIMESTAMP%.py src\ai\learning_engine.py > nul 2>&1
echo [OK] Files restored from backup
pause
exit /b 1
