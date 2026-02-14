@echo off
chcp 65001 >nul
echo ============================================
echo 🔥 최종 해결 스크립트 v6.30.41
echo ============================================
echo.

echo [1/7] 현재 디렉토리 확인...
cd
echo.

echo [2/7] Python 프로세스 완전 종료...
taskkill /F /IM python.exe /T >nul 2>&1
if errorlevel 1 (
    echo ⚠️ 실행 중인 Python 프로세스 없음
) else (
    echo ✅ Python 프로세스 종료 완료
)
echo.

echo [3/7] 모든 캐시 파일 삭제...
del /s /q *.pyc >nul 2>&1
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" >nul 2>&1
echo ✅ 캐시 정리 완료
echo.

echo [4/7] 최신 main.py 다운로드...
if exist src\main.py (
    copy src\main.py src\main_backup_%date:~0,4%%date:~5,2%%date:~8,2%.py >nul 2>&1
)

curl -s -o src\main.py https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py
if errorlevel 1 (
    echo ❌ curl 다운로드 실패! PowerShell로 재시도...
    powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py' -OutFile 'src\main.py' -UseBasicParsing"
)
echo ✅ main.py 다운로드 완료
echo.

echo [5/7] 실행 스크립트 다운로드...
curl -s -o RUN_DIRECT.py https://raw.githubusercontent.com/lee-jungkil/Lj/main/RUN_DIRECT.py
if errorlevel 1 (
    powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/lee-jungkil/Lj/main/RUN_DIRECT.py' -OutFile 'RUN_DIRECT.py' -UseBasicParsing"
)
echo ✅ RUN_DIRECT.py 다운로드 완료
echo.

echo [6/7] 코드 검증...
findstr /C:"_original_print" src\main.py >nul
if errorlevel 1 (
    echo ❌ _original_print 함수를 찾을 수 없습니다!
    echo    다운로드에 실패했을 가능성이 있습니다.
    pause
    exit /b 1
) else (
    echo ✅ _original_print 함수 확인됨
)

findstr /C:"DEBUG-LOOP" src\main.py >nul
if errorlevel 1 (
    echo ❌ DEBUG-LOOP 코드를 찾을 수 없습니다!
) else (
    echo ✅ DEBUG-LOOP 코드 확인됨
)

findstr /C:"Phase 3 체크" src\main.py >nul
if errorlevel 1 (
    echo ❌ Phase 3 코드를 찾을 수 없습니다!
) else (
    echo ✅ Phase 3 청산 체크 코드 확인됨
)
echo.

echo [7/7] 환경 설정...
set ENABLE_DEBUG_LOGS=1
set PYTHONDONTWRITEBYTECODE=1
set PYTHONUNBUFFERED=1
echo ✅ 환경 변수 설정 완료
echo.

echo ============================================
echo ✅ 모든 준비 완료!
echo ============================================
echo.
echo 🚀 봇 실행 방법을 선택하세요:
echo.
echo [1] RUN_DIRECT.py로 실행 (권장)
echo [2] 모듈 방식으로 실행
echo [3] 종료
echo.
set /p choice="선택 (1-3): "

if "%choice%"=="1" (
    echo.
    echo ▶️  RUN_DIRECT.py 실행 중...
    echo.
    python -B -u RUN_DIRECT.py
) else if "%choice%"=="2" (
    echo.
    echo ▶️  모듈 방식 실행 중...
    echo.
    python -B -u -m src.main --mode paper
) else (
    echo.
    echo 종료되었습니다.
    exit /b 0
)

echo.
echo ============================================
echo 봇 종료됨
echo ============================================
pause
