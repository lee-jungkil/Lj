# 익절/손절 미실행 긴급 분석 보고서 v6.30.21

**작성일**: 2026-02-14
**심각도**: 🔴 **CRITICAL**
**문제**: 손절뿐만 아니라 **익절도 실행되지 않음**

---

## 🚨 발견된 치명적 버그

### 버그 1: should_exit() 인자 누락

**위치**: `src/main.py` 라인 1280

**현재 코드**:
```python
# ⭐ 조건 6: 기본 손익률 기준 청산 (전략별)
self.logger.log_info(f"🔍 {ticker} 조건 6 체크: 기본 익절/손절 (전략: {position.strategy})")
should_exit, exit_reason = strategy.should_exit(position.avg_buy_price, current_price)
                                                 ^^^^^^^^^^^^^^^^^^^^^^^^  ^^^^^^^^^^^
                                                 2개 인자만 전달 ❌
```

**전략 메서드 시그니처**:
```python
# src/strategies/aggressive_scalping.py 라인 131
def should_exit(self, entry_price: float, current_price: float, 
                holding_duration: float = 0, market_snapshot=None) -> Tuple[bool, str]:
                ^^^^^^^^^^^^^^^^^^^^^^^^      ^^^^^^^^^^^^^^
                필수 인자 4개 ❌
```

**문제점**:
- `holding_duration`이 전달되지 않음 → 기본값 0
- `market_snapshot`이 전달되지 않음 → None
- **AI 청산 판단 조건 우회됨** (라인 147: `if self.learning_engine and market_snapshot and holding_duration > 0`)

---

### 버그 2: 손익률 계산이 제대로 작동하는지 의심

**AggressiveScalping.should_exit() 로직**:
```python
profit_loss_ratio = (current_price - entry_price) / entry_price

# 손절 체크
if profit_loss_ratio <= -self.stop_loss:  # -0.01 (1%)
    return True, f"손절 ({profit_loss_ratio*100:.2f}%)"

# 익절 체크
if profit_loss_ratio >= self.take_profit:  # 0.015 (1.5%)
    return True, f"익절 ({profit_loss_ratio*100:.2f}%)"

return False, "Hold position"
```

**시뮬레이션**:
```python
# 예시 1: ZRO -1.26%
entry_price = 1000
current_price = 987.4
profit_loss_ratio = (987.4 - 1000) / 1000 = -0.0126 (-1.26%)
self.stop_loss = 0.01 (1%)

-0.0126 <= -0.01  → True! 손절 조건 충족! ✅
```

**이론상으로는 작동해야 함!** → 그런데 왜 안 되는가?

---

## 🔍 추가 검증 필요

### 가설 1: 전략 객체가 None
```python
# src/main.py 라인 1342
strategy = self._get_strategy_by_name(strategy_name)

if strategy:
    # check_positions 호출
else:
    self.logger.log_warning(f"⚠️ {ticker} 전략 객체 없음: {strategy_name}")
    # 여기서 종료 → should_exit 호출 안 됨!
```

**가능성**: `position.strategy` 값이 `_get_strategy_by_name()` 매핑에 없음

---

### 가설 2: check_positions()가 호출되지 않음
```python
# src/main.py 라인 1317
if not self.risk_manager.positions:
    return  # 포지션 없으면 즉시 리턴
```

**가능성**: `risk_manager.positions`가 비어있음 (동기화 문제)

---

### 가설 3: 조건 0~5에서 이미 return됨
```python
# check_positions()는 10가지 조건을 순차 체크
# 조건 0: 리스크 평가
# 조건 1: 시간 초과
# 조건 2: 트레일링 스탑
# 조건 3: 차트 신호
# 조건 4: 급락 감지
# 조건 5: 거래량 급감

# 만약 이 중 하나에서 execute_sell() 호출하면 return
# → 조건 6 도달 안 함!
```

**가능성**: 조건 0~5 중 하나가 오작동하여 잘못된 매도 또는 return

---

## 🎯 즉시 적용할 수정

### 수정 1: should_exit() 인자 추가

**위치**: `src/main.py` 라인 1280

**변경 전**:
```python
should_exit, exit_reason = strategy.should_exit(position.avg_buy_price, current_price)
```

**변경 후**:
```python
# 보유 시간 계산
hold_time = time.time() - position.entry_time if hasattr(position, 'entry_time') else 0

# 시장 스냅샷 (간단 버전)
market_snapshot = {
    'current_price': current_price,
    'entry_price': position.avg_buy_price,
    'profit_ratio': ((current_price - position.avg_buy_price) / position.avg_buy_price) * 100
}

# 전략별 청산 판단 (4개 인자 전달)
should_exit, exit_reason = strategy.should_exit(
    position.avg_buy_price, 
    current_price,
    hold_time,
    market_snapshot
)
```

---

### 수정 2: 강제 디버그 로그 추가

**위치**: `src/strategies/aggressive_scalping.py` 라인 167-172

**변경 후**:
```python
# === 기본 손절 ===
print(f"[DEBUG] {entry_price} → {current_price} | profit_loss_ratio={profit_loss_ratio:.4f} | stop_loss={self.stop_loss}")
if profit_loss_ratio <= -self.stop_loss:
    print(f"[DEBUG] 손절 조건 충족!")
    return True, f"손절 ({profit_loss_ratio*100:.2f}%)"

# === 기본 익절 ===
print(f"[DEBUG] profit_loss_ratio={profit_loss_ratio:.4f} | take_profit={self.take_profit}")
if profit_loss_ratio >= self.take_profit:
    print(f"[DEBUG] 익절 조건 충족!")
    return True, f"익절 ({profit_loss_ratio*100:.2f}%)"

print(f"[DEBUG] 청산 조건 미충족 - 보유 유지")
return False, "Hold position"
```

---

## 🔬 검증 시나리오

### 시나리오 1: 전략 객체 검증
```bash
# 로그에서 확인
"⚠️ {ticker} 전략 객체 없음: {strategy_name}"
```
→ 이 메시지 나오면 **가설 1 확정**

---

### 시나리오 2: should_exit 도달 검증
```bash
# 로그에서 확인
"🔍 {ticker} 조건 6 체크: 기본 익절/손절"
```
→ 이 메시지 안 나오면 **가설 3 확정** (조건 0~5에서 return)

---

### 시나리오 3: 손익률 계산 검증
```bash
# 로그에서 확인 (수정 2 적용 후)
"[DEBUG] 1000 → 987.4 | profit_loss_ratio=-0.0126 | stop_loss=0.01"
"[DEBUG] 손절 조건 충족!"
```
→ 이 메시지 나오는데도 매도 안 되면 **execute_sell() 문제**

---

## 📋 다음 단계

1. ✅ **즉시**: 수정 1 적용 (should_exit 인자 추가)
2. ✅ **즉시**: 수정 2 적용 (디버그 로그)
3. 🔍 **검증**: 로그 확인하여 가설 1/2/3 중 어느 것인지 확인
4. 🔧 **수정**: 확정된 원인에 따라 추가 수정
5. 🚀 **배포**: v6.30.21 배포

---

**작성 시각**: 2026-02-14
**상태**: 긴급 분석 완료, 수정 준비 중
