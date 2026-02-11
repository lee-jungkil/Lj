# ⚠️ 환경변수 오류 해결 완료!

## 🔍 문제 원인

스크린샷에서 보이는 오류들:
```
'T_10'은(는) 내부 또는 외부 명령, 실행할 수 있는 프로그램, 또는 배치 파일이 아닙니다.
'T_20'은(는) 내부 또는 외부 명령...
'백명'은(는) 내부 또는 외부 명령...
...
```

**원인:** `.env` 파일에 동적 코인 선정 관련 환경변수가 누락되어 있어서 Config 모듈이 제대로 로드되지 않음.

---

## ✅ 해결 완료

`.env` 파일에 다음 설정 추가됨:
```env
# ===== 🆕 동적 코인 선정 시스템 =====
ENABLE_DYNAMIC_COIN_SELECTION=true  # 동적 코인 선정 활성화
CAPITAL_MODE=10                     # 자본금 모드: 10만원
COIN_SELECTION_METHOD=volume        # 거래량 기준
COIN_SELECTION_INTERVAL=300         # 5분 = 300초
```

---

## 🚀 지금 바로 실행하기

### 1단계: 환경 검증 (필수!)
```bash
verify_setup.bat
```

**예상 출력:**
```
====================================
 동적 코인 선정 시스템 검증
====================================

[1/5] 환경변수 확인
✅ TRADING_MODE = paper
✅ INITIAL_CAPITAL = 100000
✅ ENABLE_DYNAMIC_COIN_SELECTION = true
✅ CAPITAL_MODE = 10
✅ COIN_SELECTION_METHOD = volume
✅ COIN_SELECTION_INTERVAL = 300

[2/5] Config 모듈 로딩
✅ TRADING_MODE: paper
✅ INITIAL_CAPITAL: 100,000원
✅ ENABLE_DYNAMIC_COIN_SELECTION: True

[3/5] 동적 코인 선정 모듈 테스트
✅ DynamicCoinSelector 생성 완료
   - 자본금 모드: 10만원
   - 목표 코인 개수: 20개
   - 갱신 주기: 300초 (5분)

[4/5] 거래량 기준 코인 선정 테스트
✅ 전체 KRW 마켓: 200개+
✅ 거래 가능 코인: 20개

[5/5] 초단타 전략 설정 확인
✅ 초단타 전략:
   - 활성화: True
   - 손절: 1.0%
   - 익절: 1.5%
   - 최소 급등: 1.5%
   - 거래량 배수: 2.0배

====================================
✅ 모든 검증 완료!
====================================
```

---

### 2단계: 모의투자 시작
```bash
run_paper.bat
```

**정상 실행 화면:**
```
====================================
 Upbit AutoProfit Bot v5.3
====================================
MODE: PAPER (모의투자)

🔄 동적 코인 선정 시스템 활성화
📊 자본금 모드: 10만원
📈 목표 코인 개수: 20개
⏱️ 선정 간격: 300초 (5분)
🎯 선정 방법: volume

[COIN] 🔄 동적 코인 갱신 시작...
[COIN] 📊 전체 KRW 마켓: 200개+
[COIN] 📈 거래량 Top 50 추출 완료
[COIN] ✅ 최종 선정: 20개
[COIN] 📋 선정 코인: KRW-BTC, KRW-ETH, KRW-XRP, ...

🤖 봇 가동 시작! (AI 학습 통합 모드)
   📅 전체 스캔: 180초 (3분)
   ⚡ 빠른 체크: 5초
   🔥 급등 감지: 10초 (초단타 최대 2개)
```

---

### 3단계: 5분 후 확인 사항

#### ✅ 동적 코인 갱신 로그
```
[12:05:00] [COIN] 🔄 동적 코인 갱신 - 12:05:00
[12:05:00] [COIN] ✅ 코인 목록 갱신: 20개 → 20개
[12:05:00] [COIN] 📋 상위 10개: KRW-BTC, KRW-ETH, ...
[12:05:00] [COIN] 📊 다음 갱신: 295초
```

#### ✅ 초단타 진입 로그
```
[12:07:30] [INFO] 🔍 급등/급락 스캔 중... (초단타 0/2)
[12:08:15] [INFO] 🔥 급등/급락 감지: KRW-DOGE (급등) 
                   가격변동: +1.8%, 거래량: 2.3x
[12:08:15] [TRADE] ⚡ 초단타 매수: KRW-DOGE - 10,000원
```

#### ✅ 일반 매수 로그
```
[12:10:00] [TRADE] 💰 매수: KRW-BTC - aggressive_scalping
                    이유: 거래량 폭증 진입! 
                    (가격: +1.2%, 거래량: 2.6x, RSI: 52.3)
```

---

## 🔧 여전히 오류가 발생한다면?

### 오류 1: 모듈을 찾을 수 없습니다
```
ModuleNotFoundError: No module named 'dotenv'
```

**해결:**
```bash
setup.bat
```

---

### 오류 2: .env 파일이 없습니다
```
FileNotFoundError: .env file not found
```

**해결:**
```bash
# .env.dynamic_10을 .env로 복사
copy .env.dynamic_10 .env
```

---

### 오류 3: pyupbit 연결 실패
```
ConnectionError: API connection failed
```

**해결:**
- 인터넷 연결 확인
- 방화벽 설정 확인
- 잠시 후 재시도

---

## 📂 최신 파일 구조

```
Lj-main/
├── .env                          # ✅ 수정됨 (동적 설정 추가)
├── verify_setup.bat              # ✨ 신규 (환경 검증 도구)
├── verify_dynamic.py             # ✨ 신규 (검증 스크립트)
├── run_paper.bat                 # 모의투자 실행
├── run_live.bat                  # 실거래 실행
├── run_dynamic.bat               # 동적 모드 설정
├── src/
│   ├── config.py                 # ✅ 수정됨
│   ├── main.py                   # ✅ 수정됨
│   └── utils/
│       └── dynamic_coin_selector.py  # ✨ 신규
```

---

## 🎯 실행 순서 (정리)

### 초보자용 (3단계)
```
1) verify_setup.bat       ← 환경 확인
2) run_paper.bat          ← 모의투자
3) 5분 대기 → 로그 확인
```

### 자본금 모드 변경하려면
```
run_dynamic.bat
→ [1] 10만원 (20개 코인)
→ [2] 20만원 (30개 코인)
→ [3] 30만원 (40개 코인)
```

---

## 📞 추가 지원

- **동적 시스템 가이드:** `DYNAMIC_COIN_GUIDE.md`
- **빠른 시작:** `START_HERE.md`
- **코인 선정:** `COIN_SELECTION_GUIDE.md`
- **전체 가이드:** `QUICK_START.md`

---

## 🔗 GitHub

**저장소:** https://github.com/lee-jungkil/Lj  
**커밋:** 88128bf  
**해결:** 환경변수 오류 수정  
**날짜:** 2026-02-11

---

## ✅ 해결 완료 체크리스트

- [x] .env 파일에 동적 설정 추가
- [x] 검증 도구 (verify_setup.bat) 추가
- [x] 검증 스크립트 (verify_dynamic.py) 추가
- [x] GitHub 푸시 완료
- [x] 가이드 문서 작성

**이제 다시 실행하면 정상 작동합니다!** 🎉
