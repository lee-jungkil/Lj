# 📊 전략별 최대 보유 시간 가이드

## 🎯 **6가지 전략별 시간 제한**

봇은 **전략별로 다른 최대 보유 시간**을 사용합니다. 이 시간을 초과하면 **자동으로 시간 초과 청산**이 발생합니다.

---

## 📋 **전략별 최대 보유 시간 (기본값)**

| 전략 | 최대 보유 시간 | 설명 | 환경 변수 |
|------|----------------|------|-----------|
| **CHASE_BUY** | **5분** (300초) | 추격 매수 (급등 포착) | `MAX_HOLD_TIME_CHASE` |
| **ULTRA_SCALPING** | **10분** (600초) | 초단타 스캘핑 | `MAX_HOLD_TIME_ULTRA` |
| **AGGRESSIVE** | **30분** (1800초) | 공격적 스캘핑 | `MAX_HOLD_TIME_AGGRESSIVE` |
| **CONSERVATIVE** | **1시간** (3600초) | 보수적 스캘핑 | `MAX_HOLD_TIME_CONSERVATIVE` |
| **MEAN_REVERSION** | **2시간** (7200초) | 평균 회귀 전략 | `MAX_HOLD_TIME_MEAN_REVERSION` |
| **GRID** | **24시간** (86400초) | 그리드 트레이딩 | `MAX_HOLD_TIME_GRID` |

**기타 전략**: 1시간 (3600초) - 전략이 위 목록에 없으면 기본값 적용

---

## 🔧 **코드 구현 (src/main.py)**

```python
# Line 1100-1110
max_hold_times = {
    'CHASE_BUY': getattr(Config, 'MAX_HOLD_TIME_CHASE', 300),        # 5분
    'ULTRA_SCALPING': getattr(Config, 'MAX_HOLD_TIME_ULTRA', 600),   # 10분
    'AGGRESSIVE': getattr(Config, 'MAX_HOLD_TIME_AGGRESSIVE', 1800), # 30분
    'CONSERVATIVE': getattr(Config, 'MAX_HOLD_TIME_CONSERVATIVE', 3600), # 1시간
    'MEAN_REVERSION': getattr(Config, 'MAX_HOLD_TIME_MEAN_REVERSION', 7200), # 2시간
    'GRID': getattr(Config, 'MAX_HOLD_TIME_GRID', 86400)  # 24시간
}

max_hold_time = max_hold_times.get(position.strategy, 3600)  # 기본 1시간

# Line 1113-1116
if hold_time > max_hold_time:
    profit_ratio = ((current_price - position.avg_buy_price) / position.avg_buy_price) * 100
    self.execute_sell(ticker, f"시간초과청산 (보유:{hold_time/60:.0f}분, 손익:{profit_ratio:+.2f}%)")
    return
```

---

## ⚙️ **환경 변수 설정 (src/config.py)**

```python
# Line 127-132
MAX_HOLD_TIME_CHASE = int(os.getenv('MAX_HOLD_TIME_CHASE', 300))
MAX_HOLD_TIME_ULTRA = int(os.getenv('MAX_HOLD_TIME_ULTRA', 600))
MAX_HOLD_TIME_AGGRESSIVE = int(os.getenv('MAX_HOLD_TIME_AGGRESSIVE', 1800))
MAX_HOLD_TIME_CONSERVATIVE = int(os.getenv('MAX_HOLD_TIME_CONSERVATIVE', 3600))
MAX_HOLD_TIME_MEAN_REVERSION = int(os.getenv('MAX_HOLD_TIME_MEAN_REVERSION', 7200))
MAX_HOLD_TIME_GRID = int(os.getenv('MAX_HOLD_TIME_GRID', 86400))
```

---

## 🎯 **실제 동작 예시**

### **예시 1: AGGRESSIVE 전략 (30분 제한)**

**현재 포지션:**
- 코인: KRW-SOL
- 전략: AGGRESSIVE
- 보유 시간: 31분 15초
- 손익률: +0.85%

**청산 조건 평가:**
```
조건 1: 시간 초과 체크
  - max_hold_time = 1800초 (30분)
  - hold_time = 1875초 (31분 15초)
  - hold_time (1875) > max_hold_time (1800)?
  - → YES! ✅
  
→ 즉시 매도 실행!

[2026-02-14 01:15:30] ⏰ 시간초과청산: KRW-SOL
   보유: 31분 | 손익: +0.85%
   전략: AGGRESSIVE (최대 30분)
   
✅ 시간 초과 매도 완료!
💰 수익: +850원 (+0.85%)
```

---

### **예시 2: ULTRA_SCALPING 전략 (10분 제한)**

**현재 포지션:**
- 코인: KRW-DOGE
- 전략: ULTRA_SCALPING
- 보유 시간: 11분 30초
- 손익률: +1.2%

**청산 조건 평가:**
```
조건 1: 시간 초과 체크
  - max_hold_time = 600초 (10분)
  - hold_time = 690초 (11분 30초)
  - hold_time (690) > max_hold_time (600)?
  - → YES! ✅
  
→ 즉시 매도 실행!

[2026-02-14 01:20:45] ⏰ 시간초과청산: KRW-DOGE
   보유: 11분 | 손익: +1.2%
   전략: ULTRA_SCALPING (최대 10분)
   
✅ 시간 초과 매도 완료!
💰 수익: +1,200원 (+1.2%)
```

---

### **예시 3: CHASE_BUY 전략 (5분 제한)**

**현재 포지션:**
- 코인: KRW-SHIB
- 전략: CHASE_BUY
- 보유 시간: 5분 30초
- 손익률: -0.5%

**청산 조건 평가:**
```
조건 1: 시간 초과 체크
  - max_hold_time = 300초 (5분)
  - hold_time = 330초 (5분 30초)
  - hold_time (330) > max_hold_time (300)?
  - → YES! ✅
  
→ 즉시 매도 실행! (손실이어도 시간 초과 우선)

[2026-02-14 01:25:10] ⏰ 시간초과청산: KRW-SHIB
   보유: 5분 | 손익: -0.5%
   전략: CHASE_BUY (최대 5분)
   
✅ 시간 초과 매도 완료!
💸 손실: -250원 (-0.5%)
```

---

### **예시 4: MEAN_REVERSION 전략 (2시간 제한)**

**현재 포지션:**
- 코인: KRW-ETH
- 전략: MEAN_REVERSION
- 보유 시간: 2시간 5분
- 손익률: +2.5%

**청산 조건 평가:**
```
조건 1: 시간 초과 체크
  - max_hold_time = 7200초 (2시간)
  - hold_time = 7500초 (2시간 5분)
  - hold_time (7500) > max_hold_time (7200)?
  - → YES! ✅
  
→ 즉시 매도 실행!

[2026-02-14 03:30:15] ⏰ 시간초과청산: KRW-ETH
   보유: 125분 | 손익: +2.5%
   전략: MEAN_REVERSION (최대 2시간)
   
✅ 시간 초과 매도 완료!
💰 수익: +2,500원 (+2.5%)
```

---

## 🔧 **커스터마이징 방법**

### **방법 1: .env 파일 수정**

`.env` 파일에 다음을 추가하여 시간을 조정할 수 있습니다:

```bash
# 전략별 최대 보유 시간 (초 단위)
MAX_HOLD_TIME_CHASE=300         # 5분 (기본값)
MAX_HOLD_TIME_ULTRA=600         # 10분 (기본값)
MAX_HOLD_TIME_AGGRESSIVE=1800   # 30분 (기본값)
MAX_HOLD_TIME_CONSERVATIVE=3600 # 1시간 (기본값)
MAX_HOLD_TIME_MEAN_REVERSION=7200  # 2시간 (기본값)
MAX_HOLD_TIME_GRID=86400        # 24시간 (기본값)
```

**예: AGGRESSIVE 전략을 1시간으로 변경**
```bash
MAX_HOLD_TIME_AGGRESSIVE=3600  # 30분 → 1시간 (3600초)
```

**예: ULTRA_SCALPING을 5분으로 변경**
```bash
MAX_HOLD_TIME_ULTRA=300  # 10분 → 5분 (300초)
```

---

### **방법 2: Config 파일 직접 수정**

`src/config.py` 파일의 기본값을 직접 수정:

```python
# Line 127-132 수정
MAX_HOLD_TIME_CHASE = int(os.getenv('MAX_HOLD_TIME_CHASE', 600))  # 5분 → 10분
MAX_HOLD_TIME_ULTRA = int(os.getenv('MAX_HOLD_TIME_ULTRA', 300))  # 10분 → 5분
MAX_HOLD_TIME_AGGRESSIVE = int(os.getenv('MAX_HOLD_TIME_AGGRESSIVE', 3600))  # 30분 → 1시간
```

---

## 💡 **전략별 특징**

### **🚀 초단기 전략 (5~10분)**

**CHASE_BUY (5분)**
- 급등 포착 후 추격 매수
- 빠른 수익 실현이 목표
- 장기 보유 리스크 방지

**ULTRA_SCALPING (10분)**
- 초단타 스캘핑
- 작은 수익을 빠르게 실현
- 변동성에 민감

### **⚡ 단기 전략 (30분)**

**AGGRESSIVE (30분)**
- 공격적 스캘핑
- 중간 수익 목표
- 빠른 회전율

### **🔄 중기 전략 (1~2시간)**

**CONSERVATIVE (1시간)**
- 보수적 스캘핑
- 안정적인 수익 추구
- 시장 변동 대응

**MEAN_REVERSION (2시간)**
- 평균 회귀 전략
- 과매수/과매도 활용
- 추세 전환 대기

### **📊 장기 전략 (24시간)**

**GRID (24시간)**
- 그리드 트레이딩
- 레인지 장세에 적합
- 장기 보유 가능

---

## 🎯 **우선순위 정리**

### **청산 조건 평가 순서**

```
1. CRITICAL 리스크 평가       ← 최우선
2. 시간 초과 체크 ←────────── 두 번째 (이 문서 내용)
3. 급락 감지 (-1.5%)
4. 거래량 급감 (50% 이하)
5. 차트 신호 (RSI, MACD)
6. 트레일링 스탑
7. 분할 매도
8. 조건부 매도
9. 동적 손절
10. 기본 익절/손절          ← 마지막
```

**시간 초과는 두 번째 우선순위!**
- CRITICAL 리스크 다음으로 중요
- 익절/손절 조건보다 **우선 평가**
- 시간이 초과되면 **손익과 관계없이 청산**

---

## 📊 **현재 포지션 시간 체크**

스크린샷에서 확인된 포지션:

| 코인 | 손익률 | 보유 시간 | 전략 (추정) | 시간 제한 | 남은 시간 |
|------|--------|-----------|-------------|-----------|-----------|
| **SOL** | +0.23% | 24분 56초 | AGGRESSIVE | 30분 | **약 5분** |
| **STRAX** | +0.02% | 21분 56초 | AGGRESSIVE | 30분 | **약 8분** |
| **CBK** | 0.00% | 20초 | AGGRESSIVE | 30분 | **약 29분** |

**⚠️ 주의:** 
- **SOL**: 약 5분 후 **시간 초과 청산** 발생 가능!
- **STRAX**: 약 8분 후 **시간 초과 청산** 발생 가능!
- 익절 조건 (+1.5%)을 먼저 달성하지 못하면 **시간 초과로 강제 매도**

---

## 🔍 **시간 초과 청산 로그 예시**

```
[DEBUG-QUICK] [1/3] KRW-SOL 체크 시작...

조건 0: CRITICAL 리스크? → NO
조건 1: 시간 초과?
  - 전략: AGGRESSIVE
  - 최대 보유 시간: 1800초 (30분)
  - 현재 보유 시간: 1876초 (31분 16초)
  - 시간 초과! → YES ✅

⏰ 시간 초과 청산 조건 충족!

[2026-02-14 01:06:56] ⏰ 시간초과청산: KRW-SOL
   보유: 31분 | 손익: +0.85%
   전략: AGGRESSIVE (최대 보유 30분)
   
[모의거래] 매도 주문 실행
종목: KRW-SOL
수량: 0.00040486
매도가: 123,877원
예상 수익: +850원

✅ 시간 초과 매도 완료!
💰 수익: +850원 (+0.85%)
📊 청산 사유: 시간초과청산 (보유:31분, 손익:+0.85%)
```

---

## 📝 **요약**

| 항목 | 내용 |
|------|------|
| **전략 개수** | 6가지 + 기타(기본값) |
| **최단 시간** | CHASE_BUY (5분) |
| **최장 시간** | GRID (24시간) |
| **일반적 시간** | AGGRESSIVE (30분) |
| **기본값** | 1시간 (전략 미지정 시) |
| **우선순위** | CRITICAL 다음 (2위) |
| **커스터마이징** | .env 파일 또는 Config 파일 수정 |

---

## 🎯 **실전 팁**

1. **초단타 전략 (5~10분)**
   - 빠른 수익 실현
   - 변동성 큰 코인에 적합
   - 리스크 관리 중요

2. **단기 전략 (30분)**
   - 가장 일반적
   - 균형 잡힌 접근
   - 대부분의 상황에 적합

3. **중장기 전략 (1~24시간)**
   - 안정적 수익 추구
   - 레인지 장세에 유리
   - 추세 전환 활용

4. **시간 초과 방지**
   - 익절 목표를 조기 달성하면 시간 초과 전에 청산
   - 전략별 시간 제한을 고려한 코인 선택
   - 변동성 큰 코인 = 짧은 시간 제한 추천

---

**🚀 봇이 자동으로 관리하므로 신경 쓰지 않아도 됩니다!**
