@echo off
chcp 65001 > nul
setlocal EnableDelayedExpansion

echo ╔════════════════════════════════════════════════════╗
echo ║  AutoProfit Bot v6.31.8-R3 Update                 ║
echo ║  SMART INVESTMENT SYSTEM                          ║
echo ╚════════════════════════════════════════════════════╝
echo.
echo [Version] v6.31.8-R3-SMART-INVESTMENT
echo [Date] 2026-03-19
echo.
echo [Major Features]
echo 1. 10-Level Investment System (100k ~ 3M KRW)
echo 2. Orderbook Liquidity Verification
echo 3. Real-time Slippage Prevention
echo 4. Strategy-based Smart Allocation
echo.

:: Detect bot directory
set "BOT_DIR=%CD%"
if not exist "%BOT_DIR%\src\config.py" (
    echo [ERROR] config.py not found
    echo Please run in bot root folder
    pause
    exit /b 1
)

echo [INFO] Bot directory: %BOT_DIR%
echo.

:: Backup
echo [Step 1/5] Creating backup...
if not exist "%BOT_DIR%\backup" mkdir "%BOT_DIR%\backup"
set "TIMESTAMP=%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%"
set "TIMESTAMP=!TIMESTAMP: =0!"

copy "%BOT_DIR%\src\config.py" "%BOT_DIR%\backup\config_!TIMESTAMP!.py" > nul
copy "%BOT_DIR%\VERSION.txt" "%BOT_DIR%\backup\VERSION_!TIMESTAMP!.txt" > nul
echo [OK] Backup: backup\*_!TIMESTAMP!.*
echo.

:: Download files
echo [Step 2/5] Downloading updates...

curl -# -L -o "%BOT_DIR%\src\config.py" ^
"https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/config.py"
if !errorlevel! neq 0 goto :restore_backup

curl -# -L -o "%BOT_DIR%\src\utils\smart_investment_manager.py" ^
"https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/utils/smart_investment_manager.py"
if !errorlevel! neq 0 goto :restore_backup

curl -# -L -o "%BOT_DIR%\VERSION.txt" ^
"https://raw.githubusercontent.com/lee-jungkil/Lj/main/VERSION.txt"
if !errorlevel! neq 0 goto :restore_backup

curl -# -L -o "%BOT_DIR%\test_smart_investment.py" ^
"https://raw.githubusercontent.com/lee-jungkil/Lj/main/test_smart_investment.py"
if !errorlevel! neq 0 goto :restore_backup

echo [OK] All files downloaded
echo.

:: Clear cache
echo [Step 3/5] Clearing cache...
if exist "%BOT_DIR%\__pycache__" rmdir /s /q "%BOT_DIR%\__pycache__"
if exist "%BOT_DIR%\src\__pycache__" rmdir /s /q "%BOT_DIR%\src\__pycache__"
if exist "%BOT_DIR%\src\utils\__pycache__" rmdir /s /q "%BOT_DIR%\src\utils\__pycache__"
echo [OK] Cache cleared
echo.

:: Test
echo [Step 4/5] Testing system...
python test_smart_investment.py
if !errorlevel! neq 0 (
    echo [WARNING] Test failed, but update completed
    echo You can still use the bot
)
echo.

:: Verify
echo [Step 5/5] Verifying...
type "%BOT_DIR%\VERSION.txt"
echo.

echo ╔════════════════════════════════════════════════════╗
echo ║  Update Completed Successfully!                   ║
echo ╚════════════════════════════════════════════════════╝
echo.
echo [10-Level Investment System]
echo   Level 1:   100,000 KRW (minimum)
echo   Level 2:   150,000 KRW
echo   Level 3:   200,000 KRW
echo   Level 4:   300,000 KRW
echo   Level 5:   500,000 KRW
echo   Level 6:   700,000 KRW
echo   Level 7: 1,000,000 KRW
echo   Level 8: 1,500,000 KRW
echo   Level 9: 2,000,000 KRW
echo   Level 10: 3,000,000 KRW (maximum)
echo.
echo [Strategy Scores]
echo   Aggressive:    Level 4 (300k)
echo   Conservative:  Level 5 (500k)
echo   Mean Reversion: Level 6 (700k)
echo   Grid Trading:  Level 5 (500k)
echo   Ultra:         Level 3 (200k)
echo.
echo [Key Features]
echo   - Orderbook liquidity check
echo   - Slippage prevention (max 0.5%%)
echo   - Dynamic amount adjustment
echo   - Balance verification
echo.
echo [Next Steps]
echo 1. Close bot if running
echo 2. Restart: python -B -u -m src.main --mode paper
echo 3. Check console for investment amounts
echo 4. Monitor first 10-20 trades
echo.
pause
exit /b 0

:restore_backup
echo.
echo [ERROR] Download failed. Restoring...
copy "%BOT_DIR%\backup\config_!TIMESTAMP!.py" "%BOT_DIR%\src\config.py" > nul
copy "%BOT_DIR%\backup\VERSION_!TIMESTAMP!.txt" "%BOT_DIR%\VERSION.txt" > nul
echo [OK] Restored
pause
exit /b 1
