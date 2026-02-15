@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ========================================
echo  Surge Detection Config Editor
echo  v6.30.68
echo ========================================
echo.
echo Current Settings:
echo   - Max Positions: 2
echo   - Daily Limit: Unlimited
echo   - Balance Ratio: 15%%
echo   - Max Amount: 500,000 KRW
echo.
echo ========================================
echo.

:menu
echo Select an option:
echo.
echo [1] Change Max Positions (current: 2)
echo [2] Change Daily Limit (current: Unlimited)
echo [3] Change Balance Ratio (current: 15%%)
echo [4] Change Max Amount (current: 500,000 KRW)
echo [5] View Current Config
echo [6] Reset to Default
echo [7] Save and Restart Bot
echo [0] Exit
echo.
set /p choice="Enter number: "

if "%choice%"=="1" goto max_positions
if "%choice%"=="2" goto daily_limit
if "%choice%"=="3" goto balance_ratio
if "%choice%"=="4" goto max_amount
if "%choice%"=="5" goto view_config
if "%choice%"=="6" goto reset_default
if "%choice%"=="7" goto save_restart
if "%choice%"=="0" goto end
echo Invalid choice!
timeout /t 2 /nobreak >nul
cls
goto menu

:max_positions
cls
echo.
echo ========================================
echo  Change Max Positions
echo ========================================
echo.
echo Current: 2 positions
echo Recommended: 1-5 positions
echo.
set /p new_max="Enter new max positions (1-10): "
if "%new_max%"=="" goto menu

rem Update config.py
powershell -Command "(Get-Content 'src\config.py') -replace \"'max_positions': \d+,\", \"'max_positions': %new_max%,\" | Set-Content 'src\config.py'"
powershell -Command "(Get-Content 'src\config.py') -replace \"'default_positions': \d+,\", \"'default_positions': %new_max%,\" | Set-Content 'src\config.py'"

echo.
echo Max positions updated to %new_max%
echo.
pause
cls
goto menu

:daily_limit
cls
echo.
echo ========================================
echo  Change Daily Limit
echo ========================================
echo.
echo Current: Unlimited (999999)
echo.
echo Options:
echo   [1] Unlimited (999999)
echo   [2] 10 trades
echo   [3] 20 trades
echo   [4] 50 trades
echo   [5] Custom
echo.
set /p limit_choice="Select option: "

if "%limit_choice%"=="1" set new_limit=999999
if "%limit_choice%"=="2" set new_limit=10
if "%limit_choice%"=="3" set new_limit=20
if "%limit_choice%"=="4" set new_limit=50
if "%limit_choice%"=="5" (
    set /p new_limit="Enter custom limit: "
)

if "%new_limit%"=="" goto menu

rem Update config.py
powershell -Command "(Get-Content 'src\config.py') -replace \"CHASE_DAILY_LIMIT = int\(os\.getenv\('CHASE_DAILY_LIMIT', \d+\)\)\", \"CHASE_DAILY_LIMIT = int(os.getenv('CHASE_DAILY_LIMIT', %new_limit%))\" | Set-Content 'src\config.py'"

echo.
echo Daily limit updated to %new_limit%
echo.
pause
cls
goto menu

:balance_ratio
cls
echo.
echo ========================================
echo  Change Balance Ratio
echo ========================================
echo.
echo Current: 15%% of balance
echo.
echo Recommended ratios:
echo   [1] 5%% (Conservative)
echo   [2] 10%% (Moderate)
echo   [3] 15%% (Aggressive)
echo   [4] 20%% (Very Aggressive)
echo   [5] Custom
echo.
set /p ratio_choice="Select option: "

if "%ratio_choice%"=="1" set new_ratio=0.05
if "%ratio_choice%"=="2" set new_ratio=0.10
if "%ratio_choice%"=="3" set new_ratio=0.15
if "%ratio_choice%"=="4" set new_ratio=0.20
if "%ratio_choice%"=="5" (
    set /p ratio_percent="Enter percentage (1-50): "
    powershell -Command "$ratio = [double]%ratio_percent% / 100; Write-Output $ratio" > temp_ratio.txt
    set /p new_ratio=<temp_ratio.txt
    del temp_ratio.txt
)

if "%new_ratio%"=="" goto menu

rem Update config.py
powershell -Command "(Get-Content 'src\config.py') -replace \"'max_investment_ratio': [\d\.]+,\", \"'max_investment_ratio': %new_ratio%,\" | Set-Content 'src\config.py'"

echo.
echo Balance ratio updated to %new_ratio%
echo.
pause
cls
goto menu

:max_amount
cls
echo.
echo ========================================
echo  Change Max Amount
echo ========================================
echo.
echo Current: 500,000 KRW
echo.
echo Recommended amounts:
echo   [1] 100,000 KRW
echo   [2] 300,000 KRW
echo   [3] 500,000 KRW
echo   [4] 1,000,000 KRW
echo   [5] Custom
echo.
set /p amount_choice="Select option: "

if "%amount_choice%"=="1" set new_amount=100000
if "%amount_choice%"=="2" set new_amount=300000
if "%amount_choice%"=="3" set new_amount=500000
if "%amount_choice%"=="4" set new_amount=1000000
if "%amount_choice%"=="5" (
    set /p new_amount="Enter custom amount (KRW): "
)

if "%new_amount%"=="" goto menu

rem Update config.py
powershell -Command "(Get-Content 'src\config.py') -replace \"'max_investment_amount': \d+,\", \"'max_investment_amount': %new_amount%,\" | Set-Content 'src\config.py'"

echo.
echo Max amount updated to %new_amount% KRW
echo.
pause
cls
goto menu

:view_config
cls
echo.
echo ========================================
echo  Current Configuration
echo ========================================
echo.
findstr /C:"'max_positions':" src\config.py
findstr /C:"'default_positions':" src\config.py
findstr /C:"'max_investment_ratio':" src\config.py
findstr /C:"'max_investment_amount':" src\config.py
findstr /C:"CHASE_DAILY_LIMIT" src\config.py
echo.
echo ========================================
pause
cls
goto menu

:reset_default
cls
echo.
echo ========================================
echo  Reset to Default Settings
echo ========================================
echo.
echo This will reset to:
echo   - Max Positions: 2
echo   - Daily Limit: Unlimited (999999)
echo   - Balance Ratio: 15%%
echo   - Max Amount: 500,000 KRW
echo.
set /p confirm="Are you sure? (Y/N): "
if /i not "%confirm%"=="Y" goto menu

rem Reset to default
powershell -Command "(Get-Content 'src\config.py') -replace \"'max_positions': \d+,\", \"'max_positions': 2,\" | Set-Content 'src\config.py'"
powershell -Command "(Get-Content 'src\config.py') -replace \"'default_positions': \d+,\", \"'default_positions': 2,\" | Set-Content 'src\config.py'"
powershell -Command "(Get-Content 'src\config.py') -replace \"'max_investment_ratio': [\d\.]+,\", \"'max_investment_ratio': 0.15,\" | Set-Content 'src\config.py'"
powershell -Command "(Get-Content 'src\config.py') -replace \"'max_investment_amount': \d+,\", \"'max_investment_amount': 500000,\" | Set-Content 'src\config.py'"
powershell -Command "(Get-Content 'src\config.py') -replace \"CHASE_DAILY_LIMIT = int\(os\.getenv\('CHASE_DAILY_LIMIT', \d+\)\)\", \"CHASE_DAILY_LIMIT = int(os.getenv('CHASE_DAILY_LIMIT', 999999))\" | Set-Content 'src\config.py'"

echo.
echo Reset complete!
echo.
pause
cls
goto menu

:save_restart
cls
echo.
echo ========================================
echo  Save and Restart Bot
echo ========================================
echo.
echo This will:
echo   1. Stop all Python processes
echo   2. Clear cache
echo   3. Restart the bot
echo.
set /p confirm="Continue? (Y/N): "
if /i not "%confirm%"=="Y" goto menu

echo.
echo Stopping Python processes...
taskkill /F /IM python.exe /T 2>nul
timeout /t 2 /nobreak >nul

echo Clearing cache...
del /s /q *.pyc 2>nul
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul

echo.
echo Bot will restart now.
echo Press any key to start...
pause >nul

start cmd /k "python -B -u -m src.main --mode paper"
goto end

:end
echo.
echo Goodbye!
timeout /t 2 /nobreak >nul
