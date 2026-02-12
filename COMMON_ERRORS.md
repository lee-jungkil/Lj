# ⚠️ 자주 발생하는 에러와 해결 방법

## 에러 1: "fatal: not a git repository"

### 상황
```
C:\Users\admin\Downloads\Lj-main\update>git pull origin main
fatal: not a git repository (or any of the parent directories): .git
```

### 원인
`update` 폴더는 Git 저장소가 아닙니다! 프로젝트 루트에서 git pull을 실행해야 합니다.

### 해결 방법

#### 방법 1: FIX_GIT_PULL.bat 사용 (가장 간편!)
```cmd
# update 폴더에 있다면
FIX_GIT_PULL.bat
```
이 스크립트가 자동으로:
- 상위 폴더로 이동
- git pull 실행
- 다음 단계 안내

#### 방법 2: 수동으로 이동
```cmd
# 현재 update 폴더에 있다면
cd ..

# Git Pull
git pull origin main

# 업데이트 또는 실행
QUICK_UPDATE.bat
# 또는
RUN.bat
```

---

## 에러 2: "내부 또는 외부 명령이 아닙니다"

### 상황
```
'o'은(는) 내부 또는 외부 명령, 실행할 수 있는 프로그램, 또는
배치 파일이 아닙니다.
```

### 원인
- UPDATE.bat의 오래된 버전 (Python 경로 하드코딩)
- update 폴더에서 UPDATE.bat 실행 시도

### 해결 방법
```cmd
# update 폴더에서 벗어나기
cd ..

# 빠른 업데이트 사용
QUICK_UPDATE.bat
```

---

## 에러 3: "can't open file"

### 상황
```
python.exe: can't open file 'C:\Users\admin\Downloads\Lj-main\update\...'
```

### 원인
잘못된 디렉토리에서 실행

### 해결 방법
```cmd
# 프로젝트 루트로 이동
cd C:\Users\admin\Downloads\Lj-main

# 실행
RUN.bat
# 또는
python -m src.main
```

---

## 올바른 폴더 구조

```
C:\Users\admin\Downloads\Lj-main\     ← Git 저장소 (여기서 git pull!)
├── .git\                             ← Git 폴더
├── src\                              ← 소스 코드
│   ├── main.py
│   ├── config.py
│   └── utils\
│       └── risk_manager.py
├── update\                           ← 업데이트 파일들 (Git 저장소 아님!)
│   ├── main.py                       ← 최신 버전
│   ├── config.py
│   ├── risk_manager.py
│   ├── UPDATE.bat                    ← 적용만
│   ├── download_update.bat           ← 다운로드만
│   └── FIX_GIT_PULL.bat              ← Git Pull 수정
├── QUICK_UPDATE.bat                  ← 다운로드 + 적용 (권장!)
├── RUN.bat                           ← 봇 실행
├── UPDATE.bat                        ← 업데이트만
└── README.md
```

---

## 🎯 올바른 업데이트 절차

### 초보자용 (가장 간단!)

```cmd
# 어디에 있든 상관없이 프로젝트 루트로 이동
cd C:\Users\admin\Downloads\Lj-main

# Git Pull
git pull origin main

# 빠른 업데이트
QUICK_UPDATE.bat

# 실행
RUN.bat
```

### 중급자용 (단계별)

```cmd
# 1. 프로젝트 루트로
cd C:\Users\admin\Downloads\Lj-main

# 2. Git Pull
git pull origin main

# 3. update 폴더로
cd update

# 4. 다운로드 (선택사항)
download_update.bat

# 5. 적용
UPDATE.bat

# 6. 상위로
cd ..

# 7. 실행
RUN.bat
```

---

## 🔍 현재 위치 확인 방법

```cmd
# 현재 폴더 확인
cd

# 예상 출력: C:\Users\admin\Downloads\Lj-main
# (update가 포함되어 있으면 안 됨!)
```

---

## 💡 팁

### Tip 1: 항상 프로젝트 루트에서 시작
```cmd
cd C:\Users\admin\Downloads\Lj-main
```

### Tip 2: update 폴더에 있다면
```cmd
cd ..
```

### Tip 3: Git Pull은 프로젝트 루트에서만
```cmd
# ❌ 안 됨
C:\Users\admin\Downloads\Lj-main\update>git pull origin main

# ✅ 올바름
C:\Users\admin\Downloads\Lj-main>git pull origin main
```

### Tip 4: 간편 실행은 QUICK_UPDATE.bat
```cmd
cd C:\Users\admin\Downloads\Lj-main
QUICK_UPDATE.bat
```

---

## 📞 여전히 문제가 있다면

1. **FIX_GIT_PULL.bat 실행**
   ```cmd
   cd C:\Users\admin\Downloads\Lj-main\update
   FIX_GIT_PULL.bat
   ```

2. **수동 다운로드**
   - https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
   - 압축 해제
   - 기존 파일 교체

3. **GitHub Issues**
   - https://github.com/lee-jungkil/Lj/issues
   - 에러 메시지와 스크린샷 첨부

---

**Last Updated**: 2026-02-12  
**Version**: v6.30.6
