@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ========================================
echo  Latest Error Log
echo ========================================
echo.

for %%f in (trading_logs\error_*.log) do (
    echo File: %%f
    echo.
    type "%%f"
)

echo.
echo ========================================
echo  EXECUTE-SELL Logs
echo ========================================
echo.

for %%f in (trading_logs\error_*.log) do (
    findstr /C:"EXECUTE-SELL" "%%f" 2>nul
)

echo.
echo ========================================
echo  Log folder: %~dp0trading_logs
echo ========================================
echo.
pause
