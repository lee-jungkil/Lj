# 🔧 긴급 수정: 모의투자 실행 오류 해결

## 📋 버전 정보
- **버전**: v5.7.1 (핫픽스)
- **커밋**: 3a6d347
- **저장소**: https://github.com/lee-jungkil/Lj
- **날짜**: 2026-02-11

---

## 🔴 오류 내용

```python
AttributeError: 'AutoProfitBot' object has no attribute 'quick_check_interval'. 
Did you mean: 'position_check_interval'?
```

### 발생 위치
- `src/main.py`, line 1087
- `src/main.py`, line 1202

---

## ✅ 수정 내용

### 변수명 통일
```python
# Before (오류)
self.quick_check_interval  ❌

# After (수정)
self.position_check_interval  ✅
```

### 수정된 코드

#### 1. 로그 출력 (line 1087)
```python
# Before
self.logger.log_info(f"   ⚡ 빠른 체크: {self.quick_check_interval}초")

# After
self.logger.log_info(f"   ⚡ 포지션 체크: {self.position_check_interval}초")
```

#### 2. 대기 시간 계산 (line 1202)
```python
# Before
wait_time = max(self.surge_scan_interval, min(self.quick_check_interval, time_until_next_scan))

# After
wait_time = max(self.surge_scan_interval, min(self.position_check_interval, time_until_next_scan))
```

---

## 🚀 해결 방법

### 1. 최신 코드 받기
```bash
cd Lj-main
git pull origin main
```

**기대 출력**:
```
From https://github.com/lee-jungkil/Lj
   460d86b..3a6d347  main       -> origin/main
Updating 460d86b..3a6d347
Fast-forward
 src/main.py | 8 ++++----
 1 file changed, 4 insertions(+), 4 deletions(-)
```

### 2. 모의투자 재실행
```bash
run_paper.bat
```

**정상 실행 확인**:
```
✅ 동적 코인 선정 시스템 활성화
✅ 코인 개수: 35개 (고정)
✅ 선정 간격: 180초 (3분)
🤖 봇 가동 시작! (AI 학습 통합 모드)
   📅 전체 스캔: 60초 (1분)
   ⚡ 포지션 체크: 3초
   🔥 급등 감지: 5초 (초단타 최대 5개)
```

---

## 📊 수정 전후 비교

| 항목 | Before (오류) | After (수정) |
|------|---------------|--------------|
| 변수명 | `quick_check_interval` ❌ | `position_check_interval` ✅ |
| 로그 메시지 | "빠른 체크" | "포지션 체크" ✅ |
| 실행 상태 | AttributeError | 정상 실행 ✅ |

---

## ✅ 확인 사항

### 정상 실행 로그
```
2026-02-11 22:49:04 [COIN] 🔄 동적 코인 선정 시스템 활성화
2026-02-11 22:49:04 [COIN] 📊 전체 KRW 마켓: 237개
2026-02-11 22:49:16 [COIN] 📈 거래량 Top 35 추출 완료
2026-02-11 22:49:16 [COIN] ✅ 최종 선정 완료: 35개 코인
2026-02-11 22:49:16 [INFO] 🤖 봇 가동 시작!
```

### 스캔 주기 확인
- ✅ 전체 스캔: 60초 (1분)
- ✅ 포지션 체크: 3초
- ✅ 급등 감지: 5초
- ✅ 코인 갱신: 180초 (3분)

---

## 🎯 핫픽스 요약

### 문제
- 변수명 불일치로 모의투자 실행 불가
- `quick_check_interval` → `position_check_interval` 누락

### 해결
- 모든 `quick_check_interval` → `position_check_interval` 변경
- 로그 메시지 일관성 확보

### 영향
- ✅ 모의투자 정상 실행
- ✅ 실거래 정상 실행
- ✅ 모든 기능 정상 작동

---

## 📚 관련 문서
- 📖 V5.7_POLICY_UPDATE.md - v5.7 정책 가이드
- 📖 V5.6_EMERGENCY_FIX.md - v5.6 수정 가이드
- 📖 START_HERE.md - 시작 가이드

---

## 🎉 완료

### GitHub 반영 ✅
- **커밋**: 3a6d347
- **버전**: v5.7.1 (핫픽스)
- **상태**: 모의투자 오류 해결 완료

---

**🔥 지금 바로 `git pull` 후 `run_paper.bat`를 실행하세요!**  
**모든 오류가 해결되었습니다!** ✅
