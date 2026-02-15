@echo off
title Emergency Fix - Force Update and Restart
color 0C

echo ========================================
echo  EMERGENCY FIX
echo  Force code update and cache clear
echo ========================================
echo.

REM Navigate to bot directory
cd /d "%~dp0"
echo Current directory: %cd%
echo.

echo Step 1: Killing ALL Python processes...
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM pythonw.exe /T 2>nul
timeout /t 3 /nobreak > nul
echo [OK] Python stopped
echo.

echo Step 2: Nuclear cache deletion...
echo Deleting .pyc files...
del /s /q *.pyc 2>nul
echo.

echo Deleting __pycache__ folders...
for /d /r . %%d in (__pycache__) do @if exist "%%d" (
    echo Deleting: %%d
    rd /s /q "%%d" 2>nul
)
echo.

echo Specific cache targets...
if exist "src\__pycache__" (
    echo Deleting src\__pycache__
    rd /s /q "src\__pycache__" 2>nul
)
if exist "src\ai\__pycache__" (
    echo Deleting src\ai\__pycache__
    rd /s /q "src\ai\__pycache__" 2>nul
)
if exist "src\strategies\__pycache__" (
    echo Deleting src\strategies\__pycache__
    rd /s /q "src\strategies\__pycache__" 2>nul
)
if exist "src\utils\__pycache__" (
    echo Deleting src\utils\__pycache__
    rd /s /q "src\utils\__pycache__" 2>nul
)
echo [OK] Cache deleted
echo.

echo Step 3: Verify cache deletion...
dir /s /b src\__pycache__ 2>nul
if errorlevel 1 (
    echo [OK] No cache found - GOOD!
) else (
    echo [ERROR] Cache still exists!
    echo Please run as Administrator
    pause
    exit /b 1
)
echo.

echo Step 4: Backup current main.py...
if exist "src\main.py" (
    copy /Y "src\main.py" "src\main.py.old" > nul
    echo [OK] Backup created: src\main.py.old
)
echo.

echo Step 5: Download latest main.py...
echo This will overwrite your current file!
echo.
powershell -Command "try { $ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py' -OutFile 'src\main.py' -UseBasicParsing; Write-Host '[OK] main.py downloaded'; exit 0 } catch { Write-Host '[ERROR] Download failed'; exit 1 }"

if errorlevel 1 (
    echo [ERROR] Download failed!
    echo.
    echo Restoring backup...
    copy /Y "src\main.py.old" "src\main.py" > nul
    echo.
    echo Please download manually:
    echo https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py
    echo.
    pause
    exit /b 1
)
echo.

echo Step 6: Download VERSION.txt...
powershell -Command "try { $ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/lee-jungkil/Lj/main/VERSION.txt' -OutFile 'VERSION.txt' -UseBasicParsing; exit 0 } catch { exit 1 }"
echo.

echo Step 7: Verify code...
findstr /C:"[EXECUTE-SELL]" src\main.py > nul
if errorlevel 1 (
    echo [ERROR] Debug logs not found in code!
    echo Code might be corrupted!
    pause
    exit /b 1
)
echo [OK] Debug logs found
echo.

findstr /C:"order_success = False" src\main.py > nul
if errorlevel 1 (
    echo [WARN] v6.30.64 fix not detected
    echo This might still be old code
) else (
    echo [OK] v6.30.64 fix detected
)
echo.

echo Step 8: Show version...
if exist "VERSION.txt" (
    echo Current version:
    type VERSION.txt
    echo.
) else (
    echo [WARN] VERSION.txt not found
)
echo.

echo Step 9: Verify cache is gone...
dir /s /b *.pyc 2>nul
if errorlevel 1 (
    echo [OK] No .pyc files found
) else (
    echo [WARN] Some .pyc files still exist
)
echo.

echo ========================================
echo  FIX COMPLETE
echo ========================================
echo.
echo Changes applied:
echo   - All Python processes stopped
echo   - All cache deleted
echo   - Latest main.py downloaded
echo   - VERSION.txt updated
echo.
echo IMPORTANT: Start bot with -B flag
echo   python -B -u -m src.main --mode paper
echo.
echo This prevents new cache creation
echo.
set /p START="Start bot now? (Y/N): "
if /i "%START%"=="Y" (
    echo.
    echo Starting bot with -B flag...
    echo Expected logs:
    echo   [EXECUTE-SELL] execute_sell called
    echo   [EXECUTE-SELL] cleanup start
    echo   [EXECUTE-SELL] holding_protector complete
    echo   [EXECUTE-SELL] risk_manager complete
    echo   [EXECUTE-SELL] Position removed
    echo.
    timeout /t 2 /nobreak > nul
    python -B -u -m src.main --mode paper
) else (
    echo.
    echo Start manually with:
    echo   python -B -u -m src.main --mode paper
    echo.
)

pause
exit /b 0
