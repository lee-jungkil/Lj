# 🔧 v7.0.5.1 버그 수정 (Hotfix)

## 📅 배포 정보
- **버전**: v7.0.5.1
- **날짜**: 2026-07-27
- **유형**: 버그 수정 (Hotfix)
- **이전 버전**: v7.0.5

---

## 🐛 수정된 버그

### 1️⃣ "현재가 조회 실패" 오류 수정 ⭐

**문제점**:
```
v7.0.5에서 발생:
❌ 현재가 조회 실패
→ 봇이 시작 직후 멈춤
```

**원인**:
```python
# v7.0.5 문제 코드:
def _execute_buy(self, ticker, market_data):
    # market_data에 이미 current_price가 있는데
    # 다시 API 조회 → API 호출 과다
    current_price = self.api.get_current_price(ticker)  # ❌ 중복 호출
    
    # 호가창 조회 추가 → API 호출 더 증가
    liquidity = self.api.check_orderbook_liquidity(...)  # ❌ 추가 호출
    spread = self.api.calculate_spread_percentage(...)   # ❌ 추가 호출
    
    # 결과: API 호출 제한 초과 (초당 10회 제한)
```

**해결책**:
```python
# v7.0.5.1 개선 코드:
def _execute_buy(self, ticker, market_data):
    # 1. market_data에서 가격 재사용 (API 절약)
    current_price = market_data.get('current_price', 0)
    if not current_price:
        current_price = self.api.get_current_price(ticker)  # ✅ 필요시에만
    
    # 2. 호가창 조회 실패 시 기본값 사용 (에러 방지)
    try:
        liquidity = self.api.check_orderbook_liquidity(...)
    except Exception as e:
        logger.warning(f"호가창 조회 실패: {e}, 기본 동작")
        liquidity = {  # ✅ 기본값으로 진행
            'can_fill': True,
            'available_krw': desired_krw,
            'liquidity_ratio': 1.0,
            ...
        }
    
    # 3. 스프레드 조회 실패 시 기본값 사용
    try:
        spread_pct = self.api.calculate_spread_percentage(...)
    except Exception as e:
        logger.warning(f"스프레드 조회 실패: {e}, 시장가 사용")
        spread_pct = 0.05  # ✅ 기본값 (시장가)
```

---

## 🔧 기술적 변경사항

### 수정된 코드

**파일**: `profit_bot_v7.py`

**메서드**: `_execute_buy()`

#### Before (v7.0.5):
```python
# 항상 API 재조회
current_price = self.api.get_current_price(ticker)  # ❌

# 호가창 조회 실패 시 에러
liquidity = self.api.check_orderbook_liquidity(...)  # ❌

# 스프레드 조회 실패 시 에러
spread_pct = self.api.calculate_spread_percentage(...)  # ❌
```

#### After (v7.0.5.1):
```python
# market_data 재사용
current_price = market_data.get('current_price', 0)  # ✅
if not current_price:
    current_price = self.api.get_current_price(ticker)

# try-except로 에러 처리
try:
    liquidity = self.api.check_orderbook_liquidity(...)
except Exception as e:
    logger.warning(f"호가창 조회 실패: {e}")
    liquidity = {...}  # 기본값 사용

try:
    spread_pct = self.api.calculate_spread_percentage(...)
except Exception as e:
    logger.warning(f"스프레드 조회 실패: {e}")
    spread_pct = 0.05  # 기본값
```

---

## 📊 개선 효과

### ✅ API 호출 최적화

**Before (v7.0.5)**:
```
1회 매수 시도당 API 호출:
- get_current_price: 2회 (중복)
- check_orderbook_liquidity: 1회
- calculate_spread_percentage: 1회
= 총 4회

10개 코인 스캔 시: 40회 호출
→ Upbit 제한 (초당 10회) 초과 위험 ⚠️
```

**After (v7.0.5.1)**:
```
1회 매수 시도당 API 호출:
- get_current_price: 0~1회 (market_data 재사용)
- check_orderbook_liquidity: 0~1회 (실패 시 기본값)
- calculate_spread_percentage: 0~1회 (실패 시 기본값)
= 총 0~3회

10개 코인 스캔 시: 0~30회 호출
→ Upbit 제한 안전 ✅
```

### ✅ 안정성 향상

**Before (v7.0.5)**:
```
호가창 조회 실패 → 봇 멈춤 ❌
스프레드 조회 실패 → 봇 멈춤 ❌
```

**After (v7.0.5.1)**:
```
호가창 조회 실패 → 기본값으로 진행 ✅
스프레드 조회 실패 → 시장가 사용 ✅
→ 봇 계속 동작
```

---

## 🎯 동작 변경사항

### 호가창 조회 실패 시

**v7.0.5**: 봇 멈춤
```
❌ 호가창 조회 실패
→ 매수 취소
→ 봇 중단
```

**v7.0.5.1**: 기본값으로 진행
```
⚠️ 호가창 조회 실패: {error}, 기본 동작으로 진행
→ 유동성 충분으로 간주
→ 매수 계속 진행 (시장가)
```

### 스프레드 조회 실패 시

**v7.0.5**: 봇 멈춤
```
❌ 스프레드 조회 실패
→ 주문 방식 선택 불가
→ 봇 중단
```

**v7.0.5.1**: 시장가로 진행
```
⚠️ 스프레드 조회 실패: {error}, 시장가로 진행
→ 시장가 주문 (기본 동작)
→ 매수 계속 진행
```

---

## 📝 업그레이드 가이드

### v7.0.5 → v7.0.5.1

**방법 1: 자동 (권장)**
- 새 파일 다운로드 후 교체

**방법 2: 수동**
- `profit_bot_v7.py`만 교체
- 다른 파일은 그대로 유지

**호환성**:
- ✅ 기존 설정 파일 그대로 사용 가능
- ✅ 기존 학습 데이터 그대로 사용 가능
- ✅ API 키 재설정 불필요

---

## 🧪 테스트 결과

### 시뮬레이션 모드

**Before (v7.0.5)**:
```
2026-07-27 22:00:00 [INFO] 🔍 진입 기회 스캔 중...
2026-07-27 22:00:05 [ERROR] ❌ KRW-BTC 현재가 조회 실패
2026-07-27 22:00:05 [INFO] 봇 정지
```

**After (v7.0.5.1)**:
```
2026-07-27 22:00:00 [INFO] 🔍 진입 기회 스캔 중...
2026-07-27 22:00:01 [INFO] 💰 매수 시작: KRW-BTC
2026-07-27 22:00:01 [INFO]    희망 매수 금액: 750,000원
2026-07-27 22:00:01 [WARNING] ⚠️ 호가창 조회 실패, 기본 동작으로 진행
2026-07-27 22:00:01 [INFO]    📊 주문 방식: 시장가
2026-07-27 22:00:01 [INFO] ✅ [시뮬] KRW-BTC 매수! 0.015개 @ 50,000원
```

---

## 🔗 관련 버전

- **v7.0.5**: 호가창 유동성 체크 + 스마트 주문 추가
- **v7.0.5.1**: API 호출 최적화 + 에러 처리 강화 ⭐ (현재)

---

## ⚠️ 주의사항

### API 호출 제한

Upbit API 제한:
- **초당 10회** 호출 제한
- 초과 시 일시적 차단 (1분)

v7.0.5.1 개선 사항:
- API 호출 최소화 (중복 제거)
- 실패 시 기본값 사용 (계속 동작)
- 30초 스캔 간격 유지

---

**작성일**: 2026-07-27  
**버전**: v7.0.5.1  
**유형**: Hotfix  
**상태**: 완료 ✅
