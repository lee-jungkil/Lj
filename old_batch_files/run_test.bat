@echo off
chcp 65001 > nul
title Upbit AutoProfit Bot v5.2 - Test Mode (Active Trading)
color 0D

echo.
echo ========================================
echo  Upbit AutoProfit Bot v5.2
echo  TEST MODE - Active Trading
echo ========================================
echo.
echo [NOTICE] 진입 조건 완화 모드
echo   - 더 자주 거래 발생
echo   - AI 학습 데이터 빠르게 수집
echo   - 최대 5개 포지션
echo.

cd /d "%~dp0"

REM 테스트 환경 설정 복사
if exist ".env.test" (
    copy /Y .env.test .env > nul
    echo [OK] 테스트 설정 활성화
) else (
    echo [ERROR] .env.test 파일이 없습니다!
    pause
    exit /b 1
)

echo.
echo [INFO] Starting test mode...
echo.

REM 가상환경 활성화
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM 봇 실행
python src/main.py --mode paper

pause
