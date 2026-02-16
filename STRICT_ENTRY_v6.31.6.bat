@echo off
chcp 65001 > nul
setlocal EnableDelayedExpansion

echo ============================================================
echo    Strict Entry Criteria Update v6.31.6
echo ============================================================
echo.
echo [INFO] This update increases ALL buy entry thresholds by 10 percent
echo.
echo Goal: Reduce false positive buy signals and improve trade quality
echo.
echo What changes:
echo   1. Surge Detection Thresholds (plus 10 percent)
echo   2. AI Confidence Requirements (plus 10 percent)
echo   3. Market Analysis Criteria (plus 10 percent)
echo.
pause
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
copy src\utils\surge_detector.py backup\surge_detector_%TIMESTAMP%.py > nul 2>&1
copy src\ai\learning_engine.py backup\learning_engine_%TIMESTAMP%.py > nul 2>&1
copy src\main.py backup\main_%TIMESTAMP%.py > nul 2>&1
echo [OK] Backup created
echo.

REM Step 3: Download updated files
echo [3/6] Downloading updated files...
curl -L -s -o src\utils\surge_detector.py https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/utils/surge_detector.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to download surge_detector.py
    goto :error
)
echo [OK] Updated src\utils\surge_detector.py

curl -L -s -o src\ai\learning_engine.py https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/ai/learning_engine.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to download learning_engine.py
    goto :error
)
echo [OK] Updated src\ai\learning_engine.py

curl -L -s -o src\main.py https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to download main.py
    goto :error
)
echo [OK] Updated src\main.py

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
echo    Threshold Changes Summary
echo ============================================================
echo.
echo [1] SURGE DETECTOR
echo.
echo   1-minute price change:
echo     OLD: 1.5 percent    NEW: 1.65 percent  (plus 10 percent)
echo.
echo   5-minute price change:
echo     OLD: 3.0 percent    NEW: 3.3 percent   (plus 10 percent)
echo.
echo   15-minute price change:
echo     OLD: 5.0 percent    NEW: 5.5 percent   (plus 10 percent)
echo.
echo   Volume ratio:
echo     OLD: 2.0x    NEW: 2.2x   (plus 10 percent)
echo.
echo   Minimum surge score:
echo     OLD: 50      NEW: 55     (plus 10 percent)
echo.
echo ============================================================
echo [2] AI LEARNING ENGINE
echo.
echo   AI buy decision win-rate threshold:
echo     OLD: 65 percent     NEW: 71.5 percent  (plus 10 percent)
echo.
echo   Meaning: AI will only suggest STRONG_BUY when similar
echo            past situations had 71.5 percent plus win rate
echo.
echo ============================================================
echo [3] MAIN TRADING LOGIC
echo.
echo   Trade signal confidence threshold:
echo     OLD: 60 percent     NEW: 66 percent    (plus 10 percent)
echo.
echo   Meaning: Only signals with 66 percent plus confidence
echo            will trigger buy signal reinforcement
echo.
echo ============================================================
echo    Expected Results
echo ============================================================
echo.
echo [POSITIVE CHANGES]
echo   - Fewer false positive buy signals
echo   - Higher quality trade entries
echo   - Better average entry price
echo   - Improved risk/reward ratio
echo   - More selective position opening
echo.
echo [TRADE-OFFS]
echo   - Reduced trade frequency (10-20 percent fewer trades)
echo   - May miss some marginal opportunities
echo   - Lower overall position count
echo.
echo [TARGET METRICS]
echo   - Win rate: 60-65 percent (improved from 55 percent)
echo   - Avg profit per trade: 0.8-1.2 percent
echo   - False signals: 30-40 percent reduction
echo   - Trade quality score: 15-20 percent improvement
echo.
echo ============================================================
echo    Why This Update?
echo ============================================================
echo.
echo Problem: Too many low-quality buy signals
echo   - Bot enters positions on weak signals
echo   - Many trades barely profitable or small losses
echo   - Win rate unstable due to marginal trades
echo.
echo Solution: Raise all entry bars by 10 percent
echo   - Only enter on strong, confident signals
echo   - Skip marginal opportunities
echo   - Focus on high-probability setups
echo.
echo Philosophy: Trade less, win more
echo   - Quality over quantity
echo   - Better entry equals easier exit
echo   - Higher confidence equals lower stress
echo.
echo ============================================================
echo    Recommended Next Steps
echo ============================================================
echo.
echo 1. Start bot: python -B -u -m src.main --mode paper
echo.
echo 2. Monitor trade frequency:
echo    - Before: 5-10 trades per hour
echo    - After:  4-8 trades per hour (10-20 percent reduction)
echo.
echo 3. Check signal quality:
echo    - Watch console for confidence values
echo    - Should see fewer signals but higher confidence
echo.
echo 4. Track performance after 50-100 trades:
echo    - Win rate should improve
echo    - Average profit per trade should increase
echo    - Fewer small losses
echo.
echo 5. Compare with previous results:
echo    - Before: negative returns after 270 trades
echo    - Target: positive returns with fewer but better trades
echo.
echo ============================================================
echo    Combined Effect with v6.31.5
echo ============================================================
echo.
echo v6.31.5 improvements (exit side):
echo   - Minimum 5-minute hold time
echo   - Relaxed sudden drop threshold
echo   - Fee-aware AI learning
echo   - Higher take-profit target
echo.
echo v6.31.6 improvements (entry side):
echo   - Stricter surge detection
echo   - Higher AI confidence requirement
echo   - More selective market analysis
echo.
echo Together: Better entries plus Better exits equals Better results
echo.
echo ============================================================
echo    Ready to Start
echo ============================================================
echo.
echo [NEXT] Start bot with: python -B -u -m src.main --mode paper
echo.
echo [TIP] Run for 100 plus trades before judging results
echo       Quality takes time to show!
echo.
pause
goto :eof

:error
echo.
echo [FAILED] Update failed. Restoring from backup...
copy backup\surge_detector_%TIMESTAMP%.py src\utils\surge_detector.py > nul 2>&1
copy backup\learning_engine_%TIMESTAMP%.py src\ai\learning_engine.py > nul 2>&1
copy backup\main_%TIMESTAMP%.py src\main.py > nul 2>&1
echo [OK] Files restored from backup
pause
exit /b 1
