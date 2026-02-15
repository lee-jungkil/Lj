@echo off
chcp 65001 > nul
title 디버그 완전 제거 업데이트 v6.30.71

echo ============================================================
echo 디버그 완전 제거 업데이트 v6.30.71
echo ============================================================
echo.
echo 이 스크립트는:
echo 1. 봇을 중지합니다
echo 2. 모든 DEBUG/체크/확인 출력을 제거합니다
echo 3. 캐시를 정리합니다
echo 4. 봇을 재시작합니다
echo.
echo ============================================================
pause

echo.
echo [1/5] 봇 중지 중...
taskkill /F /IM python.exe /T 2>nul
if %errorlevel% equ 0 (
    echo ✅ Python 프로세스 중지 완료
) else (
    echo ⚠️  실행 중인 Python 프로세스 없음
)
timeout /t 2 /nobreak > nul

echo.
echo [2/5] 디버그 출력 제거 중...
python REMOVE_ALL_DEBUG.py
if %errorlevel% equ 0 (
    echo ✅ 디버그 출력 제거 완료
) else (
    echo ❌ 디버그 제거 실패
    pause
    exit /b 1
)

echo.
echo [3/5] 캐시 정리 중...
del /s /q *.pyc 2>nul
for /d /r %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
echo ✅ 캐시 정리 완료

echo.
echo [4/5] 버전 확인...
type VERSION.txt
echo.

echo.
echo [5/5] 봇 재시작...
echo.
echo ============================================================
echo 봇이 시작됩니다. 이제 DEBUG 출력이 표시되지 않습니다!
echo ============================================================
echo.
timeout /t 3 /nobreak > nul

python -B -u -m src.main --mode paper
