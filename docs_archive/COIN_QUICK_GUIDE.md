# 🪙 거래 코인 설정 빠른 가이드

## 📌 현재 상태

### 기본 설정: **10개 코인**
```
KRW-BTC, KRW-ETH, KRW-XRP, KRW-ADA, KRW-SOL, 
KRW-DOGE, KRW-DOT, KRW-AVAX, KRW-LINK, KRW-ATOM
```

**선정 기준:**
1. 시가총액 Top 10 글로벌 메이저 코인
2. 업비트 KRW 거래 페어 존재
3. 일일 거래량 10억원 이상
4. 일일 변동성 1~5% (안정적)
5. API 안정성 높음

---

## 🚀 코인 개수 변경 방법

### 방법 1: 원클릭 변경 (가장 간단) ✅

```bash
change_coin_count.bat
```

**메뉴:**
- [1] 10개 코인 (초보자)
- [2] 20개 코인 (중급자)
- [3] 50개 코인 (고급자)

---

### 방법 2: 수동 설정 파일 복사

#### 20개 코인으로 확장
```bash
copy .env.20coins .env
```

#### 50개 코인으로 확장
```bash
copy .env.50coins .env
```

---

### 방법 3: 직접 편집

`.env` 파일 열기 → `WHITELIST_COINS` 항목 수정

```env
# 예시: 15개로 설정
WHITELIST_COINS=KRW-BTC,KRW-ETH,KRW-XRP,KRW-ADA,KRW-SOL,KRW-DOGE,KRW-DOT,KRW-AVAX,KRW-LINK,KRW-ATOM,KRW-UNI,KRW-NEAR,KRW-ALGO,KRW-VET,KRW-FTM
```

---

## 📊 권장 설정

| 레벨 | 코인 개수 | 초기 자본 | 최대 포지션 | 학습 기간 |
|-----|---------|---------|----------|----------|
| 초보 | **10개** | 10만원 | 3개 | 1주 |
| 중급 | **20개** | 20만원 | 5개 | 2주 |
| 고급 | **50개** | 50만원 | 10개 | 1개월 |

---

## ⚙️ 함께 조정할 설정

코인 개수를 늘리면 아래 값도 함께 조정하세요:

### 20개 코인
```env
INITIAL_CAPITAL=200000      # 자본 증액
MAX_POSITIONS=5            # 포지션 증가
QUICK_CHECK_INTERVAL=10    # 스캔 간격 조정
```

### 50개 코인
```env
INITIAL_CAPITAL=500000
MAX_POSITIONS=10
QUICK_CHECK_INTERVAL=15
EXIT_MODE=aggressive       # 청산 모드 공격적으로
```

---

## 🎯 권장 학습 로드맵

### 1단계: 10개 코인 (1주일)
```bash
run_test.bat         # 테스트 모드
run_paper.bat        # 모의투자
```
**목표:** AI 학습 데이터 100건 이상, 승률 55% 이상

---

### 2단계: 20개 코인 (1주일)
```bash
change_coin_count.bat → [2] 선택
run_paper.bat
```
**목표:** 더 많은 수익 기회 확보, 분산 투자 효과 검증

---

### 3단계: 50개 코인 (실거래)
```bash
change_coin_count.bat → [3] 선택
run_live.bat         # 실거래 시작
```
**목표:** 전체 시장 기회 포착

---

## ⚠️ 주의사항

### API 호출 한도
```
Upbit 제한: 초당 10회, 분당 600회

10개 코인: API 안정적
20개 코인: API 안정적
50개 코인: API 한도 주의 (스캔 간격 조정 필요)
```

### 자본 관리
```
코인 개수 ↑ → 동시 포지션 ↑ → 필요 자본 ↑

10개 × 3포지션 = 10만원 OK
50개 × 10포지션 = 50만원 이상 필요
```

---

## 🔍 코인 추가/제거 방법

### 특정 코인만 추가
```env
# 기존 10개 + 5개 추가
WHITELIST_COINS=KRW-BTC,KRW-ETH,...,KRW-ATOM,KRW-UNI,KRW-NEAR,KRW-ALGO,KRW-VET,KRW-FTM
```

### 고변동성 코인 추가
```env
# 메이저 10개 + 고변동성 5개
WHITELIST_COINS=...,KRW-SHIB,KRW-SAND,KRW-MANA,KRW-AXS,KRW-CHZ
```

---

## 📈 예상 거래 빈도

| 코인 개수 | 시간당 신호 | 일일 거래 |
|----------|----------|---------|
| 10개     | 2~5건    | 20~50건 |
| 20개     | 5~10건   | 50~100건 |
| 50개     | 10~20건  | 100~200건 |

---

## 🛠️ 검증 방법

설정 변경 후 반드시 확인:

```bash
python test_strategy.py
```

**정상 출력:**
```
✅ 거래 대상: N개 코인
✅ 유효하지 않은 티커 제외: {...}
✅ 모든 기본 요구사항 충족
```

---

## 📂 관련 파일

- **COIN_SELECTION_GUIDE.md** - 상세 가이드
- **.env** - 현재 설정
- **.env.20coins** - 20개 프리셋
- **.env.50coins** - 50개 프리셋
- **change_coin_count.bat** - 설정 변경 도구

---

## 💡 결론

**초보자:**
- ✅ 10개 코인 유지
- ✅ 1주일 이상 학습
- ✅ 승률 55% 이상 달성 후 확장

**중급자 이상:**
- ✅ `change_coin_count.bat` 실행
- ✅ 원하는 개수 선택
- ✅ 자본 및 포지션 함께 조정

---

**GitHub:** https://github.com/lee-jungkil/Lj  
**버전:** v5.2  
**업데이트:** 2026-02-11
