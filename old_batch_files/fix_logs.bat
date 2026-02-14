@echo off
chcp 65001 > nul
title 거래 로그 복구 도구

echo.
echo ====================================
echo  거래 로그 복구 도구
echo ====================================
echo.
echo 손상된 거래 로그 파일을 복구합니다
echo.

if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo ❌ 가상환경이 없습니다
    pause
    exit /b 1
)

python fix_logs.py

echo.
echo ====================================
echo  복구 완료!
echo ====================================
echo.
echo 이제 봇을 다시 실행하세요:
echo   run_paper.bat     (모의투자)
echo   run_live.bat      (실거래)
echo.
pause
