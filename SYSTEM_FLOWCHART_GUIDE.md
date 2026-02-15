# Upbit AutoProfit Bot - System Flowchart Guide
# 업비트 자동매매 봇 - 시스템 흐름도 가이드

**Version**: v6.30.63-DIAGNOSTIC-TOOLS  
**Date**: 2026-02-15

---

## 📊 Overview / 개요

This document provides comprehensive visual flowcharts and architecture diagrams for the Upbit AutoProfit Bot system.

이 문서는 업비트 자동매매 봇의 종합적인 시각적 흐름도와 아키텍처 다이어그램을 제공합니다.

---

## 🎯 Diagram 1: Main System Flowchart / 메인 시스템 흐름도

![Main System Flowchart](https://www.genspark.ai/api/files/s/18OvhOeH?cache_control=3600)

### Description / 설명

이 다이어그램은 봇의 전체 실행 흐름을 보여줍니다:

#### 1. START Section (초기화)
- **Load Config** - .env 파일에서 설정 읽기
- **Initialize Strategies** - 4가지 전략 초기화
  - Aggressive Scalping (공격적 스캘핑)
  - Conservative Hold (보수적 보유)
  - Mean Reversion (평균회귀)
  - Grid Trading (그리드)
- **Setup Components** - 주요 컴포넌트 설정
  - Risk Manager (리스크 관리자)
  - Holding Protector (보유 보호기)
  - Smart Order Executor (스마트 주문 실행기)

#### 2. MAIN LOOP Section (메인 루프)
무한 반복 사이클:
- **Market Data Collection** - OHLCV, 가격, 거래량 수집
- **Signal Generation** - 4가지 전략에서 매수/매도 신호 생성
- **Position Check** - 현재 포지션 상태 확인

#### 3. BUY EXECUTION Branch (매수 실행)
- Strategy Signal Analysis → 전략 신호 분석
- Risk Check → 리스크 체크 (최대 포지션, 자본 한도)
- Smart Order Selection → 시장가/지정가 선택
- Position Recording → 포지션 기록
- UI Update → 화면 업데이트

#### 4. SELL EXECUTION Branch (매도 실행)
- **[EXECUTE-SELL]** Function Call → 함수 호출
- Position Validation → 포지션 존재 확인
- Current Price Fetch → 현재가 조회
- Exit Reason Determination → 매도 사유 결정
  - Time Over (시간 초과)
  - Take Profit (익절)
  - Stop Loss (손절)
  - Force Sell (강제매도)
- **holding_protector.close_bot_position()** → 보유 보호기 청산
- **risk_manager.close_position()** → 리스크 관리자 청산
- UI Position Remove → 화면에서 포지션 제거
- Trade Logging → 거래 기록

#### 5. MONITORING Section (모니터링)
- Display Update → 화면 갱신
- Performance Tracking → 성과 추적
- Error Handling → 오류 처리

---

## 🔴 Diagram 2: Detailed Sell Execution Flow / 상세 매도 실행 흐름

![Sell Execution Flow](https://www.genspark.ai/api/files/s/6hAGrR8t?cache_control=3600)

### Description / 설명

매도 실행 프로세스의 상세 흐름:

#### TOP: Sell Triggers / 매도 트리거
```
┌─────────────────────────────────────────┐
│ Time Over    │ Take Profit │ Stop Loss  │
│ (4/8분 초과)  │ (익절 달성)  │ (손절 발동) │
└─────────────────────────────────────────┘
              ↓
         Force Sell (강제매도)
```

#### MIDDLE: Execute Sell Function / 매도 함수 실행

**Step 1: Function Entry**
```python
[EXECUTE-SELL] execute_sell() called - ticker: KRW-XXX
```

**Step 2: Position Validation**
```python
[EXECUTE-SELL] Position check: True/False
if not exists → log error → ABORT
```

**Step 3: Current Price Fetch**
```python
Retry Loop (최대 3회):
  try: fetch current price
  except: wait 1s, retry
if failed after 3 attempts → ABORT
```

**Step 4: Profit/Loss Calculation**
```python
profit_loss = (current_price - avg_buy_price) * amount
profit_ratio = (profit_loss / invested_capital) * 100
```

**Step 5: Exit Reason Parsing**
```python
if "Time" in reason → ExitReason.TIME_OVER
elif "익절" in reason → ExitReason.TAKE_PROFIT
elif "손절" in reason → ExitReason.STOP_LOSS
else → ExitReason.FORCED
```

**Step 6: Smart Order Selection**
```python
order_method = order_method_selector.select_sell_method(
    exit_reason, profit_ratio, spread, market_condition
)
```

#### BOTTOM: Position Cleanup / 포지션 청산

**Step 1: Holding Protector Cleanup**
```python
try:
    [EXECUTE-SELL] holding_protector.close_bot_position() called...
    bot_profit_loss = holding_protector.close_bot_position(ticker, amount, price)
    [EXECUTE-SELL] ✅ holding_protector cleanup complete, P/L: +84
except Exception as e:
    [EXECUTE-SELL] ❌ holding_protector cleanup failed: {e}
    print(traceback.format_exc())
```

**Step 2: Risk Manager Cleanup**
```python
try:
    [EXECUTE-SELL] risk_manager.close_position() called...
    profit_loss = risk_manager.close_position(ticker, price)
    [EXECUTE-SELL] ✅ risk_manager cleanup complete, P/L: +84
except Exception as e:
    [EXECUTE-SELL] ❌ risk_manager cleanup failed: {e}
```

**Step 3: UI Update**
```python
[EXECUTE-SELL] display.remove_position() called...
display.remove_position(slot, price, profit_loss, profit_ratio)
[EXECUTE-SELL] ✅ Position removed from UI
```

**Step 4: Trade Logging**
```python
logger.log_trade(
    action='SELL',
    ticker=ticker,
    price=current_price,
    amount=sell_amount,
    strategy=strategy,
    reason=reason,
    profit_loss=profit_loss,
    balance=current_balance
)
```

#### ERROR HANDLING / 오류 처리

**Price Fetch Failure**
```
Cannot fetch price after 3 retries
→ Log error
→ Abort sell
→ Position remains
```

**Position Not Found**
```
Ticker not in positions
→ Log warning
→ Abort sell
```

**Cleanup Failure**
```
Exception in cleanup
→ Print stack trace
→ Log error
→ Continue (partial cleanup)
```

---

## 🏗️ Diagram 3: System Architecture / 시스템 아키텍처

![System Architecture](https://www.genspark.ai/api/files/s/8e6t0GXu?cache_control=3600)

### Description / 설명

7계층 아키텍처:

#### Layer 1: External Services (외부 서비스)
```
☁️ Upbit API
   - Market Data (시장 데이터)
   - Order Execution (주문 실행)
   - Balance Query (잔고 조회)

☁️ OpenAI API
   - AI Analysis (AI 분석)
   - Pattern Recognition (패턴 인식)

⏰ System Clock
   - Time Triggers (시간 트리거)
   - Scheduling (스케줄링)
```

#### Layer 2: Presentation Layer (표현 계층)
```
📺 Terminal Display UI
   - Position List (포지션 목록)
   - Real-time Updates (실시간 업데이트)

📊 Position Monitor
   - Hold Time (보유 시간)
   - P/L Tracking (손익 추적)

📈 Performance Dashboard
   - Win Rate (승률)
   - Total P/L (총 손익)

📝 Log Output
   - Debug Logs (디버그 로그)
   - Error Messages (오류 메시지)
```

#### Layer 3: Application Layer (애플리케이션 계층)
```
🎮 main.py (AutoProfitBot)
   - Central Controller (중앙 제어)
   - Orchestration (오케스트레이션)

⚙️ Config Manager
   - .env Loading (.env 로딩)
   - Settings Validation (설정 검증)

🔄 Loop Controller
   - Main Cycle (메인 사이클)
   - Timing Control (타이밍 제어)
```

#### Layer 4: Strategy Layer (전략 계층)
```
🚀 Aggressive Scalping
   - 4분 타임아웃
   - 0.8% 익절 목표

🛡️ Conservative Hold
   - 8분 타임아웃
   - 1.2% 익절 목표

📉 Mean Reversion
   - 30분 타임아웃
   - 평균 회귀 감지

📊 Grid Trading
   - 1시간 타임아웃
   - 구간별 매매

🔀 Strategy Selector
   - Signal Routing (신호 라우팅)
   - Priority Management (우선순위 관리)
```

#### Layer 5: Execution Layer (실행 계층)
```
💰 execute_buy()
   - Buy Order (매수 주문)
   - Position Recording (포지션 기록)

💸 execute_sell()
   - Sell Order (매도 주문)
   - Position Cleanup (포지션 청산)

🎯 Smart Order Executor
   - Market Order (시장가)
   - Limit Order (지정가)
   - Order Type Selection (주문 타입 선택)

🔧 Order Method Selector
   - Entry Method (진입 방법)
   - Exit Method (청산 방법)
```

#### Layer 6: Management Layer (관리 계층)
```
🎲 Risk Manager
   - Position Tracking (포지션 추적)
   - Limit Enforcement (한도 강제)
   - Portfolio Balance (포트폴리오 균형)

🛡️ Holding Protector
   - Position Safety (포지션 안전)
   - Hold Prevention (보유 방지)

💼 Portfolio Manager
   - Balance Tracking (잔고 추적)
   - Asset Allocation (자산 배분)

❌ Failed Order Tracker
   - Retry Management (재시도 관리)
   - Failure Counting (실패 카운팅)
```

#### Layer 7: Data Layer (데이터 계층)
```
💾 Position Storage
   - ticker: str
   - amount: float
   - avg_buy_price: float
   - strategy: str
   - entry_time: datetime

📜 Trade History Logger
   - Trade Records (거래 기록)
   - CSV Export (CSV 내보내기)

📊 Performance Metrics
   - Win Rate (승률)
   - Profit/Loss (손익)
   - Sharpe Ratio (샤프 비율)

⚠️ Cache System (.pyc files)
   - Compiled Bytecode (컴파일된 바이트코드)
   - **WARNING**: Can cause old code execution
   - **SOLUTION**: Delete with EMERGENCY_FIX_SIMPLE.bat
```

---

## 🔄 Data Flow / 데이터 흐름

### Buy Flow (매수 흐름)
```
External Services (Upbit API)
        ↓
Application Layer (main.py)
        ↓
Strategy Layer (signal generation)
        ↓
Execution Layer (execute_buy)
        ↓
Management Layer (risk_manager.add_position)
        ↓
Data Layer (position storage)
        ↓
Presentation Layer (UI update)
```

### Sell Flow (매도 흐름)
```
Application Layer (check_positions)
        ↓
Execution Layer (execute_sell)
        ↓
Management Layer (holding_protector + risk_manager)
        ↓
Data Layer (position removal + trade logging)
        ↓
Presentation Layer (UI update)
        ↓
External Services (Upbit API - order execution)
```

---

## 🐛 Common Issues / 일반적인 문제

### Issue 1: Sell Not Executing / 매도 미실행

**Symptom**:
```
[FORCE-SELL] ✅ 매도 주문 완료!
(But no [EXECUTE-SELL] logs)
```

**Root Cause**:
```
Data Layer → Cache System (.pyc)
Old compiled code is executing
```

**Solution**:
```
1. Stop bot
2. Run EMERGENCY_FIX_SIMPLE.bat
3. Start with: python -B -u -m src.main --mode paper
```

### Issue 2: Strategy Not Found / 전략을 찾을 수 없음

**Symptom**:
```
AttributeError: 'AutoProfitBot' has no attribute 'aggressive_scaling'
```

**Root Cause**:
```
Strategy Layer → Typo in strategy name
(aggressive_scaling vs aggressive_scalping)
```

**Solution**:
```
Strategy Selector automatically maps typos:
'aggressive_scaling' → 'aggressive_scalping'
```

### Issue 3: Position Not Clearing / 포지션 미청산

**Symptom**:
```
[EXECUTE-SELL] called
(But position remains in UI)
```

**Root Cause**:
```
Management Layer → Cleanup function not called
OR
Data Layer → Position not removed
```

**Solution**:
```
Check logs for:
- [EXECUTE-SELL] holding_protector cleanup complete
- [EXECUTE-SELL] risk_manager cleanup complete
- [EXECUTE-SELL] Position removed from UI

If missing, check error logs for stack trace.
```

---

## 📋 Debug Log Checklist / 디버그 로그 체크리스트

### Complete Sell Execution Should Show:

```
✅ [EXECUTE-SELL] execute_sell() called - ticker: KRW-XXX
✅ [EXECUTE-SELL] Position exists: True
✅ [EXECUTE-SELL] ✅ Found position: KRW-XXX, amount: 60.6
✅ [EXECUTE-SELL] Current price: 16084 KRW
✅ [EXECUTE-SELL] Profit ratio: +0.33%
✅ [EXECUTE-SELL] Exit reason: TIME_OVER
✅ [EXECUTE-SELL] Order method: MARKET
✅ [EXECUTE-SELL] ========== Position cleanup start ==========
✅ [EXECUTE-SELL] holding_protector.close_bot_position() called...
✅ [EXECUTE-SELL] ✅ holding_protector cleanup complete, P/L: +84
✅ [EXECUTE-SELL] risk_manager.close_position() called...
✅ [EXECUTE-SELL] ✅ risk_manager cleanup complete, P/L: +84
✅ [EXECUTE-SELL] Remaining positions: ['KRW-AAVE', 'KRW-TIA']
✅ [EXECUTE-SELL] ========== UI update start ==========
✅ [EXECUTE-SELL] display.remove_position() called...
✅ [EXECUTE-SELL] ✅ Position removed from UI
✅ [EXECUTE-SELL] Trade logged successfully
```

### If Any Line is Missing:

**Missing before "cleanup start"**:
- Check cache (run EMERGENCY_FIX_SIMPLE.bat)

**Missing in cleanup section**:
- Check error logs for exception
- Look for stack trace

**Missing in UI update**:
- Check display module initialization
- Verify position exists in display.positions

---

## 🔗 Related Documents / 관련 문서

- **QUICK_FIX.md** - 3단계 간단 수정
- **TROUBLESHOOTING_ENGLISH.md** - 완전한 문제 해결 가이드
- **README_WHAT_TO_DO_NOW.md** - 양국어 빠른 시작
- **RELEASE_NOTES_v6.30.63.md** - 릴리스 노트
- **FINAL_SOLUTION_KR_EN.md** - 최종 솔루션

---

## 📞 Support / 지원

**GitHub Issues**: https://github.com/lee-jungkil/Lj/issues

Include when reporting:
- Screenshot of the flowchart section causing issues
- Relevant log outputs
- VERSION.txt content
- DIAGNOSTIC_CHECK.bat results

---

**Version**: v6.30.63-DIAGNOSTIC-TOOLS  
**Last Updated**: 2026-02-15  
**Diagrams Generated**: 2026-02-15
