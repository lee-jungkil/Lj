# 🚀 업데이트 v6.15 - 빠른 참조

## ⚡ 3단계 업데이트

### Windows
```
1. update 폴더로 이동
2. UPDATE.bat 더블클릭
3. 봇 재시작 (run.bat)
```

### Linux/Unix
```bash
cp update/fixed_screen_display.py src/utils/
cp update/risk_manager.py src/utils/
```

---

## 🎯 해결된 문제 (4개)

| 문제 | 상태 |
|------|------|
| 화면 스크롤 | ✅ 완전 제거 |
| 손익 동기화 | ✅ 자동 계산 |
| 10% 손실 제어 | ✅ 자동 중단 |
| 디버그 스크롤 | ✅ 출력 억제 |

---

## 📦 업데이트 파일 (2개)

```
update/fixed_screen_display.py  → src/utils/
update/risk_manager.py          → src/utils/
```

---

## 🔍 확인 사항

### 버전 확인
```
헤더에 표시: "v6.15-UPDATE"
```

### 화면 스크롤
- ✅ 절대 스크롤 안 됨
- ✅ 제자리 업데이트만

### 손익 동기화
- ✅ 자본 변경 즉시 반영
- ✅ 정확한 손익률

### 10% 손실 제어
- ✅ -10% 도달 시 즉시 중단
- ✅ 중단 사유 화면 표시

---

## ⚠️ 주의사항

1. **봇 종료**: 업데이트 전 봇 종료 (Ctrl+C)
2. **백업 자동**: UPDATE.bat이 자동 백업
3. **재시작 필수**: 업데이트 후 봇 재시작

---

## 🔄 복원 방법

### Windows
```batch
copy /Y backup\*.bak src\utils\
```

### Linux/Unix
```bash
cp backup/*.py src/utils/
```

---

## 📊 주요 변경 코드

### 1. 화면 고정
```python
# 커서 홈으로 이동 후 덮어쓰기
sys.stdout.write('\033[H')
for line in output_lines:
    sys.stdout.write('\033[2K')  # 줄 지우기
    sys.stdout.write(line)       # 덮어쓰기
```

### 2. 손익 자동 계산
```python
if self.initial_capital > 0:
    self.total_profit = self.current_balance - self.initial_capital
    self.profit_ratio = (self.total_profit / self.initial_capital) * 100
```

### 3. 10% 손실 자동 중단
```python
def check_loss_threshold(self) -> bool:
    total_pl_ratio = self.get_total_profit_loss_ratio()
    if total_pl_ratio <= -10.0:
        self.stop_trading("손실 임계값 초과")
        return True
    return False
```

---

## 📁 파일 구조

```
update/
├── UPDATE.bat             # 자동 업데이트
├── fixed_screen_display.py
├── risk_manager.py
├── UPDATE_GUIDE.md        # 상세 가이드
└── QUICK_UPDATE.md        # 이 파일
```

---

## ✅ 체크리스트

- [ ] 봇 종료
- [ ] update 폴더 확인
- [ ] UPDATE.bat 실행
- [ ] 백업 확인
- [ ] 버전 확인 (v6.15)
- [ ] 화면 스크롤 테스트
- [ ] 손익 동기화 테스트
- [ ] 10% 손실 테스트
- [ ] 봇 정상 작동 확인

---

## 🎉 완료!

**업데이트 후 즉시 사용 가능합니다!**

모든 문제가 해결되었습니다:
- ✅ 화면 고정
- ✅ 손익 동기화
- ✅ 리스크 관리 강화
- ✅ 깔끔한 화면

**안정적으로 봇을 실행하세요!** 🚀

---

**상세 내용**: UPDATE_GUIDE.md 참조
**GitHub**: https://github.com/lee-jungkil/Lj
