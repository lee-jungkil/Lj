@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ========================================
echo  Quick Surge Config Update
echo  v6.30.68
echo ========================================
echo.
echo This will apply these settings:
echo   - Max Positions: 2
echo   - Daily Limit: Unlimited
echo   - Balance Ratio: 15%%
echo   - Max Amount: 500,000 KRW
echo.
echo ========================================
echo.
set /p confirm="Apply these settings? (Y/N): "
if /i not "%confirm%"=="Y" goto cancel

echo.
echo Updating configuration...

rem Update max_positions
powershell -Command "(Get-Content 'src\config.py') -replace \"'max_positions': \d+,\", \"'max_positions': 2,\" | Set-Content 'src\config.py'"
powershell -Command "(Get-Content 'src\config.py') -replace \"'default_positions': \d+,\", \"'default_positions': 2,\" | Set-Content 'src\config.py'"
echo   [1/4] Max positions: 2

rem Update daily_limit
powershell -Command "(Get-Content 'src\config.py') -replace \"CHASE_DAILY_LIMIT = int\(os\.getenv\('CHASE_DAILY_LIMIT', \d+\)\)\", \"CHASE_DAILY_LIMIT = int(os.getenv('CHASE_DAILY_LIMIT', 999999))\" | Set-Content 'src\config.py'"
echo   [2/4] Daily limit: Unlimited

rem Update balance_ratio
powershell -Command "(Get-Content 'src\config.py') -replace \"'max_investment_ratio': [\d\.]+,\", \"'max_investment_ratio': 0.15,\" | Set-Content 'src\config.py'"
echo   [3/4] Balance ratio: 15%%

rem Update max_amount
powershell -Command "(Get-Content 'src\config.py') -replace \"'max_investment_amount': \d+,\", \"'max_investment_amount': 500000,\" | Set-Content 'src\config.py'"
echo   [4/4] Max amount: 500,000 KRW

echo.
echo ========================================
echo  Configuration Updated Successfully!
echo ========================================
echo.
echo Next steps:
echo   1. Stop the bot (Ctrl+C)
echo   2. Clear cache: del /s /q *.pyc
echo   3. Restart: python -B -u -m src.main --mode paper
echo.
echo Or run: MINIMAL_UPDATE.bat
echo.
pause
goto end

:cancel
echo.
echo Update cancelled.
timeout /t 2 /nobreak >nul

:end
