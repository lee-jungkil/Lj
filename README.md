# Upbit AutoProfit Bot v6.30.38

🤖 **AI 기반 Upbit 자동매매 봇 - 완전 재설치 시스템**

---

## 🚀 빠른 시작 (1분)

### Windows 사용자

```batch
# 1. 프로젝트 다운로드
curl -L -o upbit-bot.zip https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
tar -xf upbit-bot.zip
cd Lj-main

# 2. 완전 재설치 (권장)
COMPLETE_REINSTALL.bat
```

**또는 Git 사용:**

```batch
git clone https://github.com/lee-jungkil/Lj.git
cd Lj
COMPLETE_REINSTALL.bat
```

---

## 📦 주요 파일

### 실행 파일
- **COMPLETE_REINSTALL.bat** - 완전 재설치 (문제 발생 시)
- **setup.bat** - 초기 설정
- **RUN_PAPER_CLEAN.bat** - 모의투자 시작
- **RUN_LIVE_CLEAN.bat** - 실전투자 시작

### 업데이트
- **QUICK_UPDATE.bat** - 빠른 업데이트
- **UPDATE.bat** - 전체 업데이트

### 기타
- **RUN.bat** - 기본 실행
- **DOWNLOAD_ALL_FILES.bat** - 전체 파일 다운로드

---

## ⚙️ 시스템 요구사항

- **OS:** Windows 10/11
- **Python:** 3.8 이상
- **메모리:** 2GB 이상
- **디스크:** 500MB 이상
- **인터넷:** 필수

---

## 📖 사용 방법

### 1️⃣ 처음 설치

```batch
# 프로젝트 다운로드
git clone https://github.com/lee-jungkil/Lj.git
cd Lj

# 완전 재설치 실행
COMPLETE_REINSTALL.bat
```

### 2️⃣ 설정

`.env` 파일 수정:

```env
# 거래 모드
TRADING_MODE=paper  # 모의투자 (paper) 또는 실전 (live)

# 초기 자본
INITIAL_CAPITAL=5000000

# 리스크 관리
MAX_DAILY_LOSS=500000
MAX_CUMULATIVE_LOSS=1000000
MAX_POSITIONS=5
MAX_POSITION_RATIO=0.3

# Upbit API 키 (실전 거래 시 필수)
UPBIT_ACCESS_KEY=
UPBIT_SECRET_KEY=
```

### 3️⃣ 실행

**모의투자:**
```batch
RUN_PAPER_CLEAN.bat
```

**실전투자:**
```batch
RUN_LIVE_CLEAN.bat
```

---

## 🔧 문제 해결

### ❌ DEBUG 로그가 안 나와요

```batch
COMPLETE_REINSTALL.bat
```

### ❌ ImportError: TradingBot 클래스 없음

```batch
COMPLETE_REINSTALL.bat
```

### ❌ 포지션 청산 체크가 안 돼요

```batch
COMPLETE_REINSTALL.bat
```

### ❌ Python이 설치 안 됐어요

1. https://www.python.org/ 방문
2. Python 3.8+ 다운로드
3. 설치 시 **"Add Python to PATH" 체크 필수**
4. 재시작 후 `COMPLETE_REINSTALL.bat` 실행

---

## 📊 예상 로그

### 정상 작동 시

```
[2026-02-14 21:00:00] 🤖 봇 가동 시작!

[DEBUG-LOOP] 메인 루프 #1 시작 - 시간: 1771067600.12

[DEBUG] Phase 3 체크 - 포지션: 0개
[DEBUG] ⚠️ 포지션 없음, Phase 3 스킵

[DEBUG-SLEEP] 5.00초 대기 중...
```

### 포지션 보유 시

```
--- ⚡ 포지션 청산 체크 #5 - 21:00:45 ---
📊 KRW-BTC 손익률: +1.23% (보유 180초)
   익절 목표: +1.5% | 손절 목표: -1.0%
   📊 보유 유지
```

### 매도 실행 시

```
✅ 익절 트리거 발동! (+1.58% >= +1.5%)

💰 매도 주문 체결 완료!
   코인: KRW-BTC
   매도가: 45,234,000 원
   수익: +358,920 원 (+1.58%)
```

---

## 📚 상세 문서

자세한 내용은 [COMPLETE_REINSTALL_GUIDE.md](COMPLETE_REINSTALL_GUIDE.md)를 참고하세요.

---

## 🌟 주요 기능

### AI 기반 매매
- ✅ 실시간 시장 분석
- ✅ 기술적 지표 복합 분석 (RSI, MACD, 볼린저밴드 등)
- ✅ AI 학습 기반 매매 전략
- ✅ 동적 손절/익절 최적화

### 리스크 관리
- ✅ 일일 손실 한도
- ✅ 누적 손실 한도
- ✅ 최대 포지션 수 제한
- ✅ 포지션별 비율 관리

### 자동 청산
- ✅ 3초마다 포지션 체크
- ✅ 10가지 청산 조건
- ✅ 즉시 매도 실행
- ✅ 완전 자동화

### 모니터링
- ✅ 실시간 손익 표시
- ✅ 상세 로그 기록
- ✅ 고정 화면 UI
- ✅ 거래 통계

---

## ⚠️ 주의사항

1. **모의투자 먼저 테스트**
   - 실전 거래 전 반드시 모의투자로 테스트하세요

2. **API 키 보안**
   - `.env` 파일을 절대 공유하지 마세요
   - Git에 업로드하지 마세요

3. **리스크 관리**
   - 초기 자본은 손실 가능한 금액으로 설정하세요
   - 손실 한도를 반드시 설정하세요

4. **법적 책임**
   - 모든 투자 손실은 사용자 책임입니다
   - 프로그램 오류로 인한 손실도 책임지지 않습니다

---

## 🔗 링크

- **GitHub:** https://github.com/lee-jungkil/Lj
- **Issues:** https://github.com/lee-jungkil/Lj/issues
- **Version:** v6.30.38-COMPLETE-REINSTALL-SYSTEM

---

## 📞 지원

문제가 발생하면:
1. [COMPLETE_REINSTALL_GUIDE.md](COMPLETE_REINSTALL_GUIDE.md) 확인
2. GitHub Issues에 문의
3. `COMPLETE_REINSTALL.bat` 실행

---

## 📜 라이선스

이 프로젝트는 개인 사용 목적으로 제공됩니다.  
상업적 사용은 제한될 수 있습니다.

---

**마지막 업데이트:** 2026-02-14  
**현재 버전:** v6.30.38
