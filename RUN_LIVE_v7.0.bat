@echo off
echo ================================================================
echo  Profit Bot v7.0 - LIVE TRADING MODE
echo ================================================================
echo.
echo *** WARNING *** WARNING *** WARNING ***
echo.
echo [LIVE MODE CAUTION]
echo - Uses REAL MONEY!
echo - API keys must be set (src\config.py)
echo - Start with small amount (100-500 USD recommended)
echo - Requires 24/7 monitoring
echo.
echo Press any key to continue or close window to cancel...
echo.
pause
echo.
echo ----------------------------------------------------------------
echo Starting LIVE trading...
echo ----------------------------------------------------------------
echo.

if not exist "src\config.py" (
    echo [ERROR] src\config.py file not found!
    echo.
    pause
    exit /b 1
)

python profit_bot_v7.py --mode live

echo.
echo ----------------------------------------------------------------
echo Bot stopped.
echo ----------------------------------------------------------------
echo.
pause
