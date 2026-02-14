# 🔍 매도 미실행 문제 진단 가이드 - v6.30.48

## 📋 현재 상황

### 확인된 문제
- ✅ Phase 3 정상 실행 (3초마다 루프)
- ✅ 포지션 6개 감지됨
- ✅ `quick_check_positions()` 진입 확인
- ✅ 각 코인별 손익률 계산 및 출력
- ❌ **`check_positions()` 호출 로그 없음**
- ❌ **실제 매도 주문 실행 안 됨**

### 포지션 현황 (스크린샷 기준)
| 코인 | 손익률 | 보유 시간 | 시간 초과 여부 (5분 기준) | 손절 필요 (-1.0%) |
|------|--------|-----------|--------------------------|-----------------|
| SOL | +0.31% | 39분 51초 | ⚠️ **34분 초과** | ❌ |
| STRAX | +0.18% | 36분 58초 | ⚠️ **31분 초과** | ❌ |
| CBK | +0.00% | 25분 15초 | ⚠️ **20분 초과** | ❌ |
| VANA | +0.18% | 16분 20초 | ⚠️ **11분 초과** | ❌ |
| OM | +0.10% | 16분 13초 | ⚠️ **11분 초과** | ❌ |
| KITE | **-1.73%** | 11분 9초 | ⚠️ **6분 초과** | ✅ **손절 필요!** |

**분석**: 
- **모든 코인이 5분 시간 제한을 초과함**
- **KITE는 손절 기준(-1.0%)도 초과함**
- → 정상적이라면 **즉시 전량 매도**되어야 함

---

## 🐛 원인 추정

### 가설 1: 전략 객체가 None으로 반환됨
```python
# quick_check_positions() 내부
strategy_name = position.strategy
strategy = self._get_strategy_by_name(strategy_name)  # ← 이게 None을 반환?

if strategy:  # ← 여기서 False가 되어 check_positions()가 호출 안 됨
    self.check_positions(ticker, strategy)
```

**가능한 원인**:
1. `position.strategy`에 저장된 문자열이 `strategy_map`에 없는 값
2. `position.strategy`가 `None` 또는 빈 문자열
3. `_get_strategy_by_name()`이 예외를 발생시키고 있음

---

## 🔧 v6.30.48 변경 사항

### 추가된 디버그 로그

#### 1. `quick_check_positions()` - 전략 객체 가져오기 전/후
```python
[DEBUG-QUICK] 포지션 전략 이름: 'AGGRESSIVE' (타입: <class 'str'>)
[DEBUG-STRATEGY-MAP] _get_strategy_by_name 호출됨
[DEBUG-STRATEGY-MAP] 입력 strategy_name: 'AGGRESSIVE' (타입: <class 'str'>)
[DEBUG-QUICK] 전략 객체 결과: <bound method AutoProfitBot.aggressive_scalping> (타입: <class 'method'>)
[DEBUG-QUICK] strategy is None? False
[DEBUG-QUICK] bool(strategy)? True
```

#### 2. `_get_strategy_by_name()` - 내부 매핑 로직
```python
[DEBUG-STRATEGY-MAP] strategy_map 키 목록: ['AGGRESSIVE', 'AGGRESSIVE_SCALPING', '공격적', 'CONSERVATIVE', 'CONSERVATIVE_SCALPING', '보수적', 'MEAN_REVERSION', '평균회귀', 'GRID', 'GRID_TRADING', '그리드', 'ULTRA_SCALPING', 'ULTRA', '초단타', 'CHASE_BUY']
[DEBUG-STRATEGY-MAP] 'AGGRESSIVE' in strategy_map? True
[DEBUG-STRATEGY-MAP] 반환 결과: <bound method AutoProfitBot.aggressive_scalping> (타입: <class 'method'>)
```

#### 3. `check_positions()` 진입 시
```python
[DEBUG-CHECK] ========== check_positions(KRW-SOL) 시작 ==========
[DEBUG-CHECK] 조건 1: 시간 초과 체크
[DEBUG-CHECK] - 전략: AGGRESSIVE
[DEBUG-CHECK] - 최대 보유 시간: 300초 (5분)
[DEBUG-CHECK] - 현재 보유 시간: 2391초 (39분 51초)
[DEBUG-CHECK] - 시간 초과? 2391.0 > 300 = True
[DEBUG-CHECK] ⚠️ 시간 초과 청산 조건 충족!
[DEBUG-CHECK] - 보유: 39분, 손익: +0.31%
⏰ 시간초과청산: KRW-SOL (보유: 39분, 손익: +0.31%)
💰 매도 주문 실행 중...
✅ 시간 초과 매도 완료! (매도가: 123,456원)
```

---

## 📥 업데이트 방법

### 방법 1: 원라이너 (Windows)
```batch
cd C:\Users\admin\Downloads\Lj-main && taskkill /F /IM python.exe /T 2>nul & curl -o src\main.py https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py && python -B -u RUN_DIRECT.py
```

### 방법 2: 단계별 실행
```batch
# 1. 봇 중지 (Ctrl+C 또는 강제 종료)
taskkill /F /IM python.exe /T

# 2. 프로젝트 디렉토리로 이동
cd C:\Users\admin\Downloads\Lj-main

# 3. 최신 코드 다운로드
curl -o src\main.py https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py

# 4. 버전 확인
type VERSION.txt
# 출력: v6.30.48-STRATEGY-DEBUG-ENHANCED

# 5. 캐시 삭제
del /s /q *.pyc
for /d /r . %d in (__pycache__) do @rd /s /q "%d"

# 6. 봇 재시작
python -B -u RUN_DIRECT.py
```

---

## 📊 업데이트 후 예상 로그

### 정상 케이스 (전략 객체 정상)
```
[DEBUG-LOOP] 메인 루프 #179 - 시간: 1771081567.82
[DEBUG-LOOP] has_positions? True (count=6)
[DEBUG-LOOP] ✅ 포지션 있음! Phase 3 실행! (count=6)
...
[DEBUG-QUICK] quick_check_positions 진입 - has_positions: True, count: 6
--- ⚡ 포지션 청산 체크 #9 --- (2026-02-14 13:45:23)

🔍 매도 조건 체크 (6개 포지션)
🔍 매도 체크 [1/6] KRW-SOL 손익률 확인...

📊 KRW-SOL 손익률: +0.31% (보유 39분 51초)
   익절 목표: +1.5% | 손절 목표: -1.0%

[DEBUG-QUICK] 포지션 전략 이름: 'AGGRESSIVE' (타입: <class 'str'>)
[DEBUG-STRATEGY-MAP] _get_strategy_by_name 호출됨
[DEBUG-STRATEGY-MAP] 입력 strategy_name: 'AGGRESSIVE' (타입: <class 'str'>)
[DEBUG-STRATEGY-MAP] strategy_map 키 목록: ['AGGRESSIVE', 'AGGRESSIVE_SCALPING', '공격적', 'CONSERVATIVE', ...]
[DEBUG-STRATEGY-MAP] 'AGGRESSIVE' in strategy_map? True
[DEBUG-STRATEGY-MAP] 반환 결과: <bound method AutoProfitBot.aggressive_scalping> (타입: <class 'method'>)

[DEBUG-QUICK] 전략 객체 결과: <bound method AutoProfitBot.aggressive_scalping> (타입: <class 'method'>)
[DEBUG-QUICK] strategy is None? False
[DEBUG-QUICK] bool(strategy)? True

[DEBUG-QUICK] ✅ check_positions() 호출 시작...
[INFO] 🎯 KRW-SOL → check_positions() 호출 (전략: AGGRESSIVE)

[DEBUG-CHECK] ========== check_positions(KRW-SOL) 시작 ==========
[DEBUG-CHECK] 조건 1: 시간 초과 체크
[DEBUG-CHECK] - 전략: AGGRESSIVE
[DEBUG-CHECK] - 최대 보유 시간: 300초 (5분)
[DEBUG-CHECK] - 현재 보유 시간: 2391초 (39분 51초)
[DEBUG-CHECK] - 시간 초과? 2391.0 > 300 = True

[DEBUG-CHECK] ⚠️ 시간 초과 청산 조건 충족!
[DEBUG-CHECK] - 보유: 39분, 손익: +0.31%

⏰ 시간초과청산: KRW-SOL (보유: 39분, 손익: +0.31%)
💰 매도 주문 실행 중...
✅ 시간 초과 매도 완료! (수익: +387원)

[DEBUG-QUICK] ✅ check_positions() 호출 완료
```

### 비정상 케이스 (전략 객체 None)
```
[DEBUG-QUICK] 포지션 전략 이름: 'UNKNOWN_STRATEGY' (타입: <class 'str'>)
[DEBUG-STRATEGY-MAP] _get_strategy_by_name 호출됨
[DEBUG-STRATEGY-MAP] 입력 strategy_name: 'UNKNOWN_STRATEGY' (타입: <class 'str'>)
[DEBUG-STRATEGY-MAP] strategy_map 키 목록: ['AGGRESSIVE', 'CONSERVATIVE', ...]
[DEBUG-STRATEGY-MAP] 'UNKNOWN_STRATEGY' in strategy_map? False
[DEBUG-STRATEGY-MAP] 반환 결과: <bound method AutoProfitBot.aggressive_scalping> (타입: <class 'method'>)  # ← 기본값 반환

[DEBUG-QUICK] 전략 객체 결과: <bound method AutoProfitBot.aggressive_scalping> (타입: <class 'method'>)
[DEBUG-QUICK] strategy is None? False
[DEBUG-QUICK] bool(strategy)? True

[DEBUG-QUICK] ✅ check_positions() 호출 시작...  # ← 이것도 정상적으로 호출되어야 함 (기본값)
```

**주의**: `_get_strategy_by_name()`은 매칭 실패 시 **기본값으로 `aggressive_scalping`을 반환**하므로, **절대 None을 반환하지 않습니다**.

따라서 만약 `if strategy:` 조건이 False라면, 이는 **다른 문제**가 있다는 뜻입니다.

---

## 🧪 진단 체크리스트

업데이트 후 스크린샷을 찍어서 다음 항목들을 확인하세요:

### ✅ 1. 전략 이름 확인
```
[DEBUG-QUICK] 포지션 전략 이름: '????' (타입: ????)
```
- **기대값**: `'AGGRESSIVE'`, `'CONSERVATIVE'`, `'MEAN_REVERSION'`, `'GRID'` 중 하나
- **타입**: `<class 'str'>`

### ✅ 2. 전략 객체 매핑 확인
```
[DEBUG-STRATEGY-MAP] 'AGGRESSIVE' in strategy_map? ????
```
- **기대값**: `True` (또는 매칭 실패 시 기본값 사용)

### ✅ 3. 전략 객체 반환 확인
```
[DEBUG-QUICK] 전략 객체 결과: ???? (타입: ????)
[DEBUG-QUICK] strategy is None? ????
[DEBUG-QUICK] bool(strategy)? ????
```
- **기대값**: 
  - 결과: `<bound method AutoProfitBot.aggressive_scalping>` (또는 다른 전략)
  - `strategy is None?`: `False`
  - `bool(strategy)?`: `True`

### ✅ 4. check_positions() 호출 확인
```
[DEBUG-QUICK] ✅ check_positions() 호출 시작...
[DEBUG-CHECK] ========== check_positions(KRW-SOL) 시작 ==========
```
- **기대**: 이 두 로그가 **반드시** 출력되어야 함

### ✅ 5. 시간 초과 조건 확인
```
[DEBUG-CHECK] - 현재 보유 시간: ????초 (??분 ??초)
[DEBUG-CHECK] - 시간 초과? ???? > 300 = ????
```
- **기대값**: 
  - SOL: `2391초 (39분 51초)`, `2391.0 > 300 = True`
  - KITE: `669초 (11분 9초)`, `669.0 > 300 = True`

### ✅ 6. 매도 실행 확인
```
[DEBUG-CHECK] ⚠️ 시간 초과 청산 조건 충족!
⏰ 시간초과청산: KRW-SOL (보유: 39분, 손익: +0.31%)
💰 매도 주문 실행 중...
✅ 시간 초과 매도 완료!
```
- **기대**: 6개 코인 모두 순차적으로 매도되어야 함

---

## 🎯 다음 단계

### 1️⃣ 업데이트 실행
```batch
cd C:\Users\admin\Downloads\Lj-main && taskkill /F /IM python.exe /T 2>nul & curl -o src\main.py https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py && python -B -u RUN_DIRECT.py
```

### 2️⃣ 30초 대기
- Phase 3가 최소 5~10회 실행될 때까지 대기

### 3️⃣ 스크린샷 촬영
- 전체 콘솔 로그 캡처
- 특히 `[DEBUG-QUICK]`, `[DEBUG-STRATEGY-MAP]`, `[DEBUG-CHECK]` 로그에 집중

### 4️⃣ 결과 공유
- 스크린샷을 보내주시면 원인을 정확히 파악할 수 있습니다

---

## 📚 관련 문서

- **레포지토리**: https://github.com/lee-jungkil/Lj
- **최신 커밋**: https://github.com/lee-jungkil/Lj/commit/dd5d508
- **main.py (raw)**: https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py
- **보유 시간 가이드**: https://github.com/lee-jungkil/Lj/blob/main/HOLD_TIME_UPDATE_v6.30.47.md

---

## 🚨 긴급 문제 해결

### Q: 로그가 전혀 안 보여요
**A**: `python -u` 옵션이 빠졌을 수 있습니다. 반드시 `python -B -u RUN_DIRECT.py`로 실행하세요.

### Q: 여전히 매도가 안 돼요
**A**: 스크린샷을 공유해주시면 디버그 로그를 분석해서 정확한 원인을 찾겠습니다.

### Q: `check_positions()` 호출 로그는 나오는데 매도가 안 돼요
**A**: 이 경우 `execute_sell()` 내부에 문제가 있을 가능성이 높습니다. 추가 디버그가 필요합니다.

---

**버전**: v6.30.48-STRATEGY-DEBUG-ENHANCED  
**날짜**: 2026-02-14  
**작성자**: AI Assistant  
**목적**: 매도 미실행 문제의 정확한 원인 파악을 위한 진단 가이드
