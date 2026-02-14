@echo off
chcp 65001 >nul
echo ================================================
echo   Upbit AutoProfit Bot v6.30.31 업데이트
echo   Import Path Fix + Position Check Fix
echo ================================================
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

echo.
echo ================================================
echo   ✅ v6.30.31 업데이트 완료!
echo ================================================
echo.
echo 🎉 수정 사항:
echo   - Import 경로 수정 (상대 → 절대 경로)
echo   - ModuleNotFoundError 해결
echo   - 포지션 청산 버그 수정 (7시간 보유 이슈)
echo   - quick_check_positions() 메서드 추가
echo   - 10가지 청산 조건 통합
echo   - 리스크 평가 시스템 (100점 척도)
echo.
echo 📖 실행 방법 변경:
echo   기존: python src\main.py
echo   신규: python -m src.main
echo.
echo 📖 자세한 내용은 ERROR_VERIFICATION_v6.30.31.md 참고
echo.
pause
