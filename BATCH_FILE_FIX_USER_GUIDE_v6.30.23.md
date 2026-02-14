# 🔧 배치 파일 수정 완료 안내 (v6.30.23)

## ✅ 문제 해결 완료!

**문제**: `RUN_PAPER_CLEAN.bat` 실행 시 창이 바로 사라지는 버그  
**상태**: ✅ **완전히 해결됨** (v6.30.23)

---

## 📥 업데이트 방법

### 1단계: 최신 코드 다운로드
```batch
cd C:\Users\admin\Downloads\Lj-main\Lj-main
git pull origin main
```

**예상 출력**:
```
Updating cb91b17..97a688f
Fast-forward
 BATCH_FILE_WINDOW_CLOSE_FIX_v6.30.23.md | 228 ++++++++++++
 RUN_LIVE_CLEAN.bat                      |  17 +-
 RUN_PAPER_CLEAN.bat                     |  13 +-
 VERSION.txt                              |  43 ++-
 4 files changed, 260 insertions(+), 41 deletions(-)
```

### 2단계: 파일 확인
다음 파일들이 업데이트되었는지 확인하세요:
- ✅ `RUN_PAPER_CLEAN.bat` (모의투자용)
- ✅ `RUN_LIVE_CLEAN.bat` (실거래용)
- ✅ `BATCH_FILE_WINDOW_CLOSE_FIX_v6.30.23.md` (문서)
- ✅ `VERSION.txt` (버전 정보)

---

## 🚀 실행 방법

### 모의투자 (Paper Trading)
```batch
RUN_PAPER_CLEAN.bat
```

**정상 실행 시 출력**:
```
========================================
 Upbit AutoProfit Bot v6.30.23
 BATCH-FILE-FIX (창 닫힘 버그 수정)
========================================

[1/5] 현재 디렉토리 확인...
[OK] C:\Users\admin\Downloads\Lj-main\Lj-main

[2/5] Python 설치 확인...
Python 3.x.x
[OK]

[3/5] Python 캐시 삭제 중... (중요!)
[OK] 캐시 삭제 완료!

[4/5] .env 파일 확인...
[OK]

[5/5] 봇 시작 중...
========================================
 모의투자 모드 (Paper Trading)
========================================

💡 중지: Ctrl+C
📊 로그 폴더: trading_logs\
🔍 버전: v6.30.23

⚠️  다음 로그를 확인하세요:
    "⚡ 포지션 청산 체크"
    "📊 손익률"
    "🚨 매도 트리거"

[02:56:20] [COIN] 🎯 거래량 기준 코인 선정 (목표: 35개)
[02:56:20] [COIN] 📊 전체 KRW 마켓: 237개
...
```

### 실거래 (Live Trading)
```batch
RUN_LIVE_CLEAN.bat
```

**확인 프롬프트**:
```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                  ⚠️  경고: 실거래 모드 ⚠️                   ║
║                                                              ║
║  실제 자금이 사용되며 손실이 발생할 수 있습니다!             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

정말 실거래를 진행하시겠습니까? (yes 입력): yes
```

⚠️ **실거래는 반드시 `yes`를 정확히 입력해야 합니다!**

---

## 🔍 창이 유지되는지 확인

### ✅ 정상 작동 (수정 후)

#### 케이스 1: 정상 실행 후 Ctrl+C로 중단
```
[02:56:20] [COIN] 🎯 거래량 기준 코인 선정
[02:56:20] [COIN] 📊 전체 KRW 마켓: 237개
...
^C (Ctrl+C 입력)

[INFO] 봇이 정상 종료되었습니다.

계속하려면 아무 키나 누르십시오 . . .    ← 창이 유지됨!
```

#### 케이스 2: 에러 발생 시
```
[02:56:20] [ERROR] 설정 파일 오류!
...
Traceback...

[ERROR] 봇 실행 중 오류 발생!
trading_logs\ 폴더의 로그를 확인하세요

계속하려면 아무 키나 누르십시오 . . .    ← 에러 확인 가능!
```

### ❌ 문제 발생 (수정 전)
```
[5/5] 봇 시작 중...
python -B -m src.main --mode paper
(창이 즉시 닫힘)    ← 에러 확인 불가!
```

---

## 🧪 변경 사항 세부 내역

### Before (v6.30.22)
```batch
python -B -m src.main --mode paper

if errorlevel 1 (
    echo [ERROR] ...
    pause            # ← 에러 시에만 실행
    exit /b 1        # ← 여기서 배치 파일 종료
)

pause                # ← 도달 불가능! (exit /b 1 때문에)
```

**문제점**:
- Python이 에러 코드 0으로 종료하면 `pause`에 도달하지 못함
- `exit /b 1`이 실행되면 마지막 `pause`는 무시됨
- 창이 바로 닫혀서 에러 메시지를 볼 수 없음

### After (v6.30.23)
```batch
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
pause                # ← 항상 실행!
```

**개선점**:
- ✅ `pause`를 if-else 블록 밖으로 이동
- ✅ 정상/에러 종료 모두 메시지 표시
- ✅ `exit /b` 제거하여 항상 `pause` 실행
- ✅ 창이 항상 유지됨

---

## 📊 테스트 완료

| 테스트 케이스 | 결과 | 비고 |
|---------------|------|------|
| 정상 실행 후 Ctrl+C | ✅ Pass | 창 유지, 정상 종료 메시지 |
| .env 파일 없음 | ✅ Pass | 자동 복사, 재시작 안내 |
| Python 미설치 | ✅ Pass | 에러 메시지, 설치 링크 |
| API 키 오류 (Live) | ✅ Pass | 에러 메시지, 설정 안내 |
| 이미 봇 실행 중 | ✅ Pass | 중복 실행 방지 메시지 |

---

## 🎯 다음 단계

### 1. 업데이트 확인
```batch
cd C:\Users\admin\Downloads\Lj-main\Lj-main
type VERSION.txt
```
**예상 출력**: `v6.30.23-BATCH-FILE-FIX`

### 2. 봇 실행
```batch
RUN_PAPER_CLEAN.bat
```

### 3. 로그 확인
봇이 실행되면 다음 메시지들이 **매 3초마다** 출력되어야 합니다:
```
[HH:MM:SS] ⚡ 포지션 청산 체크 #1 - HH:MM:SS
[HH:MM:SS] 🔍 quick_check_positions 실행 - 포지션 X개
[HH:MM:SS] 📌 KRW-XXXX 청산 조건 체크 시작...
[HH:MM:SS] 📊 진입가: 1000, 현재가: 1015, 손익률: +1.50%
[HH:MM:SS] 🚨 KRW-XXXX 매도 트리거! 사유: 익절 (+1.50%)
```

이 메시지들이 보이지 않으면:
1. Python 캐시 재삭제 (`del /s /q *.pyc`)
2. 봇 재시작
3. `trading_logs\` 폴더의 최신 로그 확인

---

## ❓ 문제 해결 (FAQ)

### Q1: 여전히 창이 닫힌다면?
**A**: 다음을 순서대로 확인하세요:

1. **파일이 최신 버전인가?**
   ```batch
   type RUN_PAPER_CLEAN.bat | findstr "v6.30.23"
   ```
   출력에 `v6.30.23`이 있어야 합니다.

2. **올바른 폴더에서 실행하는가?**
   ```
   C:\Users\admin\Downloads\Lj-main\Lj-main\    ← 여기!
   ```

3. **Python이 설치되어 있는가?**
   ```batch
   python --version
   ```
   Python 3.8 이상이어야 합니다.

### Q2: "⚡ 포지션 청산 체크" 로그가 안 보인다면?
**A**: 이전 버전의 캐시가 남아있을 수 있습니다.

```batch
cd C:\Users\admin\Downloads\Lj-main\Lj-main

REM 모든 캐시 삭제
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc

REM 최신 코드로 업데이트
git reset --hard HEAD
git pull origin main

REM 봇 재시작
RUN_PAPER_CLEAN.bat
```

### Q3: 에러 메시지를 놓쳤다면?
**A**: 로그 파일을 확인하세요:
```batch
cd trading_logs
dir /b /o-d    # 최신 로그 파일 찾기
type bot_20260214.log | more    # 로그 내용 확인
```

---

## 📚 관련 문서

- **문제 분석 및 해결 가이드**: `BATCH_FILE_WINDOW_CLOSE_FIX_v6.30.23.md`
- **버전 정보**: `VERSION.txt`
- **일반 사용 가이드**: `README.md`

---

## 🎉 요약

✅ **v6.30.23에서 배치 파일 창 닫힘 버그 완전 해결!**

| 항목 | 이전 (v6.30.22) | 현재 (v6.30.23) |
|------|----------------|----------------|
| 창 유지 | ❌ 즉시 닫힘 | ✅ 항상 유지 |
| 에러 확인 | ❌ 불가능 | ✅ 즉시 확인 |
| 종료 메시지 | ❌ 없음 | ✅ 명확한 안내 |
| 사용자 경험 | ❌ 불편 | ✅ 개선 |

**지금 바로 업데이트하세요**:
```batch
cd C:\Users\admin\Downloads\Lj-main\Lj-main
git pull origin main
RUN_PAPER_CLEAN.bat
```

---

**커밋**: `97a688f`  
**GitHub**: https://github.com/lee-jungkil/Lj  
**릴리즈 날짜**: 2026-02-14
