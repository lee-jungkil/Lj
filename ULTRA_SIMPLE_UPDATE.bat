@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ========================================
echo  Upbit Bot Update v6.30.67
echo ========================================
echo.

echo [1/4] Stopping Python...
taskkill /F /IM python.exe /T 2>nul
if errorlevel 1 (
    echo No Python process found - OK
) else (
    echo Python stopped
)
timeout /t 2 /nobreak >nul

echo.
echo [2/4] Clearing cache...
del /s /q *.pyc 2>nul
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
echo Cache cleared

echo.
echo [3/4] Downloading updates...
echo Downloading main.py...
curl -s -L "https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py" -o "src\main.py"
if errorlevel 1 (
    echo ERROR: Failed to download main.py
    goto error
)
echo main.py downloaded

echo Downloading VERSION.txt...
curl -s -L "https://raw.githubusercontent.com/lee-jungkil/Lj/main/VERSION.txt" -o "VERSION.txt"
if errorlevel 1 (
    echo ERROR: Failed to download VERSION.txt
    goto error
)
echo VERSION.txt downloaded

echo.
echo [4/4] Verifying...
if not exist "src\main.py" (
    echo ERROR: src\main.py not found
    goto error
)
if not exist "VERSION.txt" (
    echo ERROR: VERSION.txt not found
    goto error
)

echo.
echo ========================================
echo  Update completed successfully!
echo ========================================
echo.
echo Current version:
type VERSION.txt
echo.
echo.
echo To start bot, run:
echo   python -B -u -m src.main --mode paper
echo.
echo ========================================
pause
exit /b 0

:error
echo.
echo ========================================
echo  Update FAILED
echo ========================================
echo.
echo Manual update steps:
echo 1. Go to: https://github.com/lee-jungkil/Lj
echo 2. Click "Code" - "Download ZIP"
echo 3. Extract and replace files
echo.
pause
exit /b 1
