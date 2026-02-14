@echo off
chcp 65001 >nul
echo ============================================
echo 긴급 업데이트: main.py v6.30.39
echo ============================================
echo.

echo [1/6] 현재 디렉토리 확인...
cd
echo.

echo [2/6] 기존 main.py 백업...
if exist src\main.py (
    copy src\main.py src\main_backup_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%.py >nul 2>&1
    echo ✅ 백업 완료
) else (
    echo ⚠️ src\main.py 파일이 없습니다!
)
echo.

echo [3/6] 최신 main.py 다운로드 중...
curl -s -o src\main.py https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py
if errorlevel 1 (
    echo ❌ curl 다운로드 실패! PowerShell로 재시도...
    powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py' -OutFile 'src\main.py' -UseBasicParsing"
)
echo ✅ 다운로드 완료
echo.

echo [4/6] 파일 크기 확인...
dir src\main.py | findstr "main.py"
echo.

echo [5/6] Phase 3 코드 검증...
findstr /C:"Phase 3 체크" src\main.py >nul
if errorlevel 1 (
    echo ❌ Phase 3 코드를 찾을 수 없습니다!
    echo 백업 파일을 복원하거나 수동으로 확인하세요.
    pause
    exit /b 1
) else (
    echo ✅ Phase 3 청산 체크 코드 확인됨
)

findstr /C:"DEBUG-LOOP" src\main.py >nul
if errorlevel 1 (
    echo ❌ DEBUG-LOOP 코드를 찾을 수 없습니다!
) else (
    echo ✅ DEBUG-LOOP 디버그 코드 확인됨
)
echo.

echo [6/6] 캐시 정리...
del /s /q *.pyc >nul 2>&1
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" >nul 2>&1
echo ✅ 캐시 정리 완료
echo.

echo ============================================
echo ✅ 업데이트 완료!
echo ============================================
echo.
echo 이제 봇을 실행하세요:
echo.
echo   python -B -u -m src.main --mode paper
echo.
echo 또는:
echo.
echo   python -B -u -c "import sys; sys.path.insert(0, 'src'); from main import AutoProfitBot; bot = AutoProfitBot(); bot.run()"
echo.
echo ============================================
echo.
echo 예상 로그 출력 (3-5초마다):
echo.
echo   [DEBUG-LOOP] 메인 루프 #1 시작 - 시간: 1771067600.12
echo   [DEBUG] Phase 3 체크 - 현재시간: 1771067600.12, 마지막체크: 0.00, 경과: 1771067600.12초, 포지션: 0개
echo   [DEBUG] ✅ 시간 조건 충족! (^>= 3초)
echo   [DEBUG] ⚠️ 포지션 없음, Phase 3 스킵
echo   [DEBUG-SLEEP] 5.00초 대기 중...
echo.
echo 포지션이 있을 때:
echo.
echo   --- ⚡ 포지션 청산 체크 #1 - 21:30:45 ---
echo   📊 KRW-DEEP 손익률: +9.00%% (보유 240초)
echo      익절 목표: +1.5%% ^| 손절 목표: -1.0%%
echo.
echo ============================================
pause
