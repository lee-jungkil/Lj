# 📊 업비트 API 호출 현황 분석 및 최적화 가이드

## 🔍 현재 봇의 API 호출 주기 설정

### ⏱️ 3가지 스캔 주기

```python
# src/main.py 라인 187-189
self.full_scan_interval = 180  # 3분 (180초)
self.quick_check_interval = 5   # 5초
self.surge_scan_interval = 1    # 1초
```

### 📋 실행 흐름 및 API 호출 패턴

#### 1️⃣ 전체 스캔 (3분 주기)
```
실행 주기: 180초마다
대상: Config.WHITELIST_COINS (설정된 모든 코인)

API 호출:
├─ get_ohlcv('KRW-BTC', minute5, 200) - 시장 상황 분석용 (1회)
├─ get_ohlcv(ticker, minute5, 200) - 각 코인 분석 (N회)
└─ get_current_price(ticker) - 포지션 업데이트 (포지션 수만큼)

예시: 코인 10개 + 포지션 3개
= 1 (BTC) + 10 (분석) + 3 (포지션) = 14회/180초
= 평균 0.078회/초
```

#### 2️⃣ 급등/급락 감지 (1초 주기) ⚡ 최우선
```
실행 주기: 1초마다 (surge_scan_interval)
대상: 초단타 포지션 + 급등/락 스캔

API 호출:
├─ check_ultra_positions()
│  └─ get_current_price(ticker) - 각 초단타 포지션 (최대 2개)
│
└─ scan_for_surges()  # surge_detector.py
   └─ get_current_price(ticker) - 전체 코인 스캔 (N회)
   └─ get_ohlcv(ticker, minute1, 200) - 급등 확인 시

예시: 초단타 2개 + 스캔 10개
= 2 + 10 = 12회/초
```

#### 3️⃣ 빠른 포지션 체크 (5초 주기)
```
실행 주기: 5초마다 (quick_check_interval)
조건: 일반 포지션이 있을 때

API 호출:
└─ get_current_price(ticker) - 각 포지션 (N개)

예시: 포지션 3개
= 3회/5초 = 0.6회/초
```

---

## 🚨 업비트 API 제한 (Rate Limits)

### 📊 공식 제한 정책 (2025년 기준)

| API 그룹 | 제한 | 측정 단위 | 비고 |
|---------|------|----------|------|
| **시세 조회** | 초당 10회 | IP 단위 | get_current_price, get_tickers |
| **호가 조회** | 초당 10회 | IP 단위 | get_orderbook |
| **차트 (분봉)** | 초당 10회 | IP 단위 | get_ohlcv |
| **주문 조회** | 초당 30회 | 계정 단위 | 체결 대기/종료 목록 |
| **주문 생성** | 초당 8회 | 계정 단위 | buy/sell 주문 |
| **WebSocket 연결** | 초당 5회 | IP 단위 | 실시간 시세 연결 |

**중요 사항**:
- 같은 그룹 내 API는 요청 수를 함께 집계
- 반복적 초과 시 임시/영구 차단 가능
- 주문 API와 주문 외 API는 별도 계산

---

## ⚠️ 현재 봇의 API 호출 위험도 분석

### 🔴 HIGH RISK: 1초 급등 감지

```python
# 현재 설정 (라인 189)
self.surge_scan_interval = 1  # 1초

# API 호출량
- 코인 10개 스캔 시: 10회/초
- 초단타 포지션 2개: 2회/초
- 총 12회/초 → ⚠️ 제한 초과 (10회/초)
```

**문제점**:
- 시세 조회 제한 (10회/초) 초과
- 차트 조회도 동일 제한 공유
- API 차단 위험

### 🟡 MEDIUM RISK: 호가창 분석

```python
# src/utils/order_book_analyzer.py
def analyze_order_book(self, ticker):
    orderbook = self.api.get_orderbook(ticker)  # 호가 조회
```

**문제점**:
- 매 거래마다 호가창 조회
- 호가 조회 제한: 초당 10회
- 동시에 여러 코인 거래 시 초과 가능

### 🟢 LOW RISK: 전체 스캔

```python
# 3분(180초)마다 실행
- 평균 0.078회/초 → 안전
```

---

## 💡 최적화 방안

### 1️⃣ 급등 감지 주기 조정 (필수)

```python
# 현재 (위험)
self.surge_scan_interval = 1  # 1초 - 제한 초과

# 권장 (안전)
self.surge_scan_interval = 2  # 2초 - 5회/초
self.surge_scan_interval = 3  # 3초 - 3.3회/초 (가장 안전)
```

**근거**:
- 코인 10개 스캔 → 2초 간격: 5회/초 (제한 내)
- 코인 10개 스캔 → 3초 간격: 3.3회/초 (여유 있음)

### 2️⃣ WebSocket 전환 (강력 추천) 🔥

현재 문제:
```python
# REST API (폴링 방식)
while True:
    price = self.api.get_current_price(ticker)  # 매번 요청
    time.sleep(1)
```

WebSocket 방식:
```python
# 실시간 구독 (1회 연결로 지속 수신)
upbit_ws.subscribe(['KRW-BTC', 'KRW-ETH'])

# 콜백으로 자동 수신
def on_message(data):
    current_price = data['trade_price']
```

**장점**:
- API 호출 수 **0회** (연결 후 자동 수신)
- 실시간 데이터 (지연 없음)
- 초당 제한 없음 (연결 제한만 존재: 초당 5회)

**단점**:
- 초기 연결 구현 필요
- 연결 관리 (재연결 로직)

### 3️⃣ 캐싱 시스템 도입

```python
class PriceCache:
    def __init__(self, ttl=3):  # 3초 캐시
        self.cache = {}
        self.ttl = ttl
    
    def get_price(self, ticker):
        now = time.time()
        if ticker in self.cache:
            price, timestamp = self.cache[ticker]
            if now - timestamp < self.ttl:
                return price  # 캐시 반환 (API 호출 없음)
        
        # 캐시 만료 → API 호출
        price = self.api.get_current_price(ticker)
        self.cache[ticker] = (price, now)
        return price
```

**효과**:
- 중복 API 호출 제거
- 3초 내 같은 코인 조회 시 캐시 사용
- API 호출 수 50% 감소 예상

### 4️⃣ 배치 API 활용

현재:
```python
# 개별 호출 (비효율)
for ticker in tickers:
    price = self.api.get_current_price(ticker)  # 10회
```

최적화:
```python
# 배치 호출 (효율)
prices = self.api.get_tickers(tickers)  # 1회로 전체 조회
```

**효과**:
- 10회 → 1회로 감소 (90% 절감)

### 5️⃣ 스캔 대상 코인 제한

```python
# 현재
WHITELIST_COINS = [...]  # 100개+

# 권장
WHITELIST_COINS = [...][:20]  # 상위 20개로 제한
```

**근거**:
- 거래량 상위 20개만으로도 충분한 기회
- API 호출 80% 감소

---

## 🎯 추천 설정 (안전 모드)

### 📝 config.py 수정

```python
# 스캔 간격 (초)
FULL_SCAN_INTERVAL = 300  # 5분 (더 여유 있게)
QUICK_CHECK_INTERVAL = 10  # 10초 (5초 → 10초)
SURGE_SCAN_INTERVAL = 3   # 3초 (1초 → 3초) ⚠️ 필수 변경

# 스캔 대상 제한
MAX_SCAN_COINS = 20  # 상위 20개만 스캔

# 캐시 설정
ENABLE_PRICE_CACHE = True
PRICE_CACHE_TTL = 3  # 3초 캐시
```

### 📊 예상 API 호출량 (안전 모드)

| 구분 | 현재 | 최적화 | 감소율 |
|------|------|--------|--------|
| 급등 감지 | 12회/초 | 3.3회/초 | **72%** |
| 전체 스캔 | 0.078회/초 | 0.067회/초 | 14% |
| 포지션 체크 | 0.6회/초 | 0.3회/초 | 50% |
| **총합** | **12.678회/초** | **3.667회/초** | **71%** |

**결과**: 제한 초과 → 안전 범위 ✅

---

## 🚀 WebSocket 구현 가이드 (추천)

### 신규 파일: `src/utils/upbit_websocket.py`

```python
"""
업비트 WebSocket 실시간 시세 수신
REST API 호출 수를 대폭 감소
"""

import websocket
import json
import threading
from typing import Callable, List


class UpbitWebSocket:
    """업비트 WebSocket 클라이언트"""
    
    def __init__(self, on_message_callback: Callable):
        self.ws = None
        self.callback = on_message_callback
        self.running = False
        self.thread = None
        
        # 실시간 가격 캐시
        self.prices = {}
    
    def connect(self, tickers: List[str]):
        """
        WebSocket 연결 및 구독
        
        Args:
            tickers: 구독할 티커 리스트 ['KRW-BTC', ...]
        """
        def on_message(ws, message):
            data = json.loads(message)
            ticker = data.get('code')
            price = data.get('trade_price')
            
            if ticker and price:
                self.prices[ticker] = price
                self.callback(ticker, price)
        
        def on_open(ws):
            # 구독 메시지 전송
            subscribe_fmt = [
                {"ticket": "upbit_bot"},
                {
                    "type": "ticker",
                    "codes": tickers
                }
            ]
            ws.send(json.dumps(subscribe_fmt))
            print(f"✅ WebSocket 연결 완료: {len(tickers)}개 코인 구독")
        
        # WebSocket 생성
        self.ws = websocket.WebSocketApp(
            "wss://api.upbit.com/websocket/v1",
            on_message=on_message,
            on_open=on_open
        )
        
        # 백그라운드 실행
        self.running = True
        self.thread = threading.Thread(target=self.ws.run_forever, daemon=True)
        self.thread.start()
    
    def get_price(self, ticker: str):
        """실시간 가격 조회 (API 호출 없음!)"""
        return self.prices.get(ticker)
    
    def close(self):
        """WebSocket 종료"""
        self.running = False
        if self.ws:
            self.ws.close()
```

### main.py 통합

```python
# __init__ 메서드에 추가
def __init__(self, mode: str = 'backtest'):
    # ... (기존 코드)
    
    # WebSocket 초기화
    if Config.ENABLE_WEBSOCKET:
        self.websocket = UpbitWebSocket(on_message_callback=self.on_price_update)
        self.websocket.connect(self.tickers)
        self.logger.log_info("🔌 WebSocket 실시간 시세 활성화")

def on_price_update(self, ticker: str, price: float):
    """WebSocket 가격 업데이트 콜백"""
    # 동적 청산 관리자 업데이트
    if self.exit_manager and ticker in self.exit_manager.position_data:
        self.exit_manager.update_position(ticker, price)
```

**효과**:
- `get_current_price()` 호출 **0회**
- 실시간 데이터 자동 수신
- API 제한 걱정 없음

---

## 📋 체크리스트

### ✅ 즉시 적용 (필수)
- [ ] `surge_scan_interval`을 1초 → 3초로 변경
- [ ] 스캔 대상 코인을 20개로 제한
- [ ] `quick_check_interval`을 5초 → 10초로 변경

### 🔄 단기 적용 (권장)
- [ ] 가격 캐싱 시스템 구현
- [ ] 배치 API 활용 (get_tickers)
- [ ] API 호출 로깅 추가 (모니터링)

### 🚀 중장기 적용 (최적)
- [ ] WebSocket 구현 (실시간 시세)
- [ ] Redis 캐싱 (분산 환경)
- [ ] API 호출 큐 관리

---

## 📊 요약

### 현재 상태 (위험)
- 급등 감지: **12회/초** ⚠️ 제한 초과
- API 차단 위험 있음

### 최적화 후 (안전)
- 급등 감지: **3.3회/초** ✅ 안전
- WebSocket 적용 시: **0회/초** 🔥 최고

### 권장 설정
```python
SURGE_SCAN_INTERVAL = 3  # 1초 → 3초 (필수)
QUICK_CHECK_INTERVAL = 10  # 5초 → 10초
MAX_SCAN_COINS = 20  # 상위 20개만
ENABLE_WEBSOCKET = True  # WebSocket 활성화 (강력 추천)
```

**다음 단계**: Config 파일 수정 → 코드 검증 → 커밋
