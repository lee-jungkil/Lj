@echo off
chcp 65001 >nul
cls
echo ╔═══════════════════════════════════════════════════════════════════════╗
echo ║                                                                       ║
echo ║          Upbit AutoProfit Bot v6.30.6 빠른 업데이트                    ║
echo ║                                                                       ║
echo ╚═══════════════════════════════════════════════════════════════════════╝
echo.

REM 현재 위치 확인
echo 📍 현재 위치: %CD%
echo.

REM update 폴더 확인
if not exist "update" (
    echo ❌ update 폴더를 찾을 수 없습니다!
    echo.
    echo 📖 이 스크립트는 프로젝트 루트 폴더에서 실행해야 합니다.
    echo    예: C:\Users\admin\Downloads\Lj-main\
    echo.
    pause
    exit /b 1
)

echo ✅ update 폴더 확인 완료
echo.

REM update 폴더로 이동
cd update

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   Step 1: GitHub에서 최신 파일 다운로드
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo [1/3] main.py 다운로드 중...
curl -L -s -o main.py "https://raw.githubusercontent.com/lee-jungkil/Lj/main/update/main.py"
if errorlevel 1 (
    echo ❌ 다운로드 실패
    echo.
    echo 📖 해결 방법:
    echo   1. 인터넷 연결 확인
    echo   2. Git Pull: git pull origin main
    echo   3. 수동 다운로드: https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
    echo.
    pause
    exit /b 1
)
echo ✅ main.py 다운로드 완료

echo [2/3] config.py 다운로드 중...
curl -L -s -o config.py "https://raw.githubusercontent.com/lee-jungkil/Lj/main/update/config.py"
echo ✅ config.py 다운로드 완료

echo [3/3] risk_manager.py 다운로드 중...
curl -L -s -o risk_manager.py "https://raw.githubusercontent.com/lee-jungkil/Lj/main/update/risk_manager.py"
echo ✅ risk_manager.py 다운로드 완료

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   Step 2: 다운로드한 파일 적용
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo [1/3] 메인 로직 업데이트...
copy /Y main.py ..\src\main.py >nul 2>&1
if errorlevel 1 (
    echo ❌ main.py 업데이트 실패
    pause
    exit /b 1
)
echo ✅ main.py 업데이트 완료

echo [2/3] 설정 파일 업데이트...
copy /Y config.py ..\src\config.py >nul 2>&1
if errorlevel 1 (
    echo ❌ config.py 업데이트 실패
    pause
    exit /b 1
)
echo ✅ config.py 업데이트 완료

echo [3/3] 리스크 매니저 업데이트...
copy /Y risk_manager.py ..\src\utils\risk_manager.py >nul 2>&1
if errorlevel 1 (
    echo ❌ risk_manager.py 업데이트 실패
    pause
    exit /b 1
)
echo ✅ risk_manager.py 업데이트 완료

REM 상위 폴더로 복귀
cd ..

echo.
echo ╔═══════════════════════════════════════════════════════════════════════╗
echo ║                                                                       ║
echo ║                    ✅ v6.30.6 업데이트 완료!                           ║
echo ║                                                                       ║
echo ╚═══════════════════════════════════════════════════════════════════════╝
echo.
echo 🎉 수정 사항:
echo   - Import 경로 수정 (ModuleNotFoundError 해결)
echo   - 포지션 청산 버그 수정 (7시간 보유 이슈)
echo   - 리스크 평가 시스템 (100점 척도)
echo   - 10가지 청산 조건 통합
echo.
echo 📖 실행 방법:
echo   기존: python src\main.py           (❌ 작동 안 함)
echo   신규: python -m src.main           (✅ 필수)
echo   간편: RUN.bat                      (✅ 권장)
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   다음 단계: RUN.bat 실행 또는 python -m src.main
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
pause
