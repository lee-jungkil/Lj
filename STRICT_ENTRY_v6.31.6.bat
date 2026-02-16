@echo off
chcp 65001 > nul
setlocal EnableDelayedExpansion

echo ============================================================
echo    Strict Entry Criteria Update v6.31.6
echo ============================================================
echo.
echo [INFO] This update increases ALL buy entry thresholds by 10%%
echo.
echo Goal: Reduce false positive buy signals and improve trade quality
echo.
echo What changes:
echo   1. Surge Detection Thresholds (+10%%)
echo   2. AI Confidence Requirements (+10%%)
echo   3. Market Analysis Criteria (+10%%)
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
echo [OK] Backup created: backup\*_%TIMESTAMP%.py
echo.

REM Step 3: Download updated files
echo [3/6] Downloading updated files...
curl -L -s -o src\utils\surge_detector.py https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/utils/surge_detector.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to download src\utils\surge_detector.py
    goto :error
)
echo [OK] Updated src\utils\surge_detector.py

curl -L -s -o src\ai\learning_engine.py https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/ai/learning_engine.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to download src\ai\learning_engine.py
    goto :error
)
echo [OK] Updated src\ai\learning_engine.py

curl -L -s -o src\main.py https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to download src\main.py
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
echo [1] SURGE DETECTOR (src\utils\surge_detector.py)
echo.
echo   1-minute price change:
echo     OLD: >= 1.5%%    NEW: >= 1.65%%  (+10%%)
echo.
echo   5-minute price change:
echo     OLD: >= 3.0%%    NEW: >= 3.3%%   (+10%%)
echo.
echo   15-minute price change:
echo     OLD: >= 5.0%%    NEW: >= 5.5%%   (+10%%)
echo.
echo   Volume ratio (vs average):
echo     OLD: >= 2.0x    NEW: >= 2.2x   (+10%%)
echo.
echo   Minimum surge score:
echo     OLD: >= 50      NEW: >= 55     (+10%%)
echo.
echo ============================================================
echo [2] AI LEARNING ENGINE (src\ai\learning_engine.py)
echo.
echo   AI buy decision win-rate threshold:
echo     OLD: >= 65%%     NEW: >= 71.5%%  (+10%%)
echo.
echo   Meaning: AI will only suggest STRONG_BUY when similar
echo            past situations had 71.5%%+ win rate (stricter)
echo.
echo ============================================================
echo [3] MAIN TRADING LOGIC (src\main.py)
echo.
echo   Trade signal confidence threshold:
echo     OLD: >= 60%%     NEW: >= 66%%    (+10%%)
echo.
echo   Meaning: Only signals with 66%%+ confidence will trigger
echo            buy signal reinforcement (more selective)
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
echo   - Reduced trade frequency (10-20%% fewer trades)
echo   - May miss some marginal opportunities
echo   - Lower overall position count
echo.
echo [TARGET METRICS]
echo   - Win rate: 60-65%% (improved from 55%%)
echo   - Avg profit per trade: +0.8-1.2%% (improved from +0.3-0.5%%)
echo   - False signals: -30-40%% reduction
echo   - Trade quality score: +15-20%% improvement
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
echo Solution: Raise all entry bars by 10%%
echo   - Only enter on strong, confident signals
echo   - Skip marginal opportunities
echo   - Focus on high-probability setups
echo.
echo Philosophy: "Trade less, win more"
echo   - Quality over quantity
echo   - Better entry = easier exit
echo   - Higher confidence = lower stress
echo.
echo ============================================================
echo    Recommended Next Steps
echo ============================================================
echo.
echo 1. Start bot: python -B -u -m src.main --mode paper
echo.
echo 2. Monitor trade frequency:
echo    - Before: ~5-10 trades/hour
echo    - After:  ~4-8 trades/hour (10-20%% reduction)
echo.
echo 3. Check signal quality:
echo    - Watch console for "신뢰도" (confidence) values
echo    - Should see fewer signals but higher confidence
echo.
echo 4. Track performance after 50-100 trades:
echo    - Win rate should improve
echo    - Average profit per trade should increase
echo    - Fewer small losses
echo.
echo 5. Compare with previous results:
echo    - v6.31.5: -127,705 KRW after 270 trades
echo    - v6.31.6: Target positive returns with fewer but better trades
echo.
echo ============================================================
echo    Technical Details
echo ============================================================
echo.
echo Surge Score Formula (OLD):
echo   score = (1m_change/1.5) x 10 + (5m_change/3.0) x 5
echo         + (15m_change/5.0) x 2 + (volume_ratio/2.0) x 20
echo.
echo Surge Score Formula (NEW):
echo   score = (1m_change/1.65) x 10 + (5m_change/3.3) x 5
echo         + (15m_change/5.5) x 2 + (volume_ratio/2.2) x 20
echo.
echo Result: Same inputs produce 10%% lower scores = higher bar
echo.
echo AI Decision Logic (OLD):
echo   IF past_win_rate >= 65%% THEN STRONG_BUY
echo.
echo AI Decision Logic (NEW):
echo   IF past_win_rate >= 71.5%% THEN STRONG_BUY
echo.
echo Result: Need better historical performance to trigger buy
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
echo Together: Better entries + Better exits = Better results
echo.
echo ============================================================
echo    Ready to Start
echo ============================================================
echo.
echo [NEXT] Start bot with: python -B -u -m src.main --mode paper
echo.
echo [TIP] Run for 100+ trades before judging results
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
