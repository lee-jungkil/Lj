@echo off
title Upbit Bot - Diagnostic Check
color 0B

echo.
echo ========================================
echo  DIAGNOSTIC CHECK
echo ========================================
echo.

cd /d "%~dp0"

echo [1/8] Checking VERSION.txt...
if exist "VERSION.txt" (
    type VERSION.txt
    echo.
) else (
    echo [ERROR] VERSION.txt not found!
)

echo.
echo [2/8] Checking Python cache...
if exist "src\__pycache__" (
    echo [WARNING] Cache exists - this is the problem!
    dir /s /b src\__pycache__
) else (
    echo [OK] No cache found
)

echo.
echo [3/8] Checking for [EXECUTE-SELL] in code...
findstr /C:"[EXECUTE-SELL]" src\main.py > nul
if errorlevel 1 (
    echo [ERROR] Debug logs not in code!
    echo This means old code is still present.
) else (
    echo [OK] Debug logs found in code
    findstr /N /C:"[EXECUTE-SELL]" src\main.py | head -n 5
)

echo.
echo [4/8] Checking strategy mapping...
findstr /C:"aggressive_scaling" src\main.py > nul
if errorlevel 1 (
    echo [ERROR] Strategy mapping not found!
) else (
    echo [OK] Strategy mapping found
)

echo.
echo [5/8] Checking execute_sell function...
findstr /C:"def execute_sell" src\main.py > nul
if errorlevel 1 (
    echo [ERROR] execute_sell not found!
) else (
    echo [OK] execute_sell found
    findstr /N /C:"def execute_sell" src\main.py
)

echo.
echo [6/8] Checking running Python processes...
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I "python.exe" > nul
if errorlevel 1 (
    echo [OK] No Python running
) else (
    echo [WARNING] Python is running!
    echo You must restart bot after clearing cache!
    tasklist /FI "IMAGENAME eq python.exe"
)

echo.
echo [7/8] File size check...
for %%F in (src\main.py) do (
    echo src\main.py: %%~zF bytes
)

echo.
echo [8/8] Last modified time...
forfiles /m main.py /s /c "cmd /c echo @path - @fdate @ftime" 2>nul

echo.
echo ========================================
echo  DIAGNOSIS COMPLETE
echo ========================================
echo.

echo NEXT STEPS:
echo.
echo IF you see [WARNING] Cache exists:
echo   1. Run EMERGENCY_CACHE_CLEAR.bat
echo   2. Restart bot
echo.
echo IF you see [ERROR] Debug logs not in code:
echo   1. Run COMPLETE_REINSTALL.bat
echo   2. This will download latest code
echo.
echo IF everything shows [OK]:
echo   - Bot should work
echo   - Check actual bot logs for [EXECUTE-SELL]
echo.

pause
