@echo off
chcp 65001 >nul
echo ================================================
echo   Upbit AutoProfit Bot v6.30.31 실행
echo ================================================
echo.

REM 프로젝트 루트 디렉토리로 이동 (RUN.bat가 있는 위치)
cd /d "%~dp0"

REM 환경 변수 확인
if not exist ".env" (
    echo ❌ .env 파일이 없습니다!
    echo.
    echo 📝 .env 파일을 생성하고 다음 내용을 입력하세요:
    echo.
    echo UPBIT_ACCESS_KEY=your_access_key
    echo UPBIT_SECRET_KEY=your_secret_key
    echo ENABLE_DYNAMIC_STOP_LOSS=true
    echo ENABLE_SCALED_SELL=true
    echo SCALED_SELL_LEVELS=2.0:30,4.0:40,6.0:30
    echo ENABLE_CONDITIONAL_SELL=true
    echo.
    pause
    exit /b 1
)

echo ✅ .env 파일 확인 완료
echo.

REM Python 버전 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python이 설치되어 있지 않거나 PATH에 등록되지 않았습니다!
    echo.
    echo 📖 Python 3.8 이상을 설치하고 PATH에 등록하세요.
    pause
    exit /b 1
)

echo ✅ Python 버전:
python --version
echo.

REM 봇 실행
echo 🚀 봇 실행 중...
echo.
python -m src.main

REM 에러 발생 시
if errorlevel 1 (
    echo.
    echo ❌ 봇 실행 중 에러가 발생했습니다!
    echo.
    echo 📖 해결 방법:
    echo   1. Python 3.8+ 설치 확인
    echo   2. 필요한 패키지 설치: pip install -r requirements.txt
    echo   3. .env 파일 설정 확인
    echo   4. ERROR_VERIFICATION_v6.30.31.md 문서 참고
    echo.
    pause
    exit /b 1
)
