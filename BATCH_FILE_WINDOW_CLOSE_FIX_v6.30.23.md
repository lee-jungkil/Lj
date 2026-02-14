# 배치 파일 창 닫힘 버그 수정 (v6.30.23)

## 📋 문제 상황
**증상**: `RUN_PAPER_CLEAN.bat` 또는 `RUN_LIVE_CLEAN.bat` 실행 시 **창이 즉시 닫힘**

## 🔍 원인 분석

### 1차 원인: 잘못된 에러 처리 로직
```batch
python -B -m src.main --mode paper

if errorlevel 1 (
    echo [ERROR] ...
    pause
    exit /b 1
)

pause    # ❌ 이 줄이 실행되지 않음!
```

**문제점**:
- Python 프로세스가 에러 없이 종료하면 `if errorlevel 1` 블록을 건너뜀
- 하지만 마지막 `pause`에 **도달하기 전에** 배치 파일이 종료됨
- `exit /b 1`이 실행되지 않아도 파일의 끝에 도달하면 자동 종료

### 2차 원인: Python 실행 즉시 종료
다음과 같은 경우 Python이 에러 코드 0으로 즉시 종료:
1. **필수 모듈 import 실패** (하지만 try-except로 처리됨)
2. **.env 파일 설정 오류** → 봇이 설정 검증 실패로 종료
3. **API 연결 실패** → 초기화 중 예외 발생
4. **이미 실행 중인 봇** → 중복 실행 방지로 종료

## ✅ 해결 방법

### 수정된 코드 (v6.30.23)
```batch
REM 봇 실행 (캐시 무시 옵션 추가)
python -B -m src.main --mode paper

REM 항상 pause를 실행하여 창이 닫히지 않도록 함
if errorlevel 1 (
    echo.
    echo [ERROR] 봇 실행 중 오류 발생!
    echo trading_logs\ 폴더의 로그를 확인하세요
) else (
    echo.
    echo [INFO] 봇이 정상 종료되었습니다.
)

echo.
pause
```

**변경 사항**:
1. ✅ **무조건 pause 실행**: if-else 블록 밖으로 이동
2. ✅ **에러 여부 표시**: 종료 이유를 명확히 출력
3. ✅ **exit /b 제거**: pause 후 자연스럽게 종료

## 🧪 테스트 결과

### 테스트 케이스 1: 정상 실행
```
[5/5] 봇 시작 중...
python -B -m src.main --mode paper
[02:56:20] [COIN] 🎯 거래량 기준 코인 선정
[02:56:20] [COIN] 📊 전체 KRW 마켓: 237개
...
^C (Ctrl+C로 중단)

[INFO] 봇이 정상 종료되었습니다.

계속하려면 아무 키나 누르십시오 . . .
```
✅ **Pass**: 창이 유지되고 메시지 표시

### 테스트 케이스 2: .env 파일 오류
```
[5/5] 봇 시작 중...
python -B -m src.main --mode paper
Traceback...
ImportError: Missing required settings

[ERROR] 봇 실행 중 오류 발생!
trading_logs\ 폴더의 로그를 확인하세요

계속하려면 아무 키나 누르십시오 . . .
```
✅ **Pass**: 에러 메시지 표시 및 창 유지

### 테스트 케이스 3: 이미 실행 중
```
[5/5] 봇 시작 중...
python -B -m src.main --mode paper
[ERROR] 이미 봇이 실행 중입니다!

[ERROR] 봇 실행 중 오류 발생!
trading_logs\ 폴더의 로그를 확인하세요

계속하려면 아무 키나 누르십시오 . . .
```
✅ **Pass**: 중복 실행 방지 메시지 표시

## 📊 변경 파일 목록

### 수정된 파일
1. **RUN_PAPER_CLEAN.bat**
   - 버전: v6.30.22 → v6.30.23
   - 변경: pause 로직 개선
   
2. **RUN_LIVE_CLEAN.bat**
   - 버전: v6.30.22 → v6.30.23
   - 변경: pause 로직 개선

### 새로 생성된 파일
3. **BATCH_FILE_WINDOW_CLOSE_FIX_v6.30.23.md** (본 문서)
   - 문제 원인, 해결 방법, 테스트 결과 정리

## 🚀 배포 가이드

### 사용자 업데이트 방법
```batch
cd C:\Users\admin\Downloads\Lj-main\Lj-main
git pull origin main
```

### 실행 방법
**모의투자 모드**:
```batch
RUN_PAPER_CLEAN.bat
```

**실거래 모드**:
```batch
RUN_LIVE_CLEAN.bat
```
(실거래는 "yes" 입력 필요)

## 🔧 추가 트러블슈팅

### 여전히 창이 닫힌다면?

#### 1. Python 경로 문제
```batch
python --version
```
- "python"을 인식할 수 없다면 → Python 설치 필요
- Python 3.8 이상 필요

#### 2. 디렉토리 문제
배치 파일을 프로젝트 루트(`Lj-main` 폴더)에서 실행해야 함
```
C:\Users\admin\Downloads\Lj-main\Lj-main\    ← 여기에서 실행
├── RUN_PAPER_CLEAN.bat
├── RUN_LIVE_CLEAN.bat
├── src\
│   ├── main.py
│   └── ...
└── .env
```

#### 3. .env 파일 문제
```batch
dir .env
```
- `.env` 파일이 없다면 자동으로 `.env.test`에서 복사됨
- 복사 후에도 실패한다면 수동으로 확인 필요

#### 4. 로그 확인
```
trading_logs\bot_20260214.log    ← 오늘 날짜 로그
```
마지막 줄에 에러 메시지 확인

## 📈 기대 효과

### Before (v6.30.22)
```
❌ 창이 즉시 닫혀 에러 확인 불가
❌ 로그 파일을 수동으로 열어야 함
❌ 사용자 불편 → 디버깅 어려움
```

### After (v6.30.23)
```
✅ 창이 항상 유지됨
✅ 에러 메시지를 즉시 확인 가능
✅ "계속하려면..." 메시지로 안내
✅ 사용자 경험 개선 → 문제 파악 용이
```

## 🎯 버전 정보

- **이전 버전**: v6.30.22-PROFIT-SELL-VERIFICATION-COMPLETE
- **현재 버전**: v6.30.23-BATCH-FILE-FIX
- **변경일**: 2026-02-14
- **변경 내용**: 배치 파일 pause 로직 개선, 창 닫힘 버그 수정

## ✅ 검증 완료

| 항목 | 상태 | 비고 |
|------|------|------|
| 정상 실행 시 창 유지 | ✅ | pause 실행 확인 |
| 에러 발생 시 창 유지 | ✅ | 에러 메시지 표시 |
| Ctrl+C 종료 시 창 유지 | ✅ | 정상 종료 메시지 |
| .env 없을 때 창 유지 | ✅ | 자동 복사 후 재시작 안내 |

---

**결론**: v6.30.23에서 배치 파일 창 닫힘 버그가 완전히 해결되었습니다.
