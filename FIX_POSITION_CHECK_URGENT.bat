@echo off
chcp 65001 >nul
cls
echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║                                                                    ║
echo ║   🚨 v6.30.29 포지션 청산 체크 로그 미출력 문제 - 긴급 해결        ║
echo ║                                                                    ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.
echo 현재 문제:
echo   - 포지션 있음: CBK 1개 (-0.61%%)
echo   - 로그 없음: "⚡ 포지션 청산 체크" 전혀 출력 안 됨
echo   - 매도 안 됨: 익절/손절 조건 충족해도 매도 실행 안 됨
echo.
echo 원인: Python이 구버전 .pyc 파일(캐시)을 사용 중
echo.
echo 해결: 캐시 완전 삭제 + 코드 강제 최신화 + 봇 재시작
echo.
echo ════════════════════════════════════════════════════════════════════
echo.
pause
echo.

REM Step 1: 봇 완전 종료
echo [1/7] 실행 중인 Python 프로세스 종료 중...
taskkill /F /IM python.exe 2>nul
if errorlevel 1 (
    echo [INFO] 실행 중인 Python 프로세스 없음
) else (
    echo [OK] Python 프로세스 종료 완료
)
echo.
timeout /t 2 >nul

REM Step 2: Python 캐시 완전 삭제 (중요!)
echo [2/7] Python 캐시 완전 삭제 중... (중요!)
echo __pycache__ 폴더 삭제:
for /d /r . %%d in (__pycache__) do @if exist "%%d" (
    echo   삭제: %%d
    rd /s /q "%%d" 2>nul
)
echo.
echo .pyc 파일 삭제:
del /s /q *.pyc 2>nul
echo [OK] 캐시 삭제 완료
echo.
timeout /t 2 >nul

REM Step 3: 캐시 삭제 확인
echo [3/7] 캐시 삭제 확인 중...
dir /s /b __pycache__ 2>nul
if errorlevel 1 (
    echo [OK] __pycache__ 폴더 없음 (정상)
) else (
    echo [WARNING] __pycache__ 폴더가 아직 남아있음!
    echo 수동 삭제 필요
)
echo.

REM Step 4: 코드 강제 최신화
echo [4/7] 코드 강제 최신화 중...
git reset --hard HEAD
if errorlevel 1 (
    echo [ERROR] git reset 실패!
    pause
    exit /b 1
)
echo.

git pull origin main --force
if errorlevel 1 (
    echo [ERROR] git pull 실패!
    pause
    exit /b 1
)
echo [OK] 코드 최신화 완료
echo.
timeout /t 2 >nul

REM Step 5: 버전 확인
echo [5/7] 버전 확인 중...
type VERSION.txt | findstr "v6.30.29"
if errorlevel 1 (
    echo [ERROR] 버전이 v6.30.29가 아닙니다!
    echo 현재 버전:
    type VERSION.txt | findstr "^v"
    echo.
    echo git pull을 다시 실행하세요.
    pause
    exit /b 1
) else (
    echo [OK] v6.30.29-POSITION-CHECK-INTERVAL-FIX 확인됨
)
echo.
timeout /t 2 >nul

REM Step 6: 코드 검증
echo [6/7] Phase 3 코드 검증 중...
findstr /N "if current_time - self.last_position_check_time" src\main.py | findstr "2143"
if errorlevel 1 (
    echo [ERROR] Phase 3 코드가 없습니다!
    echo src\main.py를 확인하세요.
    pause
    exit /b 1
) else (
    echo [OK] Phase 3 코드 정상
)
echo.

REM Step 7: 봇 재시작 안내
echo [7/7] 준비 완료!
echo.
echo ════════════════════════════════════════════════════════════════════
echo ✅ 모든 준비 완료!
echo ════════════════════════════════════════════════════════════════════
echo.
echo 이제 RUN_PAPER_CLEAN.bat을 실행하세요.
echo.
echo 예상 결과:
echo   1. 봇 시작: Upbit AutoProfit Bot v6.30.29
echo   2. 포지션 보유 시 3초마다:
echo      [HH:MM:SS] ⚡ 포지션 청산 체크 #1 - HH:MM:SS
echo      [HH:MM:SS] 🔍 quick_check_positions 실행 - 포지션 X개
echo      [HH:MM:SS] 📌 KRW-코인명 청산 조건 체크 시작...
echo.
echo   3. 익절 조건 충족 시:
echo      💸 익절 트리거 발생!
echo      ✅ 매도 주문 체결 완료
echo.
echo   4. 손절 조건 충족 시:
echo      🚨 손절 트리거 발생!
echo      ✅ 매도 주문 체결 완료
echo.
echo ════════════════════════════════════════════════════════════════════
echo.
echo 만약 여전히 로그가 안 나온다면:
echo   1. 이 스크립트를 다시 실행
echo   2. 컴퓨터 재부팅
echo   3. 새 폴더로 완전 재설치:
echo      git clone https://github.com/lee-jungkil/Lj.git Lj-new
echo.
echo ════════════════════════════════════════════════════════════════════
echo.
pause

REM RUN_PAPER_CLEAN.bat 자동 실행 여부 확인
set /p run_now="지금 바로 RUN_PAPER_CLEAN.bat을 실행하시겠습니까? (Y/N): "
if /i "%run_now%"=="Y" (
    echo.
    echo 봇을 시작합니다...
    echo.
    call RUN_PAPER_CLEAN.bat
) else (
    echo.
    echo 준비가 되면 RUN_PAPER_CLEAN.bat을 실행하세요.
)
