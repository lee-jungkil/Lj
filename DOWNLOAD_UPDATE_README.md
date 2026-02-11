# 📦 업데이트 파일 다운로드 방법

## 🎯 목적
전체 프로젝트가 아닌 **업데이트 파일만** 다운로드하여 빠르게 업데이트

---

## 🚀 빠른 다운로드 (권장)

### Windows 사용자

#### 방법 1: 배치 파일 (가장 쉬움)
```batch
# 1. 다운로드 스크립트 받기
https://raw.githubusercontent.com/lee-jungkil/Lj/main/download_update.bat
   → 우클릭 "다른 이름으로 저장" → download_update.bat

# 2. 더블클릭 실행
download_update.bat

# 3. update 폴더가 자동으로 생성됨!
```

#### 방법 2: PowerShell
```powershell
# 1. 다운로드 스크립트 받기
https://raw.githubusercontent.com/lee-jungkil/Lj/main/download_update.ps1
   → 우클릭 "다른 이름으로 저장" → download_update.ps1

# 2. PowerShell에서 실행
powershell -ExecutionPolicy Bypass -File download_update.ps1
```

#### 방법 3: 수동 다운로드 (curl)
```batch
mkdir update
cd update
curl -L -O https://raw.githubusercontent.com/lee-jungkil/Lj/main/update/UPDATE.bat
curl -L -O https://raw.githubusercontent.com/lee-jungkil/Lj/main/update/fixed_screen_display.py
```

---

### Linux/Mac 사용자

#### 방법 1: 쉘 스크립트 (권장)
```bash
# 1. 다운로드 스크립트 받기
wget https://raw.githubusercontent.com/lee-jungkil/Lj/main/download_update.sh
# 또는
curl -O https://raw.githubusercontent.com/lee-jungkil/Lj/main/download_update.sh

# 2. 실행 권한 부여
chmod +x download_update.sh

# 3. 실행
./download_update.sh

# 4. update 폴더가 자동으로 생성됨!
```

#### 방법 2: 수동 다운로드 (wget)
```bash
mkdir -p update
cd update
wget https://raw.githubusercontent.com/lee-jungkil/Lj/main/update/UPDATE.bat
wget https://raw.githubusercontent.com/lee-jungkil/Lj/main/update/fixed_screen_display.py
```

---

## 📂 다운로드되는 파일

### 필수 파일 (2개)
1. ✅ **UPDATE.bat** (3.0 KB) - 업데이트 실행 스크립트
2. ✅ **fixed_screen_display.py** (15.9 KB) - 매도 기록 기능 포함

### 선택 파일 (5개)
3. 📄 **UPDATE_README.md** (2.0 KB) - 사용 가이드
4. 📄 **SELL_HISTORY_UPDATE.md** (4.4 KB) - 매도 기록 설명
5. 📄 **UPDATE_GUIDE.md** (8.3 KB) - 전체 업데이트 가이드
6. 🧪 **test_sell_history.py** (6.0 KB) - 테스트 스크립트
7. 🇰🇷 **UPDATE_KR.bat** (3.4 KB) - 한글 버전 (보조)

---

## 📋 사용 방법

### 1. update 폴더 배치
다운로드한 `update` 폴더를 프로젝트 루트에 배치:
```
Lj-main/
  ├── src/
  ├── update/          ← 여기에 배치
  │   ├── UPDATE.bat
  │   └── fixed_screen_display.py
  └── ...
```

### 2. 업데이트 실행

#### Windows
```batch
cd Lj-main\update
UPDATE.bat
```

#### Linux/Mac
```bash
cd Lj-main
cp update/fixed_screen_display.py src/utils/
```

---

## 🔗 다운로드 링크

### 자동 다운로드 스크립트
- **Windows 배치**: https://raw.githubusercontent.com/lee-jungkil/Lj/main/download_update.bat
- **Windows PowerShell**: https://raw.githubusercontent.com/lee-jungkil/Lj/main/download_update.ps1
- **Linux/Mac 쉘**: https://raw.githubusercontent.com/lee-jungkil/Lj/main/download_update.sh

### update 폴더 직접 접근
- **GitHub 웹**: https://github.com/lee-jungkil/Lj/tree/main/update

### 개별 파일 다운로드
- **UPDATE.bat**: https://raw.githubusercontent.com/lee-jungkil/Lj/main/update/UPDATE.bat
- **fixed_screen_display.py**: https://raw.githubusercontent.com/lee-jungkil/Lj/main/update/fixed_screen_display.py

---

## 🌐 웹 도구 사용

### DownGit (폴더 전체 ZIP)
1. https://minhaskamal.github.io/DownGit/#/home 접속
2. URL 입력: `https://github.com/lee-jungkil/Lj/tree/main/update`
3. "Download" 클릭
4. `update.zip` 다운로드 완료!

---

## ✅ 체크리스트

업데이트 전 확인:
- [ ] 프로젝트 루트 위치 확인 (`Lj-main` 폴더)
- [ ] `update` 폴더 배치 완료
- [ ] 필수 파일 다운로드 완료 (UPDATE.bat, fixed_screen_display.py)
- [ ] Python 프로세스 종료 (실행 중이면)

업데이트 후 확인:
- [ ] 백업 폴더 생성됨 (`backup/backup_YYYYMMDD_HHMMSS/`)
- [ ] 버전 표시: `v6.16-SELLHISTORY`
- [ ] 매도 기록 섹션 표시됨

---

## 💡 팁

### 최소 다운로드 (빠름)
2개 파일만:
```batch
curl -L -O https://raw.githubusercontent.com/lee-jungkil/Lj/main/update/UPDATE.bat
curl -L -O https://raw.githubusercontent.com/lee-jungkil/Lj/main/update/fixed_screen_display.py
```

### 완전 다운로드 (권장)
전체 프로젝트:
```
https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
```

---

## 🆘 문제 해결

### curl/wget이 없어요
**Windows**: Windows 10 이상은 curl 내장. PowerShell 스크립트 사용
**Linux/Mac**: 패키지 매니저로 설치
```bash
# Ubuntu/Debian
sudo apt install curl wget

# macOS
brew install wget
```

### 다운로드가 안돼요
1. 인터넷 연결 확인
2. 방화벽 확인
3. GitHub 접속 확인: https://github.com
4. 수동 다운로드 시도 (웹 브라우저)

### 파일이 깨져요
- `.bat` 파일: "다른 이름으로 저장" 사용 (복사/붙여넣기 X)
- Raw 버튼 클릭 후 저장
- 인코딩 확인: UTF-8

---

## 📞 도움

- **이슈**: https://github.com/lee-jungkil/Lj/issues
- **가이드**: UPDATE_DOWNLOAD_GUIDE.md (상세 설명)

---

**빠르게 업데이트하세요!** 🚀
