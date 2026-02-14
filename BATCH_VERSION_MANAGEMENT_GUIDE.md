# 🔄 배치 파일 버전 관리 가이드

**작성일**: 2026-02-14  
**현재 버전**: v6.30.28

---

## ⚠️ 중요: 새 버전마다 배치 파일 업데이트 필요!

새로운 버전을 릴리스할 때마다 **배치 파일의 버전 번호를 업데이트**해야 합니다.

---

## 📋 업데이트가 필요한 배치 파일 목록

### 1. **핵심 실행 파일** (필수)
- ✅ `RUN_PAPER_CLEAN.bat` - 모의투자 실행
- ✅ `RUN_LIVE_CLEAN.bat` - 실거래 실행
- ✅ `setup.bat` - 초기 설정

### 2. **업데이트 관련 파일**
- ✅ `DOWNLOAD_ALL_FILES.bat` - 전체 파일 다운로드
- ✅ `QUICK_UPDATE.bat` - 빠른 업데이트
- ✅ `RUN.bat` - 일반 실행
- ✅ `UPDATE.bat` - 업데이트

### 3. **기타 파일** (선택)
- `run_paper.bat` (v5.2 - 구버전, 사용 안 함)
- `run_live.bat` (v5.2 - 구버전, 사용 안 함)
- `run_backtest.bat` (v5.2 - 구버전, 사용 안 함)

---

## 🤖 자동 업데이트 방법 (권장)

### **방법 1: Python 스크립트 사용**

```batch
cd C:\Users\admin\Downloads\Lj-main\Lj-main
python update_batch_versions.py
```

**실행 결과**:
```
📌 현재 버전: v6.30.28
================================================================================
✅ DOWNLOAD_ALL_FILES.bat:
    v6.30.12 → v6.30.28
✅ QUICK_UPDATE.bat:
    v6.30.6 → v6.30.28
✅ RUN.bat:
    v6.30.6 → v6.30.28
✅ UPDATE.bat:
    v6.30.6 → v6.30.28
✓  RUN_PAPER_CLEAN.bat: 이미 최신 버전
✓  RUN_LIVE_CLEAN.bat: 이미 최신 버전
✓  setup.bat: 이미 최신 버전

================================================================================
📊 업데이트 결과 요약
================================================================================
✅ 업데이트 완료: 4개
```

**장점**:
- ✅ 한 번에 모든 배치 파일 업데이트
- ✅ VERSION.txt에서 자동으로 현재 버전 읽기
- ✅ 실수 방지
- ✅ 빠르고 정확

---

## 🖊️ 수동 업데이트 방법

새 버전 릴리스 시 다음 위치들을 **수동으로** 수정:

### 1. RUN_PAPER_CLEAN.bat
```batch
Line 2:  title Upbit AutoProfit Bot v6.30.28 - Paper Trading (Clean Start)
Line 7:  echo  Upbit AutoProfit Bot v6.30.28
Line 89: echo Version: v6.30.28
```

### 2. RUN_LIVE_CLEAN.bat
```batch
Line 2:  title Upbit AutoProfit Bot v6.30.28 - Live Trading (Clean Start)
Line 26: echo  Upbit AutoProfit Bot v6.30.28
Line 111: echo Version: v6.30.28
```

### 3. setup.bat
```batch
Line 2:  title Upbit AutoProfit Bot v6.30.28 - Setup
Line 7:  echo  Upbit AutoProfit Bot v6.30.28
Line 121: echo # Upbit AutoProfit Bot v6.30.28
```

### 4. DOWNLOAD_ALL_FILES.bat
```batch
Line 6:  echo ║          Upbit AutoProfit Bot v6.30.28 전체 다운로드
Line 128: echo ║                    ✅ v6.30.28 다운로드 완료!
```

### 5. QUICK_UPDATE.bat
```batch
Line 6:  echo ║          Upbit AutoProfit Bot v6.30.28 빠른 업데이트
Line 99: echo ║                    ✅ v6.30.28 업데이트 완료!
```

### 6. RUN.bat
```batch
Line 4:  echo   Upbit AutoProfit Bot v6.30.28 실행
Line 59: echo   4. ERROR_VERIFICATION_v6.30.28.md 문서 참고
```

### 7. UPDATE.bat
```batch
Line 4:  echo   Upbit AutoProfit Bot v6.30.28 업데이트
Line 38: echo   ✅ v6.30.28 업데이트 완료!
Line 53: echo 📖 자세한 내용은 ERROR_VERIFICATION_v6.30.28.md 참고
```

---

## 🔍 버전 확인 방법

### **방법 1: 배치 파일 직접 확인**
```batch
findstr /C:"v6.30" RUN_PAPER_CLEAN.bat
```

**예상 출력**:
```
title Upbit AutoProfit Bot v6.30.28 - Paper Trading (Clean Start)
echo  Upbit AutoProfit Bot v6.30.28
echo Version: v6.30.28
```

### **방법 2: 모든 배치 파일 검색**
```batch
findstr /C:"v6.30" *.bat
```

### **방법 3: 실행 시 화면 확인**
`RUN_PAPER_CLEAN.bat` 실행 시 화면 상단에 버전 표시:
```
========================================
 Upbit AutoProfit Bot v6.30.28
 Paper Trading Mode
========================================
```

---

## 📊 v6.30.28 업데이트 현황

| 파일 | 이전 버전 | 현재 버전 | 상태 |
|------|----------|----------|------|
| RUN_PAPER_CLEAN.bat | v6.30.25 | **v6.30.28** | ✅ 완료 |
| RUN_LIVE_CLEAN.bat | v6.30.25 | **v6.30.28** | ✅ 완료 |
| setup.bat | v6.30.25 | **v6.30.28** | ✅ 완료 |
| DOWNLOAD_ALL_FILES.bat | v6.30.12 | **v6.30.28** | ✅ 완료 |
| QUICK_UPDATE.bat | v6.30.6 | **v6.30.28** | ✅ 완료 |
| RUN.bat | v6.30.6 | **v6.30.28** | ✅ 완료 |
| UPDATE.bat | v6.30.6 | **v6.30.28** | ✅ 완료 |

**업데이트 완료**: 7개 파일 ✅

---

## 🚀 새 버전 릴리스 체크리스트

새 버전을 릴리스할 때 다음 순서로 작업:

### **1단계: 코드 수정**
- [ ] 버그 수정 또는 기능 추가
- [ ] 테스트 실행 및 검증

### **2단계: VERSION.txt 업데이트**
- [ ] 버전 번호 업데이트 (예: v6.30.29)
- [ ] 변경 사항 문서화

### **3단계: 배치 파일 버전 업데이트** ⭐ **중요!**
- [ ] `python update_batch_versions.py` 실행
- [ ] 또는 수동으로 모든 .bat 파일 수정

### **4단계: Git 커밋**
```batch
git add -A
git commit -m "v6.30.29: 릴리스 (배치 파일 버전 포함)"
git push origin main
```

### **5단계: 검증**
- [ ] `RUN_PAPER_CLEAN.bat` 실행 시 새 버전 확인
- [ ] 로그에 새 버전 번호 표시 확인

---

## ❓ FAQ

### **Q1: 배치 파일 버전을 업데이트하지 않으면?**

**A1**: 
- ❌ 사용자가 혼란스러워함 (화면에 구버전 표시)
- ❌ 문제 발생 시 버전 추적 어려움
- ❌ 전문성 저하

### **Q2: 자동 업데이트 스크립트를 커밋해야 하나?**

**A2**: 
- ✅ **예!** `update_batch_versions.py`는 Git에 포함
- 이유: 다음 버전 릴리스 시에도 사용

### **Q3: 구버전 배치 파일은 어떻게 하나?**

**A3**:
- `run_paper.bat` (v5.2) → 삭제하거나 `old_batch_files/` 폴더로 이동
- `RUN_PAPER_CLEAN.bat` (v6.30.28) → 현재 사용 버전

### **Q4: 배치 파일 버전과 Python 코드 버전이 다르면?**

**A4**:
- ⚠️ 혼란 발생! 반드시 일치시켜야 함
- 예: VERSION.txt가 v6.30.28이면 모든 .bat도 v6.30.28

---

## 🎯 베스트 프랙티스

1. **항상 자동 업데이트 스크립트 사용**
   ```batch
   python update_batch_versions.py
   ```

2. **VERSION.txt를 단일 소스로 사용**
   - 스크립트가 자동으로 읽어서 업데이트

3. **릴리스 전 반드시 확인**
   ```batch
   findstr /C:"v6.30" *.bat
   ```

4. **배치 파일 버전 업데이트를 커밋 메시지에 포함**
   ```
   v6.30.29: 새 기능 추가 (배치 파일 버전 v6.30.28→v6.30.29)
   ```

5. **릴리스 노트에 명시**
   ```markdown
   ## 변경 파일
   - src/main.py
   - VERSION.txt
   - 모든 .bat 파일 (버전 v6.30.29로 업데이트)
   ```

---

## 📝 수동 업데이트 템플릿

새 버전 `v6.30.XX`로 업데이트할 때 사용:

### **Find & Replace (모든 .bat 파일)**
```
Find:    v6\.30\.\d+
Replace: v6.30.XX
```

**주의**: 정규표현식 지원 에디터 사용 (VS Code, Notepad++ 등)

---

## 🔗 관련 파일

- `update_batch_versions.py` - 자동 업데이트 스크립트
- `VERSION.txt` - 현재 버전 정보
- `*.bat` - 모든 배치 파일

---

## 📞 문제 해결

**문제**: 배치 파일 버전이 VERSION.txt와 다름

**해결**:
1. `python update_batch_versions.py` 실행
2. 또는 수동으로 각 파일 수정
3. Git 커밋 및 푸시

**문제**: update_batch_versions.py 실행 오류

**해결**:
1. Python 3.x 설치 확인
2. 경로 확인 (`/home/user/webapp/` 또는 `C:\Users\admin\Downloads\Lj-main\Lj-main\`)
3. 파일 인코딩 확인 (UTF-8)

---

## ✅ 체크리스트 요약

- [x] VERSION.txt 업데이트
- [x] `python update_batch_versions.py` 실행
- [x] 모든 .bat 파일 버전 확인
- [x] Git 커밋 및 푸시
- [x] 실행 테스트 (버전 표시 확인)

---

**현재 상태**: v6.30.28로 모든 배치 파일 업데이트 완료 ✅  
**다음 버전**: v6.30.29 릴리스 시 이 가이드 참고

**작성자**: AI Assistant  
**최종 수정**: 2026-02-14
