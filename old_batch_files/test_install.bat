@echo off
chcp 65001 > nul
title Package Installation Test
color 0B

echo.
echo ========================================
echo  Testing Package Installation
echo ========================================
echo.

cd /d "%~dp0"

if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo [ERROR] Virtual environment not found!
    echo Please run setup.bat first.
    pause
    exit /b 1
)

echo Testing Python packages...
echo.

python -c "import sys; print('[OK] Python version:', sys.version)"
echo.

python -c "import pyupbit; print('[OK] pyupbit installed')" 2>nul || echo [ERROR] pyupbit not installed
python -c "import pandas; print('[OK] pandas installed')" 2>nul || echo [ERROR] pandas not installed
python -c "import numpy; print('[OK] numpy installed')" 2>nul || echo [ERROR] numpy not installed
python -c "import requests; print('[OK] requests installed')" 2>nul || echo [ERROR] requests not installed
python -c "import dotenv; print('[OK] python-dotenv installed')" 2>nul || echo [ERROR] python-dotenv not installed
python -c "import schedule; print('[OK] schedule installed')" 2>nul || echo [ERROR] schedule not installed
python -c "import colorlog; print('[OK] colorlog installed')" 2>nul || echo [ERROR] colorlog not installed

echo.
echo ========================================
echo  Test Complete
echo ========================================
echo.
echo If all packages show [OK], you are ready to run the bot!
echo.
pause
