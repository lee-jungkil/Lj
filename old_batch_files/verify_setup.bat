@echo off
chcp 65001 > nul
title 동적 코인 시스템 검증

echo.
echo ====================================
echo  동적 코인 선정 시스템 검증
echo ====================================
echo.

if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo ❌ 가상환경이 없습니다
    echo    setup.bat을 먼저 실행하세요
    pause
    exit /b 1
)

echo [1/2] 환경변수 및 설정 확인 중...
python verify_dynamic.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ 검증 실패
    pause
    exit /b 1
)

echo.
echo [2/2] 설정 완료!
echo.
echo ====================================
echo  ✅ 검증 완료!
echo ====================================
echo.
echo 이제 봇을 실행하세요:
echo   run_paper.bat     (모의투자)
echo   run_live.bat      (실거래)
echo.
pause
