# Update 폴더 다운로드 가이드

## 📦 업데이트 파일만 다운로드하는 방법

업데이트 파일만 필요한 경우, 전체 프로젝트를 다운로드할 필요 없이 `update` 폴더만 받을 수 있습니다.

---

## 🚀 방법 1: GitHub 웹에서 직접 다운로드 (가장 쉬움)

### 1. GitHub 페이지 접속
https://github.com/lee-jungkil/Lj/tree/main/update

### 2. 파일 하나씩 다운로드
각 파일을 클릭 → "Raw" 버튼 → 우클릭 "다른 이름으로 저장"

**필수 파일:**
- `UPDATE.bat` (업데이트 스크립트)
- `fixed_screen_display.py` (메인 업데이트 파일)

**문서 (선택):**
- `UPDATE_README.md`
- `SELL_HISTORY_UPDATE.md`
- `test_sell_history.py`

---

## 🔽 방법 2: DownGit 사용 (폴더 전체 ZIP)

### 1. DownGit 페이지 접속
https://minhaskamal.github.io/DownGit/#/home

### 2. URL 입력
```
https://github.com/lee-jungkil/Lj/tree/main/update
```

### 3. "Download" 버튼 클릭
`update.zip` 파일이 다운로드됩니다.

### 4. 압축 해제
`update.zip` → `update` 폴더

---

## 💻 방법 3: Git Sparse Checkout (고급)

Git이 설치된 경우:

```bash
# 1. 새 폴더 생성
mkdir Lj-update
cd Lj-update

# 2. Git 초기화
git init

# 3. 리모트 추가
git remote add origin https://github.com/lee-jungkil/Lj.git

# 4. Sparse checkout 활성화
git config core.sparseCheckout true

# 5. update 폴더만 체크아웃 설정
echo "update/*" >> .git/info/sparse-checkout

# 6. 다운로드
git pull origin main

# 결과: Lj-update/update/ 폴더에 파일들
```

---

## 📋 방법 4: wget 또는 curl 사용 (Linux/Mac)

### wget 사용
```bash
mkdir -p update
cd update

# 필수 파일 다운로드
wget https://raw.githubusercontent.com/lee-jungkil/Lj/main/update/UPDATE.bat
wget https://raw.githubusercontent.com/lee-jungkil/Lj/main/update/fixed_screen_display.py

# 문서 (선택)
wget https://raw.githubusercontent.com/lee-jungkil/Lj/main/update/UPDATE_README.md
wget https://raw.githubusercontent.com/lee-jungkil/Lj/main/update/SELL_HISTORY_UPDATE.md
```

### curl 사용
```bash
mkdir -p update
cd update

# 필수 파일 다운로드
curl -O https://raw.githubusercontent.com/lee-jungkil/Lj/main/update/UPDATE.bat
curl -O https://raw.githubusercontent.com/lee-jungkil/Lj/main/update/fixed_screen_display.py

# 문서 (선택)
curl -O https://raw.githubusercontent.com/lee-jungkil/Lj/main/update/UPDATE_README.md
curl -O https://raw.githubusercontent.com/lee-jungkil/Lj/main/update/SELL_HISTORY_UPDATE.md
```

---

## 🪟 방법 5: PowerShell 자동 다운로드 스크립트 (Windows)

### 1. PowerShell 스크립트 생성

`download_update.ps1` 파일 생성:

```powershell
# Update 폴더 생성
New-Item -ItemType Directory -Force -Path "update"
Set-Location "update"

# 기본 URL
$baseUrl = "https://raw.githubusercontent.com/lee-jungkil/Lj/main/update"

# 다운로드할 파일 목록
$files = @(
    "UPDATE.bat",
    "fixed_screen_display.py",
    "UPDATE_README.md",
    "SELL_HISTORY_UPDATE.md",
    "UPDATE_GUIDE.md",
    "test_sell_history.py"
)

# 각 파일 다운로드
foreach ($file in $files) {
    $url = "$baseUrl/$file"
    Write-Host "Downloading $file..."
    Invoke-WebRequest -Uri $url -OutFile $file
    Write-Host "  Downloaded: $file"
}

Write-Host "`nAll files downloaded successfully!"
Write-Host "Location: $PWD"
```

### 2. 실행
```powershell
powershell -ExecutionPolicy Bypass -File download_update.ps1
```

---

## 📦 필수 파일 목록

업데이트를 위한 **최소 필수 파일**:

1. ✅ **UPDATE.bat** (2.5 KB)
   - 업데이트 실행 스크립트

2. ✅ **fixed_screen_display.py** (12.8 KB)
   - 메인 업데이트 파일
   - 매도 기록 기능 포함

**권장 추가 파일** (문서):

3. 📄 **UPDATE_README.md** (2.0 KB)
   - 사용 가이드

4. 📄 **SELL_HISTORY_UPDATE.md** (2.7 KB)
   - 매도 기록 기능 설명

5. 🧪 **test_sell_history.py** (5.4 KB)
   - 테스트 스크립트

---

## 🎯 권장 방법

### Windows 사용자
**방법 2 (DownGit)** 또는 **방법 5 (PowerShell)**

### Linux/Mac 사용자
**방법 4 (wget/curl)**

### Git 사용자
**방법 3 (Sparse Checkout)**

---

## 📍 다운로드 후 사용 방법

### 1. 프로젝트 루트로 이동
```
cd Lj-main
```

### 2. update 폴더 배치
다운로드한 `update` 폴더를 프로젝트 루트에 배치:
```
Lj-main/
  ├── src/
  ├── update/          ← 여기에 배치
  │   ├── UPDATE.bat
  │   └── fixed_screen_display.py
  └── ...
```

### 3. 업데이트 실행
```batch
cd update
UPDATE.bat
```

---

## 🔗 직접 링크

### GitHub 웹페이지
**update 폴더**: https://github.com/lee-jungkil/Lj/tree/main/update

### Raw 파일 직접 다운로드
- **UPDATE.bat**: https://raw.githubusercontent.com/lee-jungkil/Lj/main/update/UPDATE.bat
- **fixed_screen_display.py**: https://raw.githubusercontent.com/lee-jungkil/Lj/main/update/fixed_screen_display.py
- **UPDATE_README.md**: https://raw.githubusercontent.com/lee-jungkil/Lj/main/update/UPDATE_README.md

---

## ⚠️ 주의사항

1. **파일 인코딩**: `.bat` 파일은 반드시 원본 그대로 다운로드
2. **폴더 구조**: `update` 폴더를 프로젝트 루트에 배치
3. **백업**: 업데이트 전 기존 파일 백업 (UPDATE.bat이 자동으로 백업)

---

## 💡 팁

### 빠른 업데이트 (2개 파일만)
최소한으로 업데이트하려면:
1. `UPDATE.bat` 다운로드
2. `fixed_screen_display.py` 다운로드
3. `update` 폴더에 저장
4. `UPDATE.bat` 실행

### 완전한 업데이트 (권장)
전체 프로젝트 다운로드:
https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip

---

## 🆘 도움이 필요하신가요?

- **이슈 보고**: https://github.com/lee-jungkil/Lj/issues
- **전체 다운로드**: https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip

---

**업데이트 파일만 필요하시면 위 방법 중 하나를 선택하세요!** 🚀
