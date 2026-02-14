@echo off
chcp 65001 > nul
title Upbit AutoProfit Bot v6.30.22 - Live Trading (Clean Start)
color 0C

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║                  ⚠️  경고: 실거래 모드 ⚠️                   ║
echo ║                                                              ║
echo ║  실제 자금이 사용되며 손실이 발생할 수 있습니다!             ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
set /p confirm="정말 실거래를 진행하시겠습니까? (yes 입력): "
if not "%confirm%"=="yes" (
    echo 취소되었습니다.
    pause
    exit /b 0
)

echo.
echo ========================================
echo  Upbit AutoProfit Bot v6.30.22
echo  PROFIT-SELL-VERIFICATION-COMPLETE
echo ========================================
echo.
echo [1/6] 현재 디렉토리 확인...
cd /d "%~dp0"
echo [OK] %cd%
echo.

echo [2/6] Python 설치 확인...
python --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python이 설치되지 않았습니다!
    pause
    exit /b 1
)
python --version
echo.

echo [3/6] Python 캐시 삭제 중... (중요!)
if exist "src\__pycache__" rmdir /s /q src\__pycache__
if exist "src\strategies\__pycache__" rmdir /s /q src\strategies\__pycache__
if exist "src\utils\__pycache__" rmdir /s /q src\utils\__pycache__
if exist "src\ai\__pycache__" rmdir /s /q src\ai\__pycache__
del /s /q *.pyc 2>nul
echo [OK] 캐시 삭제 완료!
echo.

echo [4/6] .env 파일 확인...
if not exist ".env" (
    echo [ERROR] .env 파일이 없습니다!
    echo .env.example을 복사하여 API 키를 입력하세요
    pause
    exit /b 1
)
echo [OK] .env 파일 존재
echo.

echo [5/6] Upbit API 키 확인...
findstr /C:"UPBIT_ACCESS_KEY=" .env | findstr /V /C:"UPBIT_ACCESS_KEY=$" | findstr /V /C:"UPBIT_ACCESS_KEY= " > nul
if errorlevel 1 (
    echo [ERROR] Upbit API 키가 설정되지 않았습니다!
    echo .env 파일에서 UPBIT_ACCESS_KEY와 UPBIT_SECRET_KEY를 설정하세요
    pause
    exit /b 1
)
echo [OK] API 키 설정 확인
echo.

echo [6/6] 봇 시작 중...
echo.
echo ========================================
echo  실거래 모드 (Live Trading)
echo ========================================
echo.
echo 💡 중지: Ctrl+C
echo 📊 로그 폴더: trading_logs\
echo 🔍 버전: v6.30.22
echo.
echo ✅ 익절/손절 매도 시스템 활성화
echo ✅ 포지션 청산 체크: 매 3초
echo.

REM 봇 실행 (캐시 무시 옵션 추가)
python -B -m src.main --mode live

if errorlevel 1 (
    echo.
    echo [ERROR] 봇 실행 중 오류 발생!
    echo trading_logs\ 폴더의 로그를 확인하세요
    pause
    exit /b 1
)

pause
