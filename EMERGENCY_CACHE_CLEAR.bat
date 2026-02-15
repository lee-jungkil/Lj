@echo off
chcp 65001 > nul
title EMERGENCY CACHE CLEAR - v6.30.60
color 0C

echo.
echo ========================================
echo  긴급 캐시 삭제 스크립트 v6.30.60
echo  EMERGENCY CACHE CLEAR
echo ========================================
echo.
echo 이 스크립트는 Python 캐시를 완전히 삭제하고
echo 봇을 재시작합니다.
echo.
echo 매도가 안될 때 반드시 실행하세요!
echo.

REM Change to script directory
cd /d "%~dp0"
echo 현재 디렉토리: %cd%
echo.

echo ========================================
echo  1단계: 실행 중인 Python 프로세스 종료
echo ========================================
echo.
taskkill /F /IM python.exe 2>nul
taskkill /F /IM pythonw.exe 2>nul
timeout /t 2 /nobreak >nul
echo Python 프로세스 종료 완료
echo.

echo ========================================
echo  2단계: __pycache__ 폴더 삭제
echo ========================================
echo.
for /d /r . %%d in (__pycache__) do (
    if exist "%%d" (
        echo 삭제 중: %%d
        rd /s /q "%%d" 2>nul
    )
)
echo __pycache__ 폴더 삭제 완료
echo.

echo ========================================
echo  3단계: .pyc 파일 삭제
echo ========================================
echo.
del /s /q *.pyc 2>nul
echo .pyc 파일 삭제 완료
echo.

echo ========================================
echo  4단계: src/__pycache__ 삭제
echo ========================================
echo.
if exist "src\__pycache__" (
    rd /s /q "src\__pycache__"
    echo src\__pycache__ 삭제 완료
) else (
    echo src\__pycache__ 없음
)
echo.

echo ========================================
echo  5단계: src/strategies/__pycache__ 삭제
echo ========================================
echo.
if exist "src\strategies\__pycache__" (
    rd /s /q "src\strategies\__pycache__"
    echo src\strategies\__pycache__ 삭제 완료
) else (
    echo src\strategies\__pycache__ 없음
)
echo.

echo ========================================
echo  6단계: src/ai/__pycache__ 삭제
echo ========================================
echo.
if exist "src\ai\__pycache__" (
    rd /s /q "src\ai\__pycache__"
    echo src\ai\__pycache__ 삭제 완료
) else (
    echo src\ai\__pycache__ 없음
)
echo.

echo ========================================
echo  7단계: 버전 확인
echo ========================================
echo.
if exist VERSION.txt (
    type VERSION.txt
) else (
    echo VERSION.txt 파일을 찾을 수 없습니다!
)
echo.

echo ========================================
echo  8단계: main.py 디버그 로그 확인
echo ========================================
echo.
findstr /C:"[EXECUTE-SELL]" src\main.py >nul
if errorlevel 1 (
    echo [오류] main.py에 [EXECUTE-SELL] 로그가 없습니다!
    echo GitHub에서 최신 코드를 다운로드하세요:
    echo https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
    echo.
    pause
    exit /b 1
) else (
    echo [확인] main.py에 [EXECUTE-SELL] 디버그 로그 존재
)
echo.

echo ========================================
echo  캐시 삭제 완료!
echo ========================================
echo.
echo 이제 봇을 시작합니다...
echo.
echo 로그에서 다음 메시지를 확인하세요:
echo   [EXECUTE-SELL] execute_sell() 호출됨
echo.
echo 만약 [EXECUTE-SELL] 로그가 보이지 않으면:
echo   1. 이 스크립트를 다시 실행하세요
echo   2. GitHub에서 최신 ZIP 다운로드:
echo      https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
echo.
pause

echo.
echo ========================================
echo  봇 시작 (모의거래 모드)
echo ========================================
echo.

python -B -u -m src.main --mode paper

echo.
echo ========================================
echo  봇 종료됨
echo ========================================
echo.
pause
