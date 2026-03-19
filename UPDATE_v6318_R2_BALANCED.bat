@echo off
chcp 65001 > nul
setlocal EnableDelayedExpansion

echo ========================================
echo    AutoProfit Bot v6.31.8-R2 Update
echo    BALANCED STRATEGY OPTIMIZATION
echo ========================================
echo.
echo [Version] v6.31.8-R2-BALANCED
echo [Date] 2026-03-19
echo.
echo [Major Changes]
echo 1. Aggressive Scalping: Entry +30%% stricter
echo 2. Mean Reversion: Entry -20%% easier
echo 3. Grid Trading: Entry -20%% easier  
echo 4. Ultra Scalping: Entry -27%% easier
echo.

:: Detect bot directory
set "BOT_DIR=%CD%"
if not exist "%BOT_DIR%\src\config.py" (
    echo [ERROR] config.py not found in current directory
    echo Please run this script in bot root folder
    pause
    exit /b 1
)

echo [INFO] Bot directory: %BOT_DIR%
echo.

:: Backup original files
echo [Step 1/4] Creating backup...
if not exist "%BOT_DIR%\backup" mkdir "%BOT_DIR%\backup"
set "TIMESTAMP=%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%"
set "TIMESTAMP=!TIMESTAMP: =0!"

copy "%BOT_DIR%\src\config.py" "%BOT_DIR%\backup\config_!TIMESTAMP!.py" > nul
copy "%BOT_DIR%\src\utils\surge_detector.py" "%BOT_DIR%\backup\surge_detector_!TIMESTAMP!.py" > nul
copy "%BOT_DIR%\VERSION.txt" "%BOT_DIR%\backup\VERSION_!TIMESTAMP!.txt" > nul
echo [OK] Backup completed: backup\*_!TIMESTAMP!.py
echo.

:: Download updated files
echo [Step 2/4] Downloading updates...

curl -# -L -o "%BOT_DIR%\src\config.py" ^
"https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/config.py"
if !errorlevel! neq 0 (
    echo [ERROR] Failed to download config.py
    goto :restore_backup
)

curl -# -L -o "%BOT_DIR%\src\utils\surge_detector.py" ^
"https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/utils/surge_detector.py"
if !errorlevel! neq 0 (
    echo [ERROR] Failed to download surge_detector.py
    goto :restore_backup
)

curl -# -L -o "%BOT_DIR%\VERSION.txt" ^
"https://raw.githubusercontent.com/lee-jungkil/Lj/main/VERSION.txt"
if !errorlevel! neq 0 (
    echo [ERROR] Failed to download VERSION.txt
    goto :restore_backup
)

echo [OK] All files downloaded
echo.

:: Clear Python cache
echo [Step 3/4] Clearing Python cache...
if exist "%BOT_DIR%\__pycache__" (
    rmdir /s /q "%BOT_DIR%\__pycache__"
)
if exist "%BOT_DIR%\src\__pycache__" (
    rmdir /s /q "%BOT_DIR%\src\__pycache__"
)
if exist "%BOT_DIR%\src\utils\__pycache__" (
    rmdir /s /q "%BOT_DIR%\src\utils\__pycache__"
)
echo [OK] Cache cleared
echo.

:: Verify version
echo [Step 4/4] Verifying update...
type "%BOT_DIR%\VERSION.txt"
echo.

echo ========================================
echo   Update Completed Successfully!
echo ========================================
echo.
echo [Changes Summary]
echo - Aggressive Scalping: RSI 35-65 -^> 45-55, Volume 1.3x -^> 1.7x, Price 0.8%% -^> 1.2%%
echo - Mean Reversion: Deviation 2.5%% -^> 2.0%%
echo - Grid Trading: Max Volatility 3.5%% -^> 3.0%%
echo - Ultra Scalping: 1m 1.65%% -^> 1.2%%, 5m 3.3%% -^> 2.5%%, 15m 5.5%% -^> 4.0%%
echo - Ultra Scalping: Volume 2.2x -^> 1.8x, Min Score 55 -^> 45
echo.
echo [Expected Results]
echo - Aggressive: Fewer entries, higher win rate (40-45%%)
echo - Mean/Grid: More entries, diversified risk
echo - Ultra: More frequent scalping (2-5 signals/day -^> 5-10/day)
echo - Overall Win Rate: 42-50%% target
echo.
echo [Next Steps]
echo 1. Close bot if running
echo 2. Restart: python -B -u -m src.main --mode paper
echo 3. Monitor 50-100 trades
echo 4. Check strategy distribution and win rates
echo.
pause
exit /b 0

:restore_backup
echo.
echo [ERROR] Download failed. Restoring backup...
copy "%BOT_DIR%\backup\config_!TIMESTAMP!.py" "%BOT_DIR%\src\config.py" > nul
copy "%BOT_DIR%\backup\surge_detector_!TIMESTAMP!.py" "%BOT_DIR%\src\utils\surge_detector.py" > nul
copy "%BOT_DIR%\backup\VERSION_!TIMESTAMP!.txt" "%BOT_DIR%\VERSION.txt" > nul
echo [OK] Backup restored
pause
exit /b 1
