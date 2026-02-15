@echo off
chcp 65001 > nul
title Upbit Bot - Debug Mode v6.30.66
color 0E

echo ========================================
echo  DEBUG MODE - Detailed Logging
echo ========================================
echo.

cd /d "%~dp0"

echo Starting bot with maximum logging...
echo Watch for [EXECUTE-SELL] messages!
echo.
echo Press Ctrl+C to stop
echo.

REM 환경변수 설정으로 더 상세한 로그
set PYTHONUNBUFFERED=1
set PYTHONDONTWRITEBYTECODE=1

REM 디버그 모드로 시작
python -B -u -m src.main --mode paper --log-level DEBUG 2>&1 | findstr /V /C:"INFO:urllib3" /C:"DEBUG:urllib3"

pause
