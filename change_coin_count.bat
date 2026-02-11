@echo off
chcp 65001 > nul
title Upbit AutoProfit Bot v5.2 - 코인 개수 설정 변경

echo.
echo ====================================
echo  코인 개수 설정 변경
echo ====================================
echo.
echo 현재 설정을 변경하시겠습니까?
echo.
echo [1] 10개 코인 (기본값) - 초보자 권장
echo     자본: 10만원 / 포지션: 3개
echo.
echo [2] 20개 코인 (중급) - 1주일 이상 학습 후
echo     자본: 20만원 / 포지션: 5개
echo.
echo [3] 50개 코인 (고급) - 실거래 시
echo     자본: 50만원 / 포지션: 10개
echo.
echo [0] 취소
echo.

set /p choice="번호를 선택하세요 (0-3): "

if "%choice%"=="1" goto SET_10
if "%choice%"=="2" goto SET_20
if "%choice%"=="3" goto SET_50
if "%choice%"=="0" goto CANCEL
goto INVALID

:SET_10
echo.
echo [1/2] 기본 .env 파일로 복원 중...
copy /Y .env.example .env > nul
echo ✅ 10개 코인 설정 완료
echo.
echo 설정 내용:
echo - 거래 코인: 10개
echo - 초기 자본: 100,000원
echo - 최대 포지션: 3개
echo - 일일 손실: 10,000원 (10%%)
echo - 누적 손실: 20,000원 (20%%)
echo.
goto FINISH

:SET_20
echo.
if not exist .env.20coins (
    echo ❌ .env.20coins 파일이 없습니다
    echo    GitHub에서 최신 코드를 받아주세요
    goto ERROR
)
echo [1/2] 20개 코인 설정 파일로 변경 중...
copy /Y .env.20coins .env > nul
echo ✅ 20개 코인 설정 완료
echo.
echo 설정 내용:
echo - 거래 코인: 20개
echo - 초기 자본: 200,000원
echo - 최대 포지션: 5개
echo - 일일 손실: 20,000원 (10%%)
echo - 누적 손실: 40,000원 (20%%)
echo.
goto FINISH

:SET_50
echo.
if not exist .env.50coins (
    echo ❌ .env.50coins 파일이 없습니다
    echo    GitHub에서 최신 코드를 받아주세요
    goto ERROR
)
echo [1/2] 50개 코인 설정 파일로 변경 중...
copy /Y .env.50coins .env > nul
echo ✅ 50개 코인 설정 완료
echo.
echo 설정 내용:
echo - 거래 코인: 50개
echo - 초기 자본: 500,000원
echo - 최대 포지션: 10개
echo - 일일 손실: 50,000원 (10%%)
echo - 누적 손실: 100,000원 (20%%)
echo.
echo ⚠️  주의: API 호출량이 많아집니다
echo    - 안정적인 인터넷 연결 필요
echo    - VPS 또는 24시간 실행 환경 권장
echo.
goto FINISH

:FINISH
echo [2/2] 설정 검증 중...
python test_strategy.py
echo.
echo ====================================
echo  설정 변경 완료!
echo ====================================
echo.
echo 다음 단계:
echo  1) run_test.bat       (테스트 모드)
echo  2) run_paper.bat      (모의투자)
echo  3) run_live.bat       (실거래)
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
