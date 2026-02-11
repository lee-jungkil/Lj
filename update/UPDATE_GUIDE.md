# 📦 업데이트 v6.15 - 스크롤 제거 및 리스크 관리 강화

## 🎯 업데이트 목적

사용자가 보고한 주요 문제들을 해결:
1. **화면 스크롤 문제** - 가장 큰 문제
2. **손익 동기화 문제** - 자본 변경 시 손익 미반영
3. **10% 손실 제어 실패** - 리스크 관리 미작동
4. **디버그 출력 스크롤** - 디버그 메시지로 인한 스크롤

---

## 📋 변경 사항

### 1. 화면 스크롤 완전 제거 ✅

**파일**: `src/utils/fixed_screen_display.py` → `update/fixed_screen_display.py`

**변경 내용**:
- 버전 업데이트: v6.14-FIXED → **v6.15-UPDATE**
- 완전 고정 화면 시스템 강화
- 커서 포지셔닝 최적화
- 화면 높이 제한 엄격 적용
- 디버그 출력 제거

**주요 개선**:
```python
# 기존 (v6.14)
print('\n'.join(output))  # 스크롤 발생 가능

# 개선 (v6.15)
sys.stdout.write('\033[H')  # 커서 홈으로
for i, line in enumerate(output_lines):
    sys.stdout.write('\033[2K')  # 줄 지우기
    sys.stdout.write(line)       # 덮어쓰기
    if i < len(output_lines) - 1:
        sys.stdout.write('\n')
sys.stdout.flush()
```

**결과**:
- ✅ 화면 절대 스크롤 안 됨
- ✅ 내용만 제자리 업데이트
- ✅ 디버그 출력 억제

---

### 2. 손익 동기화 개선 ✅

**파일**: `src/utils/fixed_screen_display.py`

**변경 내용**:
```python
def _render_header(self) -> str:
    """헤더 렌더링"""
    # ⭐ 손익 자동 계산 (동기화 보장)
    if self.initial_capital > 0:
        self.total_profit = self.current_balance - self.initial_capital
        self.profit_ratio = (self.total_profit / self.initial_capital) * 100
```

**메서드 개선**:
```python
def update_capital_status(self, initial_capital, current_balance, 
                         total_profit=None, profit_ratio=None):
    """자본금 업데이트 + 자동 손익 계산"""
    self.initial_capital = initial_capital
    self.current_balance = current_balance
    
    # ⭐ 자동 계산으로 동기화 보장
    if total_profit is None or profit_ratio is None:
        if initial_capital > 0:
            self.total_profit = current_balance - initial_capital
            self.profit_ratio = (self.total_profit / initial_capital) * 100
```

**결과**:
- ✅ 자본 변경 시 손익 자동 계산
- ✅ 실시간 동기화 보장
- ✅ initial_capital 기준 일관성

---

### 3. 10% 손실 자동 중단 강화 ✅

**파일**: `src/utils/risk_manager.py` → `update/risk_manager.py`

**변경 내용**:
```python
class RiskManager:
    def __init__(self, ...):
        # ⭐ 10% 손실 자동 중단
        self.loss_threshold_ratio = -10.0  # -10%
    
    def check_loss_threshold(self) -> bool:
        """⭐ 10% 손실 임계값 체크 (강화)"""
        total_pl_ratio = self.get_total_profit_loss_ratio()
        
        # ⭐ -10% 이하면 무조건 중단
        if total_pl_ratio <= self.loss_threshold_ratio:
            self.stop_trading(
                f"손실 임계값 초과: {total_pl_ratio:.2f}%"
            )
            return True
        
        return False
    
    def update_balance(self, new_balance: float):
        """잔고 업데이트 + 손실 체크"""
        self.current_balance = new_balance
        # ⭐ 매 업데이트마다 손실 임계값 체크
        self.check_loss_threshold()
    
    def update_position_price(self, ticker: str, current_price: float):
        """포지션 가격 업데이트 + 손실 체크"""
        if ticker in self.positions:
            self.positions[ticker].current_price = current_price
            # ⭐ 가격 업데이트 후에도 체크
            self.check_loss_threshold()
    
    def close_position(self, ticker: str, sell_price: float):
        """포지션 청산 + 손실 체크"""
        # ... 청산 로직 ...
        # ⭐ 청산 후 손실 임계값 체크
        self.check_loss_threshold()
```

**결과**:
- ✅ 잔고 업데이트 시 자동 체크
- ✅ 포지션 가격 변동 시 자동 체크
- ✅ 포지션 청산 시 자동 체크
- ✅ -10% 도달 시 즉시 거래 중단

---

### 4. 디버그 출력 억제 ✅

**변경 내용**:
- 모든 `print()` 및 `[DEBUG]` 출력 제거
- 화면 업데이트만 `render()` 메서드 사용
- 로그는 파일로만 기록

**결과**:
- ✅ 화면에 디버그 메시지 없음
- ✅ 스크롤 원인 제거
- ✅ 깔끔한 화면 유지

---

## 🚀 업데이트 방법

### Windows 사용자

#### 방법 1: 자동 업데이트 (권장)
```batch
1. update 폴더로 이동
2. UPDATE.bat 더블클릭
3. 완료!
```

#### 방법 2: 수동 업데이트
```batch
1. 백업 생성:
   mkdir backup
   copy src\utils\fixed_screen_display.py backup\
   copy src\utils\risk_manager.py backup\

2. 파일 교체:
   copy /Y update\fixed_screen_display.py src\utils\
   copy /Y update\risk_manager.py src\utils\

3. 완료!
```

### Linux/Unix 사용자

```bash
# 백업
mkdir -p backup
cp src/utils/fixed_screen_display.py backup/
cp src/utils/risk_manager.py backup/

# 업데이트
cp update/fixed_screen_display.py src/utils/
cp update/risk_manager.py src/utils/

echo "업데이트 완료!"
```

---

## 📊 업데이트 파일 목록

### 업데이트 폴더 구조
```
update/
├── UPDATE.bat                    # Windows 자동 업데이트 스크립트
├── fixed_screen_display.py       # 화면 표시 시스템 v6.15
├── risk_manager.py               # 리스크 관리 v6.15
├── UPDATE_GUIDE.md               # 이 파일
└── CHANGES.md                    # 변경 사항 상세
```

### 교체할 파일
```
src/utils/fixed_screen_display.py  ← update/fixed_screen_display.py
src/utils/risk_manager.py          ← update/risk_manager.py
```

---

## ✅ 업데이트 확인

업데이트 후 다음을 확인하세요:

### 1. 버전 확인
봇 실행 시 헤더에 표시:
```
Upbit AutoProfit Bot v6.15-UPDATE | 🕐 2026-02-12 07:18:24
```

### 2. 화면 스크롤 테스트
- ✅ 화면이 절대 스크롤되지 않음
- ✅ 내용만 제자리에서 업데이트
- ✅ 디버그 메시지 없음

### 3. 손익 동기화 테스트
- ✅ 자본 변경 시 손익 즉시 반영
- ✅ 실시간 손익률 정확

### 4. 리스크 관리 테스트
- ✅ -10% 도달 시 즉시 중단
- ✅ 화면에 중단 사유 표시
- ✅ 거래 재개 방지

---

## 🔍 문제 해결

### 업데이트 실패 시

**증상**: UPDATE.bat 실행 시 에러
```batch
[ERROR] update\fixed_screen_display.py 파일이 없습니다!
```

**해결**:
```batch
1. update 폴더 확인:
   dir update

2. 파일 존재 확인:
   dir update\fixed_screen_display.py
   dir update\risk_manager.py

3. 없으면 GitHub에서 재다운로드
```

---

### 백업 복원

업데이트 후 문제 발생 시:

```batch
REM Windows
copy /Y backup\fixed_screen_display.py.bak src\utils\fixed_screen_display.py
copy /Y backup\risk_manager.py.bak src\utils\risk_manager.py
```

```bash
# Linux/Unix
cp backup/fixed_screen_display.py src/utils/
cp backup/risk_manager.py src/utils/
```

---

### 봇 재시작

업데이트 후 반드시 봇 재시작:

```batch
REM 봇 종료 (Ctrl+C)

REM 봇 시작
run.bat
```

---

## 📝 변경 사항 요약

| 항목 | 이전 (v6.14) | 업데이트 (v6.15) | 상태 |
|------|-------------|-----------------|------|
| **화면 스크롤** | 발생함 | 완전 제거 | ✅ |
| **손익 동기화** | 수동 계산 | 자동 계산 | ✅ |
| **10% 손실 제어** | 미작동 | 자동 중단 | ✅ |
| **디버그 출력** | 스크롤 발생 | 억제 | ✅ |
| **버전** | v6.14-FIXED | v6.15-UPDATE | ✅ |

---

## 🎉 업데이트 완료!

모든 문제가 해결되었습니다:

- ✅ **화면 스크롤 완전 제거** - 가장 큰 문제 해결
- ✅ **손익 실시간 동기화** - 자본 변경 즉시 반영
- ✅ **10% 손실 자동 중단** - 리스크 관리 강화
- ✅ **디버그 출력 억제** - 깔끔한 화면

**업데이트 후 즉시 안정적으로 사용 가능합니다!** 🚀

---

## 📞 지원

문제 발생 시:
1. `backup` 폴더의 백업 파일 확인
2. GitHub Issues 등록
3. 이 가이드 재확인

**GitHub**: https://github.com/lee-jungkil/Lj
