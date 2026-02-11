@echo off
chcp 65001 >nul
echo ============================================================
echo  Upbit AutoProfit Bot - 업데이트 v6.16-SELLHISTORY
echo ============================================================
echo.
echo 업데이트 내용:
echo  ✅ 화면 스크롤 완전 제거
echo  ✅ 손익 동기화 개선
echo  ✅ 리스크 관리 강화 (10%% 손실 시 자동 중단)
echo  ✅ 디버그 출력 억제
echo  ⭐ 매도 기록 영구 저장 (최근 10건 유지)
echo.

REM 현재 위치 확인
echo 현재 위치: %CD%
echo.

REM 백업 디렉토리 생성
if not exist backup mkdir backup
set BACKUP_DIR=backup\backup_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set BACKUP_DIR=%BACKUP_DIR: =0%
mkdir "%BACKUP_DIR%"

echo [1/4] 기존 파일 백업 중...
if exist src\utils\fixed_screen_display.py (
    copy src\utils\fixed_screen_display.py "%BACKUP_DIR%\fixed_screen_display.py.bak" >nul
    echo ✓ fixed_screen_display.py 백업 완료
)
if exist src\utils\risk_manager.py (
    copy src\utils\risk_manager.py "%BACKUP_DIR%\risk_manager.py.bak" >nul
    echo ✓ risk_manager.py 백업 완료
)
echo [OK] 백업 완료: %BACKUP_DIR%
echo.

echo [2/4] 업데이트 파일 확인 중...
if not exist update\fixed_screen_display.py (
    echo [ERROR] update\fixed_screen_display.py 파일이 없습니다!
    echo.
    echo update 폴더에 업데이트 파일이 있는지 확인해주세요.
    pause
    exit /b 1
)
echo [OK] 업데이트 파일 확인
echo.

echo [3/4] 파일 업데이트 중...
copy /Y update\fixed_screen_display.py src\utils\fixed_screen_display.py >nul
if %errorlevel% neq 0 (
    echo [ERROR] 파일 복사 실패!
    pause
    exit /b 1
)
echo ✓ fixed_screen_display.py 업데이트
echo [OK] 파일 업데이트 완료
echo.

echo [4/4] 업데이트 완료 확인...
echo.
echo ============================================================
echo  업데이트 완료!
echo ============================================================
echo.
echo 변경 사항:
echo  • v6.16-SELLHISTORY 적용
echo  • 화면 스크롤 제거 (완전 고정)
echo  • 손익 자동 계산 (initial_capital 기준)
echo  • 디버그 출력 최소화
echo  • 리스크 관리 강화
echo  ⭐ 매도 기록 영구 저장 (최근 10건 유지, 화면에 5건 표시)
echo  ⭐ 매수 기록처럼 사라지지 않는 매도 기록
echo.
echo 백업 위치: %BACKUP_DIR%
echo.
echo 이제 run.bat을 실행하여 봇을 시작할 수 있습니다.
echo.
pause
