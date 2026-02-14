# 🚀 Advanced Order System v6.29 - Phase 1 Complete

**Version**: v6.29-ADVANCED-ORDER-SYSTEM-PHASE1  
**Release Date**: 2026-02-12  
**Priority**: 🔴 **HIGH** - 매수/매도 주문 방식 확장 및 자동화  
**Status**: 🔄 Phase 1 완료 (3/9 tasks)

---

## 📋 Phase 1 완료 항목 (3/9)

### ✅ 1. Upbit API 확장 (9가지 주문 방식)

**파일**: `src/upbit_api.py`

**추가된 메서드**:
1. `buy_best_order()` - 최유리 매수 (1호가 + IOC)
2. `sell_best_order()` - 최유리 매도
3. `buy_limit_ioc()` - IOC 지정가 매수 (부분 체결 허용)
4. `sell_limit_ioc()` - IOC 지정가 매도
5. `adjust_price_to_tick()` - 호가 단위 자동 조정
6. `calculate_spread_percentage()` - 호가창 스프레드 계산

**호가 단위 규칙**:
```python
100만원 이상: 1,000원
50만~100만: 500원
10만~50만: 100원
1만~10만: 50원
1천~1만: 10원
100~1천: 5원
10~100: 1원
10원 미만: 0.1원
```

**사용 예시**:
```python
# 최유리 매수 (슬리피지 최소화)
result = api.buy_best_order('KRW-BTC', 110000)

# IOC 매수 (부분 체결 허용)
result = api.buy_limit_ioc('KRW-BTC', 55000000, 0.002)

# 스프레드 계산
spread = api.calculate_spread_percentage('KRW-BTC')
# → 0.12% (낮은 스프레드)
```

---

### ✅ 2. SurgeDetector (급등 감지 시스템)

**파일**: `src/utils/surge_detector.py`

**핵심 기능**:
1. **급등 감지**: 1분/5분/15분 상승률 + 거래량 분석
2. **점수 계산**: 급등 점수 0~100점
3. **신뢰도 평가**: 0.0~1.0 신뢰도
4. **추격매수 조건 판단**: 5가지 조건 검증
5. **실패 이력 관리**: 24시간 내 3회 제한

**급등 점수 공식**:
```
surge_score = 
    (1분 상승률 ≥ 1.5%) × 10 +
    (5분 상승률 ≥ 3.0%) × 5 +
    (15분 상승률 ≥ 5.0%) × 2 +
    (거래량 ≥ 평균 2배) × 20
```

**추격매수 조건** (6가지):
1. ✅ 급등 점수 ≥ 50
2. ✅ 거래량 비율 ≥ 2.0
3. ✅ 신뢰도 ≥ 0.7
4. ✅ 1분 모멘텀 ≥ 1.5%
5. ✅ 시장 국면 ≠ 약세장
6. ✅ 24시간 내 3회 미만 실패

**사용 예시**:
```python
from src.utils.surge_detector import surge_detector

# 급등 감지
surge_info = surge_detector.detect_surge('KRW-BTC', api)

if surge_info:
    print(f"급등 감지!")
    print(f"  점수: {surge_info['surge_score']:.1f}")
    print(f"  1분 상승: {surge_info['change_1m']:.2f}%")
    print(f"  거래량: {surge_info['volume_ratio']:.1f}x")
    print(f"  신뢰도: {surge_info['confidence']:.2f}")
    
    # 추격매수 가능 여부
    can_chase, reason = surge_detector.can_chase_buy('KRW-BTC', surge_info)
    print(f"  추격매수: {can_chase} - {reason}")
```

---

### ✅ 3. OrderMethodSelector (자동 주문 방법 선택)

**파일**: `src/utils/order_method_selector.py`

**핵심 기능**:
1. **매수 방법 자동 선택**: 전략·시장 조건 기반 7가지 케이스
2. **매도 방법 자동 선택**: 청산 사유 기반 11가지 케이스
3. **지정가 오프셋 계산**: 전략별 가격 조정
4. **Fallback 지원**: 타임아웃 시 시장가 전환

**매수 Decision Tree**:
```
1. 추격매수 → market (즉시 진입)
2. Ultra Scalping + 스프레드 < 0.1% → best (슬리피지 최소)
3. Aggressive + 고변동성 → market
4. Aggressive + 정상 → limit -0.1%
5. Conservative → best + IOC
6. Mean Reversion → limit -0.5%
7. Grid Trading → post_only
```

**매도 Decision Tree**:
```
1. 손절 → market (즉시)
2. 긴급 → market (급락 탈출)
3. 익절 + 추격/초단타 → market
4. 익절 + 낮은 스프레드 → best
5. 익절 + 일반 → limit +0.1%
6. 트레일링 스탑 → market
7. 시간 초과 + 수익 → best
8. 시간 초과 + 손실 → market
9. 차트 신호 + 수익 ≥ 1% → best
10. 차트 신호 + 낮은 수익 → limit +0.3%
11. 거래량 급감 + 수익 > 0.5% → market
```

**사용 예시**:
```python
from src.utils.order_method_selector import order_method_selector, ExitReason

# 매수 방법 선택
method, reason = order_method_selector.select_buy_method(
    ticker='KRW-BTC',
    strategy='AGGRESSIVE_SCALPING',
    market_condition={'volatility': 'high', 'trend': 'up'},
    spread_pct=0.15,
    is_chase=False
)
print(f"매수 방법: {method.value} - {reason}")
# → market - 공격적 전략 + 고변동성 → 시장가

# 매도 방법 선택
method, reason = order_method_selector.select_sell_method(
    ticker='KRW-BTC',
    strategy='ULTRA_SCALPING',
    exit_reason=ExitReason.TAKE_PROFIT,
    spread_pct=0.08,
    profit_ratio=2.1,
    market_condition={}
)
print(f"매도 방법: {method.value} - {reason}")
# → market - 익절 (추격/초단타) → 즉시 청산
```

---

## 📊 Phase 1 구현 완료도

| 항목 | 상태 | 파일 | 라인 수 |
|------|------|------|---------|
| Upbit API 확장 | ✅ 완료 | `src/upbit_api.py` | +253 |
| SurgeDetector | ✅ 완료 | `src/utils/surge_detector.py` | 275 |
| OrderMethodSelector | ✅ 완료 | `src/utils/order_method_selector.py` | 283 |
| SmartOrderExecutor | ⏳ 대기 | - | - |
| check_positions() 확장 | ⏳ 대기 | - | - |
| LearningEngine 확장 | ⏳ 대기 | - | - |
| execute_buy/sell() 통합 | ⏳ 대기 | - | - |
| 환경 변수 추가 | ⏳ 대기 | - | - |
| 텔레그램 알림 개선 | ⏳ 대기 | - | - |

---

## 🎯 Phase 2 예정 항목 (6/9)

### 4. SmartOrderExecutor (스마트 주문 실행기)
- 재시도 로직 (최대 3회)
- Fallback 지원 (지정가 → 시장가)
- 호가 단위 자동 조정
- 주문 상태 모니터링

### 5. check_positions() 확장 (6가지 청산 조건)
- 손익 기반 청산 (손절/익절)
- 트레일링 스탑 (최고가 대비 -1%)
- 차트 신호 기반 청산
- 시간 초과 청산
- 급락 감지 청산 (1분 내 -1.5%)
- 거래량 급감 청산

### 6. LearningEngine 메타데이터 확장
- 주문 방법 기록 (`order_method`)
- 청산 사유 기록 (`exit_reason`)
- 급등 정보 기록 (`surge_info`)
- 주문 방법별 성과 분석

### 7. execute_buy/sell() 통합
- OrderMethodSelector 연동
- SmartOrderExecutor 연동
- SurgeDetector 연동 (추격매수)
- 학습 엔진 메타데이터 저장

### 8. 환경 변수 추가
```env
# 주문 설정
BUY_ORDER_TYPE=auto
SELL_ORDER_TYPE=auto
SLIPPAGE_TOLERANCE=0.5
ORDER_MAX_RETRIES=3
LIMIT_ORDER_TIMEOUT=5

# 추격매수
ENABLE_CHASE_BUY=true
SURGE_THRESHOLD_1M=1.5
CHASE_TAKE_PROFIT=2.0
CHASE_STOP_LOSS=-3.0
CHASE_MAX_HOLD_TIME=300

# 트레일링 스탑
ENABLE_TRAILING_STOP=true
TRAILING_STOP_OFFSET=1.0

# 전략별 최대 보유 시간
MAX_HOLD_TIME_CHASE=300
MAX_HOLD_TIME_ULTRA=600
MAX_HOLD_TIME_AGGRESSIVE=1800
```

### 9. 텔레그램 알림 개선
- 주문 방법 표시
- 급등 점수 표시 (추격매수 시)
- 청산 사유 표시
- 신뢰도 표시

---

## 🧪 테스트 시나리오 (Phase 1)

### 시나리오 1: 급등 감지 + 추격매수
```
1. BTC 1분 상승률 +2.0%, 거래량 3.5배
2. surge_detector.detect_surge() → surge_score: 78, confidence: 0.92
3. can_chase_buy() → True, "추격매수 조건 충족"
4. select_buy_method(is_chase=True) → market, "추격매수 - 즉시 진입 필수"
5. api.buy_market_order() → 시장가 즉시 체결
```

### 시나리오 2: 초단타 익절 청산
```
1. 포지션: ETH, 전략: ULTRA_SCALPING, 수익률 +2.1%
2. select_sell_method(exit_reason=TAKE_PROFIT) → market
3. api.sell_market_order() → 즉시 청산
4. 사유: "익절 (추격/초단타) → 즉시 청산"
```

### 시나리오 3: 평균회귀 지정가 매수
```
1. 전략: MEAN_REVERSION, 스프레드: 0.25%
2. select_buy_method() → limit, "평균회귀 전략 → 지지선 지정가 -0.5%"
3. get_limit_price_offset() → -0.5% offset
4. api.buy_limit_order(price = current * 0.995)
```

---

## 📦 설치 및 사용

### 새 파일 추가
```bash
src/upbit_api.py              # 확장됨 (+253 lines)
src/utils/surge_detector.py   # 신규 (275 lines)
src/utils/order_method_selector.py  # 신규 (283 lines)
```

### Import 예시
```python
# Surge Detector
from src.utils.surge_detector import surge_detector

# Order Method Selector
from src.utils.order_method_selector import (
    order_method_selector,
    OrderMethod,
    ExitReason
)

# Upbit API (확장)
from src.upbit_api import UpbitAPI
api = UpbitAPI(access_key, secret_key)
```

---

## 🔗 다운로드 링크

- **GitHub 프로젝트**: https://github.com/lee-jungkil/Lj
- **전체 ZIP**: https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
- **빠른 업데이트**: https://raw.githubusercontent.com/lee-jungkil/Lj/main/download_update.bat
- **Phase 1 문서**: https://github.com/lee-jungkil/Lj/blob/main/ADVANCED_ORDER_SYSTEM_PHASE1_v6.29.md

---

## 🎯 다음 단계 (Phase 2)

1. **SmartOrderExecutor** 구현 (재시도, Fallback)
2. **check_positions()** 확장 (6가지 청산 조건)
3. **LearningEngine** 메타데이터 확장
4. **execute_buy/sell()** 통합
5. **환경 변수** 추가
6. **텔레그램 알림** 개선

---

## 📝 버전 히스토리

| 버전 | 날짜 | 주요 변경 | 완료도 |
|------|------|-----------|--------|
| v6.28 | 2026-02-12 | 손익 동기화 수정 | - |
| **v6.29 Phase1** | **2026-02-12** | **고급 주문 시스템 Phase 1 (3/9)** | **33%** |

---

**Last Updated**: 2026-02-12  
**Phase**: 1/3 (Foundation)  
**Next Phase**: SmartOrderExecutor + check_positions() 확장
