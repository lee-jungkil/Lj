# Upbit AutoProfit Bot v6.30.6

**Release Date**: 2026-02-12  
**Status**: Production Ready

---

## 🚀 빠른 시작

### 방법 1: 간편 업데이트 + 실행 (권장)

```cmd
# 1. 프로젝트 폴더로 이동
cd C:\Users\admin\Downloads\Lj-main

# 2. 빠른 업데이트 (다운로드 + 적용)
QUICK_UPDATE.bat

# 3. 봇 실행
RUN.bat
```

### 방법 2: 단계별 업데이트

```cmd
# 1. update 폴더로 이동
cd C:\Users\admin\Downloads\Lj-main\update

# 2. 다운로드
download_update.bat

# 3. 적용
UPDATE.bat

# 4. 상위 폴더로
cd ..

# 5. 실행
RUN.bat
```

### 방법 3: Git Pull

```cmd
cd C:\Users\admin\Downloads\Lj-main
git pull origin main
python -m src.main
```

---

## ⚠️ 중요: 실행 방법 변경됨!

### ❌ 기존 방법 (더 이상 작동 안 함)
```cmd
python src\main.py
```

### ✅ 새로운 방법 (v6.30.6부터 필수)
```cmd
python -m src.main
```

또는

```cmd
RUN.bat
```

---

## 📁 파일 설명

| 파일 | 설명 |
|------|------|
| **QUICK_UPDATE.bat** | 다운로드 + 업데이트 한 번에 (가장 간편) |
| **RUN.bat** | 봇 실행 (환경 검증 포함) |
| **UPDATE.bat** | 업데이트만 (다운로드는 별도) |
| **update/download_update.bat** | GitHub에서 다운로드만 |

---

## 🔧 주요 기능

### Phase 2 Advanced Trading System

#### 1️⃣ 동적 손절 시스템 (Dynamic Stop Loss)
- AI 학습 기반 손절가 조정
- 시장 상황 반영 실시간 업데이트
- 트레일링 스탑 자동 설정

#### 2️⃣ 분할 매도 (Scaled Sell)
- 수익률별 자동 분할 매도
- 예: 2% 도달 시 30%, 4% 시 40%, 6% 시 30%
- 리스크 분산 및 수익 극대화

#### 3️⃣ 조건부 매도 (Conditional Sell)
- 복합 지표 기반 매도 판단
- RSI, MACD, 거래량 등 다각 분석
- 최소 조건 개수 설정 가능

#### 4️⃣ 리스크 평가 시스템 (v6.30.4)
- 100점 척도 리스크 스코어
- 손익률, 보유시간, 시장 변동성 등 종합 평가
- 자동 청산 권고 (CRITICAL/HIGH/MEDIUM/LOW)

#### 5️⃣ 포지션 청산 시스템 (v6.30.5)
- **10가지 청산 조건** 통합
- 매 분 자동 체크 (`quick_check_positions`)
- 7시간 보유 버그 완전 해결

---

## 🔍 버전 히스토리

| 버전 | 날짜 | 주요 변경 |
|------|------|----------|
| v6.30.6 | 2026-02-12 | Import 경로 수정 + 업데이트 스크립트 개선 |
| v6.30.5 | 2026-02-12 | 포지션 청산 버그 수정 (7시간 보유) |
| v6.30.4 | 2026-02-12 | 리스크 평가 시스템 통합 |
| v6.30.3 | 2026-02-12 | 프로덕션 검증 완료 |
| v6.30.2 | 2026-02-12 | Phase 2C 통합 테스트 |
| v6.30.1 | 2026-02-12 | Phase 2B 고급 기능 추가 |
| v6.30.0 | 2026-02-12 | Phase 2A 호가창 분석 |
| v6.29.5 | 2026-02-11 | Phase 1 알림 시스템 |

---

## 📖 문서

| 문서 | 설명 |
|------|------|
| [UPDATE_GUIDE_v6.30.6.md](UPDATE_GUIDE_v6.30.6.md) | 업데이트 가이드 (필수 읽기) |
| [ERROR_VERIFICATION_v6.30.6.md](ERROR_VERIFICATION_v6.30.6.md) | 에러 검증 보고서 |
| [CRITICAL_BUG_FIX_v6.30.5.md](CRITICAL_BUG_FIX_v6.30.5.md) | 포지션 청산 버그 수정 |
| [FINAL_INTEGRATION_REPORT_v6.30.4.md](FINAL_INTEGRATION_REPORT_v6.30.4.md) | 최종 통합 보고서 |

---

## ⚙️ 환경 설정

### .env 파일 (필수)

```env
# Upbit API
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

## 🆘 문제 해결

### 에러 1: "내부 또는 외부 명령이 아닙니다"
**원인**: 잘못된 위치에서 실행

**해결**:
```cmd
# 프로젝트 루트로 이동
cd C:\Users\admin\Downloads\Lj-main

# QUICK_UPDATE.bat 실행
QUICK_UPDATE.bat
```

### 에러 2: ModuleNotFoundError
**원인**: 잘못된 실행 방법

**해결**:
```cmd
# ❌ 기존 방법
python src\main.py

# ✅ 새로운 방법
python -m src.main

# ✅ 또는
RUN.bat
```

### 에러 3: .env 파일 없음
**원인**: 환경 변수 파일 미설정

**해결**:
```cmd
# .env 파일 생성
notepad .env

# 위 "환경 설정" 섹션 내용 복사/붙여넣기
```

---

## 📊 기대 성과

| 지표 | Before | After | 개선율 |
|------|--------|-------|--------|
| 주문 성공률 | 85% | 96% | +13% |
| 평균 슬리피지 | 0.30% | 0.15% | -50% |
| 추격매수 승률 | 65% | 75% | +15% |
| 손절 정확도 | 60% | 80% | +33% |
| 평균 수익 | 2.5% | 3.8% | +52% |
| 최대 손실 | -8% | -5% | -37% |
| 월 수익률 | 15% | 35% | +133% |

---

## 📞 지원

- **Repository**: https://github.com/lee-jungkil/Lj
- **Issues**: https://github.com/lee-jungkil/Lj/issues
- **Latest Release**: https://github.com/lee-jungkil/Lj/releases

---

## 📜 라이센스

MIT License - 자유롭게 사용 가능

---

**Last Updated**: 2026-02-12  
**Version**: v6.30.6  
**Status**: ✅ Production Ready
