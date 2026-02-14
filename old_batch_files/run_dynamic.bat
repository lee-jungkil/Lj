@echo off
chcp 65001 > nul
title Upbit AutoProfit Bot v5.3 - 동적 코인 선정 모드 설정

echo.
echo ====================================
echo  🆕 동적 코인 선정 모드 설정
echo ====================================
echo.
echo 5분마다 자동으로 최적 코인 선정!
echo.
echo [1] 10만원 모드 (20개 코인)
echo     - 초기 자본: 10만원
echo     - 최대 포지션: 5개
echo     - 선정 방법: 거래량 기준
echo.
echo [2] 20만원 모드 (30개 코인)
echo     - 초기 자본: 20만원
echo     - 최대 포지션: 7개
echo     - 선정 방법: 복합 기준 (거래량+RSI+변동성)
echo.
echo [3] 30만원 모드 (40개 코인)
echo     - 초기 자본: 30만원
echo     - 최대 포지션: 10개
echo     - 선정 방법: 복합 기준
echo.
echo [0] 취소
echo.

set /p choice="자본금 모드를 선택하세요 (0-3): "

if "%choice%"=="1" goto SET_10
if "%choice%"=="2" goto SET_20
if "%choice%"=="3" goto SET_30
if "%choice%"=="0" goto CANCEL
goto INVALID

:SET_10
echo.
if not exist .env.dynamic_10 (
    echo ❌ .env.dynamic_10 파일이 없습니다
    echo    GitHub에서 최신 코드를 받아주세요
    goto ERROR
)
echo [1/3] 10만원 동적 모드 설정 중...
copy /Y .env.dynamic_10 .env > nul
echo ✅ 설정 완료
echo.
echo 설정 내용:
echo - 자본금: 10만원
echo - 코인 개수: 20개 (동적 선정)
echo - 갱신 주기: 5분마다
echo - 선정 방법: 거래량 기준
echo - 최대 포지션: 5개
echo - 일일 손실: 1만원 (10%%)
echo - 누적 손실: 2만원 (20%%)
echo.
goto FINISH

:SET_20
echo.
if not exist .env.dynamic_20 (
    echo ❌ .env.dynamic_20 파일이 없습니다
    echo    GitHub에서 최신 코드를 받아주세요
    goto ERROR
)
echo [1/3] 20만원 동적 모드 설정 중...
copy /Y .env.dynamic_20 .env > nul
echo ✅ 설정 완료
echo.
echo 설정 내용:
echo - 자본금: 20만원
echo - 코인 개수: 30개 (동적 선정)
echo - 갱신 주기: 5분마다
echo - 선정 방법: 복합 기준 (거래량+RSI+변동성)
echo - 최대 포지션: 7개
echo - 일일 손실: 2만원 (10%%)
echo - 누적 손실: 4만원 (20%%)
echo.
goto FINISH

:SET_30
echo.
if not exist .env.dynamic_30 (
    echo ❌ .env.dynamic_30 파일이 없습니다
    echo    GitHub에서 최신 코드를 받아주세요
    goto ERROR
)
echo [1/3] 30만원 동적 모드 설정 중...
copy /Y .env.dynamic_30 .env > nul
echo ✅ 설정 완료
echo.
echo 설정 내용:
echo - 자본금: 30만원
echo - 코인 개수: 40개 (동적 선정)
echo - 갱신 주기: 5분마다
echo - 선정 방법: 복합 기준
echo - 최대 포지션: 10개
echo - 일일 손실: 3만원 (10%%)
echo - 누적 손실: 6만원 (20%%)
echo.
goto FINISH

:FINISH
echo [2/3] 가상환경 활성화 중...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo ⚠️  가상환경이 없습니다. setup.bat을 먼저 실행하세요.
    goto ERROR
)

echo [3/3] 동적 코인 선정 테스트 중...
python src\utils\dynamic_coin_selector.py
echo.

echo ====================================
echo  🎯 설정 완료!
echo ====================================
echo.
echo 동적 코인 선정 모드 활성화됨
echo - 5분마다 최적 코인 자동 선정
echo - 거래량/RSI/변동성 실시간 분석
echo - 초단타 + 일반 전략 혼합 운영
echo.
echo 다음 단계:
echo  1) run_paper.bat      (모의투자)
echo  2) run_live.bat       (실거래)
echo.
echo 💡 TIP: 
echo    - 모의투자로 1주일 이상 테스트 권장
echo    - 코인 목록은 자동으로 5분마다 갱신됩니다
echo    - 로그에서 '동적 코인 갱신' 메시지 확인 가능
echo.
pause
exit /b 0

:CANCEL
echo.
echo 취소되었습니다.
pause
exit /b 0

:INVALID
echo.
echo ❌ 잘못된 선택입니다. 0-3 사이의 숫자를 입력하세요.
pause
exit /b 1

:ERROR
echo.
pause
exit /b 1
