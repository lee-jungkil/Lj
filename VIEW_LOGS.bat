@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ========================================
echo  Upbit Bot - Log Viewer
echo ========================================
echo.

:menu
echo Select log to view:
echo.
echo [1] Today's Trade Log (JSON)
echo [2] Today's Error Log
echo [3] All Log Files (List)
echo [4] Last 50 Lines of Error Log
echo [5] Search for "EXECUTE-SELL" in Error Log
echo [6] Open Log Folder in Explorer
echo [0] Exit
echo.
set /p choice="Enter number: "

if "%choice%"=="1" goto trade_log
if "%choice%"=="2" goto error_log
if "%choice%"=="3" goto list_logs
if "%choice%"=="4" goto tail_error
if "%choice%"=="5" goto search_sell
if "%choice%"=="6" goto open_folder
if "%choice%"=="0" goto end
goto menu

:trade_log
echo.
echo ========================================
echo  Today's Trade Log
echo ========================================
for %%f in (trading_logs\trade_*.json) do (
    echo File: %%f
    type "%%f" 2>nul
)
echo.
echo ========================================
pause
goto menu

:error_log
echo.
echo ========================================
echo  Today's Error Log
echo ========================================
for %%f in (trading_logs\error_*.log) do (
    echo File: %%f
    type "%%f" 2>nul
)
echo.
echo ========================================
pause
goto menu

:list_logs
echo.
echo ========================================
echo  All Log Files
echo ========================================
dir /b trading_logs\*.* 2>nul
echo.
echo ========================================
pause
goto menu

:tail_error
echo.
echo ========================================
echo  Last 50 Lines of Error Log
echo ========================================
for %%f in (trading_logs\error_*.log) do (
    echo File: %%f
    powershell -Command "Get-Content '%%f' -Tail 50 -Encoding UTF8" 2>nul
)
echo.
echo ========================================
pause
goto menu

:search_sell
echo.
echo ========================================
echo  Searching for EXECUTE-SELL logs...
echo ========================================
for %%f in (trading_logs\error_*.log) do (
    echo File: %%f
    findstr /C:"EXECUTE-SELL" "%%f" 2>nul
)
echo.
echo ========================================
pause
goto menu

:open_folder
echo.
echo Opening log folder...
start "" "%~dp0trading_logs"
goto menu

:end
echo.
echo Goodbye!
timeout /t 2 /nobreak >nul
