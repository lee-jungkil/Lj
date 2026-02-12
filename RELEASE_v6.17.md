# Upbit AutoProfit Bot - 전체 릴리스 v6.17-SYNC-COMPLETE

## 📦 릴리스 정보
- **버전**: v6.17-SYNC-COMPLETE
- **릴리스 날짜**: 2026-02-12
- **커밋**: cfdc7e4
- **GitHub**: https://github.com/lee-jungkil/Lj

---

## 🎯 이번 릴리스의 주요 특징

### 1️⃣ 완전한 화면 동기화 (v6.17-SYNC)
- ✅ 모든 화면 출력 항목이 실제 데이터와 실시간 동기화
- ✅ 헤더 정보 (시간, AI 학습, 자본) 실시간 업데이트
- ✅ 보유 포지션 (슬롯 1~7) 실시간 가격 반영
- ✅ 매도 기록 영구 저장 및 표시 (최대 10건)
- ✅ 스캔/봇 상태 실시간 모니터링
- ✅ 3초 주기 자동 갱신

### 2️⃣ 매도 기록 영구 저장 (v6.16-SELLHISTORY)
- ✅ 매도 결과가 5초 후 사라지는 문제 해결
- ✅ 최대 10건 매도 기록 저장 (FIFO)
- ✅ 화면에 최근 5건 표시
- ✅ 매수 포지션처럼 영구 표시
- ✅ 시간/티커/손익/전략 모두 표시

### 3️⃣ 화면 스크롤 제거 (v6.15-UPDATE)
- ✅ ANSI 커서 제어로 완전 고정 화면
- ✅ 새 출력 시 스크롤 없음
- ✅ 제자리 업데이트로 안정적 표시
- ✅ 디버그 출력 최소화

### 4️⃣ 손익 동기화 강화 (v6.15-UPDATE)
- ✅ 초기 자본 기준 손익 자동 계산
- ✅ 자본 변화에도 손익 정확히 유지
- ✅ 실시간 손익률 계산
- ✅ 색상으로 수익/손실 구분

### 5️⃣ 리스크 관리 강화 (v6.15-UPDATE)
- ✅ 10% 손실 시 자동 중단
- ✅ 실시간 리스크 모니터링
- ✅ 자동 정지 사유 표시
- ✅ 안전한 거래 보호

### 6️⃣ 한글 인코딩 문제 해결
- ✅ UPDATE.bat 영문 버전 (권장)
- ✅ UPDATE_KR.bat 한글 버전 (보조)
- ✅ 모든 Windows 버전 지원
- ✅ 경로 자동 탐지
- ✅ 에러 처리 강화

### 7️⃣ 업데이트 시스템 구축
- ✅ download_update.bat (Windows)
- ✅ download_update.ps1 (PowerShell)
- ✅ download_update.sh (Linux/Mac)
- ✅ 자동 폴더 생성
- ✅ 빠른 다운로드 (40KB)

---

## 📂 전체 파일 구조

```
Lj-main/
├── VERSION.txt                          # 버전 정보
├── RELEASE_v6.17.md                     # 릴리스 노트 (이 파일)
├── README.md                            # 프로젝트 개요
├── requirements.txt                     # Python 패키지 의존성
│
├── 🚀 실행 파일
│   ├── run.bat                          # 백테스트 실행
│   ├── run_paper.bat                    # 모의투자 실행
│   ├── run_live.bat                     # 실거래 실행
│   ├── QUICKSTART.py                    # 빠른 시작 스크립트
│   └── register_holdings.py             # 보유 코인 등록
│
├── 📥 다운로드 도구
│   ├── download_update.bat              # Windows 업데이트 다운로드
│   ├── download_update.ps1              # PowerShell 업데이트 다운로드
│   └── download_update.sh               # Linux/Mac 업데이트 다운로드
│
├── 📁 src/ - 소스 코드
│   ├── main.py                          # 메인 실행 파일
│   ├── config.py                        # 설정 파일
│   │
│   ├── api/                             # API 모듈
│   │   └── upbit_api.py                 # Upbit API 래퍼
│   │
│   ├── ai/                              # AI 모듈
│   │   ├── learning_engine.py           # AI 학습 엔진
│   │   ├── scenario_identifier.py       # 시나리오 식별
│   │   └── strategy_selector.py         # 전략 선택기
│   │
│   ├── strategies/                      # 거래 전략
│   │   ├── aggressive_scalping.py       # 공격적 스캘핑
│   │   ├── conservative_scalping.py     # 보수적 스캘핑
│   │   └── dynamic_exit_manager.py      # 동적 청산 관리
│   │
│   ├── utils/                           # 유틸리티
│   │   ├── fixed_screen_display.py      # 고정 화면 표시 ⭐ 최신
│   │   ├── risk_manager.py              # 리스크 관리 ⭐ 최신
│   │   ├── logger.py                    # 로깅 시스템
│   │   └── notification.py              # 알림 시스템
│   │
│   └── market/                          # 시장 분석
│       ├── market_condition_analyzer.py # 시장 상태 분석
│       └── surge_detector.py            # 급등 감지
│
├── 📦 update/ - 업데이트 패키지
│   ├── UPDATE.bat                       # 업데이트 실행 (영문) ⭐ 권장
│   ├── UPDATE_KR.bat                    # 업데이트 실행 (한글)
│   ├── fixed_screen_display.py          # 최신 화면 표시 시스템
│   ├── risk_manager.py                  # 최신 리스크 관리
│   ├── test_sell_history.py             # 매도 기록 테스트
│   │
│   └── 📚 문서
│       ├── UPDATE_GUIDE.md              # 업데이트 가이드
│       ├── UPDATE_README.md             # 업데이트 설명서
│       ├── SELL_HISTORY_UPDATE.md       # 매도 기록 기능 설명
│       └── QUICK_UPDATE.md              # 빠른 업데이트 가이드
│
├── 📊 data/ - 데이터 저장소
│   ├── ai_learning/                     # AI 학습 데이터
│   │   ├── strategy_performance.json    # 전략 성과
│   │   └── market_scenarios.json        # 시장 시나리오
│   │
│   ├── backtest/                        # 백테스트 결과
│   └── logs/                            # 로그 파일
│
├── 📚 docs/ - 문서
│   ├── SYNC_COMPLETE.md                 # 동기화 완료 보고서
│   ├── SYNC_VERIFICATION_REPORT.md      # 동기화 검증 보고서
│   ├── SELLHISTORY_COMPLETE.md          # 매도 기록 완료 보고서
│   ├── ENCODING_FIX_COMPLETE.md         # 한글 깨짐 해결 보고서
│   ├── DOWNLOAD_SYSTEM_COMPLETE.md      # 다운로드 시스템 보고서
│   ├── DOWNLOAD_UPDATE_README.md        # 다운로드 가이드
│   └── UPDATE_DOWNLOAD_GUIDE.md         # 상세 다운로드 가이드
│
└── 🔧 tests/ - 테스트
    └── test_suite.py                    # 테스트 스위트
```

---

## 🚀 빠른 시작

### 1️⃣ 전체 프로젝트 다운로드

**방법 A: GitHub에서 직접 다운로드**
```
https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
```

**방법 B: Git Clone**
```bash
git clone https://github.com/lee-jungkil/Lj.git
cd Lj
```

### 2️⃣ 패키지 설치

```bash
pip install -r requirements.txt
```

**필수 패키지:**
- pyupbit
- python-dotenv
- colorama
- pandas
- numpy

### 3️⃣ 환경 설정

`.env` 파일 생성:
```env
UPBIT_ACCESS_KEY=your_access_key_here
UPBIT_SECRET_KEY=your_secret_key_here
```

### 4️⃣ 봇 실행

**백테스트 (추천)**
```bash
run.bat
# 또는
python src/main.py backtest
```

**모의투자**
```bash
run_paper.bat
# 또는
python src/main.py paper
```

**실거래 (주의!)**
```bash
run_live.bat
# 또는
python src/main.py live
```

---

## 🔄 업데이트 방법

### 방법 1: 전체 재다운로드 (권장)
```
1. https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
2. 압축 해제
3. 기존 .env 파일 복사
4. 봇 실행
```

### 방법 2: 부분 업데이트
```
1. download_update.bat 다운로드 및 실행
   https://raw.githubusercontent.com/lee-jungkil/Lj/main/download_update.bat

2. Lj-main\update 폴더로 이동
   cd Lj-main\update

3. UPDATE.bat 실행
   UPDATE.bat

4. 봇 재시작
```

### 방법 3: Git Pull
```bash
cd Lj-main
git pull origin main
```

---

## 📊 화면 출력 예시

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                     🤖 Upbit AutoProfit Bot v6.17-SYNC                      ║
║                          2026-02-12 14:35:45                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ 🧠 AI 학습: 125건 (승률: 68.8%) | 💰 자본: 10,000,000원 → 10,245,000원      ║
║ 📊 총 손익: +245,000원 (+2.45%)                                             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ 💼 보유 포지션 (2/7)                                                         ║
║ ────────────────────────────────────────────────────────────────────────────║
║ [1] KRW-BTC                                      +1.52% (+15,250원) ✅       ║
║     투자: 1,000,000원 → 현재: 1,015,250원                                   ║
║     진입: 50,450,000원 → 현재: 50,600,000원                                 ║
║     보유: 1시간 23분 45초 | 전략: aggressive                                ║
║                                                                              ║
║ [2] KRW-ETH                                      -0.87% (-8,750원) ❌       ║
║     투자: 1,000,000원 → 현재: 991,250원                                     ║
║     진입: 2,850,000원 → 현재: 2,825,000원                                   ║
║     보유: 45분 12초 | 전략: conservative                                    ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ 📜 매도 기록 (5건)                                                           ║
║ ────────────────────────────────────────────────────────────────────────────║
║ ✅ 14:35:22 | KRW-BTC  | +1,250원 (+2.45%)  | aggressi                     ║
║ ❌ 14:30:15 | KRW-ETH  | -350원 (-0.87%)    | conserva                     ║
║ ✅ 14:25:08 | KRW-XRP  | +800원 (+1.52%)    | scalping                     ║
║ ✅ 14:20:45 | KRW-ADA  | +450원 (+1.12%)    | scalping                     ║
║ ❌ 14:15:33 | KRW-DOGE | -120원 (-0.35%)    | aggressi                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ 🔍 스캔: 코인 30개 모니터링 중 | 14:35:42                                    ║
║ 🤖 상태: 정상 운영 중 | 매수: 8건 | 매도: 5건 | 14:35:45                    ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ 📊 BTC 58,450,000원 +2.1% | RSI 58 | 변동성: 보통                           ║
║ 📈 거래량: +15.2% | MACD 상승 | 진입 조건: 양호                             ║
║ 💡 추천 전략: aggressive (신뢰도: 0.85)                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 🔧 주요 설정 (config.py)

### 기본 설정
```python
# 거래 모드
MODE = 'paper'  # 'backtest', 'paper', 'live'

# 초기 자본
INITIAL_CAPITAL = 10000000  # 1천만원

# 포지션 설정
MAX_POSITIONS = 7           # 최대 동시 포지션 수
POSITION_SIZE = 0.1         # 포지션당 자본 비율 (10%)

# 손익 설정
TARGET_PROFIT = 0.02        # 목표 수익률 (2%)
STOP_LOSS = -0.01           # 손절 기준 (-1%)
MAX_LOSS_RATIO = -0.10      # 최대 손실률 (-10%)
```

### AI 학습 설정
```python
# AI 학습
ENABLE_AI_LEARNING = True   # AI 학습 활성화
AI_MIN_TRADES = 10          # 최소 학습 거래 수

# 전략 가중치
STRATEGY_WEIGHTS = {
    'aggressive': 0.4,
    'conservative': 0.3,
    'scalping': 0.3
}
```

### 스캔 설정
```python
# 스캔 주기
FULL_SCAN_INTERVAL = 300    # 전체 스캔 (5분)
POSITION_CHECK_INTERVAL = 3  # 포지션 체크 (3초)
SURGE_SCAN_INTERVAL = 30    # 급등 감지 (30초)

# 화면 갱신
DISPLAY_UPDATE_INTERVAL = 3  # 화면 갱신 (3초)
```

---

## 📈 성능 및 특징

### 실시간 동기화
- ⚡ 3초 주기 화면 갱신
- ⚡ API 실시간 가격 조회
- ⚡ 손익 자동 계산
- ⚡ 상태 실시간 모니터링

### AI 학습 시스템
- 🧠 자동 전략 학습
- 🧠 시장 시나리오 식별
- 🧠 승률 기반 최적화
- 🧠 전략 가중치 조정

### 리스크 관리
- 🛡️ 10% 손실 자동 중단
- 🛡️ 포지션별 손절/익절
- 🛡️ 실시간 리스크 모니터링
- 🛡️ 안전한 거래 보호

### 화면 표시
- 📺 완전 고정 화면 (스크롤 없음)
- 📺 색상으로 수익/손실 구분
- 📺 보유시간 자동 형식화
- 📺 천 단위 구분 표시

---

## 📝 변경 이력

### v6.17-SYNC-COMPLETE (2026-02-12)
- ✅ 모든 화면 출력 항목 실시간 동기화
- ✅ 보유시간 형식 개선 (1시간 02분 05초)
- ✅ 손익률 포맷 통일 (+2.45%)
- ✅ 실시간 가격 동기화 (API)
- ✅ 완전한 문서화

### v6.16-SELLHISTORY (2026-02-12)
- ✅ 매도 기록 영구 저장 (최대 10건)
- ✅ 화면에 최근 5건 표시
- ✅ 5초 후 사라지는 문제 해결
- ✅ FIFO 자동 정리

### v6.15-UPDATE (2026-02-11)
- ✅ 화면 스크롤 완전 제거
- ✅ 손익 동기화 강화
- ✅ 10% 손실 자동 중단
- ✅ 디버그 출력 최소화

### 한글 인코딩 해결 (2026-02-12)
- ✅ UPDATE.bat 영문 버전
- ✅ UPDATE_KR.bat 한글 버전
- ✅ 경로 자동 탐지
- ✅ 에러 처리 강화

### 다운로드 시스템 (2026-02-12)
- ✅ download_update.bat (Windows)
- ✅ download_update.ps1 (PowerShell)
- ✅ download_update.sh (Linux/Mac)
- ✅ 자동 폴더 생성

---

## ⚠️ 주의사항

### 실거래 모드
```
⚠️ 실거래 모드는 실제 자금을 사용합니다!
⚠️ 먼저 백테스트와 모의투자로 충분히 테스트하세요!
⚠️ 소액으로 시작하여 점진적으로 증액하세요!
⚠️ 투자 손실은 본인의 책임입니다!
```

### API 키 보안
```
⚠️ .env 파일을 GitHub에 올리지 마세요!
⚠️ API 키를 다른 사람과 공유하지 마세요!
⚠️ 정기적으로 API 키를 재발급하세요!
```

### 시스템 요구사항
```
✅ Python 3.8 이상
✅ Windows 10/11 (또는 Linux/Mac)
✅ 안정적인 인터넷 연결
✅ Upbit API 키 (실거래 시)
```

---

## 🔗 주요 링크

- **GitHub 저장소**: https://github.com/lee-jungkil/Lj
- **전체 다운로드**: https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
- **업데이트 폴더**: https://github.com/lee-jungkil/Lj/tree/main/update
- **이슈 보고**: https://github.com/lee-jungkil/Lj/issues

**다운로드 스크립트:**
- Windows: https://raw.githubusercontent.com/lee-jungkil/Lj/main/download_update.bat
- PowerShell: https://raw.githubusercontent.com/lee-jungkil/Lj/main/download_update.ps1
- Linux/Mac: https://raw.githubusercontent.com/lee-jungkil/Lj/main/download_update.sh

---

## 📚 문서 목록

1. **RELEASE_v6.17.md** - 릴리스 노트 (이 문서)
2. **SYNC_COMPLETE.md** - 동기화 완료 보고서
3. **SYNC_VERIFICATION_REPORT.md** - 동기화 검증 보고서
4. **SELLHISTORY_COMPLETE.md** - 매도 기록 완료 보고서
5. **ENCODING_FIX_COMPLETE.md** - 한글 깨짐 해결 보고서
6. **DOWNLOAD_SYSTEM_COMPLETE.md** - 다운로드 시스템 보고서
7. **UPDATE_GUIDE.md** - 업데이트 가이드
8. **DOWNLOAD_UPDATE_README.md** - 빠른 다운로드 가이드
9. **UPDATE_DOWNLOAD_GUIDE.md** - 상세 다운로드 가이드

---

## 💡 팁

### 백테스트 활용
```
1. 먼저 백테스트로 전략을 검증하세요
2. 다양한 기간으로 테스트하세요
3. AI 학습 데이터를 축적하세요
4. 승률과 손익을 분석하세요
```

### 모의투자 활용
```
1. 실시간 시장에서 전략을 테스트하세요
2. 실제 시장 상황을 경험하세요
3. 감정 관리 연습을 하세요
4. 충분한 자신감을 얻으세요
```

### 실거래 시작
```
1. 소액으로 시작하세요 (10만원~100만원)
2. 손실을 감당할 수 있는 금액만 투자하세요
3. 정기적으로 성과를 점검하세요
4. 문제 발생 시 즉시 중단하세요
```

---

## 📞 지원

### 문제 보고
GitHub Issues에 보고해주세요:
https://github.com/lee-jungkil/Lj/issues

### 개선 제안
Pull Request를 보내주세요:
https://github.com/lee-jungkil/Lj/pulls

### 문의
GitHub Discussions를 이용해주세요:
https://github.com/lee-jungkil/Lj/discussions

---

## 📄 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

---

## 🎉 마무리

**Upbit AutoProfit Bot v6.17-SYNC-COMPLETE**

모든 기능이 완벽하게 통합되고 동기화된 최신 버전입니다!

- ✅ 매도 기록 영구 저장
- ✅ 화면 완전 동기화
- ✅ 스크롤 제거
- ✅ 손익 자동 계산
- ✅ 리스크 자동 관리
- ✅ 한글 인코딩 해결
- ✅ 간편한 업데이트

**지금 바로 다운로드하여 사용하세요!**

📥 **전체 다운로드**: https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip

🎯 **커밋**: cfdc7e4
📅 **날짜**: 2026-02-12
🏷️ **버전**: v6.17-SYNC-COMPLETE

---

**Happy Trading! 🚀💰**
