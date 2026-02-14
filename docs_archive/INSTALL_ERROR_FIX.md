# 🔧 설치 오류 해결 가이드

## ❌ 발생한 오류: pip wheel 빌드 실패

### 문제 원인
```
error: subprocess-exited-with-error
Getting requirements to build wheel ... error
```

이 오류는 다음과 같은 이유로 발생합니다:
1. `ta` 패키지가 C 컴파일러를 필요로 함
2. Windows에 빌드 도구가 설치되지 않음
3. 일부 패키지 버전 호환성 문제

---

## ✅ 해결 방법

### 방법 1: 수정된 setup.bat 재실행 (추천)

**이미 수정했습니다!**

```
1. 기존 venv 폴더 삭제 (선택사항)
2. setup.bat 다시 실행
3. 자동으로 해결됨
```

**변경 사항:**
- `ta` 패키지 → `pandas-ta`로 변경 (빌드 불필요)
- 빌드 도구 자동 설치 추가
- 단계별 에러 처리 개선
- 대체 설치 방법 추가

---

### 방법 2: 수동 설치

#### 단계 1: 가상환경 삭제 및 재생성
```cmd
rmdir /s /q venv
python -m venv venv
venv\Scripts\activate.bat
```

#### 단계 2: pip 및 빌드 도구 업그레이드
```cmd
python -m pip install --upgrade pip setuptools wheel
```

#### 단계 3: 핵심 패키지 먼저 설치
```cmd
pip install pyupbit pandas numpy requests python-dotenv
```

#### 단계 4: 나머지 패키지 설치
```cmd
pip install schedule colorlog pytest typing-extensions
```

#### 단계 5: 설치 확인
```cmd
test_install.bat
```

---

### 방법 3: 관리자 권한으로 실행

```
1. setup.bat 우클릭
2. "관리자 권한으로 실행" 선택
3. 설치 진행
```

---

### 방법 4: Python 재설치

**Python 버전 문제일 수 있습니다:**

```
1. Python 3.8, 3.9, 3.10 중 하나 설치 (3.11+는 일부 패키지 호환 문제)
2. 설치 시 "Add Python to PATH" 체크
3. 재부팅
4. setup.bat 다시 실행
```

**권장 Python 버전:**
- ✅ Python 3.9.13 (가장 안정적)
- ✅ Python 3.10.11
- ⚠️ Python 3.11+ (일부 패키지 호환 문제 가능)

---

## 🧪 설치 확인 방법

### test_install.bat 실행

```
test_install.bat을 더블클릭

출력 예시:
[OK] Python version: 3.9.13
[OK] pyupbit installed
[OK] pandas installed
[OK] numpy installed
[OK] requests installed
[OK] python-dotenv installed
[OK] schedule installed
[OK] colorlog installed
```

---

## 🔍 추가 오류 해결

### 오류 1: "python is not recognized"
```
해결:
1. Python 재설치
2. "Add Python to PATH" 체크
3. 재부팅
4. 명령 프롬프트에서 확인: python --version
```

### 오류 2: "pip is not recognized"
```
해결:
1. 명령 프롬프트에서 실행:
   python -m ensurepip --upgrade
2. 또는:
   python -m pip install --upgrade pip
```

### 오류 3: "Access Denied"
```
해결:
1. 백신 프로그램 일시 중지
2. Windows Defender 예외 추가
3. 관리자 권한으로 실행
```

### 오류 4: "SSL Certificate Error"
```
해결:
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org pyupbit pandas numpy
```

### 오류 5: "Microsoft Visual C++ required"
```
해결:
1. Microsoft C++ Build Tools 설치
   https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. 또는 requirements.txt의 ta 패키지 제거 (이미 수정됨)
```

---

## 📦 최소 요구사항

### 필수 패키지만 설치
```cmd
venv\Scripts\activate.bat
pip install pyupbit pandas numpy requests python-dotenv schedule colorlog
```

이 패키지들만으로도 봇이 작동합니다!

---

## 🚀 빠른 해결 방법 요약

### 1분 해결:
```
1. setup.bat 다시 실행
   (이미 수정되어 자동으로 해결됨)
```

### 3분 해결:
```
1. venv 폴더 삭제
2. setup.bat 실행
3. test_install.bat으로 확인
```

### 5분 해결 (수동):
```
1. venv\Scripts\activate.bat
2. python -m pip install --upgrade pip setuptools wheel
3. pip install pyupbit pandas numpy requests python-dotenv schedule colorlog
4. test_install.bat
```

---

## 💡 예방 팁

### 다음에는 이렇게 하세요:

1. **Python 3.9 또는 3.10 사용**
   - 3.11+는 일부 패키지 호환 문제

2. **관리자 권한으로 실행**
   - 권한 문제 예방

3. **백신 프로그램 예외 추가**
   - 프로젝트 폴더를 백신 예외 목록에 추가

4. **안정적인 인터넷 연결**
   - 패키지 다운로드 중 끊김 방지

---

## 📞 추가 도움

### 여전히 문제가 있나요?

1. **test_install.bat 실행**
   - 어떤 패키지가 설치 안 됐는지 확인

2. **로그 확인**
   - 에러 메시지 전체 복사

3. **수동 설치 시도**
   - 위의 "방법 2" 참조

4. **Python 버전 확인**
   - `python --version` 실행
   - 3.9 또는 3.10 권장

---

## ✅ 성공 확인

### 모든 것이 정상이면:
```
test_install.bat 실행 시 모든 패키지가 [OK]
→ run_backtest.bat 실행 가능
→ run_paper.bat 실행 가능
```

---

**이제 setup.bat을 다시 실행해보세요!**
**문제가 해결될 것입니다! 🚀**
