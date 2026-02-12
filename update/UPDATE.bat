@echo off
chcp 65001 >nul
echo ================================================
echo   Upbit AutoProfit Bot v6.29 업데이트
echo   Advanced Order System FINAL
echo ================================================
echo.

echo [1/8] 메인 로직 업데이트...
copy /Y main.py ..\src\main.py >nul 2>&1
if errorlevel 1 (
    echo ❌ main.py 업데이트 실패
    pause
    exit /b 1
)
echo ✅ main.py 업데이트 완료

echo [2/8] 설정 파일 업데이트...
copy /Y config.py ..\src\config.py >nul 2>&1
if errorlevel 1 (
    echo ❌ config.py 업데이트 실패
    pause
    exit /b 1
)
echo ✅ config.py 업데이트 완료

echo [3/8] Upbit API 업데이트...
copy /Y upbit_api.py ..\src\upbit_api.py >nul 2>&1
if errorlevel 1 (
    echo ❌ upbit_api.py 업데이트 실패
    pause
    exit /b 1
)
echo ✅ upbit_api.py 업데이트 완료

echo [4/8] 급등 감지 시스템 업데이트...
copy /Y surge_detector.py ..\src\utils\surge_detector.py >nul 2>&1
if errorlevel 1 (
    echo ❌ surge_detector.py 업데이트 실패
    pause
    exit /b 1
)
echo ✅ surge_detector.py 업데이트 완료

echo [5/8] 주문 방법 선택기 업데이트...
copy /Y order_method_selector.py ..\src\utils\order_method_selector.py >nul 2>&1
if errorlevel 1 (
    echo ❌ order_method_selector.py 업데이트 실패
    pause
    exit /b 1
)
echo ✅ order_method_selector.py 업데이트 완료

echo [6/8] 스마트 주문 실행기 업데이트...
copy /Y smart_order_executor.py ..\src\utils\smart_order_executor.py >nul 2>&1
if errorlevel 1 (
    echo ❌ smart_order_executor.py 업데이트 실패
    pause
    exit /b 1
)
echo ✅ smart_order_executor.py 업데이트 완료

echo [7/8] AI 학습 엔진 업데이트...
copy /Y learning_engine.py ..\src\ai\learning_engine.py >nul 2>&1
if errorlevel 1 (
    echo ❌ learning_engine.py 업데이트 실패
    pause
    exit /b 1
)
echo ✅ learning_engine.py 업데이트 완료

echo [8/8] 텔레그램 알림 업데이트...
copy /Y telegram_notifier.py ..\src\utils\telegram_notifier.py >nul 2>&1
if errorlevel 1 (
    echo ❌ telegram_notifier.py 업데이트 실패
    pause
    exit /b 1
)
echo ✅ telegram_notifier.py 업데이트 완료

echo.
echo ================================================
echo   ✅ v6.29 업데이트 완료!
echo ================================================
echo.
echo 🎉 새로운 기능:
echo   - 9가지 주문 방식 (시장가, 지정가, 최유리, IOC 등)
echo   - 추격매수 시스템 (급등 자동 감지)
echo   - 6가지 청산 조건 (트레일링 스탑, 시간초과 등)
echo   - AI 학습 메타데이터 확장
echo   - 상세 텔레그램 알림
echo.
echo 📖 자세한 내용은 ADVANCED_ORDER_SYSTEM_FINAL_v6.29.md 참고
echo.
pause
