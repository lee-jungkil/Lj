@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ========================================
echo  Clean Update v6.30.70 (No DEBUG)
echo ========================================
echo.
echo This will:
echo   1. Stop Python processes
echo   2. Remove DEBUG logs
echo   3. Clear all cache
echo   4. Download latest code
echo   5. Verify version
echo   6. Restart bot
echo.
echo ========================================
echo.
set /p confirm="Apply clean update? (Y/N): "
if /i not "%confirm%"=="Y" goto cancel

echo.
echo [1/6] Stopping Python processes...
taskkill /F /IM python.exe /T 2>nul
if errorlevel 1 (
    echo No Python process found
) else (
    echo Python stopped
)
timeout /t 2 /nobreak >nul

echo.
echo [2/6] Removing DEBUG logs...
python remove_debug_logs.py
if errorlevel 1 (
    echo Warning: DEBUG removal failed, continuing...
)

echo.
echo [3/6] Clearing cache...
del /s /q *.pyc 2>nul
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
echo Cache cleared

echo.
echo [4/6] Downloading latest code...
curl -s -L "https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py" -o "src\main.py"
if errorlevel 1 (
    echo Warning: Download failed, using local version
)
curl -s -L "https://raw.githubusercontent.com/lee-jungkil/Lj/main/VERSION.txt" -o "VERSION.txt"

echo.
echo [5/6] Verifying version...
type VERSION.txt
echo.

echo.
echo [6/6] Starting bot...
echo.
echo ========================================
echo  Update Complete!
echo ========================================
echo.
echo Bot will start now with clean output
echo (no DEBUG logs).
echo.
pause

start cmd /k "python -B -u -m src.main --mode paper"
goto end

:cancel
echo.
echo Cancelled.
timeout /t 2 /nobreak >nul

:end
