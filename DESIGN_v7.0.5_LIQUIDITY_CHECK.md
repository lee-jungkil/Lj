# 📊 v7.0.5 - 호가창 유동성 체크 시스템

## 🎯 문제점

### 현재 시스템 (v7.0.4)
```python
# 시장가 매수 시 문제점:
1. 호가창 유동성을 체크하지 않음
2. 원하는 금액(75만원)을 주문하면 호가창에 물량이 부족해도 그대로 체결
3. 예: 200원 호가에 20만원만 있는데 75만원 주문
   → 200원에 20만원 체결
   → 나머지 55만원은 201원, 202원, 203원... 더 높은 가격에 체결
   → 평균 체결가가 예상보다 훨씬 높아짐 (슬리피지 발생)
```

### 사용자 요구사항
```
"시장가 매수 시, 현재 호가(예: 200원)에 있는 물량만 매수하고 싶다"
"75만원을 매수하려는데 200원 호가에 20만원만 있으면, 20만원만 매수"
"나의 매수 포지션 크기를 넘지 않게"
```

---

## ✅ 해결 방안 (v7.0.5)

### 🔧 1. 호가창 유동성 체크 함수 추가

```python
def check_orderbook_liquidity(self, ticker: str, target_krw: float, 
                               max_price_levels: int = 1) -> Dict:
    """
    호가창 유동성 체크
    
    Args:
        ticker: 코인 티커
        target_krw: 목표 매수 금액 (KRW)
        max_price_levels: 최대 호가 단계 (1 = 최우선 호가만, 2 = 2단계까지)
    
    Returns:
        {
            'can_fill': bool,           # 호가창에서 전량 체결 가능 여부
            'available_krw': float,     # 호가창에서 즉시 매수 가능한 금액
            'best_ask_price': float,    # 최우선 매도 호가 (매수 시 체결 가격)
            'liquidity_ratio': float,   # 유동성 비율 (available/target)
            'suggested_krw': float,     # 추천 매수 금액 (호가창 물량 기준)
            'orderbook_levels': List[Dict],  # 호가 단계별 정보
        }
    """
```

### 🔧 2. 매수 로직 수정

```python
# Before (v7.0.4):
quantity = self.strategy.get_position_size(available_krw, current_price)
order_value = quantity * current_price  # 75만원
result = self.order_executor.execute_buy(ticker, order_value, 'market')
# → 75만원을 무조건 시장가로 매수 (슬리피지 발생 가능)

# After (v7.0.5):
# 1. 포지션 크기 계산
desired_krw = available_krw * 0.15  # 75만원

# 2. 호가창 유동성 체크
liquidity = self.api.check_orderbook_liquidity(
    ticker=ticker,
    target_krw=desired_krw,
    max_price_levels=1  # 최우선 호가만
)

# 3. 유동성 기반 매수 금액 조정
if liquidity['can_fill']:
    # 호가창에 충분한 물량 → 원하는 금액 전량 매수
    final_krw = desired_krw
else:
    # 호가창 물량 부족 → 호가창 물량만큼만 매수
    final_krw = liquidity['suggested_krw']
    logger.warning(
        f"⚠️ {ticker} 호가창 유동성 부족\n"
        f"   희망: {desired_krw:,.0f}원 → 조정: {final_krw:,.0f}원 "
        f"({liquidity['liquidity_ratio']*100:.1f}%)"
    )

# 4. 최소 주문 금액 확인 (5000원)
if final_krw < 5000:
    logger.warning(f"⚠️ {ticker} 호가창 물량 부족으로 매수 취소")
    return

# 5. 매수 실행
result = self.order_executor.execute_buy(ticker, final_krw, 'market')
```

---

## 📊 실전 예시

### Case 1: 호가창 유동성 충분 ✅

```
코인: BTC (KRW-BTC)
희망 매수 금액: 750,000원
현재 호가창:
  200원 매도: 5,000개 (1,000,000원) ✅
  201원 매도: 3,000개 (603,000원)
  202원 매도: 2,000개 (404,000원)

결과:
✅ 호가창 유동성 충분 (133.3%)
✅ 750,000원 전량 매수 가능
✅ 매수 실행: 750,000원 @ 200원
✅ 평균 체결가: 200원 (슬리피지 0%)
```

### Case 2: 호가창 유동성 부족 ⚠️

```
코인: ETH (KRW-ETH)
희망 매수 금액: 750,000원
현재 호가창:
  200원 매도: 1,000개 (200,000원) ⚠️
  201원 매도: 5,000개 (1,005,000원)
  202원 매도: 3,000개 (606,000원)

유동성 체크 (max_price_levels=1):
⚠️ 호가창 유동성 부족 (26.7%)
⚠️ 최우선 호가(200원)에 200,000원만 가능
⚠️ 매수 금액 조정: 750,000원 → 200,000원

결과:
✅ 매수 실행: 200,000원 @ 200원
✅ 평균 체결가: 200원 (슬리피지 0%)
✅ 남은 잔액: 550,000원 (다음 기회 대기)
```

### Case 3: 호가창 극소 유동성 ❌

```
코인: SOL (KRW-SOL)
희망 매수 금액: 750,000원
현재 호가창:
  200원 매도: 20개 (4,000원) ❌
  201원 매도: 30개 (6,030원)
  202원 매도: 50개 (10,100원)

유동성 체크 (max_price_levels=1):
❌ 호가창 유동성 극소 (0.5%)
❌ 최우선 호가(200원)에 4,000원만 가능
❌ 최소 주문 금액(5,000원) 미달

결과:
❌ 매수 취소 (호가창 물량 부족)
⏳ 다음 스캔 대기
```

---

## 🎯 옵션: max_price_levels

### max_price_levels = 1 (기본, 보수적)
```python
# 최우선 호가(200원)만 사용
liquidity = check_orderbook_liquidity(ticker, 750000, max_price_levels=1)

호가창:
  200원: 200,000원 ✅ 사용
  201원: 1,000,000원 ❌ 사용 안 함
  202원: 500,000원 ❌ 사용 안 함

결과: 200,000원만 매수 (200원 단일 가격 체결)
```

### max_price_levels = 2 (약간 공격적)
```python
# 최우선 + 2순위 호가까지 사용
liquidity = check_orderbook_liquidity(ticker, 750000, max_price_levels=2)

호가창:
  200원: 200,000원 ✅ 사용
  201원: 600,000원 ✅ 사용 (200+600=800K ≥ 750K)
  202원: 500,000원 ❌ 사용 안 함

결과: 750,000원 매수 (200원에 200K, 201원에 550K 체결)
평균 체결가: 200.69원 (약간의 슬리피지 발생)
```

### max_price_levels = 3 (공격적, 기존 시장가와 유사)
```python
# 3단계 호가까지 사용 (기존 시장가와 거의 동일)
liquidity = check_orderbook_liquidity(ticker, 750000, max_price_levels=3)

호가창:
  200원: 200,000원 ✅ 사용
  201원: 300,000원 ✅ 사용
  202원: 500,000원 ✅ 사용 (200+300+500=1M ≥ 750K)

결과: 750,000원 매수 (200원에 200K, 201원에 300K, 202원에 250K)
평균 체결가: 201.07원 (슬리피지 발생)
```

---

## ⚙️ 설정 옵션

### config.py에 추가

```python
# 호가창 유동성 체크 설정
LIQUIDITY_CHECK_ENABLED = True  # 호가창 유동성 체크 활성화
MAX_PRICE_LEVELS = 1  # 최대 호가 단계 (1=최우선만, 2=2단계, 3=3단계)
MIN_LIQUIDITY_RATIO = 1.0  # 최소 유동성 비율 (1.0 = 100%, 호가창에 전량 있어야 함)

# 유동성 부족 시 동작
LIQUIDITY_INSUFFICIENT_ACTION = 'ADJUST'  # 'ADJUST' | 'CANCEL'
# - ADJUST: 호가창 물량만큼만 매수
# - CANCEL: 호가창 물량 부족 시 매수 취소
```

### 사용자 맞춤 설정

```python
# 보수적 설정 (슬리피지 최소화)
MAX_PRICE_LEVELS = 1  # 최우선 호가만
MIN_LIQUIDITY_RATIO = 1.0  # 100% 유동성 필요
LIQUIDITY_INSUFFICIENT_ACTION = 'ADJUST'  # 물량만큼만 매수

# 균형 설정 (추천)
MAX_PRICE_LEVELS = 2  # 2단계 호가까지
MIN_LIQUIDITY_RATIO = 0.8  # 80% 유동성 필요
LIQUIDITY_INSUFFICIENT_ACTION = 'ADJUST'

# 공격적 설정 (기회 최대화)
MAX_PRICE_LEVELS = 3  # 3단계 호가까지
MIN_LIQUIDITY_RATIO = 0.5  # 50% 유동성 필요
LIQUIDITY_INSUFFICIENT_ACTION = 'ADJUST'
```

---

## 📈 예상 효과

### ✅ 장점

```
1. 슬리피지 최소화
   - 예상 가격(200원)에만 체결 보장
   - 평균 체결가 편차 최소화

2. 리스크 관리
   - 유동성 부족 코인 자동 회피
   - 비정상적인 고가 체결 방지

3. 포지션 정확성
   - 계획한 포지션 크기 유지
   - 예상치 못한 대량 매수 방지

4. 투명성
   - 매수 전 정확한 체결 가격 예측 가능
   - 잔액 관리 정확도 향상
```

### ⚠️ 단점 (트레이드오프)

```
1. 진입 기회 감소
   - 호가창 유동성 부족 시 매수 불가능
   - 좋은 신호여도 물량 부족하면 포기

2. 포지션 크기 감소
   - 계획한 75만원이 20만원으로 감소할 수 있음
   - 수익 기회 축소 가능

3. 복잡성 증가
   - 추가 API 호출 필요 (호가창 조회)
   - 로직 복잡도 증가
```

---

## 🔄 대안 방안

### 방안 1: 하이브리드 (추천) ⭐

```python
# 1단계: 최우선 호가 체크
liquidity = check_orderbook_liquidity(ticker, desired_krw, max_price_levels=1)

if liquidity['liquidity_ratio'] >= 0.5:  # 50% 이상
    # 호가창 물량 50% 이상 → 조정된 금액으로 매수
    final_krw = liquidity['suggested_krw']
else:
    # 호가창 물량 50% 미만 → 이번 기회는 포기
    logger.warning(f"⚠️ {ticker} 유동성 부족 (스킵)")
    return
```

### 방안 2: 시장가 with 호가 체크

```python
# 호가창 체크 후, 유동성이 충분하면 시장가 매수
liquidity = check_orderbook_liquidity(ticker, desired_krw, max_price_levels=3)

if liquidity['liquidity_ratio'] >= 0.9:  # 90% 이상
    # 유동성 충분 → 시장가로 전량 매수
    result = api.buy_market_order(ticker, desired_krw)
else:
    # 유동성 부족 → 호가창 물량만 매수
    result = api.buy_market_order(ticker, liquidity['suggested_krw'])
```

### 방안 3: 지정가 주문

```python
# 가장 보수적: 최우선 호가로 지정가 주문
orderbook = api.get_orderbook(ticker)
best_ask = orderbook['orderbook_units'][0]['ask_price']

# 최우선 호가로 지정가 주문
result = api.buy_limit_order(ticker, best_ask, quantity)

# 장점: 정확한 가격에만 체결
# 단점: 미체결 가능성 (호가가 빠르게 변동하면 체결 실패)
```

---

## 💡 권장 설정 (사용자 요구사항 기준)

### 보수적 설정 (사용자 요구사항과 일치) ⭐⭐⭐

```python
# config.py 또는 profit_bot_v7.py
LIQUIDITY_CHECK_ENABLED = True
MAX_PRICE_LEVELS = 1  # 최우선 호가만
MIN_LIQUIDITY_RATIO = 1.0  # 100% 유동성 필요
LIQUIDITY_INSUFFICIENT_ACTION = 'ADJUST'  # 물량만큼만 매수

특징:
✅ 슬리피지 0% (예상 가격에만 체결)
✅ 리스크 최소화
⚠️ 진입 기회 감소 (유동성 부족 시 매수 불가 또는 축소)
```

### 균형 설정

```python
LIQUIDITY_CHECK_ENABLED = True
MAX_PRICE_LEVELS = 2  # 2단계 호가까지
MIN_LIQUIDITY_RATIO = 0.8  # 80% 유동성
LIQUIDITY_INSUFFICIENT_ACTION = 'ADJUST'

특징:
✅ 슬리피지 최소화 (약간 발생 가능)
✅ 진입 기회 유지
✅ 리스크와 기회의 균형
```

---

## 📝 구현 예정

### 수정 파일

1. **src/upbit_api.py**
   - `check_orderbook_liquidity()` 메서드 추가
   - 호가창 조회 및 유동성 계산

2. **profit_bot_v7.py**
   - `_execute_buy()` 메서드 수정
   - 호가창 유동성 체크 로직 추가

3. **src/config.py** (선택)
   - 유동성 체크 설정 추가

### 테스트 시나리오

```
1. 유동성 충분: 75만원 → 75만원 매수
2. 유동성 50%: 75만원 → 37.5만원 매수
3. 유동성 1%: 75만원 → 매수 취소
4. 최소 금액 미달: 3,000원 → 매수 취소 (5,000원 미만)
```

---

**작성일**: 2026-07-27
**버전**: v7.0.5 (예정)
**요청자**: 사용자
**요구사항**: "시장가 매수 시 현재 호가 물량만 매수"
