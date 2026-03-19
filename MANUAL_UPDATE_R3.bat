@echo off
chcp 65001 > nul
setlocal EnableDelayedExpansion

echo ======================================================
echo   Manual Update for v6.31.8-R3
echo ======================================================
echo.

set "BOT_DIR=%CD%"

echo Step 1: Backup
if not exist "%BOT_DIR%\backup" mkdir "%BOT_DIR%\backup"
copy "%BOT_DIR%\src\config.py" "%BOT_DIR%\backup\config_manual.py" > nul 2>&1
echo [OK] Backup created
echo.

echo Step 2: Download config.py
curl -L -o "%BOT_DIR%\src\config_new.py" "https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/config.py"
if exist "%BOT_DIR%\src\config_new.py" (
    move /Y "%BOT_DIR%\src\config_new.py" "%BOT_DIR%\src\config.py" > nul
    echo [OK] config.py updated
) else (
    echo [ERROR] Failed to download config.py
)
echo.

echo Step 3: Download smart_investment_manager.py
if not exist "%BOT_DIR%\src\utils" mkdir "%BOT_DIR%\src\utils"
curl -L -o "%BOT_DIR%\src\utils\smart_investment_manager.py" "https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/utils/smart_investment_manager.py"
if exist "%BOT_DIR%\src\utils\smart_investment_manager.py" (
    echo [OK] smart_investment_manager.py downloaded
) else (
    echo [ERROR] Failed to download smart_investment_manager.py
)
echo.

echo Step 4: Download VERSION.txt
curl -L -o "%BOT_DIR%\VERSION_new.txt" "https://raw.githubusercontent.com/lee-jungkil/Lj/main/VERSION.txt"
if exist "%BOT_DIR%\VERSION_new.txt" (
    move /Y "%BOT_DIR%\VERSION_new.txt" "%BOT_DIR%\VERSION.txt" > nul
    echo [OK] VERSION.txt updated
) else (
    echo [ERROR] Failed to download VERSION.txt
)
echo.

echo Step 5: Download test file
curl -L -o "%BOT_DIR%\test_smart_investment.py" "https://raw.githubusercontent.com/lee-jungkil/Lj/main/test_smart_investment.py"
if exist "%BOT_DIR%\test_smart_investment.py" (
    echo [OK] test_smart_investment.py downloaded
) else (
    echo [ERROR] Failed to download test file
)
echo.

echo Step 6: Clear cache
if exist "%BOT_DIR%\__pycache__" rmdir /s /q "%BOT_DIR%\__pycache__" 2>nul
if exist "%BOT_DIR%\src\__pycache__" rmdir /s /q "%BOT_DIR%\src\__pycache__" 2>nul
if exist "%BOT_DIR%\src\utils\__pycache__" rmdir /s /q "%BOT_DIR%\src\utils\__pycache__" 2>nul
echo [OK] Cache cleared
echo.

echo ======================================================
echo   Update Complete - Verify Below
echo ======================================================
echo.
type "%BOT_DIR%\VERSION.txt"
echo.
echo Run test: python test_smart_investment.py
echo.
pause
