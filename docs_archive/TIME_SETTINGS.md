# ⏱️ 감지 및 포지션 시간 설정 가이드

> **모든 시간 설정을 한눈에 파악하고 조정하는 완전 가이드**

---

## 📚 목차

1. [시간 설정 개요](#시간-설정-개요)
2. [메인 봇 시간 설정](#메인-봇-시간-설정)
3. [급등/급락 감지 설정](#급등급락-감지-설정)
4. [초단타 전략 설정](#초단타-전략-설정)
5. [일반 전략 설정](#일반-전략-설정)
6. [시간 설정 변경 방법](#시간-설정-변경-방법)
7. [권장 설정](#권장-설정)

---

## 🎯 시간 설정 개요

### 시스템 구조

```
┌─────────────────────────────────────────────┐
│           AutoProfit Bot 메인 루프          │
└─────────────────┬───────────────────────────┘
                  │
      ┌───────────┴───────────┬──────────────┐
      │                       │              │
      ▼                       ▼              ▼
┌──────────┐          ┌──────────┐    ┌──────────┐
│ 전체스캔 │          │빠른체크  │    │ 급등감지 │
│  5분     │          │  1분     │    │  1초 ⚡  │
└──────────┘          └──────────┘    └──────────┘
      ↓                     ↓              ↓
  신규진입              포지션관리      초단타진입
```

### 주요 시간 설정 위치

| 설정 항목 | 파일 위치 | 현재 값 | 설명 |
|----------|----------|---------|------|
| 전체 스캔 주기 | `src/main.py:130` | **300초 (5분)** | 모든 코인 스캔 |
| 빠른 체크 주기 | `src/main.py:131` | **60초 (1분)** | 포지션 체크 |
| 급등 감지 주기 | `src/main.py:132` | **1초** ⚡ | 초고속 감지 |
| 최소 거래 간격 | `src/main.py:127` | **60초** | 중복 거래 방지 |
| 급등 감지 쿨다운 | `src/utils/surge_detector.py:38` | **300초 (5분)** | 중복 감지 방지 |
| 초단타 최대 보유 | `src/config.py:84` | **300초 (5분)** | 강제 청산 |

---

## 🤖 메인 봇 시간 설정

### 파일: `src/main.py`

#### 1. 스캔 주기 설정 (130~132줄)

```python
# ⭐ 하이브리드 + 초단타 설정
self.full_scan_interval = 300  # 5분 - 전체 스캔
self.quick_check_interval = 60  # 1분 - 포지션 체크
self.surge_scan_interval = 1  # ⭐ 1초 - 급등감지 (초고속!)
```

**역할:**
- `full_scan_interval` (300초 = 5분)
  - 모든 코인을 스캔하여 신규 진입 기회 탐색
  - 일반 전략 (aggressive, conservative, mean_reversion, grid_trading) 적용
  
- `quick_check_interval` (60초 = 1분)
  - 현재 보유 중인 포지션 빠른 체크
  - 손익 확인 및 청산 조건 검사
  
- `surge_scan_interval` (1초) ⚡
  - 급등/급락 실시간 감지
  - 초단타 진입 기회 포착
  - **가장 빠른 주기!**

#### 2. 최소 거래 간격 (127줄)

```python
self.min_trade_interval = 60  # 최소 거래 간격 (초)
```

**역할:**
- 동일 코인에 대한 연속 거래 방지
- 중복 매수/매도 차단
- 60초 이내 재거래 불가

**작동 방식:**
```python
# src/main.py:211줄
if time.time() - last_time < self.min_trade_interval:
    continue  # 거래 스킵
```

#### 3. API 호출 간격

```python
# src/main.py:848줄
time.sleep(1)  # 티커당 1초 대기 (API 제한)
```

**역할:**
- 업비트 API 호출 제한 준수
- 과도한 요청 방지
- Rate Limit 회피

---

## 🔥 급등/급락 감지 설정

### 파일: `src/utils/surge_detector.py`

#### 1. 스캔 간격 (34줄)

```python
self.scan_interval = 30  # 30초마다 스캔
```

**⚠️ 주의**: 실제 작동은 `main.py`의 `surge_scan_interval`에 의해 제어됨
- **실제 감지 주기: 1초** (main.py에서 설정)

#### 2. 쿨다운 시간 (38줄)

```python
self.detection_cooldown = 300  # 5분 쿨다운
```

**역할:**
- 동일 코인에 대한 중복 감지 방지
- 한 번 감지된 코인은 5분간 재감지 제외
- 과도한 진입 방지

**작동 예시:**
```
00:00:00 - KRW-BTC 급등 감지 ✅
00:00:30 - KRW-BTC 재감지 시도 ❌ (쿨다운)
00:05:01 - KRW-BTC 재감지 가능 ✅
```

#### 3. API 호출 간격 (72줄)

```python
time.sleep(0.5)  # API 호출 제한 고려
```

**역할:**
- 감지 스캔 시 티커당 0.5초 대기
- API 제한 준수

#### 4. 감지 조건

```python
# src/utils/surge_detector.py:32~33줄
self.min_surge_ratio = 0.02  # 2% 이상 변동
self.min_volume_spike = 3.0  # 거래량 3배 이상
```

**조건:**
- 1분 내 가격 변화 ≥ 2%
- 거래량이 평균의 3배 이상

---

## ⚡ 초단타 전략 설정

### 파일: `src/config.py` (78~89줄)

```python
'ultra_scalping': {
    'enabled': True,
    'stop_loss': 0.005,      # 0.5% 빠른 손절
    'take_profit': 0.01,     # 1% 빠른 익절
    'min_price_surge': 0.02, # 2% 이상 급등/급락
    'volume_spike': 3.0,     # 거래량 3배 이상
    'max_hold_time': 300,    # ⏱️ 최대 5분 보유 (초)
    # ⭐ 스마트 매도 설정
    'smart_exit': True,      # 스마트 매도 활성화
    'profit_recheck_threshold': 0.005,  # 0.5% 이상부터 재확인
    'momentum_threshold': 0.001,  # 0.1% 모멘텀 기준
}
```

### 시간 관련 설정

#### 1. 최대 보유 시간 (`max_hold_time`)

**현재 값: 300초 (5분)**

```python
'max_hold_time': 300,  # 최대 5분 보유
```

**역할:**
- 초단타 포지션 최대 보유 시간
- 5분 경과 시 **무조건 강제 청산**
- 장기 홀딩 방지

**작동 로직:**
```python
# src/strategies/ultra_scalping.py:116줄
if hold_time >= self.max_hold_time:
    return True, f"시간 초과 청산 ({hold_time:.0f}초)"
```

#### 2. 조기 청산 시간 (하드코딩)

```python
# src/strategies/ultra_scalping.py:122줄
if hold_time >= 180 and profit_loss_ratio <= -0.002:
    return True, f"시간+손실 청산 (3분 경과, {profit_loss_ratio*100:.2f}%)"
```

**조건:**
- 3분 (180초) 경과
- 손실 -0.2% 이하
- → 조기 청산

### 파일: `src/strategies/ultra_scalping.py`

#### 전체 시간 로직

```python
def should_exit_smart(self, entry_price, current_price, hold_time, price_history):
    """
    스마트 청산 판단 (추세 기반)
    
    시간 체크:
    1️⃣ 손절: -0.5% → 즉시 청산
    2️⃣ 익절: +1.0% → 즉시 청산
    3️⃣ 시간 초과: 5분 → 강제 청산
    4️⃣ 조기 청산: 3분 + 손실 -0.2% → 청산
    5️⃣ 스마트 판단: 수익 시 추세 분석
    """
```

---

## 📊 일반 전략 설정

### 파일: `src/config.py`

#### 1. Aggressive Scalping (46~54줄)

```python
'aggressive_scalping': {
    'enabled': True,
    'stop_loss': 0.02,  # 2% 손절
    'take_profit': 0.015,  # 1.5% 익절
    'rsi_oversold': 30,
    'rsi_overbought': 70,
    'volume_threshold': 1.5,
    'min_price_change': 0.01,
}
```

**시간 관련:**
- 보유 시간 제한 없음
- 손익 조건 도달 시 청산

#### 2. Conservative Scalping (55~61줄)

```python
'conservative_scalping': {
    'enabled': True,
    'stop_loss': 0.015,  # 1.5% 손절
    'take_profit': 0.01,  # 1% 익절
    'rsi_min': 40,
    'rsi_max': 60,
    'bb_threshold': 0.95,
}
```

#### 3. Mean Reversion (62~67줄)

```python
'mean_reversion': {
    'enabled': True,
    'stop_loss': 0.03,  # 3% 손절
    'take_profit': 0.025,  # 2.5% 익절
    'ma_period': 20,
    'deviation_threshold': 0.05,
}
```

#### 4. Grid Trading (68~74줄)

```python
'grid_trading': {
    'enabled': True,
    'stop_loss': 0.04,  # 4% 손절
    'grid_count': 10,
    'grid_spacing': 0.005,
    'max_volatility': 0.02,
}
```

**공통점:**
- 명시적 시간 제한 없음
- 손익률 조건으로만 청산
- 전체 스캔 주기(5분)에 따라 분석

---

## 🔧 시간 설정 변경 방법

### 1. 메인 봇 스캔 주기 변경

**파일: `src/main.py` (130~132줄)**

```python
# 기본 설정 (현재)
self.full_scan_interval = 300  # 5분
self.quick_check_interval = 60  # 1분
self.surge_scan_interval = 1  # 1초

# 예시 1: 더 빠르게 (공격적)
self.full_scan_interval = 180  # 3분
self.quick_check_interval = 30  # 30초
self.surge_scan_interval = 0.5  # 0.5초 (500ms)

# 예시 2: 더 느리게 (보수적)
self.full_scan_interval = 600  # 10분
self.quick_check_interval = 120  # 2분
self.surge_scan_interval = 5  # 5초
```

### 2. 초단타 보유 시간 변경

**파일: `src/config.py` (84줄)**

```python
# 기본 설정 (현재)
'max_hold_time': 300,  # 5분

# 예시 1: 더 짧게 (공격적)
'max_hold_time': 180,  # 3분

# 예시 2: 더 길게 (여유)
'max_hold_time': 600,  # 10분
```

**⚠️ 주의**: 조기 청산 로직도 함께 수정 필요

**파일: `src/strategies/ultra_scalping.py` (122줄)**

```python
# 기본 설정 (현재)
if hold_time >= 180 and profit_loss_ratio <= -0.002:

# 예시 1: 2분으로 변경
if hold_time >= 120 and profit_loss_ratio <= -0.002:

# 예시 2: 5분으로 변경
if hold_time >= 300 and profit_loss_ratio <= -0.002:
```

### 3. 급등 감지 쿨다운 변경

**파일: `src/utils/surge_detector.py` (38줄)**

```python
# 기본 설정 (현재)
self.detection_cooldown = 300  # 5분

# 예시 1: 더 짧게 (더 많은 기회)
self.detection_cooldown = 180  # 3분

# 예시 2: 더 길게 (신중하게)
self.detection_cooldown = 600  # 10분
```

### 4. 최소 거래 간격 변경

**파일: `src/main.py` (127줄)**

```python
# 기본 설정 (현재)
self.min_trade_interval = 60  # 1분

# 예시 1: 더 짧게
self.min_trade_interval = 30  # 30초

# 예시 2: 더 길게
self.min_trade_interval = 120  # 2분
```

---

## 💡 권장 설정

### 시나리오 1: 공격적 (높은 거래 빈도)

```python
# src/main.py
self.full_scan_interval = 180  # 3분
self.quick_check_interval = 30  # 30초
self.surge_scan_interval = 0.5  # 0.5초
self.min_trade_interval = 30  # 30초

# src/config.py
'max_hold_time': 180,  # 3분

# src/utils/surge_detector.py
self.detection_cooldown = 180  # 3분
```

**특징:**
- ⚡ 매우 빠른 반응
- 📈 더 많은 거래 기회
- ⚠️ API 호출 증가
- 💸 수수료 증가

**적합한 경우:**
- 변동성이 높은 시장
- 소액 자본 (빠른 회전)
- 적극적 수익 추구

---

### 시나리오 2: 균형 (현재 기본값) ✅

```python
# src/main.py
self.full_scan_interval = 300  # 5분
self.quick_check_interval = 60  # 1분
self.surge_scan_interval = 1  # 1초
self.min_trade_interval = 60  # 1분

# src/config.py
'max_hold_time': 300,  # 5분

# src/utils/surge_detector.py
self.detection_cooldown = 300  # 5분
```

**특징:**
- ⚖️ 균형잡힌 설정
- 📊 적절한 거래 빈도
- 🔋 적정 API 사용
- 💰 합리적 수수료

**적합한 경우:**
- 대부분의 시장 상황
- 중간 자본 (100만원~)
- 안정적 수익 추구

---

### 시나리오 3: 보수적 (낮은 거래 빈도)

```python
# src/main.py
self.full_scan_interval = 600  # 10분
self.quick_check_interval = 120  # 2분
self.surge_scan_interval = 5  # 5초
self.min_trade_interval = 120  # 2분

# src/config.py
'max_hold_time': 600,  # 10분

# src/utils/surge_detector.py
self.detection_cooldown = 600  # 10분
```

**특징:**
- 🐢 느린 반응
- 📉 적은 거래 횟수
- 🔌 낮은 API 사용
- 💵 최소 수수료

**적합한 경우:**
- 안정적인 시장
- 대규모 자본
- 장기 전략 선호

---

## 📊 시간 설정 비교표

| 항목 | 공격적 | 균형 (기본) | 보수적 |
|------|--------|-------------|---------|
| **전체 스캔** | 3분 (180초) | 5분 (300초) ✅ | 10분 (600초) |
| **빠른 체크** | 30초 | 1분 (60초) ✅ | 2분 (120초) |
| **급등 감지** | 0.5초 | 1초 ✅ | 5초 |
| **최소 거래 간격** | 30초 | 1분 (60초) ✅ | 2분 (120초) |
| **초단타 보유** | 3분 (180초) | 5분 (300초) ✅ | 10분 (600초) |
| **감지 쿨다운** | 3분 (180초) | 5분 (300초) ✅ | 10분 (600초) |
| **거래 빈도** | 매우 높음 | 높음 | 보통 |
| **수수료** | 높음 | 중간 | 낮음 |
| **API 사용** | 많음 | 중간 | 적음 |

---

## ⚠️ 주의사항

### 1. API 호출 제한

**업비트 API 제한:**
- 초당 8~10회 요청 제한
- 분당 600회 제한

**권장사항:**
- `surge_scan_interval` < 0.5초는 권장하지 않음
- 코인 목록이 많으면 더 긴 간격 필요

### 2. 수수료 고려

**거래 빈도와 수수료:**
```
공격적 설정 (3분):
├─ 일일 거래: ~50회
├─ 월 거래: ~1,500회
└─ 월 수수료: 약 15만원 (자본 100만원 기준)

균형 설정 (5분):
├─ 일일 거래: ~30회
├─ 월 거래: ~900회
└─ 월 수수료: 약 9만원

보수적 설정 (10분):
├─ 일일 거래: ~15회
├─ 월 거래: ~450회
└─ 월 수수료: 약 4.5만원
```

### 3. 시장 변동성 고려

**변동성에 따른 권장:**
- **높은 변동성**: 균형 또는 공격적
- **낮은 변동성**: 보수적
- **횡보장**: 보수적 (거래 빈도 감소)

### 4. 변경 후 테스트

**변경 절차:**
1. 설정 파일 수정
2. 코드 문법 검사: `python -m py_compile src/main.py`
3. 모의투자 모드로 테스트
4. 최소 1일 이상 관찰
5. 실거래 적용

---

## 🎯 빠른 참조

### 핵심 설정 파일 위치

```
시간 설정 파일 목록:

1. src/main.py
   ├─ 130줄: full_scan_interval (5분)
   ├─ 131줄: quick_check_interval (1분)
   ├─ 132줄: surge_scan_interval (1초)
   └─ 127줄: min_trade_interval (1분)

2. src/config.py
   └─ 84줄: max_hold_time (5분)

3. src/utils/surge_detector.py
   ├─ 34줄: scan_interval (30초) ※미사용
   └─ 38줄: detection_cooldown (5분)

4. src/strategies/ultra_scalping.py
   └─ 122줄: 조기 청산 시간 (3분)
```

### 실시간 확인 명령어

```bash
# 현재 설정 확인
cd /home/user/webapp

# 메인 봇 설정
grep -n "interval" src/main.py | grep "self\."

# 초단타 설정
grep -n "max_hold_time" src/config.py

# 급등 감지 설정
grep -n "cooldown\|scan_interval" src/utils/surge_detector.py
```

---

## 🔗 관련 문서

- [초단타 시스템 가이드](ULTRA_SCALPING.md)
- [AI 학습 시스템](AI_LEARNING_SYSTEM.md)
- [실거래 가이드](LIVE_TRADING_GUIDE.md)
- [README](README.md)

---

## 📞 지원

- **GitHub**: https://github.com/lee-jungkil/Lj
- **다운로드**: https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip

---

**"시간 설정을 최적화하여 최대 수익을 달성하세요!"** ⏱️
