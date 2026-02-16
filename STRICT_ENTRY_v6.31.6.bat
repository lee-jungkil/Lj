@echo off
chcp 65001 > nul
setlocal EnableDelayedExpansion

echo ============================================================
echo    Strict Entry Criteria Update v6.31.6
echo ============================================================
echo.
echo [INFO] This update increases ALL buy entry thresholds by 10 percent
echo.
echo Changes:
echo   1. Surge Detection Thresholds (plus 10 percent)
echo   2. AI Confidence Requirements (plus 10 percent)
echo   3. Market Analysis Criteria (plus 10 percent)
echo.
echo Press any key to continue...
pause > nul
echo.

REM Step 1: Check if bot is running
echo [1/6] Checking bot status...
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [WARNING] Python bot detected. Stopping...
    taskkill /IM python.exe /F 2>NUL
    timeout /t 2 /nobreak > nul
    echo [OK] Bot stopped
) else (
    echo [OK] No bot running
)
echo.

REM Step 2: Backup
echo [2/6] Creating backup...
if not exist "backup" mkdir backup
set TIMESTAMP=%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%

if exist "src\utils\surge_detector.py" (
    copy "src\utils\surge_detector.py" "backup\surge_detector_%TIMESTAMP%.py" > nul 2>&1
    echo [OK] Backed up surge_detector.py
) else (
    echo [SKIP] src\utils\surge_detector.py not found
)

if exist "src\ai\learning_engine.py" (
    copy "src\ai\learning_engine.py" "backup\learning_engine_%TIMESTAMP%.py" > nul 2>&1
    echo [OK] Backed up learning_engine.py
) else (
    echo [SKIP] src\ai\learning_engine.py not found
)

if exist "src\main.py" (
    copy "src\main.py" "backup\main_%TIMESTAMP%.py" > nul 2>&1
    echo [OK] Backed up main.py
) else (
    echo [SKIP] src\main.py not found
)
echo.

REM Step 3: Download
echo [3/6] Downloading updated files...

curl -L -o "src\utils\surge_detector.py" "https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/utils/surge_detector.py" 2>nul
if exist "src\utils\surge_detector.py" (
    echo [OK] Downloaded surge_detector.py
) else (
    echo [ERROR] Failed to download surge_detector.py
    echo [INFO] Check internet connection
    goto :error
)

curl -L -o "src\ai\learning_engine.py" "https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/ai/learning_engine.py" 2>nul
if exist "src\ai\learning_engine.py" (
    echo [OK] Downloaded learning_engine.py
) else (
    echo [ERROR] Failed to download learning_engine.py
    goto :error
)

curl -L -o "src\main.py" "https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py" 2>nul
if exist "src\main.py" (
    echo [OK] Downloaded main.py
) else (
    echo [ERROR] Failed to download main.py
    goto :error
)

curl -L -o "VERSION.txt" "https://raw.githubusercontent.com/lee-jungkil/Lj/main/VERSION.txt" 2>nul
echo [OK] Downloaded VERSION.txt
echo.

REM Step 4: Clean cache
echo [4/6] Cleaning Python cache...
del /s /q *.pyc > nul 2>&1
for /d /r %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
echo [OK] Cache cleared
echo.

REM Step 5: Verify
echo [5/6] Verifying version...
if exist "VERSION.txt" (
    type "VERSION.txt"
) else (
    echo [WARNING] VERSION.txt not found
)
echo.

REM Step 6: Complete
echo [6/6] Update complete!
echo.
echo ============================================================
echo    Threshold Changes
echo ============================================================
echo.
echo [SURGE DETECTOR]
echo   - 1min change: 1.5 to 1.65 percent
echo   - 5min change: 3.0 to 3.3 percent
echo   - 15min change: 5.0 to 5.5 percent
echo   - Volume ratio: 2.0x to 2.2x
echo   - Min score: 50 to 55
echo.
echo [AI ENGINE]
echo   - Win-rate threshold: 65 to 71.5 percent
echo.
echo [MAIN LOGIC]
echo   - Confidence threshold: 60 to 66 percent
echo.
echo ============================================================
echo    Expected Results
echo ============================================================
echo.
echo POSITIVE:
echo   - Fewer false buy signals
echo   - Higher quality entries
echo   - Better win rate (target 60-65 percent)
echo   - Better profit per trade (0.8-1.2 percent)
echo.
echo TRADE-OFFS:
echo   - 10-20 percent fewer trades (intentional)
echo   - More selective entries
echo.
echo ============================================================
echo    Next Steps
echo ============================================================
echo.
echo 1. Start bot:
echo    python -B -u -m src.main --mode paper
echo.
echo 2. Monitor for 100+ trades before judging
echo.
echo 3. Compare results with previous performance
echo.
echo ============================================================
echo    SUCCESS - Update Complete
echo ============================================================
echo.
pause
exit /b 0

:error
echo.
echo ============================================================
echo    ERROR - Update Failed
echo ============================================================
echo.
echo Attempting to restore from backup...
if exist "backup\surge_detector_%TIMESTAMP%.py" (
    copy "backup\surge_detector_%TIMESTAMP%.py" "src\utils\surge_detector.py" > nul 2>&1
    echo [OK] Restored surge_detector.py
)
if exist "backup\learning_engine_%TIMESTAMP%.py" (
    copy "backup\learning_engine_%TIMESTAMP%.py" "src\ai\learning_engine.py" > nul 2>&1
    echo [OK] Restored learning_engine.py
)
if exist "backup\main_%TIMESTAMP%.py" (
    copy "backup\main_%TIMESTAMP%.py" "src\main.py" > nul 2>&1
    echo [OK] Restored main.py
)
echo.
echo Files restored from backup
echo Please check your internet connection and try again
echo.
pause
exit /b 1
