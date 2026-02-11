@echo off
REM Korean version - CP949 encoding
chcp 949 >nul 2>&1
cls

echo ============================================================
echo  Upbit AutoProfit Bot ¾÷µ¥ÀÌÆ® v6.16-SELLHISTORY
echo ============================================================
echo.
echo ¾÷µ¥ÀÌÆ® ³»¿ë:
echo  [OK] È­¸é ½ºÅ©·Ñ ¿ÏÀü Á¦°Å
echo  [OK] ¼ÕÀÍ µ¿±âÈ­ °³¼±
echo  [OK] ¸®½ºÅ© °ü¸® °­È­ (10%% ¼Õ½Ç ½Ã ÀÚµ¿ Áߴܠ)
echo  [OK] µð¹ö±× Ãâ·Â ¾ïÁ¦
echo  [NEW] ¸Åµµ ±â·Ï ¿µ±¸ ÀúÀå (ÃÖ±Ù 10°Ç À¯Áö)
echo.

REM ÇöÀç µð·ºÅ丮 ÀúÀå
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..

REM ÇÁ·ÎÁ§Æ® ·çÆ®·Î À̵¿
cd /d "%PROJECT_ROOT%"

echo ÇöÀç À§Ä¡: %CD%
echo.

REM µð·ºÅ丮 È®ÀÎ
if not exist "src\utils" (
    echo [ERROR] ÇÁ·ÎÁ§Æ® ±¸Á¶¸¦ Ã£À» ¼ö ¾ø½À´Ï´Ù!
    echo.
    echo ½ÇÇà À§Ä¡: Lj-main\update\UPDATE_KR.bat
    echo ÇöÀç °æ·Î: %CD%
    echo.
    pause
    exit /b 1
)

REM ¹é¾÷ µð·ºÅ丮 »ý¼º
if not exist "backup" mkdir "backup"
set BACKUP_DIR=backup\backup_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set BACKUP_DIR=%BACKUP_DIR: =0%
mkdir "%BACKUP_DIR%" 2>nul

echo [1/4] ±âÁ¸ ÆÄÀÏ ¹é¾÷ Áß...
if exist "src\utils\fixed_screen_display.py" (
    copy "src\utils\fixed_screen_display.py" "%BACKUP_DIR%\fixed_screen_display.py.bak" >nul 2>&1
    if %errorlevel% equ 0 (
        echo  + fixed_screen_display.py ¹é¾÷ ¿Ï·á
    )
)
echo [OK] ¹é¾÷ ¿Ï·á: %BACKUP_DIR%
echo.

echo [2/4] ¾÷µ¥ÀÌÆ® ÆÄÀÏ È®ÀÎ Áß...
if not exist "update\fixed_screen_display.py" (
    echo [ERROR] update\fixed_screen_display.py ÆÄÀÏÀ» Ã£À» ¼ö ¾ø½À´Ï´Ù!
    echo.
    echo update Æú´õ¿¡ ÆÄÀÏÀÌ Àִ°¡ È®ÀÎÇØÁÖº¸¼¼¿ä.
    pause
    exit /b 1
)
echo [OK] ¾÷µ¥ÀÌÆ® ÆÄÀÏ È®ÀÎ ¿Ï·á
echo.

echo [3/4] ÆÄÀÏ ¾÷µ¥ÀÌÆ® Áß...
copy /Y "update\fixed_screen_display.py" "src\utils\fixed_screen_display.py" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] ÆÄÀÏ º¹»ç ½ÇÆÐ!
    echo.
    echo ¹®Á¦ ÇØ°á:
    echo  1. °ü¸®ÀÚ ±Ç±ÕÀ¸·Î ½ÇÇà
    echo  2. Python ÇÁ·Î¼¼½º Á¾·á
    echo  3. ÆÄÀÏ ±Ç¹Ñ È®ÀÎ
    echo.
    pause
    exit /b 1
)
echo  + fixed_screen_display.py ¾÷µ¥ÀÌÆ® ¿Ï·á
echo [OK] ÆÄÀÏ ¾÷µ¥ÀÌÆ® ¿Ï·á
echo.

echo [4/4] ¾÷µ¥ÀÌÆ® È®ÀÎ Áß...
echo.
echo ============================================================
echo  ¾÷µ¥ÀÌÆ® ¼º°ø!
echo ============================================================
echo.
echo º¯°æ »çÇ×:
echo  - v6.16-SELLHISTORY Àû¿ë
echo  - È­¸é ½ºÅ©·Ñ Á¦°Å (¿ÏÀü °íÁ¤)
echo  - ¼ÕÀÍ ÀÚµ¿ °è»ê (initial_capital ±âÁØ)
echo  - µð¹ö±× Ãâ·Â ÃÖ¼ÒÈ­
echo  - ¸®½ºÅ© °ü¸® °­È­ (-10%% ÀÚµ¿ Áߴܠ)
echo  [NEW] ¸Åµµ ±â·Ï: ÃÖ´ë 10°Ç À¯Áö
echo  [NEW] È­¸é¿¡ ÃÖ±Ù 5°Ç Ç¥½Ã
echo  [NEW] ¸Åµµ ±â·ÏÀÌ ¸Å¼ö Æ÷Áö¼Çó·³ Áö¼Ó
echo.
echo ¹é¾÷ À§Ä¡: %BACKUP_DIR%
echo.
echo ´ÙÀ½ ´Ü°è: ºÃ ½ÇÇà
echo   run.bat ¶Ç´Â run_live.bat ¶Ç´Â run_paper.bat
echo.
pause
