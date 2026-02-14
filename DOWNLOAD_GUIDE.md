# 빠른 다운로드 및 설치 가이드

## 🚀 가장 빠른 방법 (1분)

### Windows CMD에서 실행:

```batch
curl -L -o upbit-bot.zip https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip && tar -xf upbit-bot.zip && cd Lj-main && COMPLETE_REINSTALL.bat
```

---

## 📦 단계별 설명

### 1️⃣ 다운로드

**방법 1: ZIP 파일 (Git 없어도 됨)**
```batch
curl -L -o upbit-bot.zip https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
tar -xf upbit-bot.zip
cd Lj-main
```

**방법 2: Git (권장)**
```batch
git clone https://github.com/lee-jungkil/Lj.git
cd Lj
```

**방법 3: 웹 브라우저**
1. https://github.com/lee-jungkil/Lj 방문
2. 초록색 "Code" 버튼 클릭
3. "Download ZIP" 클릭
4. 압축 해제
5. 폴더로 이동

---

### 2️⃣ 설치

```batch
COMPLETE_REINSTALL.bat
```

- 모든 것을 자동으로 설치합니다
- Y를 입력하여 진행
- 2-5분 소요

---

### 3️⃣ 실행

```batch
RUN_PAPER_CLEAN.bat
```

---

## 🔗 다운로드 링크

### GitHub 저장소
https://github.com/lee-jungkil/Lj

### ZIP 다운로드 (Git 불필요)
https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip

### 특정 파일만 다운로드

**COMPLETE_REINSTALL.bat:**
```batch
curl -o COMPLETE_REINSTALL.bat https://raw.githubusercontent.com/lee-jungkil/Lj/main/COMPLETE_REINSTALL.bat
```

**setup.bat:**
```batch
curl -o setup.bat https://raw.githubusercontent.com/lee-jungkil/Lj/main/setup.bat
```

**RUN_PAPER_CLEAN.bat:**
```batch
curl -o RUN_PAPER_CLEAN.bat https://raw.githubusercontent.com/lee-jungkil/Lj/main/RUN_PAPER_CLEAN.bat
```

**src/main.py:**
```batch
curl -o src\main.py https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py
```

---

## ⚠️ 문제 해결

### curl 명령어가 없어요

Windows 10 1803 이상에는 기본 포함됩니다.  
구버전이면 PowerShell 사용:

```powershell
Invoke-WebRequest -Uri "https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip" -OutFile "upbit-bot.zip"
Expand-Archive -Path "upbit-bot.zip" -DestinationPath "."
cd Lj-main
.\COMPLETE_REINSTALL.bat
```

### Python이 없어요

1. https://www.python.org/downloads/ 방문
2. Python 3.8+ 다운로드
3. 설치 시 "Add Python to PATH" 체크 필수
4. CMD 재시작
5. `python --version` 확인

---

## 📞 지원

- **GitHub Issues:** https://github.com/lee-jungkil/Lj/issues
- **문서:** README.md, COMPLETE_REINSTALL_GUIDE.md

---

**현재 버전:** v6.30.38  
**마지막 업데이트:** 2026-02-14
