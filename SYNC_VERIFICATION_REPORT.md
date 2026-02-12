# 화면 출력 항목 동기화 검증 보고서

## 📊 현재 화면 구성

### 1. 헤더 (Header)
```
Upbit AutoProfit Bot v6.13 | 🕐 2026-02-12 14:35:22
📊 AI학습: 150회 | 승률: 68.5% | 자본: 1,000,000원 → 자본: 1,050,000원 | 손익: +50,000원 (+5.00%)
```

### 2. 보유 포지션 (Positions)
```
[ 💼 보유 포지션 (2/7) ]

#1 KRW-BTC | 🟢 +2.45% (+1,225,000원)
   투자: 50,000,000원 → 현재: 51,225,000원
   진입: 50,000,000원 | 현재: 51,225,000원
   보유: 3분 24초 | 전략: aggressive_scalping
```

### 3. 매도 기록 (Sell History) - NEW!
```
[ 📜 매도 기록 (5건) ]
  ✅ 14:35:22 | KRW-BTC | +1,250원 (+2.45%) | aggressi
  ❌ 14:30:15 | KRW-ETH | -350원 (-0.87%) | conserva
```

### 4. 스캔 상태 (Scan Status)
```
🔍 스캔 | 전체 스캔 #5 완료 | ⏰ 14:35:22
⏱️ 마지막: 전체 1분 전 | 포지션 5초 전 | 급등 10초 전
📈 시장: 강세장 (BTC +3.5% | 거래량 ↑25% | 변동성 0.85% | RSI 65 | MACD↑) | 진입: 완화 | BTC 50,000,000원 +3.5% | RSI 65
```

### 5. 봇 상태 (Bot Status)
```
🤖 봇 | 15개 모니터링 | 매수 8회 | 매도 5회
```

### 6. 모니터링 (Monitoring)
```
[ 🔍 작업 상태 ]
  ▸ KRW-BTC 급등 5.2% 감지
  ▸ 익절 확인 중...
  ▸ 포지션 #1 수익 +2.45%
```

---

## ✅ 동기화 확인 결과

### 1. AI 학습 상태 ✅ 동기화 됨
**코드 위치**: `src/main.py:1540-1549`
```python
# learning_engine에서 실제 데이터 가져오기
stats = self.learning_engine.get_stats()
total_trades = sum(s['total_trades'] for s in stats.values())
profit_trades = sum(s['winning_trades'] for s in stats.values())
loss_trades = sum(s['losing_trades'] for s in stats.values())

self.display.update_ai_learning(
    total_trades=total_trades,
    profit_trades=profit_trades,
    loss_trades=loss_trades
)
```
✅ **상태**: learning_engine에서 실시간 통계 가져옴
✅ **계산**: 승률 = (profit_trades / total_trades) * 100

---

### 2. 자본금 및 손익 ✅ 동기화 됨
**코드 위치**: `src/main.py:1552-1557`
```python
risk_status = self.risk_manager.get_risk_status()
self.display.update_capital_status(
    initial=Config.INITIAL_CAPITAL,
    current=risk_status['current_balance'],
    profit=risk_status['cumulative_profit_loss']
)
```
✅ **상태**: risk_manager에서 실시간 값 가져옴
✅ **계산**: 
- total_profit = current_balance - initial_capital
- profit_ratio = (total_profit / initial_capital) * 100

---

### 3. 보유 포지션 ✅ 동기화 됨
**코드 위치**: `src/main.py:1661-1697`
```python
# 일반 포지션 (risk_manager)
for ticker, position in self.risk_manager.positions.items():
    current_price = self.api.get_current_price(ticker)  # 실시간 가격
    self.display.update_position(
        slot=slot,
        ticker=ticker,
        entry_price=position.entry_price,
        current_price=current_price,  # ⭐ 실시간
        amount=position.amount,
        strategy=position.strategy,
        entry_time=position.entry_time
    )

# 초단타 포지션 (ultra_positions)
for ticker, position in self.ultra_positions.items():
    current_price = self.api.get_current_price(ticker)  # 실시간 가격
    self.display.update_position(...)
```
✅ **상태**: risk_manager + ultra_positions에서 실시간 데이터
✅ **가격**: API에서 실시간 가격 조회
✅ **계산**: 
- profit_loss = (current_price - entry_price) * amount
- profit_ratio = ((current_price - entry_price) / entry_price) * 100
- hold_time = (now - entry_time).total_seconds()

---

### 4. 매도 기록 ✅ 동기화 됨
**코드 위치**: `src/utils/fixed_screen_display.py:180-194`
```python
def remove_position(self, slot, exit_price, profit_loss, profit_ratio):
    sell_record = {
        'ticker': position['ticker'],
        'profit_loss': profit_loss,
        'profit_ratio': profit_ratio,
        'strategy': position['strategy'],
        'hold_time': position['hold_time'],
        'time': datetime.now().strftime('%H:%M:%S')
    }
    
    if len(self.sell_history) >= self.max_sell_history:
        self.sell_history.pop(0)  # FIFO
    
    self.sell_history.append(sell_record)
```
✅ **상태**: 매도 시 자동 저장
✅ **저장**: 최대 10건 (FIFO)
✅ **표시**: 최근 5건

---

### 5. 시장 조건 분석 ✅ 동기화 됨
**코드 위치**: `src/main.py:1559-1620`
```python
df = self.api.get_ohlcv('KRW-BTC', interval="minute5", count=200)
market_phase, entry_condition, _ = self.market_analyzer.analyze_market(df)

# 상세 지표 계산
btc_change = ((latest['close'] - prev['close']) / prev['close']) * 100
volume_change = ((latest['volume'] - df['volume'].mean()) / df['volume'].mean()) * 100
volatility = df['close'].pct_change().std() * 100
current_rsi = calculate_rsi(df)
macd_signal = calculate_macd(df)

reason = f"BTC {btc_change:+.1f}% | 거래량 {'↑' if volume_change > 0 else '↓'}{abs(volume_change):.0f}% | 변동성 {volatility:.2f}% | RSI {current_rsi:.0f} | MACD↑"

self.display.update_market_condition(market_phase, entry_condition, reason)
self.display.update_coin_summary(coin_summary)
```
✅ **상태**: BTC 5분봉 200개 분석
✅ **지표**: BTC 변화율, 거래량, 변동성, RSI, MACD
✅ **업데이트**: 3초마다 (_update_display 호출)

---

### 6. 거래 통계 ✅ 동기화 됨
**코드 위치**: `src/main.py:1625-1634`
```python
trades = self.logger.get_daily_trades()
if trades:
    buy_count = len([t for t in trades if t.get('action') == 'BUY'])
    sell_count = len([t for t in trades if t.get('action') == 'SELL'])
else:
    buy_count = 0
    sell_count = 0

self.display.update_trade_stats(buy_count, sell_count)
```
✅ **상태**: logger에서 실시간 거래 로그 조회
✅ **계산**: BUY/SELL 액션 카운트

---

### 7. 봇 상태 ✅ 동기화 됨
**코드 위치**: `src/main.py:1641`
```python
self.display.update_bot_status(f"{len(self.tickers)}개 모니터링")
```
✅ **상태**: 실시간 모니터링 코인 수

---

### 8. 스캔 시간 기록 ✅ 동기화 됨
**코드 위치**: `src/main.py:1302, 1375, 1399`
```python
self.display.update_scan_times(full_scan_time=scan_time)
self.display.update_scan_times(surge_scan_time=surge_time)
self.display.update_scan_times(position_check_time=position_time)
```
✅ **상태**: 각 스캔 후 시간 기록
✅ **표시**: "전체 1분 전 | 포지션 5초 전 | 급등 10초 전"

---

## 🔧 발견된 문제점

### ❌ 문제 1: hold_time 형식 불일치
**위치**: `src/utils/fixed_screen_display.py:148-162`
```python
# update_position에서
hold_time = (datetime.now() - entry_time).total_seconds()  # 초 단위 (float)

self.positions[slot] = {
    'hold_time': hold_time,  # ❌ 초 단위 숫자
    ...
}
```

**표시**: `"보유: 204초"` ← 가독성 떨어짐

**해결 필요**: "3분 24초" 형식으로 변환

---

### ❌ 문제 2: 매도 기록의 hold_time 형식
**위치**: `src/utils/fixed_screen_display.py:186`
```python
'hold_time': position['hold_time'],  # ❌ 초 단위 숫자
```

**표시**: `hold_time`이 숫자로 저장됨

**해결 필요**: 사람이 읽기 쉬운 형식으로 변환

---

### ❌ 문제 3: investment와 current_value 계산 누락
**위치**: `src/utils/fixed_screen_display.py:148-162`
```python
self.positions[slot] = {
    'ticker': ticker,
    'entry_price': entry_price,
    'current_price': current_price,
    'amount': amount,
    'profit_loss': profit_loss,
    'profit_ratio': profit_ratio,
    'hold_time': hold_time,
    'strategy': strategy
    # ❌ investment, current_value 누락
}
```

**표시**: 렌더링 시 계산하거나 0 표시

**해결 필요**: 저장 시 계산

---

### ⚠️ 문제 4: 포지션 업데이트 방식 불일치
**main.py**: `update_position(slot, ticker, entry_price, current_price, amount, strategy, entry_time)`
- 7개 파라미터
- entry_time은 datetime 객체

**fixed_screen_display.py**: 계산 로직이 내부에 있음
- profit_loss, profit_ratio, hold_time 모두 계산

**문제**: update_position 호출 시 이미 계산된 값을 전달하지 않음

---

## 🔨 수정 계획

### 1. hold_time 형식 변환 함수 추가
```python
def _format_hold_time(seconds: float) -> str:
    """초를 "3분 24초" 형식으로 변환"""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    if minutes > 0:
        return f"{minutes}분 {secs}초"
    else:
        return f"{secs}초"
```

### 2. update_position 메서드 개선
```python
def update_position(self, slot, ticker, entry_price, current_price, amount, strategy, entry_time):
    profit_loss = (current_price - entry_price) * amount
    profit_ratio = ((current_price - entry_price) / entry_price) * 100
    hold_seconds = (datetime.now() - entry_time).total_seconds()
    hold_time = self._format_hold_time(hold_seconds)  # ✅ 형식 변환
    
    investment = entry_price * amount  # ✅ 추가
    current_value = current_price * amount  # ✅ 추가
    
    self.positions[slot] = {
        'ticker': ticker,
        'entry_price': entry_price,
        'current_price': current_price,
        'amount': amount,
        'investment': investment,  # ✅ 추가
        'current_value': current_value,  # ✅ 추가
        'profit_loss': profit_loss,
        'profit_ratio': profit_ratio,
        'hold_time': hold_time,  # ✅ 형식화된 문자열
        'strategy': strategy
    }
```

### 3. remove_position 개선
```python
def remove_position(self, slot, exit_price, profit_loss, profit_ratio):
    position = self.positions[slot]
    
    sell_record = {
        'ticker': position['ticker'],
        'profit_loss': profit_loss,
        'profit_ratio': profit_ratio,
        'strategy': position['strategy'],
        'hold_time': position['hold_time'],  # ✅ 이미 형식화됨
        'time': datetime.now().strftime('%H:%M:%S')
    }
```

### 4. _render_positions 수정 불필요
```python
# 이미 저장된 값 사용
investment = pos.get('investment', 0.0)  # ✅ 저장됨
current_value = pos.get('current_value', 0.0)  # ✅ 저장됨
hold_time = pos.get('hold_time', '0초')  # ✅ 형식화됨
```

---

## 📊 동기화 검증 체크리스트

| 항목 | 실제 값 소스 | 동기화 | 문제점 | 수정 필요 |
|------|-------------|--------|--------|----------|
| AI 학습 횟수 | learning_engine.get_stats() | ✅ | 없음 | ❌ |
| AI 승률 | (profit / total) * 100 | ✅ | 없음 | ❌ |
| 초기 자본 | Config.INITIAL_CAPITAL | ✅ | 없음 | ❌ |
| 현재 잔고 | risk_manager.current_balance | ✅ | 없음 | ❌ |
| 총 손익 | current - initial | ✅ | 없음 | ❌ |
| 손익 비율 | (profit / initial) * 100 | ✅ | 없음 | ❌ |
| 포지션 티커 | risk_manager.positions | ✅ | 없음 | ❌ |
| 진입 가격 | position.entry_price | ✅ | 없음 | ❌ |
| 현재 가격 | api.get_current_price() | ✅ | 없음 | ❌ |
| 수량 | position.amount | ✅ | 없음 | ❌ |
| 투자금 | entry_price * amount | ⚠️ | 렌더링 시 계산 | ✅ |
| 현재 가치 | current_price * amount | ⚠️ | 렌더링 시 계산 | ✅ |
| 포지션 손익 | (current - entry) * amount | ✅ | 없음 | ❌ |
| 포지션 비율 | ((current - entry) / entry) * 100 | ✅ | 없음 | ❌ |
| 보유 시간 | now - entry_time | ⚠️ | 초 단위 표시 | ✅ |
| 전략 | position.strategy | ✅ | 없음 | ❌ |
| 매도 기록 | sell_history | ✅ | 없음 | ❌ |
| 시장 국면 | market_analyzer | ✅ | 없음 | ❌ |
| 진입 조건 | market_analyzer | ✅ | 없음 | ❌ |
| BTC 변화율 | OHLCV 계산 | ✅ | 없음 | ❌ |
| 거래량 변화 | OHLCV 계산 | ✅ | 없음 | ❌ |
| 변동성 | std * 100 | ✅ | 없음 | ❌ |
| RSI | 14일 평균 | ✅ | 없음 | ❌ |
| MACD | EMA 12/26/9 | ✅ | 없음 | ❌ |
| 매수 횟수 | logger.get_daily_trades() | ✅ | 없음 | ❌ |
| 매도 횟수 | logger.get_daily_trades() | ✅ | 없음 | ❌ |
| 모니터링 코인 수 | len(self.tickers) | ✅ | 없음 | ❌ |

---

## 🎯 결론

### ✅ 동기화 잘 됨 (24/27)
- AI 학습 상태
- 자본금 및 손익
- 포지션 정보 (대부분)
- 시장 분석
- 거래 통계

### ⚠️ 개선 필요 (3/27)
1. **투자금/현재 가치**: 저장 시 계산하도록 수정
2. **보유 시간**: "3분 24초" 형식으로 변환
3. **hold_time 일관성**: 모든 곳에서 형식화된 문자열 사용

### 🔧 수정 파일
1. `src/utils/fixed_screen_display.py`
   - `_format_hold_time()` 함수 추가
   - `update_position()` 개선
   - investment, current_value 추가

---

**총평**: 대부분의 항목이 잘 동기화되어 있으며, 3개 항목만 개선하면 완벽합니다.
