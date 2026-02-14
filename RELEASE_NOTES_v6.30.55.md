# 🚀 Upbit AutoProfit Bot v6.30.55 Release Notes

**릴리스 날짜:** 2026-02-14  
**버전:** v6.30.55-STRATEGY-TYPO-FIX  
**GitHub:** https://github.com/lee-jungkil/Lj

---

## 🎯 주요 변경사항

### 🐛 버그 수정 - 매도 안되는 문제 완전 해결!

#### 문제 상황
- 매도가 실행되지 않는 심각한 버그 발견
- 에러 로그: `AttributeError: 'AutoProfitBot' object has no attribute 'aggressive_scaling'`
- 포지션을 보유하고 있어도 청산 체크가 실행되지 않음
- 손익률이 익절/손절 조건을 만족해도 매도가 트리거되지 않음

#### 근본 원인
포지션 데이터에 저장된 전략 이름과 실제 전략 매핑 이름이 불일치:
```
저장된 전략 이름:  aggressive_scaling   ❌ (오타 - 'p' 빠짐)
실제 전략 코드:    aggressive_scalping  ✅ (올바른 철자)
```

이로 인해 `_get_strategy_by_name()` 함수가 전략 객체를 찾지 못하고,  
매도 조건 체크 함수(`check_positions`)가 호출되지 않았습니다.

#### 해결 방법
전략 매핑 딕셔너리에 **오타 버전도 추가**하여 하위 호환성 확보:

**수정 파일:** `src/main.py` - `_get_strategy_by_name()` 함수

**추가된 매핑:**
```python
# Aggressive Scalping (공격적 단타)
'AGGRESSIVE_SCALING': self.strategies.get('aggressive_scalping'),  # ← NEW
'aggressive_scaling': self.strategies.get('aggressive_scalping'),  # ← NEW
'AGGRESSIVE-SCALING': self.strategies.get('aggressive_scalping'),  # ← NEW
'aggressive-scaling': self.strategies.get('aggressive_scalping'),  # ← NEW

# Conservative Scalping (보수적 단타)
'CONSERVATIVE_SCALING': self.strategies.get('conservative_scalping'),  # ← NEW
'conservative_scaling': self.strategies.get('conservative_scalping'),  # ← NEW
'CONSERVATIVE-SCALING': self.strategies.get('conservative_scalping'),  # ← NEW
'conservative-scaling': self.strategies.get('conservative_scalping'),  # ← NEW
```

---

## ✅ 해결된 문제

1. **매도 실행 안되는 문제** ✅
   - 기존에 `aggressive_scaling`로 저장된 포지션도 정상 처리
   - 전략 객체를 올바르게 찾아서 매도 조건 체크 실행

2. **AttributeError 해결** ✅
   - `'AutoProfitBot' object has no attribute 'aggressive_scaling'` 에러 완전 제거
   - 모든 전략 이름 케이스 (대소문자, 하이픈, 언더스코어) 지원

3. **하위 호환성 유지** ✅
   - 기존 포지션 데이터 변경 없이 작동
   - 새로운 포지션과 기존 포지션 모두 정상 처리

---

## 📋 변경 파일 목록

### 코드 수정
- ✅ `src/main.py` - 전략 매핑 딕셔너리 확장

### 버전 업데이트
- ✅ `VERSION.txt` - v6.30.55-STRATEGY-TYPO-FIX
- ✅ `README.md` - 버전 정보 및 릴리스 노트 추가
- ✅ `COMPLETE_REINSTALL.bat` - v6.30.55
- ✅ `RUN_PAPER_CLEAN.bat` - v6.30.55
- ✅ `RUN_LIVE_CLEAN.bat` - v6.30.55
- ✅ `RUN.bat` - v6.30.55
- ✅ `setup.bat` - v6.30.55
- ✅ `QUICK_UPDATE.bat` - v6.30.55

### 새 파일
- ✅ `RELEASE_NOTES_v6.30.55.md` - 이 문서

---

## 📥 설치 방법

### 방법 1: 완전 재설치 (권장)

```batch
# 1. 프로젝트 다운로드
curl -L -o upbit-bot.zip https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
tar -xf upbit-bot.zip
cd Lj-main

# 2. 완전 재설치 실행
COMPLETE_REINSTALL.bat
```

### 방법 2: Git으로 업데이트

```batch
# 기존 프로젝트 폴더에서
git pull origin main
python -m pip install -r requirements.txt

# 캐시 삭제 (중요!)
del /s /q *.pyc
for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"

# 실행
RUN_PAPER_CLEAN.bat
```

### 방법 3: 직접 다운로드

**ZIP 다운로드 링크:**
```
https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
```

**직접 파일 다운로드 (main.py만):**
```
https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py
```

다운로드 후 `COMPLETE_REINSTALL.bat` 실행

---

## 🧪 테스트 체크리스트

업데이트 후 다음 사항을 확인하세요:

- [ ] 봇이 정상적으로 시작됨
- [ ] 매수 실행 가능
- [ ] 포지션 보유 시 3초마다 청산 체크 로그 출력
- [ ] 익절/손절 조건 만족 시 자동 매도 실행
- [ ] `AttributeError` 발생하지 않음
- [ ] 기존 포지션 정상 처리

---

## 💡 예상 로그

### 정상 작동 시
```
[DEBUG-LOOP] 메인 루프 #152 시작 - 시간: 1739530800.45
[DEBUG-QUICK] 포지션 전략 이름: 'aggressive_scaling' (타입: <class 'str'>)
[DEBUG-STRATEGY-MAP] _get_strategy_by_name 호출됨
[DEBUG-STRATEGY-MAP] 입력 strategy_name: 'aggressive_scaling' (타입: <class 'str'>)
[DEBUG-STRATEGY-MAP] 'aggressive_scaling' in strategy_map? True
[DEBUG-STRATEGY-MAP] ✅ 정확히 매칭됨!
[DEBUG-QUICK] ✅ check_positions() 호출 시작...

--- ⚡ 포지션 청산 체크 #152 - 21:00:00 ---
📊 KRW-BTC 손익률: +1.85% (보유 450초)
   익절 목표: +1.5% | 손절 목표: -1.0%
   ✅ 익절 트리거 발동! (+1.85% >= +1.5%)

💰 매도 주문 체결 완료!
```

---

## ⚠️ 업데이트 전 주의사항

1. **백업 권장**
   - 기존 `.env` 파일 백업
   - 중요한 로그 파일 백업

2. **봇 중지**
   - 업데이트 전 실행 중인 봇 종료 (Ctrl+C)

3. **캐시 삭제**
   - 업데이트 후 반드시 Python 캐시 삭제
   - `COMPLETE_REINSTALL.bat`가 자동으로 처리

---

## 🔗 관련 링크

- **GitHub Repository:** https://github.com/lee-jungkil/Lj
- **Pull Request:** https://github.com/lee-jungkil/Lj/pull/1
- **Issues:** https://github.com/lee-jungkil/Lj/issues

---

## 📞 지원

문제가 발생하면:

1. `COMPLETE_REINSTALL.bat` 실행 (가장 확실한 방법)
2. GitHub Issues에 문의
3. 로그 파일 (`trading_logs/`) 확인

---

## 🎉 다음 버전 예고

v6.30.56에서 예정된 기능:
- 매수/매도 실행 속도 최적화
- 추가적인 전략 안정성 개선
- 로그 시스템 개선

---

**업데이트 후 정상 작동을 확인하시면 GitHub에 ⭐ 부탁드립니다!**

Happy Trading! 🚀📈
