# 🚀 빠른 실행 가이드

## ⚡ 3단계로 바로 시작하기!

### Linux/Mac 사용자
```bash
# 1. 다운로드 및 압축 해제
unzip upbit-autobot.zip
cd upbit-autobot

# 2. 실행 스크립트 실행
./run.sh
```

### Windows 사용자
```batch
# 1. upbit-autobot.zip 다운로드 및 압축 해제

# 2. run.bat 더블클릭 또는 명령 프롬프트에서 실행
run.bat
```

---

## 📋 실행 스크립트가 자동으로 해주는 것

✅ Python 버전 확인  
✅ 가상환경 자동 생성  
✅ 의존성 패키지 자동 설치  
✅ .env 파일 자동 생성  
✅ 모드 선택 메뉴 제공  

---

## 🎯 거래 모드 선택

스크립트 실행 시 선택할 수 있습니다:

1. **backtest** - 백테스트 (실제 거래 없음, API 키 불필요)
2. **paper** - 모의투자 (가상 거래)
3. **live** - 실거래 (⚠️ 실제 자금 사용!)

---

## 📝 API 키 설정 (실거래/모의투자 시)

1. [Upbit API 관리](https://upbit.com/mypage/open_api_management)에서 키 발급
2. `.env` 파일 열기
3. API 키 입력:
   ```
   UPBIT_ACCESS_KEY=발급받은_액세스_키
   UPBIT_SECRET_KEY=발급받은_시크릿_키
   ```

---

## ✅ 테스트 실행

```bash
# 모든 테스트 실행
python -m pytest tests/test_bot.py -v

# 결과: 11/11 테스트 통과 ✅
```

---

## 🔧 수동 실행 (고급 사용자)

```bash
# 1. 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 환경 설정
cp .env.example .env
# .env 파일 편집

# 4. 봇 실행
python src/main.py --mode backtest
```

---

## 📊 실행 화면 예시

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           🚀 Upbit AutoProfit Bot 🚀                        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

✅ Python 발견: Python 3.12.11
✅ 가상환경 생성 완료!
✅ 의존성 설치 완료!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  거래 모드를 선택하세요:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1) backtest  - 백테스트 (실제 거래 없음, API 키 불필요)
  2) paper     - 모의투자 (가상 거래)
  3) live      - 실거래 (⚠️  실제 자금 사용!)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

선택 (1-3): 1

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 봇 시작 중... (모드: backtest)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2024-02-10 15:30:00 [INFO] 🚀 AutoProfit Bot 시작 (모드: backtest)
2024-02-10 15:30:00 [INFO] 🤖 봇 가동 시작!
2024-02-10 15:30:02 [INFO] 📊 시장 감정: NEUTRAL (0.50)
...
```

---

## ⚠️ 주의사항

### 실거래 전 필수 확인
- ✅ 백테스트로 충분히 테스트
- ✅ 소액으로 먼저 시작 (50만원 권장)
- ✅ API 키 권한 확인 (자산 조회, 주문)
- ✅ 손실 한도 설정 확인

### 보안
- 🔒 API 키를 절대 공유하지 마세요
- 🔒 .env 파일을 Git에 올리지 마세요
- 🔒 공개 저장소에 주의하세요

---

## 🆘 문제 해결

### Python이 없다고 나올 때
- Python 3.8 이상 설치 필요
- https://www.python.org/downloads/

### 패키지 설치 실패 시
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### API 키 오류
- Upbit에서 API 키 권한 확인
- .env 파일에 올바르게 입력했는지 확인

---

## 📞 지원

- 📖 상세 문서: `README.md`
- 🚀 빠른 가이드: `QUICKSTART.py`
- 💾 다운로드: `DOWNLOAD.md`

---

**💡 Tip**: 백테스트 모드로 먼저 실행해보고, 로그를 확인한 후 실거래를 시작하세요!
