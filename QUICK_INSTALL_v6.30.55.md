# 🚀 Upbit AutoProfit Bot v6.30.55 - 빠른 설치 가이드

**버전:** v6.30.55-STRATEGY-TYPO-FIX  
**릴리스:** 2026-02-14  
**중요도:** 🔴 CRITICAL - 매도 안되는 버그 해결

---

## ⚡ 1분 빠른 설치 (Windows)

### 방법 1: ZIP 다운로드 (가장 쉬움) ✨

1. **ZIP 파일 다운로드**
   ```
   https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
   ```

2. **압축 해제**
   - 다운로드한 `main.zip` 파일을 우클릭
   - "압축 풀기" 선택
   - 원하는 폴더에 압축 해제

3. **자동 설치 실행**
   - 압축 푼 폴더로 이동
   - `COMPLETE_REINSTALL.bat` 더블클릭
   - 모든 것이 자동으로 설치됩니다!

---

### 방법 2: curl 명령어 (빠름)

**PowerShell 또는 명령 프롬프트에서 실행:**

```batch
# 1. 다운로드 및 압축 해제
curl -L -o upbit-bot.zip https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
tar -xf upbit-bot.zip

# 2. 폴더 이동
cd Lj-main

# 3. 자동 설치
COMPLETE_REINSTALL.bat
```

---

### 방법 3: Git Clone (개발자용)

```batch
# 1. Clone
git clone https://github.com/lee-jungkil/Lj.git
cd Lj

# 2. 설치
COMPLETE_REINSTALL.bat
```

---

## 📥 직접 다운로드 링크

### 전체 프로젝트
- **ZIP 파일:** https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
- **GitHub 릴리스:** https://github.com/lee-jungkil/Lj/releases

### 개별 파일 (급할 때)
- **main.py:** https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py
- **config.py:** https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/config.py
- **requirements.txt:** https://raw.githubusercontent.com/lee-jungkil/Lj/main/requirements.txt

---

## 🔄 기존 사용자 업데이트 방법

### 자동 업데이트 (권장)

기존 프로젝트 폴더에서:

```batch
# Git이 있는 경우
git pull origin main
COMPLETE_REINSTALL.bat

# Git이 없는 경우
QUICK_UPDATE.bat
```

### 수동 업데이트

1. 기존 `.env` 파일 백업
2. 위의 "방법 1" 또는 "방법 2"로 새로 다운로드
3. `.env` 파일 복원
4. `COMPLETE_REINSTALL.bat` 실행

---

## ⚙️ 설치 후 설정

### 1. .env 파일 수정

```env
# 거래 모드
TRADING_MODE=paper  # 모의투자는 paper, 실전은 live

# 초기 자본
INITIAL_CAPITAL=5000000

# 리스크 관리
MAX_DAILY_LOSS=500000
MAX_CUMULATIVE_LOSS=1000000
MAX_POSITIONS=7
MAX_POSITION_RATIO=0.3

# 실전 거래 시 필수 (모의투자는 불필요)
UPBIT_ACCESS_KEY=여기에_본인의_키_입력
UPBIT_SECRET_KEY=여기에_본인의_키_입력
```

### 2. 실행 방법

**모의투자 (테스트):**
```batch
RUN_PAPER_CLEAN.bat
```

**실전투자:**
```batch
RUN_LIVE_CLEAN.bat
```

---

## 🆕 v6.30.55 업데이트 내용

### 🐛 Critical Bug Fix
**매도가 실행되지 않는 심각한 버그 완전 해결!**

#### 증상
- ❌ 매도가 안됨
- ❌ AttributeError 발생
- ❌ 포지션 청산 체크 실패

#### 해결
- ✅ 전략 이름 오타 처리 (`aggressive_scaling` → `aggressive_scalping`)
- ✅ 하위 호환성 유지
- ✅ 모든 케이스 지원 (대소문자, 하이픈, 언더스코어)

#### 결과
- ✅ 기존 포지션 정상 작동
- ✅ 자동 매도 정상 실행
- ✅ 에러 완전 제거

---

## ✅ 설치 확인 체크리스트

설치 후 다음을 확인하세요:

- [ ] Python 3.8 이상 설치됨
- [ ] `src\main.py` 파일 존재
- [ ] `.env` 파일 생성됨
- [ ] 필요한 패키지 설치 완료
- [ ] 봇이 정상적으로 시작됨
- [ ] DEBUG 로그가 3-5초마다 출력됨

**정상 작동 시 로그 예시:**
```
[DEBUG-LOOP] 메인 루프 #1 시작...
[DEBUG] Phase 3 체크 - 포지션: 0개
[DEBUG-SLEEP] 5.00초 대기 중...
```

---

## 🚨 문제 해결

### Python이 설치되지 않음
1. https://www.python.org/ 방문
2. Python 3.8 이상 다운로드
3. 설치 시 **"Add Python to PATH" 반드시 체크**
4. 재부팅 후 재시도

### 패키지 설치 실패
```batch
# 수동 설치
python -m pip install --upgrade pip
python -m pip install pyupbit pandas numpy requests python-dotenv colorlog ta
```

### 봇이 시작되지 않음
```batch
# 완전 재설치
COMPLETE_REINSTALL.bat
```

### DEBUG 로그가 안 나옴
```batch
# 캐시 삭제 후 재시작
del /s /q *.pyc
RUN_PAPER_CLEAN.bat
```

---

## 📞 지원

### 문제 보고
- **GitHub Issues:** https://github.com/lee-jungkil/Lj/issues
- **Pull Request:** https://github.com/lee-jungkil/Lj/pull/1

### 문서
- **README:** https://github.com/lee-jungkil/Lj/blob/main/README.md
- **릴리스 노트:** https://github.com/lee-jungkil/Lj/blob/main/RELEASE_NOTES_v6.30.55.md

---

## 📦 시스템 요구사항

- **OS:** Windows 10/11
- **Python:** 3.8 이상
- **메모리:** 2GB 이상
- **디스크:** 500MB 이상
- **인터넷:** 필수 (실시간 시세)

---

## ⚠️ 중요 공지

### 모의투자 먼저!
실전 거래 전 반드시 **모의투자(paper mode)**로 충분히 테스트하세요!

### API 키 보안
- `.env` 파일을 절대 공유하지 마세요
- Git에 업로드하지 마세요
- API 키는 타인에게 노출되면 안 됩니다

### 투자 책임
- 모든 투자 손실은 사용자 본인의 책임입니다
- 프로그램 오류로 인한 손실도 책임지지 않습니다
- 리스크를 충분히 이해한 후 사용하세요

---

## 🎉 성공적인 설치를 기원합니다!

설치가 완료되고 정상 작동하면:
- GitHub에 ⭐ 부탁드립니다!
- 문제가 있으면 Issues에 남겨주세요

**Happy Trading! 🚀📈**

---

**최종 업데이트:** 2026-02-14  
**버전:** v6.30.55-STRATEGY-TYPO-FIX  
**GitHub:** https://github.com/lee-jungkil/Lj
