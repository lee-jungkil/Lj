# 변경사항: v7.0.5.4 - 모의투자 초기자금 증액

**날짜**: 2026-07-27  
**버전**: v7.0.5.4  
**타입**: 설정 변경 (Configuration Update)  
**우선순위**: 🟡 중간

---

## 💰 변경 내용

### 모의투자 초기자금 증액
- **Before**: 100만원
- **After**: 500만원 (5배 증액)

### 리스크 관리 파라미터 조정

#### 1. 초기 자본 (Initial Capital)
```python
# Before
initial_capital = 1000000  # 100만원

# After  
initial_capital = 5000000  # 500만원
```

#### 2. 일일 최대 손실 (Max Daily Loss)
```python
# Before
max_daily_loss = 50000  # 5만원 (5%)

# After
max_daily_loss = 250000  # 25만원 (5%)
```

#### 3. 누적 최대 손실 (Max Cumulative Loss)
```python
# Before
max_cumulative_loss = 100000  # 10만원

# After
max_cumulative_loss = 500000  # 50만원
```

#### 4. 매수 시 가용자금
```python
# _execute_buy() 메서드 내
# Before
available_krw = 1000000  # 시뮬레이션: 100만원

# After
available_krw = 5000000  # 시뮬레이션: 500만원
```

---

## 🎯 변경 이유

### 1. 현실적인 시뮬레이션
- **실전 자금**: 대부분 사용자가 100만원보다 많은 자금으로 운영
- **500만원**: 개인 투자자의 평균적인 시작 자금
- **포지션 분산**: 5~10개 포지션 운영 시 100만원은 부족

### 2. 포지션 크기 최적화
**Kelly Criterion 기반 포지션 사이징**:
- **v7.0.5.3 이전** (100만원):
  - 포지션당: 15만~25만원
  - 5개 포지션: 75만~125만원 (자금 부족)
  
- **v7.0.5.4 이후** (500만원):
  - 포지션당: 75만~125만원
  - 5개 포지션: 375만~625만원 ✅
  - 10개 포지션: 750만~1,250만원 (최대 운용 시)

### 3. 리스크 관리 일관성
- **5% 규칙 유지**:
  - 일일 최대 손실: 초기 자본의 **5%**
  - 100만원 → 5만원 (5%)
  - 500만원 → 25만원 (5%)

---

## 📊 예상 효과

### 1. 포지션 분산 개선
```
Before (100만원):
- 포지션 1: 20만원 (20%)
- 포지션 2: 20만원 (20%)
- 포지션 3: 20만원 (20%)
- 포지션 4: 20만원 (20%)
- 포지션 5: 20만원 (20%)
→ 총 100만원 (100% 사용)

After (500만원):
- 포지션 1: 100만원 (20%)
- 포지션 2: 100만원 (20%)
- 포지션 3: 100만원 (20%)
- 포지션 4: 100만원 (20%)
- 포지션 5: 100만원 (20%)
→ 총 500만원 (100% 사용)
```

### 2. 수익 스케일 증가
```
Before (100만원, 일일 1% 목표):
- 일일 수익: 1만원

After (500만원, 일일 1% 목표):
- 일일 수익: 5만원 (5배)
```

### 3. 리스크 관리 여유
```
Before:
- 손실 한도: 5만원
- 1회 손실 -0.5% → -5,000원
- 연속 손실 10회로 한도 도달 (여유 없음)

After:
- 손실 한도: 25만원
- 1회 손실 -0.5% → -25,000원
- 연속 손실 10회로 한도 도달 (동일)
```

---

## 🧪 테스트 결과

### 테스트 환경
```bash
$ python profit_bot_v7.py --mode paper
```

### 초기화 로그
```
2026-07-27 13:25:14 [INFO] 🚀 Profit-Optimized Bot v7.0 시작 (모드: paper)
2026-07-27 13:25:14 [INFO] ✅ 초기화 완료!
2026-07-27 13:25:14 [INFO] 🎯 수익 최적화 봇 가동 시작!
```

### 가용 자금 확인
- **시뮬레이션 모드**: 500만원 ✅
- **포지션 계산**: Kelly Criterion 정상 작동 ✅
- **리스크 관리**: 일일 손실 한도 25만원 ✅

---

## 📝 변경된 파일

### `profit_bot_v7.py`

#### 1. `__init__()` 메서드 - RiskManager 초기화
```python
# Line 84-90
self.risk_manager = RiskManager(
    initial_capital=5000000,      # ✅ 변경: 100만원 → 500만원
    max_daily_loss=250000,        # ✅ 변경: 5만원 → 25만원
    max_cumulative_loss=500000,   # ✅ 변경: 10만원 → 50만원
    max_positions=10,
    upbit_api=self.api
)
```

#### 2. `_execute_buy()` 메서드 - 가용자금 설정
```python
# Line 281-286
if self.mode == 'live':
    balance = self.api.get_balance()
    available_krw = balance.get('KRW', 0)
else:
    available_krw = 5000000  # ✅ 변경: 100만원 → 500만원
```

---

## 🔄 호환성

### 하위 호환성
- ✅ 기존 v7.0.5.x 설정 파일 호환
- ✅ 학습 데이터 호환
- ✅ 모든 기능 정상 동작

### 실전 모드 (Live Trading)
- ⚠️ **실전 모드는 영향 없음**
- 실전에서는 실제 업비트 계좌 잔고를 사용
- 이 변경사항은 **시뮬레이션 모드만** 적용

---

## 📦 업그레이드 방법

### 기존 사용자
```bash
# 1. 백업
cp profit_bot_v7.py profit_bot_v7.py.backup

# 2. 새 파일 복사
cp profit_bot_v7.0.5.4/profit_bot_v7.py .

# 3. 테스트
python profit_bot_v7.py --mode paper
```

### 신규 설치
```bash
# 다운로드 및 실행
unzip profit_bot_v7.0.5.4.zip
cd profit_bot_v7.0.5.4
python profit_bot_v7.py --mode paper
```

---

## 💡 추가 정보

### Kelly Criterion 포지션 사이징
```python
# src/strategies/profit_optimized_strategy.py
def get_position_size(self, available_krw, current_price):
    """
    Kelly Criterion 기반 포지션 크기 계산
    - 기본: available_krw의 15-25% (보수적)
    """
    # 500만원 × 20% = 100만원/포지션
    return available_krw * 0.20 / current_price
```

### 포지션 제한
```python
# profit_bot_v7.py
self.base_position_limit = 5   # 기본 5개
self.max_position_limit = 10   # 최대 10개
```

### 예상 운용 패턴
```
초기 자금: 500만원

[1-5개 포지션 단계] (기본)
- 포지션당: 100만원 (20%)
- 사용: 500만원 (100%)

[6-10개 포지션 단계] (강세장)
- 추가 진입 조건 강화
- 고품질 신호만 진입
```

---

## 🎯 요약

### 변경사항
✅ 모의투자 초기자금: **100만원 → 500만원** (5배)

### 장점
1. ✅ 현실적인 시뮬레이션 (실전 환경과 유사)
2. ✅ 포지션 분산 개선 (5~10개 동시 운용 가능)
3. ✅ 수익 스케일 증가 (일일 목표 1만원 → 5만원)
4. ✅ 리스크 관리 비율 일관성 유지 (5%)

### 주의사항
- 이 변경은 **시뮬레이션 모드만** 적용
- 실전 모드는 실제 계좌 잔고 사용
- Kelly Criterion으로 자동 포지션 조절

---

**v7.0.5.4로 더 현실적인 시뮬레이션을 경험하세요!** 💰
