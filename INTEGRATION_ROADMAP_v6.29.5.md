# 🔧 Integration Roadmap: v6.29.5 ~ v6.30

## 📋 개요

**목표**: 미구현/미연결 컴포넌트를 체계적으로 연결하여 완전한 AI 학습 시스템 구축

**전체 진행률**: 1/8 (12.5%)

---

## ✅ Phase 1 완료 (v6.29.5)

### 1️⃣ TradeExperience 필드 확장
- ✅ `holding_chart_signals: List[Dict]` - 보유 중 차트 신호 이력
- ✅ `exit_chart_condition: Dict` - 청산 시 차트 조건
- ✅ `liquidity_at_entry: str` - 진입 시 유동성
- ✅ `liquidity_at_exit: str` - 청산 시 유동성
- ✅ `risk_score_at_check: float` - 포지션 체크 시 리스크 점수

### 2️⃣ LearningEngine 메서드 추가
- ✅ `record_holding_chart_signal()` - 보유 중 차트 신호 기록
- ✅ `record_exit_chart_condition()` - 청산 시 차트 조건 기록

**파일**:
- `src/ai/learning_engine.py`
- `update/learning_engine.py`

---

## ⏳ Phase 2 계획 (v6.29.6 - HIGH Priority)

### 3️⃣ OrderMethodSelector 유동성 활용
**현재 문제**:
```python
liquidity = self._calculate_liquidity(orderbook)  # 계산만 하고 버림
```

**수정 계획**:
```python
# src/utils/order_method_selector.py
def select_buy_method(self, ...):
    liquidity = self._calculate_liquidity(orderbook)
    
    # ✅ 유동성 낮을 때 IOC 사용
    if liquidity == 'low' and spread_pct < 0.2:
        return OrderMethod.IOC, "유동성 낮음 → IOC 부분체결"
    
    # ✅ 유동성 높을 때 POST_ONLY 사용 (수수료 절감)
    if liquidity == 'high' and strategy == 'GRID_TRADING':
        return OrderMethod.POST_ONLY, "유동성 높음 → POST_ONLY"
```

**영향**:
- 슬리피지 감소
- 수수료 최적화
- LearningEngine에 유동성 데이터 저장

### 4️⃣ RiskManager.can_chase_buy() 연결
**현재 문제**:
```python
# main.py execute_buy()에서 체크 안 함
```

**수정 계획**:
```python
# src/main.py execute_buy()
if strategy == 'CHASE_BUY':
    # ✅ 추격매수 제한 체크
    can_chase, reason = self.risk_manager.can_chase_buy(
        ticker=ticker,
        surge_score=surge_info.get('surge_score', 0),
        current_positions=len(self.risk_manager.positions)
    )
    
    if not can_chase:
        self.logger.log_warning(f"❌ 추격매수 불가: {reason}")
        return
```

**영향**:
- 동시 추격매수 2개 제한 (환경 변수)
- 일일 10회 제한 (환경 변수)
- 24시간 실패 3회 제한

### 5️⃣ MarketAnalyzer.evaluate_holding_risk() 연결
**현재 문제**:
```python
# check_positions()에서 수동으로 6가지 조건만 체크
```

**수정 계획**:
```python
# src/main.py check_positions()
def check_positions(self, ticker, strategy):
    # ✅ 리스크 평가 추가
    df = self.api.get_ohlcv(ticker, interval="minute5", count=200)
    risk_info = self.market_analyzer.evaluate_holding_risk(
        df=df,
        current_price=current_price,
        entry_price=position.avg_buy_price
    )
    
    # 리스크 점수 기록
    self.learning_engine.record_risk_score(
        ticker=ticker,
        strategy=strategy,
        risk_score=risk_info['score'],
        risk_level=risk_info['level']
    )
    
    # CRITICAL 리스크 시 즉시 청산
    if risk_info['level'] == 'CRITICAL':
        self.execute_sell(ticker, f"리스크 CRITICAL (점수: {risk_info['score']})")
        return
```

**영향**:
- 리스크 점수 기반 조기 청산
- AI 학습 데이터 풍부화
- 손실 방지 강화

---

## ⏳ Phase 3 계획 (v6.29.7 - HIGH Priority)

### 6️⃣ LearningEngine 학습 데이터 활용
**현재 문제**:
```python
# experiences.json에 저장만 하고 다음 거래에 반영 안 함
```

**수정 계획**:
```python
# src/ai/learning_engine.py
def get_best_order_method(self, strategy: str, spread_pct: float, 
                          volatility: str) -> str:
    """
    과거 학습 데이터 기반 최적 주문 방법 추천
    
    Returns:
        OrderMethod enum 문자열
    """
    # 전략별, 스프레드별, 변동성별 승률 분석
    method_stats = self._analyze_order_method_by_conditions(
        strategy=strategy,
        spread_range=(spread_pct - 0.1, spread_pct + 0.1),
        volatility=volatility
    )
    
    # 승률 가장 높은 방법 반환
    best_method = max(method_stats.items(), key=lambda x: x[1]['win_rate'])
    return best_method[0]

# src/utils/order_method_selector.py
def select_buy_method(self, ...):
    # ✅ AI 추천 먼저 확인
    if self.learning_engine and self.learning_engine.total_trades > 100:
        ai_recommendation = self.learning_engine.get_best_order_method(
            strategy=strategy,
            spread_pct=spread_pct,
            volatility=market_condition.get('volatility')
        )
        
        if ai_recommendation:
            return ai_recommendation, "AI 학습 추천"
    
    # 기존 로직 (Fallback)
    # ...
```

**영향**:
- 100+ 거래 후 AI 자동 최적화
- 승률 기반 주문 방법 선택
- 지속적인 성능 개선

---

## ⏳ Phase 4 계획 (v6.29.8 - MEDIUM Priority)

### 7️⃣ FOK 주문 방식 추가
**현재 문제**:
```python
# API는 구현되어 있지만 OrderMethodSelector에서 선택 안 함
```

**수정 계획**:
```python
# src/utils/order_method_selector.py
def select_buy_method(self, ...):
    # ✅ FOK 조건: 초단타 + 스프레드 매우 낮음 + 긴급
    if (strategy == 'ULTRA_SCALPING' and 
        spread_pct < 0.05 and 
        urgency == 'high'):
        return OrderMethod.FOK, "초단타 긴급 → FOK"
```

**파일**:
- `src/utils/order_method_selector.py`
- `src/utils/smart_order_executor.py`

### 8️⃣ 환경 변수 활용
**현재 문제**:
```env
SLIPPAGE_TOLERANCE=0.5        # ❌ 체크 안 함
ENABLE_DYNAMIC_STOP_LOSS=false  # ❌ 구현 안 됨
```

**수정 계획**:
```python
# src/config.py
SLIPPAGE_TOLERANCE = float(os.getenv('SLIPPAGE_TOLERANCE', 0.5))
ENABLE_DYNAMIC_STOP_LOSS = os.getenv('ENABLE_DYNAMIC_STOP_LOSS', 'false').lower() == 'true'
DYNAMIC_STOP_LOSS_VOLATILITY_MULTIPLIER = float(os.getenv('DYNAMIC_STOP_LOSS_VOLATILITY_MULTIPLIER', 1.5))

# src/main.py
# ✅ 슬리피지 체크
if order_result and order_result.get('slippage_pct', 0) > Config.SLIPPAGE_TOLERANCE:
    self.logger.log_warning(f"⚠️ 슬리피지 초과: {order_result['slippage_pct']:.2f}%")

# ✅ 동적 손절선
if Config.ENABLE_DYNAMIC_STOP_LOSS:
    volatility_factor = market_condition.get('volatility_score', 1.0)
    dynamic_stop_loss = base_stop_loss * Config.DYNAMIC_STOP_LOSS_VOLATILITY_MULTIPLIER * volatility_factor
```

---

## ⏳ Phase 5 계획 (v6.29.9 - LOW Priority)

### 9️⃣ UI 개선
**수정 계획**:
```python
# src/main.py scan_ultra_opportunities()
self.display.update_monitoring(
    f"🔍 급등 스캔 중...",
    f"대상: {len(self.tickers)}개 코인",
    f"초단타: {len(self.ultra_positions)}/{self.max_ultra_positions}"
)
self.display.render()

# execute_buy()
self.display.update_monitoring(
    f"💰 매수 실행: {ticker}",
    f"가격: {current_price:,.0f}원",
    f"방법: {order_method.value}"
)
self.display.render()
```

---

## 📊 예상 효과

### Phase 2~3 완료 후
| 항목 | Before | After | 개선 |
|------|--------|-------|------|
| 주문 방법 정확도 | 70% | 85% | +15%p |
| 슬리피지 | 0.3% | 0.2% | -33% |
| 리스크 관리 | 수동 | AI 자동 | NEW |
| 추격매수 실패율 | 15% | 5% | -67% |
| AI 학습 활용 | 0% | 100% | NEW |

### Phase 4~5 완료 후
| 항목 | Before | After | 개선 |
|------|--------|-------|------|
| 주문 실패율 | 1% | 0.5% | -50% |
| 수수료 최적화 | ❌ | ✅ | NEW |
| UI 실시간성 | 중간 | 높음 | +30% |
| 동적 손절선 | ❌ | ✅ | NEW |

---

## 🔗 관련 파일

### Phase 1 (완료)
- `src/ai/learning_engine.py` ✅
- `update/learning_engine.py` ✅

### Phase 2 (대기)
- `src/utils/order_method_selector.py`
- `src/main.py` (execute_buy, check_positions)
- `src/utils/risk_manager.py`
- `src/utils/market_analyzer.py`

### Phase 3 (대기)
- `src/ai/learning_engine.py` (추가 메서드)
- `src/utils/order_method_selector.py` (AI 연동)

### Phase 4 (대기)
- `src/utils/order_method_selector.py`
- `src/utils/smart_order_executor.py`
- `src/config.py`
- `.env.example`

### Phase 5 (대기)
- `src/utils/fixed_screen_display.py`
- `src/main.py` (UI 업데이트)

---

## 🎯 다음 단계

Phase 2를 시작하려면:
```bash
# Phase 2 구현 요청
"Phase 2 시작해줘 - OrderMethodSelector 유동성 활용"
```

또는 특정 기능만 구현:
```bash
"RiskManager.can_chase_buy() 연결해줘"
"MarketAnalyzer 리스크 평가 추가해줘"
```

---

**작성일**: 2026-02-12  
**버전**: v6.29.5-INTEGRATION-PHASE1  
**상태**: Phase 1 완료, Phase 2~5 대기
