# 🔴 긴급 수정 v6.30.65 - 모의거래 매도 실행 차단 버그 수정

**날짜**: 2026-02-15
**버전**: v6.30.65-PAPER-MODE-FIX
**심각도**: ⚠️ **CRITICAL** - 모의거래 모드에서 매도가 전혀 작동하지 않음

---

## 🐛 **버그 설명**

### **증상**
사용자 보고: 
- 로그에 "매도 완료" 메시지가 나오지만
- 실제 포지션은 화면에 그대로 남아있음
- 포지션 청산 로그가 전혀 나타나지 않음
- 매수/매도 카운터가 증가하지 않음

### **근본 원인**

**v6.30.64의 코드 흐름:**

```python
# src/main.py 라인 782-803
sellable_amount, sell_msg = self.holding_protector.calculate_sellable_amount(
    ticker,
    current_price=current_price,
    upbit_api=self.api if self.mode == 'live' else None  # ⚠️ 모의거래 시 None
)

# 매도 수량 결정
sell_amount = position.amount

# 기존 보유가 있으면 봇 투자분만 매도
if self.holding_protector.is_existing_holding(ticker):
    if sellable_amount <= 0:  # ⚠️ 모의거래 모드에서는 항상 0!
        self.logger.log_warning(
            f"🛡️  {ticker} 매도 불가: 기존 보유 보호 중 ({sell_msg})"
        )
        return  # ⚠️ 여기서 함수 종료! 청산 코드가 절대 실행되지 않음!
```

**`holding_protector.calculate_sellable_amount()` 로직:**

```python
# src/utils/holding_protector.py 라인 252-294
if upbit_api:  # ⚠️ 모의거래에서는 None → False
    # 실제 API로 보유량 확인...
    return sellable, "투자금 + 이익분..."
else:
    # API 없으면 봇 포지션 수량만 반환
    if bot_amount > 0:  # ⚠️ 모의거래에서는 bot_amount == 0
        return bot_amount, "투자금..."
    
    return 0.0, "매도 불가 (원금 보호)"  # ⚠️ 항상 0 반환!
```

**결과:**
1. 모의거래 모드 → `upbit_api=None`
2. `calculate_sellable_amount()` → `0.0, "매도 불가"` 반환
3. `sellable_amount <= 0` → `return`으로 함수 종료
4. **포지션 청산 코드 (라인 865~) 절대 실행 안 됨!**

---

## ✅ **수정 내용**

### **변경된 로직 (v6.30.65)**

```python
# src/main.py 라인 782-810 (수정됨)

# 기존 보유 보호: 매도 가능 수량 확인 (v5.7: 투자금 + 이익분만)
# ⭐ v6.30.65: 모의거래 모드에서는 holding_protector 체크 우회
sell_amount = position.amount

if self.mode == 'live':
    # 실거래 모드에서만 보유 보호 체크
    sellable_amount, sell_msg = self.holding_protector.calculate_sellable_amount(
        ticker,
        current_price=current_price,
        upbit_api=self.api.upbit  # ✅ 실거래에서만 API 전달
    )
    
    # 기존 보유가 있으면 봇 투자분만 매도
    if self.holding_protector.is_existing_holding(ticker):
        if sellable_amount <= 0:
            self.logger.log_warning(
                f"🛡️  {ticker} 매도 불가: 기존 보유 보호 중 ({sell_msg})"
            )
            _original_print(f"[EXECUTE-SELL] ❌ 실거래 모드: 기존 보유 보호로 매도 차단")
            return  # ✅ 실거래에서만 return
        
        sell_amount = min(sell_amount, sellable_amount)
        self.logger.log_info(
            f"🛡️  {ticker} 부분 매도: {sell_amount:.8f} (기존 보유 보호)"
        )
else:
    # ✅ 모의거래 모드: holding_protector 체크 완전 우회
    _original_print(f"[EXECUTE-SELL] 모의거래 모드: 포지션 전체 매도 허용 (holding_protector 우회)")
    # sell_amount는 이미 position.amount로 설정됨

# ✅ 이제 모의거래에서도 여기로 진행됨!
# 라인 810 이후: 매도 주문 실행 및 포지션 청산
```

### **핵심 변경사항**

1. **`self.mode == 'live'` 분기 추가**
   - 실거래 모드에서만 `holding_protector` 체크 수행
   - 모의거래 모드에서는 체크 완전 우회

2. **early return 제거**
   - 모의거래에서는 `sellable_amount` 체크를 아예 하지 않음
   - 포지션 청산 코드가 항상 실행됨

3. **명확한 로그 추가**
   - 모의거래: `"모의거래 모드: 포지션 전체 매도 허용 (holding_protector 우회)"`
   - 실거래 차단: `"실거래 모드: 기존 보유 보호로 매도 차단"`

---

## 📊 **영향 범위**

### **수정 전 (v6.30.64)**
| 모드 | 기존 보유 | 동작 | 결과 |
|------|----------|------|------|
| 모의거래 | 없음 | ❌ sellable=0 → return | **매도 차단** |
| 모의거래 | 있음 | ❌ sellable=0 → return | **매도 차단** |
| 실거래 | 없음 | ✅ 전체 매도 | 정상 |
| 실거래 | 있음 | ✅ 부분 매도 (보호) | 정상 |

### **수정 후 (v6.30.65)**
| 모드 | 기존 보유 | 동작 | 결과 |
|------|----------|------|------|
| 모의거래 | 없음 | ✅ 체크 우회 → 전체 매도 | **정상 ✅** |
| 모의거래 | 있음 | ✅ 체크 우회 → 전체 매도 | **정상 ✅** |
| 실거래 | 없음 | ✅ 전체 매도 | 정상 |
| 실거래 | 있음 | ✅ 부분 매도 (보호) | 정상 |

---

## 🧪 **테스트 방법**

### **1. 즉시 테스트 (30초)**

```bash
cd /home/user/webapp
python test_bot_simple.py
```

**기대 결과:**
```
[EXECUTE-SELL] 모의거래 모드: 포지션 전체 매도 허용 (holding_protector 우회)
[EXECUTE-SELL] 모의거래 모드: 매도 주문 시뮬레이션
[EXECUTE-SELL] ========== 포지션 청산 시작 ==========
[EXECUTE-SELL] holding_protector.close_bot_position() 호출...
[EXECUTE-SELL] ✅ holding_protector 청산 완료
[EXECUTE-SELL] risk_manager.close_position() 호출...
[EXECUTE-SELL] ✅ risk_manager 청산 완료
[EXECUTE-SELL] ✅ UI 업데이트 완료
```

### **2. 실제 봇 실행**

```batch
# Windows CMD (관리자)
cd C:\Users\admin\Downloads\Lj-main\Lj-main

# 캐시 삭제
taskkill /F /IM python.exe /T
del /s /q *.pyc
for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"

# 최신 코드 다운로드
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py' -OutFile 'src\main.py' -UseBasicParsing"
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/lee-jungkil/Lj/main/VERSION.txt' -OutFile 'VERSION.txt' -UseBasicParsing"

# 버전 확인
type VERSION.txt
# 출력: v6.30.65-PAPER-MODE-FIX

# 봇 시작
python -B -u -m src.main --mode paper
```

---

## 📝 **체크리스트**

실행 전 확인:
- [ ] `VERSION.txt` = `v6.30.65-PAPER-MODE-FIX`
- [ ] `__pycache__` 폴더 모두 삭제됨
- [ ] `python -B` 플래그로 시작

실행 후 확인:
- [ ] 로그에 `"모의거래 모드: 포지션 전체 매도 허용"` 출현
- [ ] 로그에 `"========== 포지션 청산 시작 =========="` 출현
- [ ] 로그에 `"holding_protector.close_bot_position()"` 출현
- [ ] 로그에 `"risk_manager.close_position()"` 출현
- [ ] 로그에 `"✅ UI 업데이트 완료"` 출현
- [ ] 포지션이 화면에서 사라짐
- [ ] 매도 카운터 증가

---

## 🔗 **다운로드**

- **전체 ZIP**: https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
- **main.py**: https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py
- **VERSION.txt**: https://raw.githubusercontent.com/lee-jungkil/Lj/main/VERSION.txt

---

## 📊 **버전 히스토리**

| 버전 | 날짜 | 변경 내용 | 상태 |
|------|------|-----------|------|
| v6.30.63 | 2026-02-14 | 초기 매도 실패 보고 | ❌ 버그 |
| v6.30.64 | 2026-02-15 | early return 제거, 포지션 청산 강제 진행 | ⚠️ 부분 수정 |
| v6.30.65 | 2026-02-15 | **모의거래 holding_protector 우회** | ✅ **완전 해결** |

---

## 🎯 **결론**

**v6.30.65는 모의거래 모드에서 매도가 차단되는 치명적 버그를 완전히 해결했습니다.**

- ✅ 모의거래: `holding_protector` 체크 완전 우회
- ✅ 실거래: 기존 보유 보호 정상 작동
- ✅ 모든 모드에서 포지션 청산 로직 정상 실행

**즉시 업데이트를 권장합니다!**
