# 🚀 한글 실행 가이드

## ⚠️ 배치 파일 한글 깨짐 해결

배치 파일(`.bat`)은 Windows 명령 프롬프트의 인코딩 제한으로 한글이 깨져 보일 수 있습니다.
하지만 **실행에는 전혀 문제가 없습니다!**

---

## 📋 실행 순서 (간단 요약)

### 1️⃣ setup.bat (처음 한 번만)
```
더블클릭으로 실행
→ Python 확인
→ 가상환경 생성
→ 패키지 설치
→ .env 파일 생성
```

### 2️⃣ run_backtest.bat (백테스트)
```
더블클릭으로 실행
→ 과거 데이터로 테스트
→ 완전 안전 (실제 거래 없음)
```

### 3️⃣ run_paper.bat (모의투자)
```
더블클릭으로 실행
→ 실시간 데이터
→ 가상 거래 (완전 안전)
→ AI 학습 데이터 수집
```

### 4️⃣ run_live.bat (실거래)
```
⚠️ 주의: 실제 돈으로 거래!

사전 준비:
1. .env 파일 열기 (메모장)
2. UPBIT_ACCESS_KEY 입력
3. UPBIT_SECRET_KEY 입력
4. TRADING_MODE=live로 변경

실행:
더블클릭으로 실행
→ 경고 메시지 확인
→ 아무 키나 눌러 시작
```

---

## 🎯 배치 파일 메뉴 해석

### setup.bat 실행 시
```
[1/4] Python 설치 확인 중...
[OK] Python installation confirmed
→ Python이 설치되어 있음

[2/4] 가상환경 생성 중...
[OK] Virtual environment created
→ 가상환경 생성 완료

[3/4] 필요한 패키지 설치 중...
[OK] Packages installed successfully
→ pyupbit, pandas 등 설치 완료

[4/4] 환경 설정 파일 생성 중...
[OK] .env file created
→ 설정 파일 준비 완료

Setup Complete!
→ 모든 설정 완료!
```

### run_backtest.bat 실행 시
```
[INFO] Preparing environment...
→ 환경 준비 중

[OK] Python installation confirmed
→ Python 확인 완료

Starting Backtest Mode
→ 백테스트 시작

(이후 봇이 실행되고 콘솔에 실시간 로그가 표시됩니다)
```

### run_paper.bat 실행 시
```
Initial Capital: 100,000 KRW
Max Daily Loss: 10%
Max Cumulative Loss: 20%
→ 초기 자본: 10만원
→ 일일 최대 손실: 10%
→ 누적 최대 손실: 20%

Starting Paper Trading Mode
→ 모의투자 시작

TIP: Press Ctrl+C to stop
→ 팁: Ctrl+C를 눌러 종료
```

### run_live.bat 실행 시
```
WARNING: LIVE TRADING MODE
This mode trades with REAL MONEY!
→ 경고: 실거래 모드
→ 실제 돈으로 거래합니다!

Please confirm:
  1. Upbit API keys are configured in .env
  2. Tested thoroughly with backtest and paper trading
  3. Risk management settings are verified
→ 확인 사항:
→ 1. API 키가 .env에 설정됨
→ 2. 백테스트와 모의투자로 충분히 테스트함
→ 3. 리스크 관리 설정을 확인함

Press any key to continue...
→ 계속하려면 아무 키나 누르세요
```

---

## 🔍 에러 메시지 해석

### [ERROR] Python is not installed!
```
→ Python이 설치되지 않았습니다
→ https://www.python.org/ 에서 Python 3.8 이상 다운로드
→ 설치 시 "Add Python to PATH" 체크 필수
```

### [ERROR] Failed to create virtual environment!
```
→ 가상환경 생성 실패
→ 관리자 권한으로 다시 실행해보세요
```

### [ERROR] Failed to install packages!
```
→ 패키지 설치 실패
→ pip 업그레이드: python -m pip install --upgrade pip
→ 재시도: 배치 파일 다시 실행
```

### [ERROR] .env file not found!
```
→ .env 파일이 없습니다
→ setup.bat을 먼저 실행하세요
→ 또는 .env.example을 .env로 복사하세요
```

### [ERROR] Upbit API keys are not configured!
```
→ Upbit API 키가 설정되지 않았습니다
→ .env 파일을 열어서
→ UPBIT_ACCESS_KEY와 UPBIT_SECRET_KEY를 입력하세요
```

### [ERROR] Bot encountered an error!
```
→ 봇 실행 중 오류 발생
→ trading_logs/ 폴더에서 로그 확인
→ 자세한 내용은 QUICK_START.md의 "6. 문제 해결" 참조
```

---

## 📊 실행 후 확인사항

### 정상 실행 시 콘솔 화면
```
========================================
 Upbit AutoProfit Bot v5.2
 Mode: PAPER | AI Learning: ACTIVE
========================================

현재 상태:
잔고: ₩100,000
총 자산: ₩100,000
총 수익률: +0.00%
일일 손익: ₩0
승률: 0.00% (0/0)
총 거래 수: 0

보유 포지션: 없음

AI 학습 단계: Phase 2-A (규칙 기반)
전략: 20개 | 시나리오: 45개
```

---

## 💡 핵심 팁

### 1. 한글이 깨져도 정상입니다
- 배치 파일의 한글은 깨져 보일 수 있지만
- 실행에는 전혀 문제가 없습니다
- 영어로 표시되는 메시지를 참고하세요

### 2. 실행 순서 준수
```
setup.bat (처음 한 번)
   ↓
run_backtest.bat (테스트)
   ↓
run_paper.bat (모의투자, 1주일)
   ↓
run_live.bat (실거래, 선택)
```

### 3. 로그 확인 위치
```
trading_logs/           ← 거래 기록
├── trading_YYYYMMDD.log
├── error_YYYYMMDD.log
└── performance_YYYYMMDD.json

learning_data/          ← AI 학습 데이터
├── trade_history.json
├── scenarios/
├── strategies/
└── losses/
```

### 4. 종료 방법
```
Ctrl + C 누르기
→ 안전하게 종료됩니다
→ 모든 포지션은 자동으로 청산됩니다
```

### 5. 설정 변경
```
메모장으로 .env 파일 열기
→ 원하는 설정 변경
→ 저장
→ 배치 파일 다시 실행
```

---

## 🚨 중요 주의사항

### ⚠️ 실거래 전 필수 체크
- [ ] 백테스트 수익률 +15% 이상
- [ ] 모의투자 1주일 이상 안정적 운영
- [ ] AI 학습 데이터 100개 이상
- [ ] Upbit API 키 발급 완료
- [ ] .env에 API 키 입력 완료
- [ ] TRADING_MODE=live로 변경

### ⚠️ API 키 발급 방법
```
1. Upbit 홈페이지 (https://upbit.com) 로그인
2. 마이페이지 > Open API 관리
3. API 키 발급
   ✅ 조회 권한
   ✅ 거래 권한
   ❌ 출금 권한 (보안상 비활성화)
4. .env 파일에 입력
   UPBIT_ACCESS_KEY=발급받은_키
   UPBIT_SECRET_KEY=발급받은_비밀키
5. TRADING_MODE=live로 변경
```

---

## 📚 추가 도움말

### 상세 가이드
- **QUICK_START.md** - 초보자용 완전 가이드 (13KB)
- **START_HERE.md** - 1분 빠른 시작
- **EXECUTION_READY.md** - 실행 준비 체크리스트

### 문제 해결
- **QUICK_START.md > 6. 문제 해결** 섹션
- **trading_logs/** 폴더의 로그 파일

### AI 학습 시스템
- **LEARNING_COMPLETE_REPORT.md** - 완전 학습 보고서
- **AI_LEARNING_SYSTEM.md** - AI 시스템 상세

---

## 🎉 준비 완료!

**모든 배치 파일이 준비되었습니다!**

```
setup.bat을 더블클릭하여 시작하세요!
```

---

**GitHub**: https://github.com/lee-jungkil/Lj  
**버전**: v5.2  
**날짜**: 2026-02-11
