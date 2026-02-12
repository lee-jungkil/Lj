# 업데이트 가이드 v6.30.6

**Release Date**: 2026-02-12  
**Version**: v6.30.6 (Import Path Fix)

---

## 📥 업데이트 방법

### 방법 1: 자동 업데이트 스크립트 (권장)

```cmd
cd C:\Users\admin\Downloads\Lj-main\update
download_update.bat
UPDATE.bat
```

### 방법 2: Git Pull

```bash
cd C:\Users\admin\Downloads\Lj-main
git pull origin main
```

### 방법 3: 전체 다운로드

1. https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip 다운로드
2. 압축 해제
3. 기존 폴더와 교체

---

## 🚀 실행 방법 (중요 - 변경됨!)

### ❌ 기존 방법 (v6.30.5 이하 - 더 이상 작동 안 함)
```cmd
python src\main.py
```

### ✅ 새로운 방법 (v6.30.6부터 필수)

**방법 1: 간편 실행 스크립트 (권장)**
```cmd
cd C:\Users\admin\Downloads\Lj-main
RUN.bat
```

**방법 2: 직접 실행**
```cmd
cd C:\Users\admin\Downloads\Lj-main
python -m src.main
```

---

## 🔧 에러 해결

### 에러 1: ModuleNotFoundError: No module named 'src'

**원인**: 잘못된 디렉토리에서 실행

**해결**:
```cmd
# 1. 프로젝트 루트로 이동
cd C:\Users\admin\Downloads\Lj-main

# 2. 현재 위치 확인 (Lj-main이어야 함)
cd

# 3. 실행
python -m src.main
```

### 에러 2: can't open file 'C:\\Users\\admin\\Downloads\\Lj-main\\update\\update'

**원인**: `update` 폴더에서 실행하려고 함

**해결**:
```cmd
# update 폴더에서 나가기
cd ..

# 실행
python -m src.main
```

### 에러 3: python: No module named src.main

**원인**: Python이 설치되지 않았거나 PATH에 등록 안 됨

**해결**:
1. Python 3.8+ 설치: https://www.python.org/downloads/
2. 설치 시 "Add Python to PATH" 체크
3. 명령 프롬프트 재시작

### 에러 4: .env 파일 없음

**원인**: 환경 변수 파일이 없음

**해결**:
```cmd
cd C:\Users\admin\Downloads\Lj-main
notepad .env
```

`.env` 파일 내용:
```
UPBIT_ACCESS_KEY=your_access_key_here
UPBIT_SECRET_KEY=your_secret_key_here

# Phase 2B Features
ENABLE_DYNAMIC_STOP_LOSS=true
ENABLE_SCALED_SELL=true
SCALED_SELL_LEVELS=2.0:30,4.0:40,6.0:30
ENABLE_CONDITIONAL_SELL=true
CONDITIONAL_SELL_MIN_CONDITIONS=2

# Order Settings
SLIPPAGE_TOLERANCE=0.5
ENABLE_ORDERBOOK_ANALYSIS=true
MIN_LIQUIDITY_SCORE=30.0
MAX_SLIPPAGE_RISK=MEDIUM

# Chase Buy Settings
CHASE_MIN_SCORE=50
CHASE_DAILY_LIMIT=10
SURGE_THRESHOLD_1M=1.5
SURGE_THRESHOLD_5M=3.0
SURGE_THRESHOLD_15M=5.0
VOLUME_SURGE_RATIO=2.0
```

---

## 📝 변경 사항 (v6.30.6)

### 1. Import 경로 수정
- 모든 상대 import → 절대 경로로 변경
- `from config import` → `from src.config import`
- `from utils.* import` → `from src.utils.* import`
- **33개 import 경로 수정**

### 2. 실행 방법 변경
- **필수**: `python -m src.main` 으로 모듈 실행
- 직접 실행 (`python src/main.py`) 더 이상 불가

### 3. 포지션 청산 버그 수정 (v6.30.5)
- `quick_check_positions()` 메서드 추가
- 7시간 보유 이슈 해결
- 10가지 청산 조건 통합

### 4. 리스크 평가 시스템 (v6.30.4)
- `evaluate_holding_risk()` 구현
- 100점 척도 리스크 스코어
- 자동 청산 로직

---

## 🔍 업데이트 검증

### 1. Python 버전 확인
```cmd
python --version
```
**예상 출력**: `Python 3.8.0` 이상

### 2. 디렉토리 확인
```cmd
cd C:\Users\admin\Downloads\Lj-main
dir
```
**예상 출력**: `src`, `update`, `RUN.bat`, `.env` 폴더/파일 보임

### 3. 모듈 import 테스트
```cmd
python -c "from src.config import Config; print('✅ Import OK')"
```
**예상 출력**: `✅ Import OK`

### 4. 봇 초기화 테스트
```cmd
python -m src.main
```
**예상 출력**:
```
[12:00:00] [COIN] 🎯 거래량 기준 코인 선정 (목표: 35개)
[12:00:01] [COIN] 📊 전체 KRW 마켓: 237개
```

---

## 📊 업데이트 체크리스트

업데이트 후 다음 항목을 확인하세요:

- [ ] **파일 업데이트**
  - [ ] `src/main.py` (104KB)
  - [ ] `src/config.py`
  - [ ] `src/utils/risk_manager.py`
  - [ ] `UPDATE.bat` (v6.30.6)
  - [ ] `RUN.bat` (신규)

- [ ] **환경 설정**
  - [ ] `.env` 파일 존재
  - [ ] Upbit API 키 설정
  - [ ] Phase 2B 환경 변수 설정

- [ ] **실행 검증**
  - [ ] `python --version` (3.8+)
  - [ ] `python -m src.main` 실행 가능
  - [ ] 봇 초기화 성공
  - [ ] 코인 선정 로그 확인

- [ ] **문서 확인**
  - [ ] `ERROR_VERIFICATION_v6.30.6.md`
  - [ ] `CRITICAL_BUG_FIX_v6.30.5.md`
  - [ ] `FINAL_INTEGRATION_REPORT_v6.30.4.md`

---

## 🆘 문제 발생 시

### 1. 로그 확인
```cmd
cd C:\Users\admin\Downloads\Lj-main
type src\trading_logs\error_YYYYMMDD.log
```

### 2. 디버그 모드 실행
```cmd
python -m src.main --verbose
```

### 3. 깨끗한 재설치
```cmd
# 1. 기존 폴더 백업
move Lj-main Lj-main.backup

# 2. 새로 다운로드
# https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip

# 3. 압축 해제 후 .env 파일만 복사
copy Lj-main.backup\.env Lj-main\

# 4. 실행
cd Lj-main
RUN.bat
```

### 4. GitHub 이슈 등록
- Repository: https://github.com/lee-jungkil/Lj/issues
- 에러 메시지와 로그 첨부

---

## 📚 관련 문서

| 문서 | 설명 |
|------|------|
| [ERROR_VERIFICATION_v6.30.6.md](ERROR_VERIFICATION_v6.30.6.md) | 에러 검증 보고서 |
| [CRITICAL_BUG_FIX_v6.30.5.md](CRITICAL_BUG_FIX_v6.30.5.md) | 포지션 청산 버그 수정 |
| [FINAL_INTEGRATION_REPORT_v6.30.4.md](FINAL_INTEGRATION_REPORT_v6.30.4.md) | 최종 통합 보고서 |
| [PRODUCTION_VERIFICATION_v6.30.3.md](PRODUCTION_VERIFICATION_v6.30.3.md) | 프로덕션 검증 |
| [INTEGRATION_PHASE2B_COMPLETE.md](INTEGRATION_PHASE2B_COMPLETE.md) | Phase 2B 완료 |

---

## 🎯 다음 단계

1. ✅ **업데이트 완료** - 이 문서의 지침 따름
2. ✅ **검증 완료** - 체크리스트 모두 확인
3. 🚀 **봇 실행** - `RUN.bat` 또는 `python -m src.main`
4. 📊 **모니터링** - 거래 로그 및 텔레그램 알림 확인
5. 💰 **수익 확인** - 실 거래 시작

---

**Last Updated**: 2026-02-12 22:50 KST  
**Version**: v6.30.6  
**Status**: ✅ Production Ready
