@echo off
chcp 65001 > nul
title Learning Data Fix v6.31.3

echo ============================================================
echo Learning Data Fix Update v6.31.3
echo ============================================================
echo.
echo This update fixes the AI learning data query error:
echo Error: "not supported between instances of 'NoneType' and 'int'"
echo.
echo Fixed in: src/strategies/dynamic_stop_loss.py
echo Location: _get_learned_stop_loss() method
echo.
echo What was fixed:
echo - Added type checking for profit_loss_ratio values
echo - Added None value filtering in loss trade calculations
echo - Added empty list validation before max/min operations
echo - Improved error handling for missing data
echo.
echo Result: No more learning data query errors!
echo.
pause

echo.
echo [1/5] Stopping bot...
taskkill /F /IM python.exe /T 2>nul
timeout /t 2 /nobreak > nul

echo.
echo [2/5] Clearing cache...
del /s /q *.pyc 2>nul
for /d /r %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
echo [OK] Cache cleared

echo.
echo [3/5] Downloading fixed code...
curl -L -o dynamic_stop_loss.py.tmp https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/strategies/dynamic_stop_loss.py 2>nul
if %errorlevel% equ 0 (
    move /y dynamic_stop_loss.py.tmp src\strategies\dynamic_stop_loss.py >nul
    echo [OK] dynamic_stop_loss.py updated
) else (
    echo [ERROR] Download failed
    pause
    exit /b 1
)

curl -L -o VERSION.txt https://raw.githubusercontent.com/lee-jungkil/Lj/main/VERSION.txt 2>nul
if %errorlevel% equ 0 (
    echo [OK] VERSION.txt updated
)

echo.
echo [4/5] Version:
type VERSION.txt
echo.

echo.
echo [5/5] Starting bot...
echo.
echo ============================================================
echo Learning data fix applied! Bot starting...
echo ============================================================
echo.
echo The bot will now handle learning data safely:
echo - No more NoneType comparison errors
echo - Empty data lists handled gracefully
echo - Invalid data types filtered out
echo - AI learning continues smoothly
echo.
timeout /t 3 /nobreak > nul

python -B -u -m src.main --mode paper
