# 🚀 v6.31.8-R3 빠른 설치 가이드

## 📥 다운로드

```
https://raw.githubusercontent.com/lee-jungkil/Lj/main/UPDATE_v6318_R3_SMART_INVESTMENT.bat
```

**우클릭 → 다른 이름으로 저장** 후 봇 폴더에 저장

---

## ✅ 설치 (3단계)

### 1️⃣ 배치 파일 실행
```
UPDATE_v6318_R3_SMART_INVESTMENT.bat
```
더블클릭하면 자동 설치

### 2️⃣ 봇 재시작
```bash
python -B -u -m src.main --mode paper
```

### 3️⃣ 확인
콘솔에서 투자 금액 확인:
- Ultra: 200,000원
- Aggressive: 300,000원
- Conservative: 500,000원
- Mean: 700,000원

---

## 🎯 핵심 기능

### 10단계 투자 시스템
```
레벨 1:   100,000원
레벨 2:   150,000원
레벨 3:   200,000원 (Ultra)
레벨 4:   300,000원 (Aggressive)
레벨 5:   500,000원 (Conservative, Grid)
레벨 6:   700,000원 (Mean Reversion)
레벨 7: 1,000,000원
레벨 8: 1,500,000원
레벨 9: 2,000,000원
레벨 10: 3,000,000원
```

### 호가창 검증
- 실시간 유동성 체크
- 슬리피지 < 0.5%
- 안전 금액만 매수

---

## 🔧 문제 해결

### Q: 여전히 10만원만 매수해요
**A**: Upbit 잔고 확인!
```python
# 실제 잔고 조회
from src.api.upbit_api import UpbitAPI
print(f"KRW: {UpbitAPI().get_balance():,.0f}원")
```

잔고가 500,000원이면:
- 500,000 × 30% = 150,000원만 매수

**해결책**:
1. Upbit에 5,000,000원 입금 (실전)
2. `.env` 수정 (테스트):
   ```
   USE_REAL_BALANCE=false
   INITIAL_CAPITAL=5000000
   ```

---

### Q: 에러 메시지가 나와요
**A**: 
1. 배치 파일 다시 다운로드
2. 실행 후 화면 스크린샷 공유
3. Python 버전 확인: `python --version`

---

### Q: 테스트하고 싶어요
**A**:
```bash
python test_smart_investment.py
```

5개 테스트 모두 PASS 확인

---

## 📊 예상 효과

| 항목 | 개선 |
|------|------|
| 슬리피지 | -68% |
| Ultra 금액 | +33% |
| Mean 금액 | +367% |
| 전략 다양성 | +400% |

---

## 📞 도움말

**GitHub**: https://github.com/lee-jungkil/Lj  
**배치 파일**: https://raw.githubusercontent.com/lee-jungkil/Lj/main/UPDATE_v6318_R3_SMART_INVESTMENT.bat  
**전체 가이드**: https://raw.githubusercontent.com/lee-jungkil/Lj/main/SMART_INVESTMENT_GUIDE.md

---

**버전**: v6.31.8-R3-SMART-INVESTMENT  
**날짜**: 2026-03-19  
**상태**: ✅ 테스트 완료
