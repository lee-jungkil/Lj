@echo off
chcp 65001 >nul
cls
echo ╔═══════════════════════════════════════════════════════════════════════╗
echo ║                                                                       ║
echo ║          Upbit AutoProfit Bot v6.30.30 전체 다운로드                   ║
echo ║                                                                       ║
echo ╚═══════════════════════════════════════════════════════════════════════╝
echo.

REM 현재 위치 확인
echo 📍 현재 위치: %CD%
echo.

REM src 폴더 확인 및 생성
if not exist "src" (
    echo 📁 src 폴더 생성 중...
    mkdir src
    echo ✅ src 폴더 생성 완료
)

if not exist "src\utils" (
    echo 📁 src\utils 폴더 생성 중...
    mkdir src\utils
    echo ✅ src\utils 폴더 생성 완료
)

REM update 폴더 확인 및 생성
if not exist "update" (
    echo 📁 update 폴더 생성 중...
    mkdir update
    echo ✅ update 폴더 생성 완료
)

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   Step 1: 핵심 파일 다운로드 (src 폴더)
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo [1/3] main.py 다운로드 중...
curl -L -s -o src\main.py "https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py"
if errorlevel 1 (
    echo ❌ main.py 다운로드 실패
    goto ERROR
)
echo ✅ main.py 다운로드 완료

echo [2/3] config.py 다운로드 중...
curl -L -s -o src\config.py "https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/config.py"
if errorlevel 1 (
    echo ❌ config.py 다운로드 실패
    goto ERROR
)
echo ✅ config.py 다운로드 완료

echo [3/3] risk_manager.py 다운로드 중...
curl -L -s -o src\utils\risk_manager.py "https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/utils/risk_manager.py"
if errorlevel 1 (
    echo ❌ risk_manager.py 다운로드 실패
    goto ERROR
)
echo ✅ risk_manager.py 다운로드 완료

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   Step 2: 백업 파일 다운로드 (update 폴더)
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo [1/3] update/main.py 다운로드 중...
curl -L -s -o update\main.py "https://raw.githubusercontent.com/lee-jungkil/Lj/main/update/main.py"
if errorlevel 1 (
    echo ❌ update/main.py 다운로드 실패
    goto ERROR
)
echo ✅ update/main.py 다운로드 완료

echo [2/3] update/config.py 다운로드 중...
curl -L -s -o update\config.py "https://raw.githubusercontent.com/lee-jungkil/Lj/main/update/config.py"
if errorlevel 1 (
    echo ❌ update/config.py 다운로드 실패
    goto ERROR
)
echo ✅ update/config.py 다운로드 완료

echo [3/3] update/risk_manager.py 다운로드 중...
curl -L -s -o update\risk_manager.py "https://raw.githubusercontent.com/lee-jungkil/Lj/main/update/risk_manager.py"
if errorlevel 1 (
    echo ❌ update/risk_manager.py 다운로드 실패
    goto ERROR
)
echo ✅ update/risk_manager.py 다운로드 완료

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   Step 3: 배치 파일 다운로드
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo [1/6] RUN.bat 다운로드 중...
curl -L -s -o RUN.bat "https://raw.githubusercontent.com/lee-jungkil/Lj/main/RUN.bat"
echo ✅ RUN.bat 다운로드 완료

echo [2/6] run_paper.bat 다운로드 중...
curl -L -s -o run_paper.bat "https://raw.githubusercontent.com/lee-jungkil/Lj/main/run_paper.bat"
echo ✅ run_paper.bat 다운로드 완료

echo [3/6] run_live.bat 다운로드 중...
curl -L -s -o run_live.bat "https://raw.githubusercontent.com/lee-jungkil/Lj/main/run_live.bat"
echo ✅ run_live.bat 다운로드 완료

echo [4/6] run_backtest.bat 다운로드 중...
curl -L -s -o run_backtest.bat "https://raw.githubusercontent.com/lee-jungkil/Lj/main/run_backtest.bat"
echo ✅ run_backtest.bat 다운로드 완료

echo [5/6] setup.bat 다운로드 중...
curl -L -s -o setup.bat "https://raw.githubusercontent.com/lee-jungkil/Lj/main/setup.bat"
echo ✅ setup.bat 다운로드 완료

echo [6/6] QUICK_UPDATE.bat 다운로드 중...
curl -L -s -o QUICK_UPDATE.bat "https://raw.githubusercontent.com/lee-jungkil/Lj/main/QUICK_UPDATE.bat"
echo ✅ QUICK_UPDATE.bat 다운로드 완료

echo.
echo ╔═══════════════════════════════════════════════════════════════════════╗
echo ║                                                                       ║
echo ║                    ✅ v6.30.30 다운로드 완료!                          ║
echo ║                                                                       ║
echo ╚═══════════════════════════════════════════════════════════════════════╝
echo.
echo 📦 다운로드된 파일:
echo   - src\main.py (메인 로직)
echo   - src\config.py (설정)
echo   - src\utils\risk_manager.py (리스크 관리)
echo   - update\main.py (백업)
echo   - update\config.py (백업)
echo   - update\risk_manager.py (백업)
echo   - RUN.bat (메인 실행)
echo   - run_paper.bat (모의투자)
echo   - run_live.bat (실거래)
echo   - run_backtest.bat (백테스트)
echo   - setup.bat (초기 설정)
echo   - QUICK_UPDATE.bat (빠른 업데이트)
echo.
echo 📖 다음 단계:
echo   1. setup.bat 실행 (초기 설정)
echo   2. run_paper.bat 실행 (모의투자 1주일 권장)
echo   3. run_live.bat 실행 (실거래, 신중히)
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   다운로드 소스: https://github.com/lee-jungkil/Lj
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
pause
exit /b 0

:ERROR
echo.
echo ❌ 다운로드 중 에러가 발생했습니다!
echo.
echo 📖 해결 방법:
echo   1. 인터넷 연결 확인
echo   2. 전체 ZIP 다운로드:
echo      https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
echo   3. Git Clone:
echo      git clone https://github.com/lee-jungkil/Lj.git
echo.
pause
exit /b 1
