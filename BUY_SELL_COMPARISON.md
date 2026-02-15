# 매수 vs 매도 로직 비교 분석

## 📊 전체 흐름 비교

### ✅ 매수 (execute_buy) - 정상 작동

```python
def execute_buy(self, ticker: str, strategy: str, reason: str, indicators: Dict, ...):
    # 1. 포지션 개설 가능 여부 확인
    can_open, msg = self.risk_manager.can_open_position(ticker)
    if not can_open:
        return
    
    # 2. 현재가 조회
    current_price = self.api.get_current_price(ticker)
    if not current_price:
        return
    
    # 3. 투자 금액 계산
    investment = self.risk_manager.calculate_position_size(current_price)
    
    # 4. 수량 계산
    amount = investment / current_price
    
    # 5. 실거래 모드면 실제 주문 (live mode)
    if self.mode == 'live' and self.api.upbit:
        order_result = self.smart_order_executor.execute_buy(...)
        if not order_result:
            return
    else:
        # 모의거래: 로그만 출력
        self.logger.log_info(f"[모의거래] 매수: {ticker}, {investment:,.0f}원")
    
    # 6. 포지션 추가 ✅
    success = self.risk_manager.add_position(
        ticker=ticker,
        amount=amount,
        price=current_price,
        strategy=strategy
    )
    
    # 7. holding_protector에도 추가 ✅
    if success:
        self.holding_protector.add_bot_position(
            ticker=ticker,
            amount=amount,
            price=current_price,
            strategy=strategy
        )
```

**결과**: 포지션이 `self.risk_manager.positions`에 추가됨 ✅

---

### ❓ 매도 (execute_sell) - 문제 발생

```python
def execute_sell(self, ticker: str, reason: str):
    # 1. 포지션 존재 확인
    if ticker not in self.risk_manager.positions:
        return  # ❌ 여기서 바로 종료!
    
    position = self.risk_manager.positions[ticker]
    
    # 2. 현재가 조회 (재시도 3회)
    current_price = None
    for attempt in range(3):
        current_price = self.api.get_current_price(ticker)
        if current_price:
            break
    
    if not current_price:
        return
    
    # 3. 손익률 계산
    profit_ratio = ((current_price - position.avg_buy_price) / position.avg_buy_price) * 100
    
    # 4. ExitReason 파싱
    exit_reason = ExitReason.TAKE_PROFIT
    if "손절" in reason: exit_reason = ExitReason.STOP_LOSS
    elif "시간초과" in reason: exit_reason = ExitReason.TIME_EXCEEDED
    ...
    
    # 5. 시장 조건 분석
    market_condition = {...}
    
    # 6. 매도 수량 결정
    sell_amount = position.amount
    
    # 7. 실거래 모드면 실제 주문 (live mode)
    if self.mode == 'live' and self.api.upbit:
        # 최대 3회 재시도
        for attempt in range(3):
            order_result = self.smart_order_executor.execute_sell(...)
            if order_result and order_result.get('success'):
                break
    else:
        # 모의거래: 로그만 출력 ✅
        self.logger.log_info(f"[모의거래] 매도: {ticker}, {sell_amount:.8f}")
    
    # 8. holding_protector에서 포지션 청산 ✅
    bot_profit_loss = self.holding_protector.close_bot_position(
        ticker, sell_amount, current_price
    )
    
    # 9. risk_manager에서 포지션 청산 ✅
    profit_loss = self.risk_manager.close_position(ticker, current_price)
    
    # 10. 화면에서 포지션 제거 ✅
    slot = self.display.get_slot_by_ticker(ticker)
    if slot:
        self.display.remove_position(slot, current_price, profit_loss, profit_ratio)
```

**결과**: 로직 자체는 정상, 하지만 실행 안됨 ❌

---

## 🔍 핵심 차이점

| 항목 | 매수 | 매도 | 차이점 |
|------|------|------|--------|
| **호출 지점** | `scan_market()` → `execute_buy()` | `check_positions()` → `execute_sell()` | 매도는 check_positions 내부 |
| **사전 조건 확인** | `can_open_position()` | `ticker in positions` | 동일 |
| **API 호출** | `api.get_current_price()` | `api.get_current_price()` (3회 재시도) | 동일 |
| **주문 실행** | `smart_order_executor.execute_buy()` | `smart_order_executor.execute_sell()` | 동일 |
| **모의거래 처리** | 로그만 출력 | 로그만 출력 | 동일 |
| **포지션 관리** | `add_position()` + `add_bot_position()` | `close_position()` + `close_bot_position()` | 동일 |

---

## ⚠️ 실제 문제점

### 문제 1: `check_positions()` 함수가 중단됨

```python
def check_positions(self, ticker: str, strategy, position=None):
    # 조건 0: 리스크 평가
    try:
        df = self.api.get_ohlcv(ticker, interval="minute1", count=10)
        
        # ❌ 여기서 DataFrame 오류 발생!
        if ohlcv and len(ohlcv) >= 2:  # ValueError: ambiguous truth value
            ...
    except Exception as e:
        # 예외 발생 → 함수 종료 → execute_sell() 호출 안됨!
        return
```

**증거**:
- 로그에 `[FORCE-SELL] ✅ 매도 주문 완료!` 출력됨
- 하지만 `[EXECUTE-SELL]` 로그는 없음
- 이는 `execute_sell()`이 **호출조차 안됨**을 의미

### 문제 2: Python 캐시(.pyc) 문제

```
GitHub 코드: ✅ 수정된 코드 (if ohlcv is not None)
로컬 .py 파일: ✅ 수정된 코드
캐시 .pyc 파일: ❌ 오래된 코드 (if ohlcv and len...)
실제 실행: ❌ 캐시 파일 실행 → 오류 발생
```

---

## 📈 실행 흐름 비교

### 매수 흐름 (정상 ✅)

```
[Main Loop]
  ↓
scan_market()  # 코인 스캔
  ↓
전략.generate_signal()  # 매수 신호 확인
  ↓
if signal == BUY:
  ↓
execute_buy()  ✅ 직접 호출
  ↓
risk_manager.add_position()  ✅ 포지션 추가
  ↓
화면에 표시  ✅
```

### 매도 흐름 (문제 ❌)

```
[Main Loop]
  ↓
check_positions()  # 포지션 체크
  ↓
조건 0: 리스크 평가 시작
  ↓
if ohlcv and len(ohlcv) >= 2:  ❌ DataFrame 오류!
  ↓
예외 발생 → return  ❌ 함수 종료
  ↓
execute_sell()  ❌ 호출 안됨!
```

---

## 🎯 결론

### 매수가 되는 이유 ✅
1. `scan_market()` → `execute_buy()` 직접 호출
2. 중간에 DataFrame 처리 없음
3. 오류 발생 지점 없음

### 매도가 안 되는 이유 ❌
1. `check_positions()` 내부에서 DataFrame 오류 발생
2. 오류로 인해 함수가 조기 종료
3. `execute_sell()` 호출 자체가 안됨
4. Python 캐시(.pyc)가 수정 전 코드를 실행

---

## ✅ 해결 방법

### 즉시 해결
```batch
# 캐시 완전 삭제
taskkill /F /IM python.exe
del /s /q *.pyc
for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"

# 최신 코드 다운로드
git pull origin main

# 봇 재시작
python -B -u -m src.main --mode paper
```

### 검증 방법
봇 시작 후 다음 로그 **반드시** 나타나야 함:
```
[EXECUTE-SELL] execute_sell() 호출됨 - ticker: KRW-XXX
[EXECUTE-SELL] 포지션 존재 여부 체크: True
```

만약 위 로그가 없다면 → 아직도 오래된 캐시 사용 중!

---

## 📋 요약

| 항목 | 상태 | 비고 |
|------|------|------|
| 매수 로직 | ✅ 정상 | DataFrame 처리 없음 |
| 매도 로직 | ✅ 정상 | 코드 자체는 완벽 |
| check_positions | ❌ 오류 | DataFrame boolean 체크 오류 |
| Python 캐시 | ❌ 문제 | 수정 전 코드 실행 중 |
| GitHub 코드 | ✅ 최신 | v6.30.61 수정 완료 |
| 로컬 .py 파일 | ✅ 최신 | git pull 완료 |
| 실행 중인 코드 | ❌ 오래됨 | .pyc 캐시 사용 |

**결론**: 매수와 매도 로직은 동일한 형식으로 잘 만들어졌습니다. 
문제는 **Python 캐시 파일(.pyc)**이 수정 전 코드를 실행하고 있어서 
`check_positions()` 함수에서 오류가 발생하고, 
그로 인해 `execute_sell()`이 호출조차 안 되는 것입니다.

**해결**: 캐시 완전 삭제 후 재시작!
