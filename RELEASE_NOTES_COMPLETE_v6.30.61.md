# Release Notes v6.30.61 - 완전 통합 재설치 스크립트

## 🎯 주요 업데이트

### ⭐ COMPLETE_REINSTALL.bat 완전 개선 (v6.30.61)

사용자의 기존 스타일을 유지하면서 긴급 캐시 수정을 통합한 **완전한 한 번에 해결** 스크립트입니다.

---

## 📋 새 기능

### 1️⃣ **9단계 완전 재설치 프로세스**

```batch
STEP 1/9: 설정 백업 (Backup Configuration)
STEP 2/9: 실행 중인 프로세스 중지 (Stop Running Processes)
STEP 3/9: ⭐ Python 캐시 완전 삭제 (Delete Python Cache) v6.30.61
STEP 4/9: Python 설치 확인 (Check Python Installation)
STEP 5/9: 최신 코드 다운로드 (Download Fresh Code)
STEP 6/9: 코드 무결성 확인 (Verify Code Integrity)
STEP 7/9: 의존성 설치 (Install Dependencies)
STEP 8/9: 설정 복원 (Restore Configuration)
STEP 9/9: 최종 검증 (Final Verification) ⭐ v6.30.61
```

### 2️⃣ **완전한 한글/영어 이중 언어 지원**

모든 메시지가 한글과 영어로 동시에 표시됩니다:
```
설정 백업 (Backup Configuration)
[확인 OK] .env backed up to .env.backup
[오류 ERROR] Python is not installed!
```

### 3️⃣ **v6.30.61 특화 검증**

#### ✅ **캐시 삭제 확인**
- `src\__pycache__` 삭제 검증
- `src\strategies\__pycache__` 삭제 검증
- `src\ai\__pycache__` 삭제 검증
- `src\utils\__pycache__` 삭제 검증

#### ✅ **코드 무결성 검증**
```batch
# AutoProfitBot 클래스 확인
findstr /C:"class AutoProfitBot" src\main.py

# v6.30.60+ [EXECUTE-SELL] 로그 확인
findstr /C:"[EXECUTE-SELL]" src\main.py

# v6.30.58+ DataFrame 수정 확인
findstr /C:"if ohlcv is not None and len" src\main.py
```

#### ✅ **VERSION.txt 자동 확인**
```
현재 버전 Current version:
v6.30.61-COMPLETE-REINSTALL-INTEGRATED
```

### 4️⃣ **상세한 오류 처리**

#### Python 미설치
```
[오류 ERROR] Python이 설치되지 않았습니다!
https://www.python.org/ 에서 Python 3.8+ 를 설치하세요.
설치 시 "Add Python to PATH" 를 체크하세요.
```

#### 네트워크 오류
```
[오류 ERROR] GitHub에서 코드 가져오기 실패!
인터넷 연결을 확인하고 다시 시도하세요.
```

#### 파일 손상
```
[오류 ERROR] AutoProfitBot 클래스를 찾을 수 없습니다!
다운로드된 파일이 손상되었을 수 있습니다.
```

### 5️⃣ **Git 유무에 따른 자동 처리**

#### Git 있을 때
```batch
git init
git remote add origin https://github.com/lee-jungkil/Lj.git
git fetch origin main
git reset --hard origin/main
```

#### Git 없을 때
```batch
# PowerShell로 자동 다운로드
powershell -Command "Invoke-WebRequest ..."
```

### 6️⃣ **스마트 .env 관리**

1. **백업 우선**: `.env.backup` 생성
2. **복원**: 백업이 있으면 자동 복원
3. **기본값**: 없으면 v6.30.61 기본 설정 생성
4. **보존**: 사용자 설정 유지

### 7️⃣ **최종 검증 및 안내**

```
예상되는 로그 Expected logs:
  [EXECUTE-SELL] execute_sell() 호출됨
  [EXECUTE-SELL] 포지션 존재 여부 체크
  [EXECUTE-SELL] ✅ 포지션 찾음

⭐ [EXECUTE-SELL] 로그를 확인하세요!
   Watch for [EXECUTE-SELL] logs!
```

---

## 🆚 이전 버전과 비교

### Before (v6.30.55)
- 8단계 프로세스
- 영어 위주 메시지
- 캐시 삭제만 수행
- 검증 부족

### After (v6.30.61)
- ✅ 9단계 프로세스
- ✅ 완전한 한/영 이중언어
- ✅ 캐시 삭제 + 검증
- ✅ 코드 무결성 확인
- ✅ v6.30.61 특화 검증
- ✅ [EXECUTE-SELL] 로그 확인
- ✅ DataFrame 수정 확인
- ✅ VERSION.txt 표시

---

## 📥 사용 방법

### Option 1: ZIP 다운로드 (추천)
```
1. 다운로드: https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
2. 압축 해제
3. COMPLETE_REINSTALL.bat 더블클릭
4. Y 입력 → 자동 완료
```

### Option 2: Git Clone
```batch
git clone https://github.com/lee-jungkil/Lj.git
cd Lj
COMPLETE_REINSTALL.bat
```

### Option 3: 기존 설치 업데이트
```batch
cd C:\Users\YourName\Lj
COMPLETE_REINSTALL.bat
```

---

## ✅ 성공 확인

### 재설치 완료 메시지
```
========================================
 재설치 완료! REINSTALL COMPLETE!
========================================

현재 버전 Current version: v6.30.61 (Emergency Cache Fix)

⭐ 중요한 변경사항:
  - Python 캐시 완전 삭제
  - [EXECUTE-SELL] 디버그 로그 추가
  - DataFrame 오류 수정
  - 매도 로직 정상화
```

### 봇 시작 후 확인
```
[2026-02-15 XX:XX:XX] 🤖 Bot started!
[DEBUG-LOOP] Main loop #1...
[EXECUTE-SELL] execute_sell() 호출됨  ← 반드시 보여야 함!
```

**만약 `[EXECUTE-SELL]` 로그가 없다면**:
- 스크립트를 다시 실행하세요
- 또는 ZIP을 새로 다운로드하세요

---

## 🎯 매도 문제 해결

### 이 스크립트가 해결하는 문제들

| 문제 | 원인 | 해결 |
|------|------|------|
| 매도 안됨 | Python 캐시(.pyc) | ✅ 완전 삭제 |
| [EXECUTE-SELL] 로그 없음 | 구버전 코드 실행 | ✅ 최신 코드 다운로드 |
| DataFrame 오류 | `if ohlcv and len` | ✅ `if ohlcv is not None` |
| 시간 초과 매도 안됨 | check_positions 중단 | ✅ 예외 처리 추가 |
| 포지션 그대로 유지 | execute_sell 미호출 | ✅ 로직 수정 |

---

## 📊 실행 시간

- **총 소요 시간**: 약 3-5분
- **캐시 삭제**: 10초
- **코드 다운로드**: 30초 (Git 사용 시)
- **패키지 설치**: 2-4분
- **검증**: 10초

---

## 🔧 기술 사양

### 지원 환경
- Windows 10/11
- Python 3.8+
- Git (선택사항)

### 자동 설치 패키지
- pyupbit
- pandas
- numpy
- requests
- python-dotenv
- colorlog
- ta

### 자동 설정
- UTF-8 코드페이지
- 무버퍼 출력 (-u)
- 캐시 비활성화 (-B)

---

## 💡 Pro Tips

### 1. 캐시 문제 예방
```batch
# 항상 -B 플래그 사용
python -B -u -m src.main --mode paper
```

### 2. 정기 업데이트
```batch
# 주 1회 실행 권장
COMPLETE_REINSTALL.bat
```

### 3. .env 백업
```batch
# 재설치 전 자동 백업됨
.env → .env.backup
```

### 4. 로그 확인
```batch
# [EXECUTE-SELL] 반드시 확인
findstr /C:"[EXECUTE-SELL]" trading_logs\*.log
```

---

## 📞 문제 해결

### Q: "Python is not installed" 오류
**A**: https://www.python.org/ 에서 설치, "Add to PATH" 체크

### Q: "[EXECUTE-SELL] 로그가 안 보여요"
**A**: 
1. COMPLETE_REINSTALL.bat 다시 실행
2. PC 재부팅
3. 새 ZIP 다운로드

### Q: "Git not found" 경고
**A**: 정상입니다. PowerShell로 자동 다운로드됩니다.

### Q: 패키지 설치 실패
**A**: 
```batch
python -m pip install --upgrade pip
python -m pip install pyupbit pandas numpy requests python-dotenv colorlog ta
```

---

## 🎉 요약

| 항목 | 상태 |
|------|------|
| **완전 자동화** | ✅ 한 번 클릭으로 완료 |
| **이중 언어** | ✅ 한글/영어 동시 지원 |
| **캐시 삭제** | ✅ 완전 제거 + 검증 |
| **코드 무결성** | ✅ 자동 검증 |
| **v6.30.61 특화** | ✅ [EXECUTE-SELL] 확인 |
| **오류 처리** | ✅ 상세한 안내 |
| **.env 보호** | ✅ 자동 백업/복원 |
| **사용자 친화적** | ✅ 단계별 상세 설명 |

---

**Version**: v6.30.61-COMPLETE-REINSTALL-INTEGRATED  
**Release Date**: 2026-02-15  
**Priority**: 🚨 CRITICAL - 매도 기능 완전 복구

**📥 다운로드**: https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip

**실행**: `COMPLETE_REINSTALL.bat` 더블클릭 → Y 입력 → 완료!
