# 매도 미실행 디버그 패치 v6.30.18

**작성일**: 2026-02-13  
**커밋**: (pending)  
**버전**: v6.30.18-SELL-DEBUG-PATCH  
**이슈**: 보유 포지션 (BOUNTY, ZK, XLM) 여전히 매도 안됨

---

## 🚨 문제 상황

**사용자 리포트**: "여전히 매도가 안된다"

**보유 포지션**:
1. **BOUNTY** | 진입가: 30,000원 → 현재가: 28,730원 | 손익: -1,268원 (-1.33%)
2. **ZK** | 진입가: 21,000원 → 현재가: 20,930원 | 손익: -84원 (-0.40%)
3. **XLM** | 진입가: 14,700원 → 현재가: 14,822원 | 손익: +122원 (+0.83%)

**예상**: 손절 조건 도달 시 자동 매도 (BOUNTY -1.33%, ZK -0.40%)

**실제**: 매도 안됨

---

## 🔍 문제 진단

### 의심되는 원인

1. **quick_check_positions() 호출 확인 안됨**
   - PHASE 3에서 호출되고 있지만 실제 동작 여부 불명확

2. **check_positions() 실행 확인 안됨**
   - 10가지 청산 조건이 제대로 체크되는지 확인 필요

3. **로그 부족**
   - 어느 단계에서 멈추는지 파악 불가

---

## 🔧 적용된 패치

### 1. **quick_check_positions() 디버그 로그 추가**

**파일**: `src/main.py` (라인 1292-1330)

**Before**:
```python
def quick_check_positions(self):
    """빠른 포지션 체크"""
    try:
        if not self.risk_manager.positions:
            return
        
        positions_to_check = list(self.risk_manager.positions.items())
        
        for ticker, position in positions_to_check:
            try:
                current_price = self.api.get_current_price(ticker)
                if not current_price:
                    continue
                
                self.risk_manager.update_positions({ticker: current_price})
                strategy = self._get_strategy_by_name(position.strategy)
                
                if strategy:
                    self.check_positions(ticker, strategy)
```

**After** (⭐ v6.30.18):
```python
def quick_check_positions(self):
    """빠른 포지션 체크"""
    try:
        if not self.risk_manager.positions:
            return
        
        # ⭐ v6.30.18: 디버그 로그 추가
        self.logger.log_info(f"🔍 quick_check_positions 실행 - 포지션 {len(self.risk_manager.positions)}개")
        
        positions_to_check = list(self.risk_manager.positions.items())
        
        for ticker, position in positions_to_check:
            try:
                # ⭐ v6.30.18: 포지션별 체크 시작 로그
                self.logger.log_info(f"📌 {ticker} 청산 조건 체크 시작...")
                
                current_price = self.api.get_current_price(ticker)
                if not current_price:
                    self.logger.log_warning(f"⚠️ {ticker} 가격 조회 실패")
                    continue
                
                self.risk_manager.update_positions({ticker: current_price})
                strategy = self._get_strategy_by_name(position.strategy)
                
                if strategy:
                    self.logger.log_info(f"🎯 {ticker} → check_positions() 호출 (전략: {position.strategy})")
                    self.check_positions(ticker, strategy)
                else:
                    self.logger.log_warning(f"⚠️ {ticker} 전략 객체 없음: {position.strategy}")
```

---

### 2. **check_positions() 진입 로그 추가**

**파일**: `src/main.py` (라인 987-1030)

**Before**:
```python
def check_positions(self, ticker: str, strategy):
    """포지션 손익 체크 및 자동 청산"""
    if ticker not in self.risk_manager.positions:
        return
    
    position = self.risk_manager.positions[ticker]
    current_price = self.api.get_current_price(ticker)
    
    if not current_price:
        return
```

**After** (⭐ v6.30.18):
```python
def check_positions(self, ticker: str, strategy):
    """포지션 손익 체크 및 자동 청산"""
    # ⭐ v6.30.18: check_positions 진입 로그
    self.logger.log_info(f"✅ check_positions({ticker}) 진입 - 10가지 청산 조건 검사 시작")
    
    if ticker not in self.risk_manager.positions:
        self.logger.log_warning(f"⚠️ {ticker} 포지션 없음 (이미 청산됨?)")
        return
    
    position = self.risk_manager.positions[ticker]
    current_price = self.api.get_current_price(ticker)
    
    if not current_price:
        self.logger.log_warning(f"⚠️ {ticker} 현재가 조회 실패")
        return
    
    # 손익률 계산 및 로그
    profit_ratio = ((current_price - position.avg_buy_price) / position.avg_buy_price) * 100
    self.logger.log_info(
        f"💰 {ticker} 현재 상태: "
        f"진입가 {position.avg_buy_price:,.0f}원 → "
        f"현재가 {current_price:,.0f}원 | "
        f"손익률 {profit_ratio:+.2f}%"
    )
```

---

### 3. **조건 6 (기본 익절/손절) 디버그 로그 추가**

**파일**: `src/main.py` (라인 1278-1290)

**Before**:
```python
# 조건 6: 기본 손익률 기준 청산
should_exit, exit_reason = strategy.should_exit(position.avg_buy_price, current_price)

if should_exit:
    self.execute_sell(ticker, exit_reason)
```

**After** (⭐ v6.30.18):
```python
# ⭐ 조건 6: 기본 손익률 기준 청산 (전략별)
self.logger.log_info(f"🔍 {ticker} 조건 6 체크: 기본 익절/손절 (전략: {position.strategy})")
should_exit, exit_reason = strategy.should_exit(position.avg_buy_price, current_price)

if should_exit:
    self.logger.log_info(f"🚨 {ticker} 매도 트리거! 사유: {exit_reason}")
    self.execute_sell(ticker, exit_reason)
    return
else:
    self.logger.log_info(f"✅ {ticker} 청산 조건 미충족 - 보유 유지")
```

---

### 4. **중복 코드 제거**

**Before**:
```python
if should_exit:
    self.logger.log_info(f"🚨 {ticker} 매도 트리거!")
    self.execute_sell(ticker, exit_reason)
    return
else:
    self.logger.log_info(f"✅ {ticker} 청산 조건 미충족")

if should_exit:  # ⚠️ 중복!
    self.execute_sell(ticker, exit_reason)
```

**After** (수정됨):
```python
if should_exit:
    self.logger.log_info(f"🚨 {ticker} 매도 트리거!")
    self.execute_sell(ticker, exit_reason)
    return
else:
    self.logger.log_info(f"✅ {ticker} 청산 조건 미충족")
```

---

## 📊 예상 로그 출력

### 정상 동작 시 예상 로그

```
[09:13:00] 🔍 quick_check_positions 실행 - 포지션 3개
[09:13:00] 📌 KRW-BOUNTY 청산 조건 체크 시작...
[09:13:00] 🎯 KRW-BOUNTY → check_positions() 호출 (전략: aggressive_scalping)
[09:13:00] ✅ check_positions(KRW-BOUNTY) 진입 - 10가지 청산 조건 검사 시작
[09:13:00] 💰 KRW-BOUNTY 현재 상태: 진입가 30,000원 → 현재가 28,730원 | 손익률 -1.33%
[09:13:00] 🔍 KRW-BOUNTY 조건 6 체크: 기본 익절/손절 (전략: aggressive_scalping)
[09:13:00] 🚨 KRW-BOUNTY 매도 트리거! 사유: 손절 -1.5%
[09:13:00] 💸 KRW-BOUNTY 매도 실행...
```

### 문제 발생 시 예상 로그

#### 케이스 1: quick_check_positions() 호출 안됨
```
(로그 없음)
```

#### 케이스 2: check_positions() 진입 안됨
```
[09:13:00] 🔍 quick_check_positions 실행 - 포지션 3개
[09:13:00] 📌 KRW-BOUNTY 청산 조건 체크 시작...
[09:13:00] ⚠️ KRW-BOUNTY 전략 객체 없음: aggressive_scalping
```

#### 케이스 3: 청산 조건 미충족
```
[09:13:00] 🔍 quick_check_positions 실행 - 포지션 3개
[09:13:00] 📌 KRW-BOUNTY 청산 조건 체크 시작...
[09:13:00] 🎯 KRW-BOUNTY → check_positions() 호출
[09:13:00] ✅ check_positions(KRW-BOUNTY) 진입
[09:13:00] 💰 KRW-BOUNTY 현재 상태: 손익률 -1.33%
[09:13:00] 🔍 KRW-BOUNTY 조건 6 체크: 기본 익절/손절
[09:13:00] ✅ KRW-BOUNTY 청산 조건 미충족 - 보유 유지
```

---

## 🎯 다음 단계

### 사용자 액션

1. **봇 재시작**
   ```bash
   cd C:\Users\admin\Downloads\Lj-main
   git pull origin main
   python -m src.main --mode live
   ```

2. **로그 모니터링**
   - `trading_logs/` 폴더의 최신 로그 파일 확인
   - 위 예상 로그 패턴과 비교

3. **문제 케이스 식별**
   - 케이스 1: PHASE 3 실행 안됨 → 메인 루프 문제
   - 케이스 2: 전략 객체 없음 → `_get_strategy_by_name()` 문제
   - 케이스 3: 청산 조건 미충족 → 전략 설정 문제

---

## ✅ 변경 사항 요약

| 파일 | 라인 | 변경 내용 |
|------|------|----------|
| `src/main.py` | 1292-1330 | quick_check_positions() 디버그 로그 추가 |
| `src/main.py` | 987-1030 | check_positions() 진입 로그 추가 |
| `src/main.py` | 1278-1290 | 조건 6 디버그 로그 + 중복 코드 제거 |
| `update/main.py` | 전체 | src/main.py와 동기화 |

---

## 🔍 예상 문제 및 해결

### 문제 1: 전략 객체 못 찾음
**증상**: "⚠️ 전략 객체 없음" 로그  
**원인**: `_get_strategy_by_name()` 매핑 오류  
**해결**: 전략 이름 매핑 확인 및 수정

### 문제 2: 손절 기준 설정 오류
**증상**: "청산 조건 미충족" 로그 (손실 중인데도)  
**원인**: 전략별 손절 비율 설정 오류  
**해결**: Config.py 손절 비율 확인

### 문제 3: PHASE 3 실행 안됨
**증상**: 로그 자체가 없음  
**원인**: 메인 루프 타이밍 문제  
**해결**: wait_time 로직 재검토

---

**패치 완료일**: 2026-02-13  
**다음 버전 예정**: v6.30.19 (로그 분석 후 근본 원인 수정)
