# 🆕 AI 학습 데이터 보존 + 전체 새로 설치 가이드

## 🎯 이 방법을 사용하는 경우

- ✅ 완전히 새로 설치하고 싶을 때
- ✅ 파일이 많이 꼬여서 정리가 필요할 때
- ✅ 최신 GitHub 코드 전체를 받고 싶을 때
- ✅ **단, AI 학습 데이터는 보존해야 할 때**

---

## 📥 다운로드

```
https://raw.githubusercontent.com/lee-jungkil/Lj/main/fresh_install_with_ai_backup.py
```

**저장 위치**: `C:\Users\admin\Downloads\Lj-main\Lj-main\`

---

## 🚀 사용 방법

### **Step 1**: 스크립트 다운로드
```bash
cd C:\Users\admin\Downloads\Lj-main\Lj-main
curl -L -o fresh_install_with_ai_backup.py https://raw.githubusercontent.com/lee-jungkil/Lj/main/fresh_install_with_ai_backup.py
```

### **Step 2**: 실행
```bash
python fresh_install_with_ai_backup.py
```

### **Step 3**: 화면 안내 따라 진행
```
Enter를 눌러 계속... → Enter
Enter를 눌러 다운로드 시작... → Enter
```

---

## 📋 자동 처리 과정 (2~3분)

### **1. AI 데이터 백업** (5초)
```
백업 항목:
✅ ai_learning_data.json (AI 학습 데이터)
✅ trade_history.json (거래 기록)
✅ ai_learning.db (데이터베이스)
✅ .env (API 키 등)
✅ logs/ (로그 폴더)
✅ data/ (데이터 폴더)

→ AI_BACKUP_20260319_160530/ 폴더에 저장
```

### **2. GitHub에서 최신 코드 다운로드** (30초~1분)
```
다운로드: https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
크기: ~5MB
→ Lj-main.zip 다운로드 완료
```

### **3. 압축 해제** (10초)
```
Lj-main.zip 압축 해제
→ 새 폴더: C:\Users\admin\Downloads\Lj-main\
```

### **4. AI 데이터 복원** (5초)
```
백업 → 새 폴더로 복원:
✅ ai_learning_data.json
✅ trade_history.json
✅ ai_learning.db
✅ .env
✅ logs/
✅ data/
```

### **5. 캐시 삭제** (5초)
```
✅ 모든 __pycache__ 폴더 삭제
✅ 모든 .pyc 파일 삭제
```

### **6. 검증** (5초)
```
✅ VERSION: v6.31.8-R3-SMART-INVESTMENT
✅ 필수 파일 확인
✅ AI 데이터 확인
```

---

## 📂 폴더 구조

### **Before** (실행 전)
```
C:\Users\admin\Downloads\
└── Lj-main\
    └── Lj-main\  ← 현재 여기 (기존 봇)
        ├── src/
        ├── ai_learning_data.json
        └── ...
```

### **After** (실행 후)
```
C:\Users\admin\Downloads\
├── Lj-main\  ← 새 봇 (최신 코드 + AI 데이터)
│   ├── src/
│   ├── ai_learning_data.json  ← 복원됨
│   └── ...
│
└── Lj-main (old)\
    ├── Lj-main\  ← 기존 봇 (삭제 가능)
    └── AI_BACKUP_20260319_160530\  ← 백업 (보관 권장)
```

---

## ✅ 완료 후 작업

### **1. 새 폴더로 이동**
```bash
cd C:\Users\admin\Downloads\Lj-main
```

### **2. 테스트 실행**
```bash
python test_smart_investment.py
```

**예상 출력**:
```
✅ Test 1 PASS
✅ Test 2 PASS
✅ Test 3 PASS
✅ Test 4 PASS
✅ Test 5 PASS
🎉 모든 테스트 완료!
```

### **3. 봇 시작**
```bash
python -B -u -m src.main --mode paper
```

**확인 사항**:
```
✅ 버전: v6.31.8-R3-SMART-INVESTMENT
✅ SmartInvestmentManager 초기화 완료
✅ AI 학습 데이터 로드 (이전 데이터 계속 사용)
```

---

## 🔍 AI 데이터 보존 확인

### **거래 기록 확인**
```python
python -c "import json; data = json.load(open('ai_learning_data.json')); print(f'총 거래: {len(data.get(\"trades\", []))}건')"
```

**예상 출력**:
```
총 거래: 1376건  ← 이전 데이터 그대로 유지
```

### **.env 확인**
```bash
type .env
```

**예상 출력**:
```
UPBIT_ACCESS_KEY=your_key...
UPBIT_SECRET_KEY=your_secret...
INITIAL_CAPITAL=5000000
...
```

---

## 💡 장점

### ✅ **완전 새로 설치**
- 모든 파일 최신 버전으로 교체
- 꼬인 파일 정리
- 캐시 완전 삭제

### ✅ **AI 학습 데이터 보존**
- 1000건 이상의 거래 기록 유지
- AI 학습 진행 상황 유지
- API 키 등 설정 유지

### ✅ **자동 백업**
- 혹시 모를 문제에 대비
- 타임스탬프로 여러 백업 보관
- 언제든 복원 가능

---

## 🆘 문제 해결

### **Q: 다운로드가 너무 느려요**
**A**: 수동 다운로드
```
1. 브라우저에서 열기:
   https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip

2. 다운로드 완료 후:
   C:\Users\admin\Downloads\에 저장

3. 압축 해제:
   우클릭 → 압축 풀기 → Lj-main

4. AI 데이터 복사:
   기존 Lj-main\Lj-main\ai_learning_data.json
   → 새 Lj-main\ai_learning_data.json
```

### **Q: .env 파일이 없다고 나와요**
**A**: 수동 생성
```bash
copy .env.example .env
notepad .env
```

필수 설정:
```
UPBIT_ACCESS_KEY=your_key
UPBIT_SECRET_KEY=your_secret
INITIAL_CAPITAL=5000000
USE_REAL_BALANCE=true
```

### **Q: 기존 폴더는 삭제해도 되나요?**
**A**: 백업 확인 후 삭제
```
1. AI_BACKUP_* 폴더 확인
2. 새 봇에서 정상 작동 확인 (10~20건 거래)
3. 기존 폴더 삭제

⚠️ 백업 폴더는 보관 권장!
```

---

## 📊 비교: 업데이트 vs 새로 설치

| 항목 | 업데이트 | 새로 설치 |
|------|----------|----------|
| **속도** | 빠름 (30초) | 느림 (2~3분) |
| **안전성** | 중간 | 높음 |
| **AI 데이터** | 유지 | 유지 |
| **파일 정리** | 일부 | 완전 |
| **권장 시기** | 정상 작동 시 | 문제 발생 시 |

---

## 🎯 추천 순서

1. **정상 작동 중**: 일반 업데이트 사용
   - `UPDATE_v6318_R3_SMART_INVESTMENT.bat`
   - `update_r3_manual.py`

2. **문제 발생**: 전체 업데이트
   - `full_reinstall_with_ai_backup.py`

3. **완전히 망가짐**: **이 스크립트 사용** ⭐
   - `fresh_install_with_ai_backup.py`

---

## 📦 다운로드

```
https://raw.githubusercontent.com/lee-jungkil/Lj/main/fresh_install_with_ai_backup.py
```

---

**버전**: v6.31.8-R3-SMART-INVESTMENT  
**날짜**: 2026-03-19  
**AI 학습 데이터**: 100% 보존
