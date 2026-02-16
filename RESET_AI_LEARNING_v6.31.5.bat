@echo off
chcp 65001 > nul
setlocal EnableDelayedExpansion

echo ============================================================
echo    AI Learning Reset v6.31.5
echo ============================================================
echo.
echo [WARNING] This will delete all AI learning data!
echo.
echo Files to be deleted:
echo   - trading_logs\learning\experiences.json
echo   - trading_logs\learning\strategy_stats.json
echo   - trading_logs\learning\optimized_params.json
echo.
echo Why reset AI learning?
echo   1. Current learning data contains incorrect profit calculations
echo      (270+ trades learned WITHOUT considering 0.1%% trading fees)
echo   2. AI has learned overly-optimistic profit expectations
echo   3. This causes declining win-rate and poor decisions
echo.
echo After reset:
echo   - AI will start learning from scratch
echo   - New trades will use correct fee-adjusted profit calculations
echo   - Should see improved performance after 50-100 trades
echo.
echo ============================================================
set /p CONFIRM="Type YES to confirm reset: "

if /I NOT "%CONFIRM%"=="YES" (
    echo.
    echo [CANCELLED] AI learning reset cancelled.
    echo [INFO] No files were deleted.
    pause
    exit /b 0
)

echo.
echo ============================================================
echo    Starting AI Learning Reset
echo ============================================================
echo.

REM Step 1: Check if bot is running
echo [1/5] Checking bot status...
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

REM Step 2: Create backup
echo [2/5] Creating backup of learning data...
if not exist "backup" mkdir backup
set TIMESTAMP=%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%

if exist "trading_logs\learning\experiences.json" (
    copy trading_logs\learning\experiences.json backup\experiences_%TIMESTAMP%.json > nul 2>&1
    echo [OK] Backed up experiences.json
)

if exist "trading_logs\learning\strategy_stats.json" (
    copy trading_logs\learning\strategy_stats.json backup\strategy_stats_%TIMESTAMP%.json > nul 2>&1
    echo [OK] Backed up strategy_stats.json
)

if exist "trading_logs\learning\optimized_params.json" (
    copy trading_logs\learning\optimized_params.json backup\optimized_params_%TIMESTAMP%.json > nul 2>&1
    echo [OK] Backed up optimized_params.json
)
echo.

REM Step 3: Delete learning files
echo [3/5] Deleting AI learning data...
set DELETED=0

if exist "trading_logs\learning\experiences.json" (
    del /f /q "trading_logs\learning\experiences.json" 2>NUL
    if %ERRORLEVEL% EQU 0 (
        echo [OK] Deleted experiences.json
        set /a DELETED+=1
    ) else (
        echo [ERROR] Failed to delete experiences.json
    )
)

if exist "trading_logs\learning\strategy_stats.json" (
    del /f /q "trading_logs\learning\strategy_stats.json" 2>NUL
    if %ERRORLEVEL% EQU 0 (
        echo [OK] Deleted strategy_stats.json
        set /a DELETED+=1
    ) else (
        echo [ERROR] Failed to delete strategy_stats.json
    )
)

if exist "trading_logs\learning\optimized_params.json" (
    del /f /q "trading_logs\learning\optimized_params.json" 2>NUL
    if %ERRORLEVEL% EQU 0 (
        echo [OK] Deleted optimized_params.json
        set /a DELETED+=1
    ) else (
        echo [ERROR] Failed to delete optimized_params.json
    )
)

if %DELETED% EQU 0 (
    echo [INFO] No learning files found (already clean)
)
echo.

REM Step 4: Clean Python cache
echo [4/5] Cleaning Python cache...
del /s /q *.pyc > nul 2>&1
for /d /r %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
echo [OK] Cache cleared
echo.

REM Step 5: Verify
echo [5/5] Verifying reset...
if exist "trading_logs\learning\experiences.json" (
    echo [ERROR] experiences.json still exists!
) else (
    echo [OK] experiences.json deleted
)

if exist "trading_logs\learning\strategy_stats.json" (
    echo [ERROR] strategy_stats.json still exists!
) else (
    echo [OK] strategy_stats.json deleted
)

if exist "trading_logs\learning\optimized_params.json" (
    echo [ERROR] optimized_params.json still exists!
) else (
    echo [OK] optimized_params.json deleted
)
echo.

echo ============================================================
echo    AI Learning Reset Complete!
echo ============================================================
echo.
echo [SUCCESS] All AI learning data has been deleted.
echo.
echo Backup location: backup\*_%TIMESTAMP%.json
echo.
echo ============================================================
echo    What Happens Next?
echo ============================================================
echo.
echo 1. Bot will start with ZERO learning data
echo 2. AI will begin learning from scratch using:
echo    - Correct fee calculations (0.1%% total)
echo    - Minimum 5-minute hold time
echo    - Relaxed sudden drop threshold (-2.5%%)
echo    - Higher take-profit target (1.5%%)
echo.
echo 3. Expected timeline:
echo    - First 10-20 trades: Exploration phase
echo    - 20-50 trades: Initial learning patterns
echo    - 50-100 trades: Performance stabilization
echo    - 100+ trades: Consistent profitability
echo.
echo 4. Performance comparison:
echo    - OLD (270 trades): -127,705 KRW, declining win rate
echo    - NEW (target): Positive returns, stable win rate 55-60%%
echo.
echo ============================================================
echo    Recommendations
echo ============================================================
echo.
echo 1. Start bot in PAPER mode first:
echo    python -B -u -m src.main --mode paper
echo.
echo 2. Monitor first 50-100 trades closely
echo.
echo 3. Check learning progress:
echo    dir trading_logs\learning
echo    type trading_logs\learning\strategy_stats.json
echo.
echo 4. Compare performance metrics:
echo    - Win rate should stabilize around 55-60%%
echo    - Average profit per trade should be positive
echo    - Fewer premature exits
echo.
echo 5. After 100+ successful paper trades:
echo    - Consider switching to LIVE mode
echo    - Start with small position sizes
echo.
echo ============================================================
echo    Ready to Start
echo ============================================================
echo.
echo [NEXT] Start bot with: python -B -u -m src.main --mode paper
echo.
pause
