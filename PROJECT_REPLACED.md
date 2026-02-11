# ✅ 프로젝트 교체 완료!

## 📦 업로드된 파일로 교체

**파일**: Lj-main.zip (425KB)  
**소스**: 사용자 업로드  
**날짜**: 2026-02-11

---

## 🔄 교체 작업 내용

### 1. 백업
- 이전 프로젝트 → `/home/user/webapp_backup`으로 백업

### 2. 신규 프로젝트 배포
- Lj-main.zip 압축 해제
- `/home/user/webapp`에 신규 프로젝트 배포

### 3. Git 저장소 재구성
- 새로운 Git 저장소 초기화
- 전체 파일 커밋
- 강제 푸시: `git push -f origin main`

---

## 📊 새 프로젝트 정보

### 버전
**Upbit AutoProfit Bot v5.1**

### 주요 특징
- ✅ **Phase 1**: 텔레그램/Gmail 손익 알림 시스템
- ✅ **Phase 2**: 20가지 분할 전략 + 45가지 시나리오 + 호가창 분석
- ✅ **AI 학습**: 보유 시간 최적화 + 전략 선택 + 동적 청산
- ✅ **실시간 호가창 모니터링** + 학습 시스템
- ✅ **실시간 체결 데이터 수집** + 매수/매도 강도 분석
- 3분 주기: 전체 코인 스캔 + 신규 진입
- 5초 주기: 포지션 빠른 체크
- 10초 주기: 급등/급락 감지 (최적화)

---

## 📁 프로젝트 구조

### 배치 파일 (11개)
```
setup.bat              - 초기 설치
run.bat                - 기본 실행 (백테스트)
run_backtest.bat       - 백테스트 모드
run_paper.bat          - 모의투자 모드
run_live.bat           - 실거래 모드
run_dynamic.bat        - 동적 코인 선택 모드
run_test.bat           - 테스트 모드
test_install.bat       - 설치 확인
verify_setup.bat       - 설정 검증
change_coin_count.bat  - 코인 개수 변경
fix_logs.bat           - 로그 수정
```

### 소스 코드
```
src/
├── main.py                    # 메인 봇 엔진 (v5.1)
├── config.py                  # 설정 관리
├── upbit_api.py               # Upbit API 래퍼
├── strategies/                # 전략 모듈
│   ├── aggressive_scalping.py
│   ├── conservative_scalping.py
│   ├── mean_reversion.py
│   ├── grid_trading.py
│   ├── ultra_scalping.py
│   ├── split_strategies.py    # 20가지 분할 전략
│   └── dynamic_exit_manager.py
├── ai/                        # AI 학습 시스템
│   ├── learning_engine.py
│   ├── strategy_selector.py
│   ├── holding_time_optimizer.py
│   ├── scenario_identifier.py # 45가지 시나리오
│   ├── adaptive_learner.py
│   └── auto_optimizer.py
└── utils/                     # 유틸리티
    ├── fixed_screen_display.py
    ├── order_book_analyzer.py  # 호가창 분석
    ├── orderbook_monitor.py    # 호가창 모니터링
    ├── trade_monitor.py        # 체결 데이터 모니터링
    ├── smart_order_executor.py # 스마트 주문 실행
    ├── telegram_notifier.py    # 텔레그램 알림
    ├── email_reporter.py       # 이메일 보고서
    └── ...
```

### 문서 (50+ 개)
```
README.md                      - 프로젝트 개요
START_HERE.md                  - 시작 가이드
QUICK_START.md                 - 빠른 시작
QUICKRUN.md                    - 빠른 실행 가이드
PHASE1_PHASE2_INTEGRATION.md   - Phase 1+2 통합 가이드
PHASE2_COMPLETE_GUIDE.md       - Phase 2 완전 가이드
AI_LEARNING_SYSTEM.md          - AI 학습 시스템 가이드
REALTIME_MONITORING_GUIDE.md   - 실시간 모니터링 가이드
ULTRA_SCALPING.md              - 초단타 전략 가이드
ADAPTIVE_LEARNING.md           - 적응형 학습 가이드
... (40+ 추가 가이드)
```

---

## 🚀 사용 방법

### Windows 사용자

#### 1. 초기 설치
```
setup.bat 더블클릭
```

#### 2. .env 파일 설정
```env
UPBIT_ACCESS_KEY=실제_액세스_키
UPBIT_SECRET_KEY=실제_시크릿_키

INITIAL_CAPITAL=500000
MAX_POSITIONS=7
TRADING_MODE=backtest
```

#### 3. 실행
```
run.bat 더블클릭              # 백테스트
run_paper.bat 더블클릭        # 모의투자
run_live.bat 더블클릭         # 실거래
run_dynamic.bat 더블클릭      # 동적 코인 선택
```

### Linux/Unix 사용자

```bash
# 설치
pip install -r requirements.txt

# .env 설정
cp .env.example .env
nano .env

# 실행
./run.sh backtest             # 백테스트
./run.sh paper                # 모의투자
./run.sh live                 # 실거래
```

---

## 📊 통계

### Git
```
Commit: 070afef
Files: 134 files
Lines: 37,689 insertions
Branch: main
Remote: https://github.com/lee-jungkil/Lj.git
```

### 파일 수
```
배치 파일: 11개
Python 소스: 30+ 개
문서: 50+ 개
환경 설정: 6개 (.env.*)
테스트 파일: 5개
```

---

## 🔗 다운로드

**GitHub 저장소**:
```
https://github.com/lee-jungkil/Lj
```

**최신 커밋**:
```
https://github.com/lee-jungkil/Lj/commit/070afef
```

**ZIP 다운로드**:
```
https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
```

---

## ✨ 주요 기능

### Phase 1 - 알림 시스템
- ✅ 텔레그램 실시간 알림
- ✅ Gmail 일일/주간 보고서
- ✅ 손익 자동 보고

### Phase 2 - 고급 전략
- ✅ 20가지 분할 매수/매도 전략
- ✅ 45가지 시장 시나리오 인식
- ✅ 호가창 실시간 분석
- ✅ 체결 데이터 학습
- ✅ 슬리피지 최소화

### AI 학습
- ✅ 보유 시간 최적화 학습
- ✅ 전략 자동 선택
- ✅ 동적 손절/익절 조정
- ✅ 시장 상황 적응형 학습
- ✅ 파라미터 자동 최적화

### 실시간 모니터링
- ✅ 호가창 실시간 모니터링
- ✅ 체결 강도 분석
- ✅ 급등/급락 감지
- ✅ 고정 화면 표시 (스크롤 없음)

---

## 📝 환경 설정 파일

```
.env.example       - 기본 예시
.env.20coins       - 20개 코인 설정
.env.50coins       - 50개 코인 설정
.env.dynamic_10    - 동적 10개 코인
.env.dynamic_20    - 동적 20개 코인
.env.dynamic_30    - 동적 30개 코인
.env.test          - 테스트 설정
```

---

## 🎯 시작 가이드

### 빠른 시작 (Windows)
```
1. setup.bat
2. .env 파일 편집
3. run.bat
```

### 상세 가이드 확인
```
START_HERE.md       - 여기서부터 시작
QUICK_START.md      - 빠른 시작 가이드
QUICKRUN.md         - 즉시 실행 가이드
```

---

## 🎉 완료!

**새로운 Upbit AutoProfit Bot v5.1이 성공적으로 배포되었습니다!**

- ✅ 업로드된 Lj-main.zip으로 완전 교체
- ✅ Git 저장소 업데이트
- ✅ 모든 파일 정상 배포
- ✅ 11개 배치 파일 포함
- ✅ 50+ 문서 포함
- ✅ Phase 1 + Phase 2 완전 통합
- ✅ AI 학습 시스템 포함
- ✅ 실시간 모니터링 시스템 포함

**다운로드**: https://github.com/lee-jungkil/Lj  
**버전**: v5.1  
**커밋**: 070afef

---

**지금 바로 시작하세요!** 🚀
