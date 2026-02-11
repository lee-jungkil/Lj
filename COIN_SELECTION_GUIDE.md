# 🪙 거래 코인 선정 가이드

## 📋 현재 설정된 10개 코인

```
KRW-BTC    (비트코인)      - 시가총액 1위
KRW-ETH    (이더리움)      - 시가총액 2위  
KRW-XRP    (리플)         - 결제/송금 특화
KRW-ADA    (카르다노)      - 스마트컨트랙트
KRW-SOL    (솔라나)       - 고속 블록체인
KRW-DOGE   (도지코인)      - 밈코인 대표
KRW-DOT    (폴카닷)       - 크로스체인
KRW-AVAX   (아발란체)      - DeFi 플랫폼
KRW-LINK   (체인링크)      - 오라클 네트워크
KRW-ATOM   (코스모스)      - 블록체인 허브
```

---

## 🎯 10개 코인 선정 기준

### 1. **시가총액 기준** (안정성 확보)
- **Top 10 글로벌 코인** 우선 선정
- 시가총액이 클수록 가격 변동성이 안정적
- 유동성이 높아 대량 거래 시 슬리피지 최소화

### 2. **업비트 거래량 기준** (한국 시장)
- **KRW 거래 페어** 존재 (원화 직접 거래 가능)
- **일일 거래량 상위권** (10억 원 이상)
- 호가창 두께가 충분 (체결 용이)

### 3. **변동성 기준** (수익 기회)
- **일일 변동성 1~5%** 범위
- 너무 낮으면 수익 기회 부족
- 너무 높으면 리스크 과다

### 4. **기술적 안정성**
- **메이저 프로젝트** (개발 활발)
- 보안 이슈 최소
- 상장 폐지 리스크 낮음

### 5. **API 안정성**
- Upbit API에서 **데이터 조회 실패율 낮음**
- 호가창/체결 데이터 지속적 제공

---

## 🚀 코인 개수를 늘리는 방법

### 방법 1: .env 파일 직접 수정 (권장)

#### 1) `.env` 파일 열기
```
메모장 또는 VS Code로 .env 파일 열기
```

#### 2) `WHITELIST_COINS` 항목 찾기
```env
# 거래 대상 코인 (화이트리스트)
WHITELIST_COINS=KRW-BTC,KRW-ETH,KRW-XRP,KRW-ADA,KRW-SOL,KRW-DOGE,KRW-DOT,KRW-AVAX,KRW-LINK,KRW-ATOM
```

#### 3) 코인 추가
```env
# 예시: 20개로 확장
WHITELIST_COINS=KRW-BTC,KRW-ETH,KRW-XRP,KRW-ADA,KRW-SOL,KRW-DOGE,KRW-DOT,KRW-AVAX,KRW-LINK,KRW-ATOM,KRW-MATIC,KRW-UNI,KRW-NEAR,KRW-ALGO,KRW-SAND,KRW-MANA,KRW-AXS,KRW-ENJ,KRW-CHZ,KRW-SHIB
```

#### 4) 저장 후 봇 재시작

---

### 방법 2: 전체 코인 자동 스캔 (고급)

#### 1) `src/config.py` 수정

기존:
```python
WHITELIST_COINS = os.getenv("WHITELIST_COINS", 
    "KRW-BTC,KRW-ETH,KRW-XRP,KRW-ADA,KRW-SOL,KRW-DOGE,KRW-DOT,KRW-AVAX,KRW-LINK,KRW-ATOM"
).split(",")
```

수정:
```python
# 전체 코인 자동 스캔 모드
ENABLE_AUTO_COIN_SCAN = os.getenv("ENABLE_AUTO_COIN_SCAN", "false").lower() == "true"

if ENABLE_AUTO_COIN_SCAN:
    # Upbit 전체 KRW 마켓 코인 가져오기
    import pyupbit
    WHITELIST_COINS = pyupbit.get_tickers(fiat="KRW")
else:
    WHITELIST_COINS = os.getenv("WHITELIST_COINS", 
        "KRW-BTC,KRW-ETH,KRW-XRP,KRW-ADA,KRW-SOL,KRW-DOGE,KRW-DOT,KRW-AVAX,KRW-LINK,KRW-ATOM"
    ).split(",")
```

#### 2) `.env` 파일에 추가
```env
# 전체 코인 자동 스캔 (200개 이상)
ENABLE_AUTO_COIN_SCAN=true
```

#### ⚠️ **주의사항**
- **API 호출 한도 초과 위험** (Upbit: 초당 10회 제한)
- 봇 시작 시간이 길어짐 (1~2분)
- 메모리 사용량 증가
- **변동성이 극단적인 코인 포함** (리스크 증가)

---

## 📊 권장 코인 개수별 설정

### 10개 (현재 기본값) ✅ **권장**
```
초기 자본: 100,000원
최대 포지션: 3개
진입 조건: 보통

장점:
- 관리 용이
- API 호출 안정적
- 학습 데이터 빠르게 축적
- 메이저 코인 집중
```

### 20개 (중급)
```
초기 자본: 200,000원 이상
최대 포지션: 5개
진입 조건: 완화

장점:
- 더 많은 수익 기회
- 다양한 전략 테스트 가능
```

### 50개 이상 (고급)
```
초기 자본: 500,000원 이상
최대 포지션: 10개
진입 조건: 자동화

⚠️ 주의:
- API 호출 최적화 필수
- VPS 또는 24시간 실행 환경 권장
- 자본 관리 복잡
```

### 전체 코인 (200개+) (전문가)
```
초기 자본: 1,000,000원 이상
최대 포지션: 20개
진입 조건: AI 자동 선택

⚠️ 주의:
- 고성능 서버 필요
- WebSocket 실시간 데이터 필수
- 급등/급락 코인 자동 필터링 필요
```

---

## 🔍 추천 코인 추가 목록

### Top 20 추가 (안정성 중시)
```env
WHITELIST_COINS=KRW-BTC,KRW-ETH,KRW-XRP,KRW-ADA,KRW-SOL,KRW-DOGE,KRW-DOT,KRW-AVAX,KRW-LINK,KRW-ATOM,KRW-UNI,KRW-NEAR,KRW-ALGO,KRW-VET,KRW-FTM,KRW-HBAR,KRW-ICP,KRW-APT,KRW-OP,KRW-ARB
```

### 고변동성 추가 (공격적 전략)
```env
# 메이저 10개 + 고변동성 10개
WHITELIST_COINS=KRW-BTC,KRW-ETH,KRW-XRP,KRW-ADA,KRW-SOL,KRW-DOGE,KRW-DOT,KRW-AVAX,KRW-LINK,KRW-ATOM,KRW-SHIB,KRW-SAND,KRW-MANA,KRW-AXS,KRW-CHZ,KRW-ENJ,KRW-GALA,KRW-FLOW,KRW-1INCH,KRW-CRV
```

---

## ⚙️ 코인 개수 증가 시 함께 조정할 설정

### `.env` 파일 권장 값

```env
# 20개 코인으로 확장 시
MAX_POSITIONS=5              # 최대 포지션 3 → 5
INITIAL_CAPITAL=200000       # 초기 자본 10만 → 20만

# 50개 코인으로 확장 시
MAX_POSITIONS=10
INITIAL_CAPITAL=500000

# 전체 코인 스캔 시
MAX_POSITIONS=20
INITIAL_CAPITAL=1000000
ENABLE_AUTO_COIN_SCAN=true
```

---

## 🛠️ 실전 적용 순서

### 1단계: 10개 코인으로 학습 (1주)
```bash
run_test.bat          # 테스트 모드
run_paper.bat         # 모의투자
```

**목표:**
- AI 학습 데이터 100건 이상
- 승률 55% 이상 달성
- 전략별 특성 파악

---

### 2단계: 20개 코인으로 확장 (1주)
```env
# .env 수정
WHITELIST_COINS=...(20개)...
MAX_POSITIONS=5
INITIAL_CAPITAL=200000
```

**목표:**
- 더 많은 수익 기회 확보
- 분산 투자 효과 검증

---

### 3단계: 50개+ 자동 스캔 (실거래 시)
```env
ENABLE_AUTO_COIN_SCAN=true
MAX_POSITIONS=10
```

**목표:**
- 전체 시장 기회 포착
- AI 자동 코인 선택

---

## 📈 코인 개수별 예상 거래 빈도

| 코인 개수 | 시간당 신호 | 일일 거래 | 학습 속도 |
|----------|----------|---------|---------|
| 10개     | 2~5건    | 20~50건  | 보통    |
| 20개     | 5~10건   | 50~100건 | 빠름    |
| 50개     | 10~20건  | 100~200건| 매우 빠름|
| 200개+   | 30~50건  | 300~500건| 극한    |

---

## ⚠️ 중요 경고

### 1. **API 호출 한도**
```
Upbit API 제한:
- 초당 10회
- 분당 600회

코인 50개 이상 스캔 시:
→ 1회 전체 스캔 = 50~100회 API 호출
→ WebSocket으로 전환 필요
```

### 2. **자본 관리**
```
코인 개수 증가 → 동시 포지션 증가 → 필요 자본 증가

예시:
10개 코인 × 포지션 3개 = 자본 10만원 OK
50개 코인 × 포지션 10개 = 자본 50만원 이상 필요
```

### 3. **학습 품질**
```
코인이 많을수록:
- 학습 데이터는 빠르게 축적
- 하지만 코인별 특성 학습은 느림

권장:
- 초기 1~2주: 10개 코인 집중 학습
- 이후: 20~50개로 확장
```

---

## 🎯 결론 및 권장사항

### 초보자 (1~2주)
```
✅ 10개 코인 (현재 기본값)
✅ 테스트 모드 → 모의투자
✅ 학습 데이터 100건 이상 축적
```

### 중급자 (1개월 이후)
```
✅ 20개 코인
✅ 최대 포지션 5개
✅ 자본 20만원 이상
```

### 고급자 (실거래)
```
✅ 50개 이상 또는 자동 스캔
✅ 최대 포지션 10개 이상
✅ VPS 24시간 실행
```

---

## 📂 관련 파일

- `.env` - 화이트리스트 설정
- `src/config.py` - 코인 목록 로딩
- `src/main.py` - 코인 검증 및 스캔
- `QUICK_START.md` - 실행 가이드

---

## 📞 문제 해결

### Q1: 코인을 추가했는데 거래가 안 돼요
```
A: 티커 유효성 검증 확인
   python test_strategy.py
   
   유효하지 않은 티커 제외: {...}
   거래 대상: N개
```

### Q2: API 호출 에러가 자주 발생해요
```
A: 코인 개수를 줄이거나 스캔 간격 조정
   .env 파일:
   QUICK_CHECK_INTERVAL=10  # 5초 → 10초
```

### Q3: 봇이 느려졌어요
```
A: 코인 개수를 20개 이하로 유지
   또는 고성능 서버로 이전
```

---

**마지막 업데이트:** 2026-02-11  
**버전:** v5.2  
**GitHub:** https://github.com/lee-jungkil/Lj
