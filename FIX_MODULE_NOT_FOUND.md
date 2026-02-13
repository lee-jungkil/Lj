# 🚨 ModuleNotFoundError 해결 가이드

**에러 메시지**: `ModuleNotFoundError: No module named 'src'`  
**발생 버전**: v6.30.10  
**해결일**: 2026-02-13

---

## 🔍 문제 원인

Windows 환경에서 `RUN.bat` 실행 시 잘못된 디렉토리 경로로 인해 `src` 모듈을 찾지 못함.

**잘못된 코드**:
```batch
cd /d "%~dp0.."  # ← 상위 폴더로 이동 (잘못됨)
python -m src.main
```

**문제**:
- `RUN.bat`가 `C:\Users\admin\Downloads\Lj-main\RUN.bat`에 위치
- `cd /d "%~dp0.."`는 `C:\Users\admin\Downloads\`로 이동
- `src` 폴더는 `C:\Users\admin\Downloads\Lj-main\src`에 있음
- → `src` 모듈을 찾을 수 없음!

---

## ✅ 해결 방법

### 방법 1: RUN.bat 수정 (권장) ✅

**수정된 코드**:
```batch
cd /d "%~dp0"  # ← 현재 폴더 유지 (올바름)
python -m src.main
```

**적용 방법**:
```cmd
cd C:\Users\admin\Downloads\Lj-main
git pull origin main
```

---

### 방법 2: 수동으로 RUN.bat 편집

1. `C:\Users\admin\Downloads\Lj-main\RUN.bat` 파일을 메모장으로 열기
2. 9번째 줄 찾기:
   ```batch
   cd /d "%~dp0.."
   ```
3. 다음으로 변경:
   ```batch
   cd /d "%~dp0"
   ```
4. 저장 후 다시 실행

---

### 방법 3: 명령 프롬프트에서 직접 실행

```cmd
cd C:\Users\admin\Downloads\Lj-main
python -m src.main
```

**주의**: 반드시 `Lj-main` 폴더에서 실행해야 함!

---

## 🧪 수정 확인

### 1. 올바른 위치 확인
```cmd
cd C:\Users\admin\Downloads\Lj-main
dir
```

**출력 예상**:
```
src/          ← src 폴더가 보여야 함
RUN.bat
UPDATE.bat
.env
...
```

### 2. Python 경로 확인
```cmd
cd C:\Users\admin\Downloads\Lj-main
python -c "import sys; print(sys.path[0])"
```

**출력 예상**:
```
C:\Users\admin\Downloads\Lj-main  ← 현재 폴더
```

### 3. src 모듈 확인
```cmd
cd C:\Users\admin\Downloads\Lj-main
python -c "import src.config; print('OK')"
```

**출력 예상**:
```
OK
```

---

## 📋 체크리스트

수정 후 다음을 확인하세요:

- [ ] `cd C:\Users\admin\Downloads\Lj-main` 실행
- [ ] `dir` 명령으로 `src` 폴더 확인
- [ ] `RUN.bat` 9번째 줄이 `cd /d "%~dp0"`인지 확인
- [ ] `RUN.bat` 실행
- [ ] "Starting Paper Trading Mode" 메시지 확인

---

## 🚀 최신 버전 가져오기

### Git Pull (권장)
```cmd
cd C:\Users\admin\Downloads\Lj-main
git pull origin main
```

### 수동 다운로드
1. https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
2. 압축 해제
3. 기존 폴더 백업 후 교체

---

## ❓ 여전히 에러가 발생하는 경우

### 에러 1: "Python이 설치되어 있지 않습니다"
**해결**:
```cmd
python --version
```
- Python 3.8+ 설치 확인
- PATH 환경 변수에 Python 등록 확인

### 에러 2: "No module named 'pyupbit'"
**해결**:
```cmd
cd C:\Users\admin\Downloads\Lj-main
pip install -r requirements.txt
```

### 에러 3: ".env 파일이 없습니다"
**해결**:
1. `C:\Users\admin\Downloads\Lj-main\.env` 파일 생성
2. 다음 내용 입력:
```env
UPBIT_ACCESS_KEY=your_access_key
UPBIT_SECRET_KEY=your_secret_key
ENABLE_DYNAMIC_STOP_LOSS=true
ENABLE_SCALED_SELL=true
ENABLE_CONDITIONAL_SELL=true
```

---

## 📞 추가 지원

이 가이드로 해결되지 않는 경우:
1. `ERROR_VERIFICATION_v6.30.10.md` 문서 참고
2. `COMMON_ERRORS.md` 문서 참고
3. GitHub Issues: https://github.com/lee-jungkil/Lj/issues

---

**수정 버전**: v6.30.10 → v6.30.11 (수정 완료)  
**작성일**: 2026-02-13  
**상태**: ✅ 해결됨
