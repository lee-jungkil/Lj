@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ========================================
echo  Latest Error Log (Last 100 lines)
echo ========================================
echo.

for %%f in (trading_logs\error_*.log) do (
    echo File: %%f
    echo.
    powershell -Command "Get-Content '%%f' -Tail 100 -Encoding UTF8"
)

echo.
echo ========================================
echo  Searching for EXECUTE-SELL...
echo ========================================
echo.

for %%f in (trading_logs\error_*.log) do (
    findstr /C:"EXECUTE-SELL" "%%f" 2>nul
)

echo.
echo ========================================
echo  Log folder location:
echo  %~dp0trading_logs
echo ========================================
echo.
echo To open folder: start trading_logs
echo.
pause
