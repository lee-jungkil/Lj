@echo off
REM Update Files Auto-Download Script for Windows
REM Downloads ONLY the update folder from GitHub

chcp 65001 >nul 2>&1
cls

echo ============================================================
echo  Upbit AutoProfit Bot - Update Files Downloader
echo ============================================================
echo.
echo This script will download update files from GitHub
echo.

REM Create update directory
if not exist "update" mkdir "update"
cd update

echo [1/7] Downloading UPDATE.bat (required)...
curl -sS -L -o UPDATE.bat https://raw.githubusercontent.com/lee-jungkil/Lj/main/update/UPDATE.bat
if %errorlevel% equ 0 (
    echo  + Downloaded: UPDATE.bat
) else (
    echo  ! Failed: UPDATE.bat
)

echo.
echo [2/7] Downloading fixed_screen_display.py (required)...
curl -sS -L -o fixed_screen_display.py https://raw.githubusercontent.com/lee-jungkil/Lj/main/update/fixed_screen_display.py
if %errorlevel% equ 0 (
    echo  + Downloaded: fixed_screen_display.py
) else (
    echo  ! Failed: fixed_screen_display.py
)

echo.
echo [3/7] Downloading UPDATE_README.md (optional)...
curl -sS -L -o UPDATE_README.md https://raw.githubusercontent.com/lee-jungkil/Lj/main/update/UPDATE_README.md
if %errorlevel% equ 0 (
    echo  + Downloaded: UPDATE_README.md
) else (
    echo  ! Failed: UPDATE_README.md
)

echo.
echo [4/7] Downloading SELL_HISTORY_UPDATE.md (optional)...
curl -sS -L -o SELL_HISTORY_UPDATE.md https://raw.githubusercontent.com/lee-jungkil/Lj/main/update/SELL_HISTORY_UPDATE.md
if %errorlevel% equ 0 (
    echo  + Downloaded: SELL_HISTORY_UPDATE.md
) else (
    echo  ! Failed: SELL_HISTORY_UPDATE.md
)

echo.
echo [5/7] Downloading UPDATE_GUIDE.md (optional)...
curl -sS -L -o UPDATE_GUIDE.md https://raw.githubusercontent.com/lee-jungkil/Lj/main/update/UPDATE_GUIDE.md
if %errorlevel% equ 0 (
    echo  + Downloaded: UPDATE_GUIDE.md
) else (
    echo  ! Failed: UPDATE_GUIDE.md
)

echo.
echo [6/7] Downloading test_sell_history.py (optional)...
curl -sS -L -o test_sell_history.py https://raw.githubusercontent.com/lee-jungkil/Lj/main/update/test_sell_history.py
if %errorlevel% equ 0 (
    echo  + Downloaded: test_sell_history.py
) else (
    echo  ! Failed: test_sell_history.py
)

echo.
echo [7/7] Downloading UPDATE_KR.bat (optional)...
curl -sS -L -o UPDATE_KR.bat https://raw.githubusercontent.com/lee-jungkil/Lj/main/update/UPDATE_KR.bat
if %errorlevel% equ 0 (
    echo  + Downloaded: UPDATE_KR.bat
) else (
    echo  ! Failed: UPDATE_KR.bat
)

echo.
echo ============================================================
echo  Download Complete!
echo ============================================================
echo.
echo Location: %CD%
echo.
echo Next Steps:
echo  1. Move this 'update' folder to your Lj-main project root
echo  2. Navigate to: Lj-main\update\
echo  3. Run: UPDATE.bat
echo.
echo Note: If download failed, you may need to:
echo  - Install curl (Windows 10+ has it built-in)
echo  - Check your internet connection
echo  - Use PowerShell script instead: download_update.ps1
echo.
pause
