# ⏱️ v6.30.47 - 최대 보유 시간 단축 설정

## 🎯 **변경 사항**

사용자 요청에 따라 **전략별 최대 보유 시간을 대폭 단축**했습니다.

---

## 📊 **변경 전/후 비교**

| 전략 | ⏰ 변경 전 | ✅ 변경 후 | 📉 단축률 |
|------|------------|------------|-----------|
| **CHASE_BUY** | 5분 | **5분** | 유지 |
| **ULTRA_SCALPING** | 10분 | **10분** | 유지 |
| **AGGRESSIVE** | 30분 | **5분** | **83% 단축** ⚡ |
| **CONSERVATIVE** | 1시간 (60분) | **10분** | **83% 단축** ⚡ |
| **MEAN_REVERSION** | 2시간 (120분) | **30분** | **75% 단축** ⚡ |
| **GRID** | 24시간 (1440분) | **1시간** | **96% 단축** ⚡ |
| **기타 (기본값)** | 1시간 (60분) | **10분** | **83% 단축** ⚡ |

---

## 🎯 **변경 목적**

### **빠른 회전율**
- 포지션을 짧은 시간 내에 청산
- 자본 회전 속도 증가
- 더 많은 거래 기회 포착

### **리스크 감소**
- 장기 보유에 따른 리스크 최소화
- 시장 급변 시 피해 감소
- 손실 확대 방지

### **스캘핑 최적화**
- 모든 전략이 **초단기~단기** 전략으로 전환
- 작은 수익을 빠르게 실현
- 손절도 빠르게 실행

---

## 🔧 **수정된 파일**

### **1. src/config.py (Line 126-132)**

```python
# 변경 전
MAX_HOLD_TIME_AGGRESSIVE = int(os.getenv('MAX_HOLD_TIME_AGGRESSIVE', 1800))  # 30분
MAX_HOLD_TIME_CONSERVATIVE = int(os.getenv('MAX_HOLD_TIME_CONSERVATIVE', 3600))  # 1시간
MAX_HOLD_TIME_MEAN_REVERSION = int(os.getenv('MAX_HOLD_TIME_MEAN_REVERSION', 7200))  # 2시간
MAX_HOLD_TIME_GRID = int(os.getenv('MAX_HOLD_TIME_GRID', 86400))  # 24시간

# 변경 후
MAX_HOLD_TIME_AGGRESSIVE = int(os.getenv('MAX_HOLD_TIME_AGGRESSIVE', 300))  # 5분 ⭐
MAX_HOLD_TIME_CONSERVATIVE = int(os.getenv('MAX_HOLD_TIME_CONSERVATIVE', 600))  # 10분 ⭐
MAX_HOLD_TIME_MEAN_REVERSION = int(os.getenv('MAX_HOLD_TIME_MEAN_REVERSION', 1800))  # 30분 ⭐
MAX_HOLD_TIME_GRID = int(os.getenv('MAX_HOLD_TIME_GRID', 3600))  # 1시간 ⭐
```

---

### **2. src/main.py (Line 1098-1110)**

```python
# 변경 전
max_hold_times = {
    'AGGRESSIVE': getattr(Config, 'MAX_HOLD_TIME_AGGRESSIVE', 1800),  # 30분
    'CONSERVATIVE': getattr(Config, 'MAX_HOLD_TIME_CONSERVATIVE', 3600),  # 1시간
    'MEAN_REVERSION': getattr(Config, 'MAX_HOLD_TIME_MEAN_REVERSION', 7200),  # 2시간
    'GRID': getattr(Config, 'MAX_HOLD_TIME_GRID', 86400)  # 24시간
}
max_hold_time = max_hold_times.get(position.strategy, 3600)  # 기본 1시간

# 변경 후
max_hold_times = {
    'AGGRESSIVE': getattr(Config, 'MAX_HOLD_TIME_AGGRESSIVE', 300),  # 5분 ⭐
    'CONSERVATIVE': getattr(Config, 'MAX_HOLD_TIME_CONSERVATIVE', 600),  # 10분 ⭐
    'MEAN_REVERSION': getattr(Config, 'MAX_HOLD_TIME_MEAN_REVERSION', 1800),  # 30분 ⭐
    'GRID': getattr(Config, 'MAX_HOLD_TIME_GRID', 3600)  # 1시간 ⭐
}
max_hold_time = max_hold_times.get(position.strategy, 600)  # 기본 10분 ⭐
```

---

## 📊 **예상 효과**

### **✅ 장점**

1. **빠른 자본 회전**
   - 5~30분 내 포지션 청산
   - 하루 더 많은 거래 가능
   - 기회비용 감소

2. **리스크 감소**
   - 장기 보유 리스크 최소화
   - 시장 급변 시 피해 감소
   - 손실 확대 방지

3. **스캘핑 최적화**
   - 작은 수익을 빠르게 실현
   - 손절도 빠르게 실행
   - 트레이딩 효율 증가

### **⚠️ 주의사항**

1. **익절 기회 감소**
   - 5분 내 +1.5% 도달 어려울 수 있음
   - 시간 초과로 +0.5% 수익에서 청산 가능

2. **거래 횟수 증가**
   - 수수료 증가 (업비트 0.05%)
   - 더 많은 매수/매도 발생

3. **승률 중요**
   - 짧은 시간 = 작은 수익
   - 승률이 낮으면 손실 누적

---

## 🎯 **실제 동작 예시**

### **시나리오 1: AGGRESSIVE 전략 (5분 제한)**

**변경 전 (30분):**
```
00:00 매수: KRW-SOL (100,000원)
00:10 손익: +0.5%
00:20 손익: +0.8%
00:30 시간 초과 청산 → +0.8% 수익 (800원)
```

**변경 후 (5분):**
```
00:00 매수: KRW-SOL (100,000원)
00:05 시간 초과 청산 → +0.3% 수익 (300원) ⚡
```

**결과:**
- 회전 속도: 6배 빠름 (30분 → 5분)
- 수익률: 낮아짐 (+0.8% → +0.3%)
- 하루 거래 횟수: 증가 (48회 → 288회)

---

### **시나리오 2: CONSERVATIVE 전략 (10분 제한)**

**변경 전 (1시간):**
```
00:00 매수: KRW-ETH (100,000원)
00:30 손익: +1.2%
01:00 시간 초과 청산 → +1.2% 수익 (1,200원)
```

**변경 후 (10분):**
```
00:00 매수: KRW-ETH (100,000원)
00:10 시간 초과 청산 → +0.6% 수익 (600원) ⚡
```

**결과:**
- 회전 속도: 6배 빠름 (60분 → 10분)
- 수익률: 절반 (+1.2% → +0.6%)
- 하루 거래 횟수: 6배 증가

---

### **시나리오 3: MEAN_REVERSION 전략 (30분 제한)**

**변경 전 (2시간):**
```
00:00 매수: KRW-XRP (100,000원)
01:00 손익: +1.8%
02:00 시간 초과 청산 → +1.8% 수익 (1,800원)
```

**변경 후 (30분):**
```
00:00 매수: KRW-XRP (100,000원)
00:30 시간 초과 청산 → +0.9% 수익 (900원) ⚡
```

**결과:**
- 회전 속도: 4배 빠름 (120분 → 30분)
- 수익률: 절반 (+1.8% → +0.9%)
- 하루 거래 횟수: 4배 증가

---

### **시나리오 4: GRID 전략 (1시간 제한)**

**변경 전 (24시간):**
```
09:00 매수: KRW-BTC (100,000원)
15:00 손익: +3.5%
익일 09:00 시간 초과 청산 → +3.5% 수익 (3,500원)
```

**변경 후 (1시간):**
```
09:00 매수: KRW-BTC (100,000원)
10:00 시간 초과 청산 → +0.5% 수익 (500원) ⚡
```

**결과:**
- 회전 속도: 24배 빠름 (1440분 → 60분)
- 수익률: 대폭 감소 (+3.5% → +0.5%)
- 하루 거래 횟수: 24배 증가

---

## 📈 **전략별 특징 (변경 후)**

| 전략 | 시간 제한 | 특징 | 적합한 상황 |
|------|-----------|------|-------------|
| **CHASE_BUY** | 5분 | 급등 추격 | 급등장, 높은 변동성 |
| **ULTRA_SCALPING** | 10분 | 초단타 | 빠른 변동, 높은 거래량 |
| **AGGRESSIVE** | 5분 ⚡ | 매우 공격적 | 단기 급등, 즉시 수익 |
| **CONSERVATIVE** | 10분 ⚡ | 빠른 보수적 | 안정적 소폭 상승 |
| **MEAN_REVERSION** | 30분 ⚡ | 중기 평균회귀 | 과매도/과매수 반전 |
| **GRID** | 1시간 ⚡ | 단기 그리드 | 레인지 장세 |

---

## 🚀 **즉시 적용 방법**

### **방법 1: 최신 코드 다운로드 (권장)**

```batch
cd C:\Users\admin\Downloads\Lj-main
curl -o src\config.py https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/config.py
curl -o src\main.py https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py
python -B -u RUN_DIRECT.py
```

### **방법 2: .env 파일 수정**

`.env` 파일에 다음 추가:

```bash
# 전략별 최대 보유 시간 (초) - v6.30.47 단축형
MAX_HOLD_TIME_AGGRESSIVE=300      # 5분
MAX_HOLD_TIME_CONSERVATIVE=600    # 10분
MAX_HOLD_TIME_MEAN_REVERSION=1800 # 30분
MAX_HOLD_TIME_GRID=3600           # 1시간
```

### **방법 3: 한 줄 명령어**

```batch
cd C:\Users\admin\Downloads\Lj-main && taskkill /F /IM python.exe /T 2>nul & curl -o src\config.py https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/config.py && curl -o src\main.py https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py && python -B -u RUN_DIRECT.py
```

---

## 📊 **예상 로그 출력**

### **변경 전 (30분 제한)**

```
[00:36:15] 매수: KRW-SOL (전략: AGGRESSIVE)
[01:06:20] ⏰ 시간초과청산: KRW-SOL
   보유: 30분 | 손익: +0.85%
```

### **변경 후 (5분 제한)**

```
[00:36:15] 매수: KRW-SOL (전략: AGGRESSIVE)
[00:41:15] ⏰ 시간초과청산: KRW-SOL ⚡
   보유: 5분 | 손익: +0.35%
```

---

## ⚙️ **커스터마이징**

원하는 시간으로 추가 조정 가능:

```python
# src/config.py 또는 .env 파일 수정

# 예: AGGRESSIVE를 3분으로 변경
MAX_HOLD_TIME_AGGRESSIVE=180  # 3분

# 예: CONSERVATIVE를 15분으로 변경
MAX_HOLD_TIME_CONSERVATIVE=900  # 15분

# 예: MEAN_REVERSION을 1시간으로 변경
MAX_HOLD_TIME_MEAN_REVERSION=3600  # 1시간
```

---

## 📝 **요약**

| 항목 | 내용 |
|------|------|
| **버전** | v6.30.46 → v6.30.47 |
| **변경 파일** | src/config.py, src/main.py, VERSION.txt |
| **주요 변경** | 전략별 최대 보유 시간 대폭 단축 |
| **단축률** | 75~96% 단축 |
| **목적** | 빠른 회전, 리스크 감소, 스캘핑 최적화 |
| **적용 방법** | 최신 코드 다운로드 또는 .env 수정 |

---

## 🎯 **최종 확인**

변경 후 봇을 실행하면:

1. **5분 이내** 포지션 청산 (AGGRESSIVE)
2. **10분 이내** 포지션 청산 (CONSERVATIVE)
3. **30분 이내** 포지션 청산 (MEAN_REVERSION)
4. **1시간 이내** 포지션 청산 (GRID)

**더 이상 30분, 1시간, 2시간을 기다리지 않습니다!** ⚡

---

**🚀 지금 바로 업데이트하고 빠른 회전율을 경험하세요!**
