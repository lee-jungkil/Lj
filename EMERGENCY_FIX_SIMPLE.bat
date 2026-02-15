@echo off
title EMERGENCY FIX - Stop and Clear Cache
color 0C

echo.
echo ========================================
echo  EMERGENCY FIX
echo  Stop Bot + Clear All Cache
echo ========================================
echo.

cd /d "%~dp0"

echo Step 1: Stop all Python processes...
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM pythonw.exe /T 2>nul
timeout /t 2 /nobreak > nul
echo [OK] Python stopped
echo.

echo Step 2: Delete .pyc files...
del /s /q *.pyc 2>nul
echo [OK] .pyc deleted
echo.

echo Step 3: Delete __pycache__ folders...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
echo [OK] __pycache__ deleted
echo.

echo Step 4: Delete specific cache folders...
if exist "src\__pycache__" rd /s /q "src\__pycache__"
if exist "src\ai\__pycache__" rd /s /q "src\ai\__pycache__"
if exist "src\strategies\__pycache__" rd /s /q "src\strategies\__pycache__"
if exist "src\utils\__pycache__" rd /s /q "src\utils\__pycache__"
echo [OK] All specific caches deleted
echo.

echo Step 5: Verify cache is gone...
if exist "src\__pycache__" (
    echo [ERROR] Cache still exists!
    echo Please run as Administrator!
    pause
    exit /b 1
) else (
    echo [OK] Cache successfully deleted
)
echo.

echo ========================================
echo  FIX COMPLETE
echo ========================================
echo.
echo Cache has been completely cleared.
echo.
echo NOW START THE BOT:
echo   python -B -u -m src.main --mode paper
echo.
echo The -B flag prevents new cache creation.
echo.
echo EXPECTED LOGS AFTER START:
echo   [EXECUTE-SELL] execute_sell called
echo   [EXECUTE-SELL] cleanup start
echo   [EXECUTE-SELL] protector called
echo.
echo If you still don't see these logs,
echo run COMPLETE_REINSTALL.bat
echo.

pause
