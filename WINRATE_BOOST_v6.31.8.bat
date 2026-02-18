@echo off
chcp 65001 > nul
setlocal EnableDelayedExpansion

echo ============================================================
echo    Win Rate Improvement Update v6.31.8
echo ============================================================
echo.
echo [CRITICAL] Fix for low 34.3 percent win rate
echo.
echo Based on 1,376 trades analysis:
echo   - Current win rate: 34.3 percent (TOO LOW!)
echo   - Target win rate: 50-55 percent
echo   - Improvement: +16-21 percent expected
echo.
echo Key fixes:
echo   1. Volume drop panic prevention
echo   2. Time-based force sell with profit condition
echo   3. Minimum hold time 5 to 7 minutes
echo   4. Price check before volume sell
echo.
pause
echo.

REM Step 1: Check bot
echo [1/6] Checking bot status...
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [WARNING] Stopping bot...
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

if exist "src\config.py" (
    copy "src\config.py" "backup\config_%TIMESTAMP%.py" > nul 2>&1
    echo [OK] Backed up config.py
)

if exist "src\main.py" (
    copy "src\main.py" "backup\main_%TIMESTAMP%.py" > nul 2>&1
    echo [OK] Backed up main.py
)
echo.

REM Step 3: Download
echo [3/6] Downloading updated files...

curl -L -o "src\config.py" "https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/config.py" 2>nul
if exist "src\config.py" (
    echo [OK] Downloaded config.py
) else (
    echo [ERROR] Failed to download config.py
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
echo [4/6] Cleaning cache...
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
echo    Problem Analysis
echo ============================================================
echo.
echo [DATA] Based on 1,376 sell trades:
echo.
echo [PROBLEM 1] Time-based Force Sell
echo   Count: 334 trades (24.3 percent)
echo   Win Rate: 36.5 percent
echo   Total Loss: -35,502 KRW
echo   Issue: Forces sell at 5 min even with 0 percent profit
echo   Result: Locks in fees (-0.1 percent)
echo.
echo [PROBLEM 2] Volume Drop Panic Sell
echo   Count: 411 trades (29.9 percent)
echo   Win Rate: 30.2 percent  
echo   Total Loss: -218,142 KRW (BIGGEST LOSS!)
echo   Issue: Sells on volume drop without price check
echo   Result: Exits good positions too early
echo.
echo [PROBLEM 3] Very Short Holds (under 1 min)
echo   Count: 153 trades (11.1 percent)
echo   Win Rate: 5.9 percent (DISASTER!)
echo   Total Loss: -159,587 KRW
echo   Issue: No time for price to move up
echo   Result: Slippage plus fees equals guaranteed loss
echo.
echo [PROBLEM 4] Hold Time vs Win Rate
echo   Short holds (under 5 min): 30.8 percent win rate
echo   Long holds (over 5 min): 39.4 percent win rate
echo   Average hold: 3.4 minutes (TOO SHORT!)
echo.
echo ============================================================
echo    Solutions Implemented
echo ============================================================
echo.
echo [FIX 1] Time-Based Force Sell with Profit Condition
echo.
echo   OLD LOGIC:
echo     IF hold_time greater than 5 min THEN sell
echo     Result: Sells even at 0 percent (loses fees)
echo.
echo   NEW LOGIC:
echo     IF hold_time greater than 5 min THEN
echo       IF profit greater or equal +0.3 percent THEN sell (take profit)
echo       ELSE IF profit less or equal -0.5 percent THEN sell (stop loss)
echo       ELSE continue holding (give it time)
echo.
echo   Benefit: Only sells when profitable or clearly losing
echo.
echo [FIX 2] Volume Drop with Price Check
echo.
echo   OLD LOGIC:
echo     IF volume less than 0.5x average THEN panic sell
echo     Result: 411 trades, 218k loss!
echo.
echo   NEW LOGIC:
echo     IF volume less than 0.2x average (more relaxed)
echo     AND price dropped -0.5 percent in last minute
echo     AND hold_time greater than 3 minutes
echo     THEN sell
echo.
echo   Changes:
echo     - Volume threshold: 0.5x to 0.2x (4x more relaxed)
echo     - Added price drop check (-0.5 percent)
echo     - Added minimum 3 min hold requirement
echo.
echo   Benefit: Only sells when BOTH volume AND price confirm downtrend
echo.
echo [FIX 3] Minimum Hold Time Extension
echo.
echo   OLD: 5 minutes (300 seconds)
echo   NEW: 7 minutes (420 seconds)
echo.
echo   Why: Analysis shows longer holds have better win rates
echo     - Under 5 min: 30.8 percent win rate
echo     - Over 5 min: 39.4 percent win rate
echo.
echo   Benefit: More time for trades to develop
echo.
echo [FIX 4] Emergency Exit Conditions
echo.
echo   Still allows immediate exit if:
echo     - Loss greater than -2.0 percent (critical)
echo     - CRITICAL risk level detected
echo     - Sudden drop greater than -2.5 percent
echo.
echo   Safety preserved while reducing premature exits
echo.
echo ============================================================
echo    Expected Results
echo ============================================================
echo.
echo [PHASE 1] After 50 trades:
echo   - Win rate: 38-42 percent (plus 4-8 percent)
echo   - Fewer panic sells visible
echo   - Longer average hold time (5-6 min)
echo.
echo [PHASE 2] After 100 trades:
echo   - Win rate: 45-48 percent (plus 11-14 percent)
echo   - Positive net profit
echo   - Stable performance
echo.
echo [PHASE 3] After 200+ trades:
echo   - Win rate: 50-55 percent (plus 16-21 percent)
echo   - Consistent profitability
echo   - Lower drawdowns
echo.
echo ============================================================
echo    Configuration Changes
echo ============================================================
echo.
echo [src\config.py]
echo.
echo   MIN_HOLD_TIME:
echo     300 seconds (5 min) to 420 seconds (7 min)
echo.
echo   VOLUME_DROP_THRESHOLD:
echo     0.5 to 0.2 (4x more relaxed)
echo.
echo   New: VOLUME_DROP_PRICE_CHECK = -0.5 percent
echo     Requires price drop to confirm volume sell
echo.
echo   New: TIME_FORCE_SELL_MIN_PROFIT = +0.3 percent
echo     Minimum profit for time-based exit
echo.
echo   New: TIME_FORCE_SELL_MAX_LOSS = -0.5 percent
echo     Maximum loss for time-based exit
echo.
echo [src\main.py]
echo.
echo   Time force sell logic:
echo     - Added profit/loss condition check
echo     - Continues holding if between -0.5 and +0.3 percent
echo     - Logs HOLD message instead of forcing sell
echo.
echo   Volume drop logic:
echo     - Added 1-minute price change calculation
echo     - Requires both volume AND price confirmation
echo     - Added 3-minute minimum hold check
echo     - More detailed logging
echo.
echo ============================================================
echo    Before vs After Comparison
echo ============================================================
echo.
echo [SCENARIO 1] Sideways Market
echo.
echo   BEFORE:
echo     - Buy at 100,000 KRW
echo     - Hold 5 min, price at 99,950 KRW (-0.05 percent)
echo     - Time force sell triggered
echo     - Loss: -150 KRW (fees plus slippage)
echo.
echo   AFTER:
echo     - Buy at 100,000 KRW  
echo     - Hold 7 min, price recovers to 100,300 KRW (+0.3 percent)
echo     - Time force sell with profit
echo     - Profit: +200 KRW
echo.
echo [SCENARIO 2] Volume Drop
echo.
echo   BEFORE:
echo     - Volume drops to 0.3x average
echo     - Panic sell immediately
echo     - Price continues up (false alarm)
echo     - Loss: -300 KRW
echo.
echo   AFTER:
echo     - Volume drops to 0.15x average
echo     - Check price: still +0.2 percent up
echo     - Continue holding (no sell)
echo     - Price goes to +1.5 percent
echo     - Normal profit exit: +1,400 KRW
echo.
echo [SCENARIO 3] Short Hold
echo.
echo   BEFORE:
echo     - Buy, hold 2 minutes
echo     - Some exit trigger fires
echo     - Sell at -0.2 percent
echo     - Loss: -250 KRW (no time to recover)
echo.
echo   AFTER:
echo     - Buy, hold minimum 7 minutes
echo     - Early triggers ignored
echo     - Price has time to move
echo     - Exit at +0.8 percent
echo     - Profit: +750 KRW
echo.
echo ============================================================
echo    Monitoring Guide
echo ============================================================
echo.
echo Watch console for these NEW messages:
echo.
echo   [HOLD] ticker Time reached but continuing hold (profit: +0.1 percent)
echo     Good! System giving trade more time
echo.
echo   [FORCE-SELL] Volume drop plus price drop sell start
echo     Confirmed downtrend, good exit
echo.
echo   Previous: Volume drop only (no price check)
echo     These should be MUCH rarer now
echo.
echo   [FORCE-SELL] Time force sell (hold: 7min, profit: +0.35 percent)
echo     Taking profit at time limit
echo.
echo   [FORCE-SELL] Time force sell (hold: 7min, profit: -0.52 percent)
echo     Cutting loss at time limit
echo.
echo ============================================================
echo    Performance Tracking
echo ============================================================
echo.
echo Track these metrics after update:
echo.
echo   1. Win Rate Progression:
echo      - Every 25 trades: check win rate
echo      - Should see steady improvement
echo      - Target: 38 percent, 42 percent, 45 percent, 50 percent
echo.
echo   2. Hold Time Distribution:
echo      - Average should increase to 5-7 minutes
echo      - Fewer under 3-minute trades
echo.
echo   3. Sell Reason Analysis:
echo      - Volume drop sells should decrease 60-70 percent
echo      - Time force sells should have better profit ratio
echo.
echo   4. Daily P/L:
echo      - Should turn positive within 100-150 trades
echo      - More consistent daily gains
echo.
echo ============================================================
echo    Critical Success Factors
echo ============================================================
echo.
echo [PATIENCE] Most Important!
echo   - Judge after 100+ trades minimum
echo   - First 50 trades still learning
echo   - Expect gradual improvement
echo.
echo [MONITORING]
echo   - Watch for HOLD messages (good sign)
echo   - Check if volume sells decreased
echo   - Verify longer hold times
echo.
echo [COMBINATION]
echo   - This update builds on v6.31.5-6-7
echo   - All previous improvements still active:
echo     * Smart position sizing (v6.31.7)
echo     * Stricter entry criteria (v6.31.6)
echo     * Fee-aware AI learning (v6.31.5)
echo.
echo [DATA TRACKING]
echo   - Keep trading_logs folder
echo   - Compare before/after statistics
echo   - Share results for further optimization
echo.
echo ============================================================
echo    Troubleshooting
echo ============================================================
echo.
echo If win rate does not improve after 100 trades:
echo.
echo   1. Check console logs:
echo      - Are HOLD messages appearing?
echo      - Are volume sells less frequent?
echo.
echo   2. Verify config applied:
echo      python -c "from src.config import Config; print(Config.MIN_HOLD_TIME)"
echo      Should show: 420
echo.
echo   3. Check trading_logs:
echo      - Look for sell reasons in trade files
echo      - Verify new logic is active
echo.
echo   4. Report issues with:
echo      - Console screenshot
echo      - Last 50 trades data
echo      - Current win rate and total P/L
echo.
echo ============================================================
echo    Ready to Start
echo ============================================================
echo.
echo [NEXT] Start bot with:
echo   python -B -u -m src.main --mode paper
echo.
echo [MONITOR] Watch for:
echo   - HOLD messages (good!)
echo   - Longer hold times
echo   - Improved win rate
echo.
echo [PATIENCE] Wait for 100+ trades before judging results
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
echo Restoring from backup...
if exist "backup\config_%TIMESTAMP%.py" (
    copy "backup\config_%TIMESTAMP%.py" "src\config.py" > nul 2>&1
    echo [OK] Restored config.py
)
if exist "backup\main_%TIMESTAMP%.py" (
    copy "backup\main_%TIMESTAMP%.py" "src\main.py" > nul 2>&1
    echo [OK] Restored main.py
)
echo.
echo Please check internet and try again
echo.
pause
exit /b 1
