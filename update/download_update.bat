@echo off
chcp 65001 >nul
echo ================================================
echo   GitHub에서 최신 업데이트 다운로드
echo   Repository: lee-jungkil/Lj
echo ================================================
echo.

REM GitHub API를 통해 최신 파일 다운로드
echo [1/3] main.py 다운로드 중...
curl -L -o main.py "https://raw.githubusercontent.com/lee-jungkil/Lj/main/update/main.py" 2>nul
if errorlevel 1 (
    echo ❌ main.py 다운로드 실패
    echo.
    echo 📖 해결 방법:
    echo   1. 인터넷 연결 확인
    echo   2. 수동 다운로드: https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
    pause
    exit /b 1
)
echo ✅ main.py 다운로드 완료

echo [2/3] config.py 다운로드 중...
curl -L -o config.py "https://raw.githubusercontent.com/lee-jungkil/Lj/main/update/config.py" 2>nul
if errorlevel 1 (
    echo ❌ config.py 다운로드 실패
    pause
    exit /b 1
)
echo ✅ config.py 다운로드 완료

echo [3/3] risk_manager.py 다운로드 중...
curl -L -o risk_manager.py "https://raw.githubusercontent.com/lee-jungkil/Lj/main/update/risk_manager.py" 2>nul
if errorlevel 1 (
    echo ❌ risk_manager.py 다운로드 실패
    pause
    exit /b 1
)
echo ✅ risk_manager.py 다운로드 완료

echo.
echo ================================================
echo   ✅ 다운로드 완료!
echo ================================================
echo.
echo 다음 단계:
echo   1. UPDATE.bat 실행
echo   2. cd ..
echo   3. RUN.bat 실행
echo.
pause
