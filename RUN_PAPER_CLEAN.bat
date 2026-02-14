@echo off
chcp 65001 > nul
title Upbit AutoProfit Bot v6.30.23 - Paper Trading (Clean Start)
color 0A

echo.
echo ========================================
echo  Upbit AutoProfit Bot v6.30.23
echo  BATCH-FILE-FIX (창 닫힘 버그 수정)
echo ========================================
echo.
echo [1/5] 현재 디렉토리 확인...
cd /d "%~dp0"
echo [OK] %cd%
echo.

echo [2/5] Python 설치 확인...
python --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python이 설치되지 않았습니다!
    echo https://www.python.org/ 에서 설치하세요
    pause
    exit /b 1
)
python --version
echo.

echo [3/5] Python 캐시 삭제 중... (중요!)
echo 구버전 .pyc 파일 제거...
if exist "src\__pycache__" rmdir /s /q src\__pycache__
if exist "src\strategies\__pycache__" rmdir /s /q src\strategies\__pycache__
if exist "src\utils\__pycache__" rmdir /s /q src\utils\__pycache__
if exist "src\ai\__pycache__" rmdir /s /q src\ai\__pycache__
del /s /q *.pyc 2>nul
echo [OK] 캐시 삭제 완료!
echo.

echo [4/5] .env 파일 확인...
if not exist ".env" (
    echo [WARNING] .env 파일이 없습니다. .env.test를 복사합니다...
    copy .env.test .env
    echo [OK] .env 파일 생성 완료!
)
echo.

echo [5/5] 봇 시작 중...
echo.
echo ========================================
echo  모의투자 모드 (Paper Trading)
echo ========================================
echo.
echo 💡 중지: Ctrl+C
echo 📊 로그 폴더: trading_logs\
echo 🔍 버전: v6.30.23
echo.
echo ⚠️  다음 로그를 확인하세요:
echo     "⚡ 포지션 청산 체크"
echo     "📊 손익률"
echo     "🚨 매도 트리거"
echo.

REM 봇 실행 (캐시 무시 옵션 추가)
python -B -m src.main --mode paper

REM 항상 pause를 실행하여 창이 닫히지 않도록 함
if errorlevel 1 (
    echo.
    echo [ERROR] 봇 실행 중 오류 발생!
    echo trading_logs\ 폴더의 로그를 확인하세요
) else (
    echo.
    echo [INFO] 봇이 정상 종료되었습니다.
)

echo.
pause
