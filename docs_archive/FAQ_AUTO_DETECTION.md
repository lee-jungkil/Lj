# 🔍 FAQ: 기존 손실 코인 자동 인식

## ❓ Q: 기존 손실 코인을 봇이 인식할 수 있어?

## ✅ A: 네! 자동으로 인식하고 보호합니다!

---

## 🎯 핵심 기능

### 1️⃣ 자동 감지
```
봇 첫 실행 시 (실거래 모드):
├─ 업비트 현재 보유 자동 조회
├─ 코인 목록 + 손익률 표시
├─ "보호할까요?" 사용자 확인
├─ Y 입력 시 자동 등록
└─ 🛡️ 절대 매도하지 않음!
```

### 2️⃣ 실시간 손익 계산
```python
자동 계산 항목:
- 현재가 조회
- 손익률 계산
- 손실 여부 판단
- ⚠️ 손실 중! 경고 표시
```

### 3️⃣ 안전한 보호
```
보호 등록 후:
✅ 기존 코인: 절대 매도 안 함
✅ 봇 매수분: 자유롭게 거래
✅ 완전 분리 관리
```

---

## 📊 실제 동작 예시

### 시나리오: -90% 손실 DOGE 자동 감지

```bash
$ ./run.sh
선택: 3 (live)

🚀 AutoProfit Bot 시작 (모드: live)
📡 업비트 API 연결 성공
🔍 기존 보유 코인 자동 감지 중...

════════════════════════════════════════════════════════
🔍 기존 보유 코인 발견!
════════════════════════════════════════════════════════

KRW-DOGE:
  수량: 10000.00000000
  평균가: 100원
  현재가: 10원
  손익: -90.00%
  ⚠️  손실 중!

KRW-XRP:
  수량: 50000.00000000
  평균가: 500원
  현재가: 250원
  손익: -50.00%
  ⚠️  손실 중!

────────────────────────────────────────────────────────

⚠️  중요: 이 코인들을 보호 대상으로 등록할까요?
   등록 시: 봇이 절대 매도하지 않습니다.
   미등록 시: 봇이 매도 신호 시 매도할 수 있습니다.

기존 보유 코인을 보호할까요? (Y/n): Y

🔄 기존 보유 자동 등록 중...

✅ 기존 보유 등록: KRW-DOGE
   수량: 10000.00000000
   평균가: 100원
   메모: 자동 감지 (손익: -90.00%)

✅ 기존 보유 등록: KRW-XRP
   수량: 50000.00000000
   평균가: 500원
   메모: 자동 감지 (손익: -50.00%)

✅ 총 2개 코인 보호 등록 완료!
🛡️  이 코인들은 봇이 절대 매도하지 않습니다.

🛡️  기존 보유 2개 코인 보호 활성화
🧠 전략 학습 시스템 활성화
🤖 봇 가동 시작!
```

---

## 🚀 사용 방법 (초간단!)

### ✨ 방법 1: 자동 감지 (권장!)

```bash
# 1. 그냥 실행
./run.sh

# 2. 모드 선택
선택: 3 (live)

# 3. 자동 감지 시작
🔍 기존 보유 코인 자동 감지 중...

# 4. 목록 확인 후 Y 입력
기존 보유 코인을 보호할까요? (Y/n): Y

# 5. 끝! 🎉
```

### 📝 방법 2: 수동 등록 (선택)

```bash
# 1. 미리 등록
python register_holdings.py

# 2. 봇 실행
./run.sh
```

---

## 🛡️ 안전 장치

### 1. 첫 실행만 물어봄

```
첫 실행:
✅ 업비트 조회
✅ 기존 코인 감지
✅ 사용자 확인
✅ 자동 등록
📝 JSON 저장

두 번째 실행:
✅ 저장된 목록 로드
❌ 다시 묻지 않음
⚡ 빠른 시작
```

### 2. 사용자 승인 필수

```
Y 입력:
✅ 보호 등록
🛡️ 절대 매도 안 함
💪 회복 기회 유지

n 입력:
❌ 등록 안 함
🆓 봇이 자유롭게 거래
⚠️ 손실 코인도 매도 가능
```

### 3. 언제든지 수정 가능

```bash
# 방법 1: 파일 직접 수정
vi trading_logs/existing_holdings.json

# 방법 2: 특정 코인 제거
# (JSON에서 해당 코인 항목 삭제)

# 방법 3: 전체 초기화
rm trading_logs/existing_holdings.json

# 봇 재시작
./run.sh
```

---

## 💡 실전 활용 팁

### ✅ Tip 1: 손실 코인은 Y

```
손실 중인 코인:
✅ 보호 등록 (Y)
✅ 회복 기회 유지
✅ 봇은 새로 매수한 것만 거래
✅ 정신 건강에 좋음 😌

예시:
- DOGE -90%
- XRP -50%
- ADA -70%
→ 모두 Y!
```

### ❌ Tip 2: 수익 코인은 n

```
수익 중인 코인:
❌ 보호 안 함 (n)
✅ 봇이 자유롭게 거래
✅ 추가 수익 기회
✅ 익절 자동화

예시:
- BTC +30%
- ETH +50%
→ n 입력
```

### 🔄 Tip 3: 정기 검토

```
월 1회 권장:
1. trading_logs/existing_holdings.json 확인
2. 회복된 코인 제거
3. 새로운 손실 코인 추가
4. 전략 조정
```

---

## ⚙️ 고급 설정

### 자동 승인 (묻지 않기)

```python
# src/main.py (86-89줄) 수정
self.holding_protector.auto_detect_existing_holdings(
    self.api, 
    prompt_user=False  # True → False 변경
)
```

**주의**: 자동 승인 시 모든 기존 코인이 자동으로 보호됩니다!

### 특정 코인만 보호

```bash
# 1. 일단 Y로 전체 등록
기존 보유 코인을 보호할까요? (Y/n): Y

# 2. JSON 파일 수정
vi trading_logs/existing_holdings.json

# 3. 보호하고 싶지 않은 코인 삭제
# 예: BTC는 제거, DOGE만 남김

# 4. 봇 재시작
```

---

## 🔧 기술 상세

### 자동 감지 흐름

```python
# src/utils/holding_protector.py

def auto_detect_existing_holdings(upbit_api, prompt_user=True):
    """
    1. 업비트 API로 현재 보유 조회
    2. KRW 제외하고 코인만 필터
    3. 각 코인의 현재가 조회
    4. 손익률 계산
    5. 사용자에게 목록 표시
    6. 확인 후 자동 등록
    7. JSON 파일 저장
    """
    
    # 1. 현재 보유 조회
    balances = upbit_api.get_balances()
    
    # 2. 코인만 필터
    holdings = []
    for balance in balances:
        if balance['currency'] != 'KRW':
            ticker = f"KRW-{balance['currency']}"
            amount = float(balance['balance'])
            avg_price = float(balance['avg_buy_price'])
            
            # 3-4. 현재가 조회 및 손익률 계산
            current_price = upbit_api.get_current_price(ticker)
            profit_loss_ratio = ((current_price - avg_price) / avg_price) * 100
            
            holdings.append({
                'ticker': ticker,
                'amount': amount,
                'avg_price': avg_price,
                'current_price': current_price,
                'profit_loss_ratio': profit_loss_ratio
            })
    
    # 5. 사용자에게 표시
    print("🔍 기존 보유 코인 발견!")
    for h in holdings:
        print(f"{h['ticker']}: {h['profit_loss_ratio']:+.2f}%")
    
    # 6. 확인
    if prompt_user:
        response = input("기존 보유 코인을 보호할까요? (Y/n): ")
        if response.lower() == 'n':
            return False
    
    # 7. 자동 등록 및 저장
    for h in holdings:
        register_existing_holding(
            ticker=h['ticker'],
            amount=h['amount'],
            avg_buy_price=h['avg_price'],
            note=f"자동 감지 (손익: {h['profit_loss_ratio']:+.2f}%)"
        )
    
    save_existing_holdings()  # JSON 저장
    return True
```

### 저장 파일 구조

```json
// trading_logs/existing_holdings.json
{
  "holdings": {
    "KRW-DOGE": {
      "ticker": "KRW-DOGE",
      "amount": 10000.0,
      "avg_buy_price": 100.0,
      "current_value": 100000.0,
      "loss_ratio": -90.0,
      "lock_date": "2025-02-10T12:00:00",
      "note": "자동 감지 (손익: -90.00%)"
    },
    "KRW-XRP": {
      "ticker": "KRW-XRP",
      "amount": 50000.0,
      "avg_buy_price": 500.0,
      "current_value": 12500000.0,
      "loss_ratio": -50.0,
      "lock_date": "2025-02-10T12:00:00",
      "note": "자동 감지 (손익: -50.00%)"
    }
  },
  "updated_at": "2025-02-10T12:00:00"
}
```

---

## 🎓 실전 시나리오

### 시나리오 A: 처음 사용

```
상황:
- DOGE 10,000개 (-90%)
- 봇 처음 실행

실행:
$ ./run.sh
선택: 3

결과:
✅ 자동 감지
✅ DOGE 표시
✅ Y 입력
✅ 보호 등록
🛡️ DOGE 절대 매도 안 함!
```

### 시나리오 B: 두 번째 실행

```
상황:
- DOGE 이미 등록됨
- 봇 재실행

실행:
$ ./run.sh
선택: 3

결과:
✅ 저장된 목록 로드
✅ 바로 시작
❌ 다시 묻지 않음
⚡ 빠름!
```

### 시나리오 C: 보호 해제

```
상황:
- DOGE 회복됨 (-90% → -10%)
- 이제 팔고 싶음

해제:
$ vi trading_logs/existing_holdings.json
# DOGE 항목 삭제

$ ./run.sh
선택: 3

결과:
✅ DOGE 보호 해제
✅ 봇이 자유롭게 거래
✅ 매도 신호 시 매도 가능
```

---

## ⚠️ 주의사항

### 1. 첫 실행 타이밍이 중요!

```
좋은 타이밍:
✅ 손실 코인이 있을 때
✅ 장기 보유 계획이 있을 때
✅ 회복 기다리는 중일 때
✅ 정신 건강을 위해 😌

나쁜 타이밍:
❌ 곧 팔 예정인 코인
❌ 단기 거래 중인 코인
❌ 실험 중인 코인
```

### 2. Y/n 선택 신중하게!

```
Y (보호):
- 절대 매도 안 함
- 회복 기회 유지
- 봇 매수분만 거래

n (보호 안 함):
- 매도 신호 시 매도
- 손실 확정 가능
- 자유로운 거래
```

### 3. 정기 검토 필수!

```
월 1회 확인:
1. 손실 코인 상태
2. 회복 여부
3. 전략 조정
4. 보호 목록 업데이트
```

---

## 📊 통계 및 효과

### Before (자동 감지 전)

```
문제점:
❌ 수동 등록 필요
❌ 등록 안 하면 위험
❌ 기존 코인 매도 사고 발생
❌ 정신적 스트레스

결과:
- 의도치 않은 손실 확정
- 회복 기회 상실
- 사용자 불만
```

### After (자동 감지 후)

```
개선점:
✅ 자동 감지
✅ 사용자 확인
✅ 안전 보장
✅ 정신 건강 보호

결과:
- 손실 코인 보호
- 회복 기회 유지
- 봇 신뢰도 상승
- 사용자 만족
```

---

## 🎉 최종 정리

### 핵심 기능

| 기능 | 설명 | 상태 |
|------|------|------|
| 🔍 자동 조회 | 업비트에서 현재 보유 자동 조회 | ✅ 작동 중 |
| 💰 손익 계산 | 실시간 손익률 자동 계산 | ✅ 작동 중 |
| 🛡️ 자동 보호 | 사용자 승인 후 자동 등록 | ✅ 작동 중 |
| ✅ 안전 확인 | 사용자 승인 필수 | ✅ 작동 중 |
| 📝 영구 저장 | JSON 파일 저장 | ✅ 작동 중 |
| 🔄 자동 로드 | 다음 실행 시 자동 로드 | ✅ 작동 중 |
| ⚙️ 수정 가능 | 언제든지 수정/삭제 가능 | ✅ 작동 중 |

### 작동 흐름

```
봇 실행 (./run.sh)
       ↓
업비트 API 연결
       ↓
기존 보유 조회
       ↓
코인 발견? ──No→ 바로 시작
       ↓ Yes
목록 + 손익률 표시
       ↓
"보호할까요?"
       ↓
Y ─────────→ 자동 등록 → 🛡️ 보호 활성화
n ─────────→ 등록 안 함 → 🆓 자유 거래
       ↓
🤖 봇 가동 시작!
```

---

## 🔗 관련 문서

- **자동 감지 가이드**: `EXISTING_COIN_DETECTION.md`
- **보호 시스템 상세**: `HOLDING_PROTECTION.md`
- **빠른 시작 가이드**: `QUICKRUN.md`
- **전체 가이드**: `README.md`
- **실거래 가이드**: `LIVE_TRADING_GUIDE.md`

---

## 📦 소스 코드 위치

```
src/utils/holding_protector.py
├─ ExistingHolding 클래스
├─ HoldingProtector 클래스
└─ auto_detect_existing_holdings() (390-494줄) ⭐

src/main.py
└─ 자동 감지 호출 (82-94줄) ⭐

trading_logs/
└─ existing_holdings.json (저장 파일)
```

---

## 💬 자주 묻는 질문

### Q1: 등록을 잘못했어요!

**A**: `trading_logs/existing_holdings.json` 파일을 수정하거나 삭제하고 봇을 재시작하세요.

```bash
# 전체 초기화
rm trading_logs/existing_holdings.json

# 봇 재시작
./run.sh
```

### Q2: 자동으로 등록하고 싶어요 (묻지 말고)

**A**: `src/main.py` 88줄을 수정하세요.

```python
# 수정 전
prompt_user=True

# 수정 후
prompt_user=False
```

### Q3: 특정 코인만 보호하고 싶어요

**A**: 일단 전체 등록 후 JSON 파일에서 원하지 않는 코인을 삭제하세요.

```bash
vi trading_logs/existing_holdings.json
# 보호하고 싶지 않은 코인 항목 삭제
```

### Q4: 백테스트/모의투자에서도 작동하나요?

**A**: 아니요. 실거래 모드(live)에서만 작동합니다.

```python
# src/main.py (83줄)
if mode == 'live' and self.api.upbit:
    # 실거래 모드에서만 자동 감지
```

### Q5: 저장 파일이 어디 있나요?

**A**: `trading_logs/existing_holdings.json`

```bash
# 파일 확인
cat trading_logs/existing_holdings.json

# 파일 수정
vi trading_logs/existing_holdings.json
```

---

## ✅ 결론

### 질문: 기존 손실 코인을 봇이 인식할 수 있어?

### 답변: ✅ 완벽하게 자동으로 인식합니다!

```
✨ 핵심 기능
├─ 🔍 자동 감지: 업비트에서 현재 보유 자동 조회
├─ 💰 손익 계산: 실시간 손익률 자동 계산
├─ 🛡️ 자동 보호: 사용자 승인 후 자동 등록
├─ ✅ 안전 확인: 사용자 승인 필수
├─ 📝 영구 저장: JSON 파일 저장
└─ 🔄 자동 로드: 다음 실행 시 자동 로드

🎯 사용 방법
└─ ./run.sh → 3 (live) → Y 입력 → 끝!

🛡️ 안전 장치
├─ 첫 실행만 물어봄
├─ 사용자 승인 필수
└─ 언제든지 수정 가능

💡 실전 팁
├─ 손실 코인: Y (보호)
├─ 수익 코인: n (자유 거래)
└─ 월 1회 검토
```

**이제 그냥 봇을 실행만 하면 기존 손실 코인을 자동으로 보호합니다!** 🚀

---

## 🔗 링크

- **GitHub**: https://github.com/lee-jungkil/Lj
- **다운로드**: https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip

---

**최종 업데이트**: 2025-02-10  
**작성자**: AutoProfit Bot Team  
**버전**: 1.0
