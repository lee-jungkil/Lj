# 배치 파일 사용 가이드 (v6.30.23)

## ✅ 사용해야 할 파일 (최신)

### 설치
- **setup.bat** ✅ - 최초 설치 (v6.30.23, 2026-02-14 업데이트)

### 봇 실행
- **RUN_PAPER_CLEAN.bat** ✅ - 모의투자 (v6.30.23)
- **RUN_LIVE_CLEAN.bat** ✅ - 실거래 (v6.30.23)

---

## ❌ 사용하지 말아야 할 파일 (구버전)

### 구버전 실행 파일 (v5.x)
- ❌ run_paper.bat (v5.2, 2026-02-13)
- ❌ run_live.bat (v5.2, 2026-02-13)
- ❌ run_backtest.bat (v5.2, 2026-02-13)
- ❌ run.bat (v5.2, 2026-02-11)
- ❌ run_dynamic.bat (v5.2, 2026-02-11)
- ❌ run_test.bat (v5.2, 2026-02-11)

**문제점**:
- Python 캐시를 삭제하지 않음 → 구버전 코드 실행
- 버전 정보 표시 없음
- pause 로직 오류 (창 닫힘)

---

## 📋 파일별 설명

### 1. setup.bat (v6.30.23) ✅
**용도**: 최초 설치 및 환경 설정

**기능**:
- Python 설치 확인
- 가상환경 생성 (선택사항)
- 필수 패키지 설치
- .env 파일 생성

**실행 시기**:
- 최초 설치 시
- requirements.txt 변경 후
- 패키지 재설치가 필요할 때

**개선 사항** (v6.30.23):
- ✅ 가상환경 실패 시에도 계속 진행 (시스템 Python 사용)
- ✅ .env.test 파일도 자동 복사
- ✅ 버전 v6.30.23 표시
- ✅ 항상 pause 실행 (창 유지)
- ✅ 최신 배치 파일 안내

**사용법**:
```batch
setup.bat
```

---

### 2. RUN_PAPER_CLEAN.bat (v6.30.23) ✅
**용도**: 모의투자 모드 실행

**기능**:
- Python 캐시 자동 삭제
- .env 파일 확인 및 자동 생성
- 모의투자 모드로 봇 실행 (`--mode paper`)

**장점**:
- ✅ 항상 최신 코드 실행 (캐시 삭제)
- ✅ 창이 닫히지 않음 (에러 확인 가능)
- ✅ 버전 정보 표시 (v6.30.23)
- ✅ 안전 (실제 자금 사용 안 함)

**사용법**:
```batch
RUN_PAPER_CLEAN.bat
```

**로그 확인**:
```
[02:56:20] ⚡ 포지션 청산 체크 #1 - 02:56:20
[02:56:20] 🔍 quick_check_positions 실행 - 포지션 3개
[02:56:20] 📊 손익률: -0.53% (AUCTION)
[02:56:20] 🚨 매도 트리거! 사유: 손절 (-1.00%)
```

---

### 3. RUN_LIVE_CLEAN.bat (v6.30.23) ✅
**용도**: 실거래 모드 실행

**기능**:
- Python 캐시 자동 삭제
- Upbit API 키 확인
- 실거래 모드로 봇 실행 (`--mode live`)

**안전 장치**:
- ✅ "yes" 입력 확인 (실수 방지)
- ✅ API 키 설정 확인
- ✅ 경고 메시지 표시

**사용법**:
```batch
RUN_LIVE_CLEAN.bat
(프롬프트에서 "yes" 입력)
```

**주의사항**:
- ⚠️ 실제 자금이 사용됩니다!
- ⚠️ 반드시 .env 파일에 API 키 설정 필요
- ⚠️ 모의투자로 충분히 테스트 후 사용

---

## 🔄 마이그레이션 가이드

### 구버전 사용자 (v5.x → v6.30.23)

#### 1단계: 최신 코드 다운로드
```batch
cd C:\Users\admin\Downloads\Lj-main\Lj-main
git pull origin main
```

#### 2단계: 구버전 배치 파일 사용 중단
**더 이상 사용하지 마세요**:
- ❌ run_paper.bat
- ❌ run_live.bat
- ❌ run_backtest.bat

**대신 사용**:
- ✅ RUN_PAPER_CLEAN.bat
- ✅ RUN_LIVE_CLEAN.bat

#### 3단계: 캐시 완전 삭제
```batch
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc
```

#### 4단계: 새 배치 파일 실행
```batch
RUN_PAPER_CLEAN.bat
```

---

## 📊 비교표

| 항목 | 구버전 (run_paper.bat) | 신버전 (RUN_PAPER_CLEAN.bat) |
|------|----------------------|----------------------------|
| 버전 | v5.2 | v6.30.23 |
| 캐시 삭제 | ❌ | ✅ |
| 버전 표시 | ❌ | ✅ |
| 창 유지 | ⚠️ (불안정) | ✅ (항상) |
| .env 자동 생성 | ❌ | ✅ |
| 에러 메시지 | ❌ | ✅ |
| 로그 가이드 | ❌ | ✅ |

---

## ❓ FAQ

### Q1: 구버전 배치 파일을 삭제해야 하나요?
**A**: 삭제하지 않아도 되지만, **사용하지 마세요**. 혼동 방지를 위해 삭제하거나 `old_` 접두사를 붙여 이름 변경을 권장합니다.

```batch
ren run_paper.bat old_run_paper.bat
ren run_live.bat old_run_live.bat
ren run_backtest.bat old_run_backtest.bat
```

### Q2: setup.bat은 언제 다시 실행하나요?
**A**: 다음 경우에 실행:
- 최초 설치 시
- Python 버전 업그레이드 후
- requirements.txt 변경 후
- "ModuleNotFoundError" 발생 시

### Q3: 가상환경이 필요한가요?
**A**: 선택사항입니다.
- **가상환경 사용 시**: 프로젝트 간 패키지 충돌 방지
- **시스템 Python 사용 시**: 간편하지만 다른 프로젝트에 영향 가능

setup.bat (v6.30.23)은 가상환경 실패 시에도 시스템 Python으로 계속 진행합니다.

### Q4: 왜 CLEAN이라는 이름인가요?
**A**: 
- **CLEAN** = Python 캐시를 **깨끗이(Clean)** 삭제하고 실행
- 항상 최신 코드가 실행됨을 보장
- 구버전 파일과 명확히 구분

### Q5: run_backtest.bat은 없나요?
**A**: 현재 버전(v6.30.23)에는 백테스트 전용 CLEAN 파일이 없습니다. 필요하면:
```batch
python -B -m src.main --mode backtest
```
수동 실행하거나, RUN_BACKTEST_CLEAN.bat 파일 생성을 요청하세요.

---

## 🎯 권장 사용 흐름

### 최초 설치 시
```
1. setup.bat 실행
   ↓
2. .env 파일 확인 및 수정
   ↓
3. RUN_PAPER_CLEAN.bat 실행 (모의투자 테스트)
   ↓
4. 충분한 테스트 후
   ↓
5. RUN_LIVE_CLEAN.bat 실행 (실거래)
```

### 일상 사용
```
모의투자: RUN_PAPER_CLEAN.bat
실거래: RUN_LIVE_CLEAN.bat
```

### 코드 업데이트 후
```
1. git pull origin main
   ↓
2. RUN_PAPER_CLEAN.bat
   (캐시가 자동으로 삭제되므로 추가 작업 불필요)
```

---

## 📝 요약

### ✅ 항상 사용
- **setup.bat** (최초 설치)
- **RUN_PAPER_CLEAN.bat** (모의투자)
- **RUN_LIVE_CLEAN.bat** (실거래)

### ❌ 사용 중단
- run_paper.bat (구버전)
- run_live.bat (구버전)
- run_backtest.bat (구버전)
- 기타 run_*.bat 파일들

### 🔑 핵심 차이점
- **CLEAN 파일**: 캐시 삭제 + 창 유지 + 버전 표시
- **구버전 파일**: 캐시 유지 + 창 닫힘 + 구버전 실행

---

**버전**: v6.30.23  
**업데이트**: 2026-02-14  
**문서**: BATCH_FILE_USAGE_GUIDE_v6.30.23.md
