@echo off
chcp 65001 > nul
:: Upbit AutoProfit Bot - Windows 빠른 실행 스크립트

echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║           🚀 Upbit AutoProfit Bot 🚀                        ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: Python 확인
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python이 설치되지 않았습니다!
    echo    https://www.python.org/downloads/ 에서 다운로드하세요
    pause
    exit /b 1
)

echo ✅ Python 발견
python --version

:: 가상환경 확인
if not exist "venv\" (
    echo 📦 가상환경 생성 중...
    python -m venv venv
    echo ✅ 가상환경 생성 완료!
)

:: 가상환경 활성화
echo 🔧 가상환경 활성화 중...
call venv\Scripts\activate.bat

:: 의존성 설치
if not exist "venv\Lib\site-packages\pyupbit\" (
    echo 📦 의존성 패키지 설치 중...
    pip install -q -r requirements.txt
    echo ✅ 의존성 설치 완료!
)

:: .env 파일 확인
if not exist ".env" (
    echo ⚠️  .env 파일이 없습니다!
    echo    .env.example을 복사하여 API 키를 입력하세요.
    copy .env.example .env
    echo ✅ .env 파일 생성 완료!
    echo.
    echo ⚠️  .env 파일을 편집하여 Upbit API 키를 입력해주세요!
    echo.
    set /p api_confirm="API 키를 입력하셨나요? (y/N): "
    if /i not "%api_confirm%"=="y" (
        echo API 키를 먼저 입력해주세요!
        pause
        exit /b 1
    )
)

:: 모드 선택
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   거래 모드를 선택하세요:
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   1) backtest  - 백테스트 (실제 거래 없음, API 키 불필요)
echo   2) paper     - 모의투자 (가상 거래)
echo   3) live      - 실거래 (⚠️  실제 자금 사용!)
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

set /p mode_choice="선택 (1-3): "

if "%mode_choice%"=="1" (
    set MODE=backtest
) else if "%mode_choice%"=="2" (
    set MODE=paper
) else if "%mode_choice%"=="3" (
    set MODE=live
    echo.
    echo ╔══════════════════════════════════════════════════════════════╗
    echo ║                                                              ║
    echo ║                  ⚠️  경고: 실거래 모드 ⚠️                   ║
    echo ║                                                              ║
    echo ║  실제 자금이 사용되며 손실이 발생할 수 있습니다!             ║
    echo ║                                                              ║
    echo ╚══════════════════════════════════════════════════════════════╝
    echo.
    set /p confirm="정말 실거래를 진행하시겠습니까? (yes/no): "
    if not "!confirm!"=="yes" (
        echo 취소되었습니다.
        pause
        exit /b 0
    )
) else (
    echo 잘못된 선택입니다. 백테스트 모드로 실행합니다.
    set MODE=backtest
)

:: 봇 실행
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 🚀 봇 시작 중... (모드: %MODE%)
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 💡 중지하려면 Ctrl+C를 누르세요
echo.

python src\main.py --mode %MODE%

pause
