# 🎉 Upbit AutoProfit Bot v5.2 실행 준비 완료!

> **커밋**: c8500ea  
> **날짜**: 2026-02-11  
> **GitHub**: https://github.com/lee-jungkil/Lj

---

## ✅ 완료된 작업

### 1️⃣ 실행 파일 생성
- ✅ **setup.bat** - 자동 초기 설정
- ✅ **run_backtest.bat** - 백테스트 실행
- ✅ **run_paper.bat** - 모의투자 실행 (기본값)
- ✅ **run_live.bat** - 실거래 실행

### 2️⃣ 환경 설정
- ✅ **.env** - 초기 설정 완료
  - 초기 자본: **100,000원**
  - 일일 최대 손실: **10,000원 (10%)**
  - 누적 최대 손실: **20,000원 (20%)**
  - 거래 모드: **paper** (모의투자)

### 3️⃣ 문서화
- ✅ **START_HERE.md** - 1분 빠른 시작 가이드
- ✅ **QUICK_START.md** - 초보자용 상세 가이드
- ✅ **.env.example** - 설정 템플릿

---

## 🚀 실행 순서 (처음 사용자)

### 📋 체크리스트

- [ ] **1단계**: setup.bat 실행 (처음 한 번만)
- [ ] **2단계**: run_backtest.bat 실행 (안전한 테스트)
- [ ] **3단계**: run_paper.bat 실행 (모의투자 연습)
- [ ] **4단계**: 1주일 관찰 및 AI 학습
- [ ] **5단계**: .env 파일 최적화
- [ ] **6단계**: run_live.bat 실행 (실거래, 선택)

---

## 🎯 지금 바로 시작하기!

### 방법 1: 자동 설정 (추천)
```
1. setup.bat 더블클릭
2. 설치 완료까지 대기
3. run_backtest.bat 더블클릭
```

### 방법 2: 수동 설정
```
1. 명령 프롬프트 열기
2. cd [프로젝트 폴더 경로]
3. python -m venv venv
4. venv\Scripts\activate.bat
5. pip install -r requirements.txt
6. run_backtest.bat 더블클릭
```

---

## 📊 실행 후 확인사항

### 콘솔에서 확인
```
========================================
 Upbit AutoProfit Bot v5.2
 Mode: PAPER | AI Learning: ACTIVE
========================================

💰 현재 상태:
잔고: ₩100,000
총 자산: ₩100,000
총 수익률: +0.00%
```

### 로그 파일에서 확인
```
trading_logs/
├── trading_20260211.log    # 거래 기록
├── error_20260211.log      # 에러 기록
└── performance_20260211.json  # 성과 데이터
```

### AI 학습 데이터
```
learning_data/
├── trade_history.json      # 전체 거래 이력
├── scenarios/              # 시나리오별 학습
├── strategies/             # 전략별 성과
├── holding_times/          # 보유 시간 최적화
├── losses/                 # 손실 분석
└── optimization/           # 자동 최적화
```

---

## ⚙️ 설정 변경 방법

### .env 파일 수정
```
메모장으로 .env 파일 열기

변경 가능 항목:
- INITIAL_CAPITAL=100000        # 초기 자본
- MAX_DAILY_LOSS=10000          # 일일 최대 손실
- MAX_CUMULATIVE_LOSS=20000     # 누적 최대 손실
- MAX_POSITIONS=3               # 최대 포지션 수
- EXIT_MODE=moderate            # 청산 모드
- TRADING_MODE=paper            # 거래 모드
```

---

## 🤖 AI 시스템 기능

### 현재 활성화된 기능
- ✅ **고급 AI 학습** (ENABLE_ADVANCED_AI)
- ✅ **호가창 분석** (ENABLE_ORDERBOOK_ANALYSIS)
- ✅ **시나리오 감지** (ENABLE_SCENARIO_DETECTION)
- ✅ **스마트 분할 매매** (ENABLE_SMART_SPLIT)
- ✅ **보유 시간 AI** (ENABLE_HOLDING_TIME_AI)
- ✅ **동적 청산** (ENABLE_DYNAMIC_EXIT)

### 학습 단계
```
Phase 2-A: 규칙 기반 (0~20 거래)
   → 사전 정의된 규칙으로 거래

Phase 2-B: 데이터 수집 (20~100 거래)
   → AI가 패턴 학습 시작

Phase 2-C: 고급 최적화 (100+ 거래)
   → AI 완전 자동화
```

---

## 🎓 학습 로드맵

### 1주차: 백테스트
```
목표: 시스템 이해하기
방법: run_backtest.bat 실행
확인: 전략 동작, 손절/익절, 수익률
```

### 2주차: 모의투자
```
목표: 실시간 시장 경험
방법: run_paper.bat 실행 (24시간)
확인: 급등/급락 대응, 포지션 관리
```

### 3주차: AI 학습 분석
```
목표: 학습 데이터 이해
방법: learning_data/ 폴더 분석
확인: 시나리오 승률, 전략 성과
```

### 4주차: 설정 최적화
```
목표: 개인 맞춤 설정
방법: .env 파일 조정
확인: 포지션 수, 청산 모드
```

### 5주차 이후: 실거래 (선택)
```
목표: 소액 실전 투자
조건: 백테스트 +15%, 모의투자 1주일
방법: API 키 입력 → run_live.bat
```

---

## 🔔 알림 설정 (선택사항)

### 텔레그램 알림
```
.env 파일에 추가:

TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

발급 방법:
1. 텔레그램에서 @BotFather 검색
2. /newbot 명령으로 봇 생성
3. 토큰 입력
```

### Gmail 알림
```
.env 파일에 추가:

GMAIL_SENDER=your_email@gmail.com
GMAIL_PASSWORD=your_app_password
GMAIL_RECEIVER=receiver@email.com

발급 방법:
1. Gmail 보안 설정
2. 2단계 인증 활성화
3. 앱 비밀번호 생성
```

---

## ⚠️ 실거래 전 확인사항

### 필수 체크리스트
- [ ] 백테스트 수익률 +15% 이상
- [ ] 모의투자 1주일 이상 안정적 운영
- [ ] AI 학습 데이터 100개 이상
- [ ] 손실 제한 설정 확인
- [ ] Upbit API 키 발급 완료
- [ ] 긴급 상황 대응 계획

### Upbit API 키 발급
```
1. Upbit 홈페이지 로그인
2. 마이페이지 > Open API 관리
3. API 키 발급
   - 조회 권한: ✓
   - 거래 권한: ✓
   - 출금 권한: ✗ (보안상 권장하지 않음)
4. IP 화이트리스트 설정 (선택)
5. .env 파일에 키 입력
```

---

## 🚨 문제 해결

### "Python을 찾을 수 없습니다"
```
→ Python 재설치 (Add to PATH 체크)
→ 시스템 환경변수 확인
```

### "패키지 설치 실패"
```
→ 관리자 권한으로 실행
→ pip 업그레이드: pip install --upgrade pip
```

### "봇이 거래를 하지 않습니다"
```
→ 콘솔 로그 확인
→ trading_logs/ 폴더 확인
→ 시장 조건 확인 (진입 조건 미충족 가능)
```

### "API 키 오류"
```
→ .env 파일에 키 정확히 입력
→ Upbit API 권한 확인
→ IP 화이트리스트 확인
```

---

## 📈 목표 지표

| 지표 | 목표 | 현재 |
|------|------|------|
| 총 수익률 | +15% 이상 | 0% (시작 전) |
| 승률 | 60% 이상 | - |
| 최대 낙폭 | -10% 미만 | - |
| 일일 손익 | +3% 이상 | - |

---

## 📚 추가 문서

- **START_HERE.md** - 1분 빠른 시작 가이드
- **QUICK_START.md** - 초보자용 상세 가이드 (8,000자)
- **API_OPTIMIZATION_SUMMARY.md** - API 최적화 보고서
- **LEARNING_COMPLETE_REPORT.md** - AI 학습 시스템 보고서
- **REALTIME_MONITORING_GUIDE.md** - 실시간 모니터링 가이드

---

## 🎉 준비 완료!

모든 준비가 완료되었습니다.  
**setup.bat**을 실행하여 시작하세요!

```
프로젝트 폴더에서:
1. setup.bat 더블클릭
2. 설치 완료까지 대기
3. run_backtest.bat 더블클릭
```

---

## 📞 지원

- **GitHub**: https://github.com/lee-jungkil/Lj
- **버전**: v5.2
- **커밋**: c8500ea
- **날짜**: 2026-02-11

---

## ⚠️ 면책 조항

- 이 봇은 교육 및 연구 목적으로 제공됩니다
- 실제 거래로 인한 손실에 대해 개발자는 책임지지 않습니다
- 투자는 본인의 판단과 책임 하에 진행하세요
- 과거 성과가 미래 수익을 보장하지 않습니다

---

**💡 팁: 처음에는 반드시 백테스트부터 시작하세요!**
