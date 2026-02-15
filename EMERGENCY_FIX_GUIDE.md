# 🚨 매도 안되는 문제 - 긴급 해결 가이드

## 문제 원인

**Python 캐시 파일(.pyc)이 오래된 코드를 사용**하고 있어서 매도가 실행되지 않습니다.

- GitHub에는 최신 수정 코드가 있음 ✅
- 하지만 봇은 오래된 `.pyc` 캐시 파일을 실행 중 ❌

## 📥 해결 방법 (3가지 옵션)

### ⭐ 방법 1: 긴급 캐시 삭제 (가장 빠름, 추천!)

1. 봇이 실행 중이라면 **Ctrl+C**로 먼저 종료
2. 다운로드:
   ```
   https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
   ```
3. ZIP 압축 해제
4. **EMERGENCY_CACHE_CLEAR.bat** 더블클릭

또는 기존 설치가 있다면:

```batch
cd C:\Users\YourName\Lj
git pull origin main
EMERGENCY_CACHE_CLEAR.bat
```

### 방법 2: 수동 캐시 삭제

```batch
# 1. 봇 종료
taskkill /F /IM python.exe

# 2. 캐시 삭제
cd C:\Users\YourName\Lj
del /s /q *.pyc
for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"

# 3. 최신 코드 받기
git pull origin main

# 4. 봇 재시작
RUN_PAPER_CLEAN.bat
```

### 방법 3: 완전 재설치

```batch
cd C:\Users\YourName\Lj
COMPLETE_REINSTALL.bat
```

## ✅ 성공 확인 방법

봇을 재시작한 후 **반드시 다음 로그가 보여야 합니다**:

```
[DEBUG-CHECK] 조건 1: 시간 초과 체크
[DEBUG-CHECK] - 보유 시간: 697초 (11분 37초)
[FORCE-SELL] 🚨 강제 매도 실행 시작!
[EXECUTE-SELL] execute_sell() 호출됨 - ticker: KRW-BORA
[EXECUTE-SELL] 포지션 존재 여부 체크: True
[EXECUTE-SELL] ✅ 포지션 찾음: KRW-BORA
[EXECUTE-SELL] 모의거래 모드: 매도 주문 시뮬레이션
[EXECUTE-SELL] risk_manager 청산 완료
[FORCE-SELL] ✅ 매도 주문 완료!
```

**중요**: `[EXECUTE-SELL]` 로그가 **반드시** 나타나야 합니다!

만약 `[EXECUTE-SELL]` 로그가 없다면 → 아직도 오래된 캐시 사용 중

## 🔍 체크리스트

캐시 삭제 후 확인:

- [ ] VERSION.txt에 `v6.30.61` 표시
- [ ] `__pycache__` 폴더가 없음
- [ ] 봇 시작 시 `[EXECUTE-SELL]` 로그 출력
- [ ] 4분 이상 보유 시 자동 매도

## 📊 현재 상황 (KRW-BORA 예시)

**Before (문제)**:
- 보유 시간: 697초 (11분 37초)
- 강제 매도 기준: 240초 (4분)
- 조건 충족: 697 > 240 ✅
- 로그: `[FORCE-SELL] ✅ 매도 주문 완료!`
- **실제 매도: ❌ 안됨 (포지션 그대로)**
- `[EXECUTE-SELL]` 로그: ❌ 없음

**After (해결)**:
- 캐시 삭제 후 재시작
- `[EXECUTE-SELL]` 로그 출력 ✅
- 실제 매도 실행 ✅
- 포지션 자동 청산 ✅

## 🎯 매도 조건 (정상 작동 시)

### 1. 시간 초과 청산
- **Aggressive 전략**: 4분 (240초) 이상
- **Conservative 전략**: 8분 (480초) 이상

### 2. 손익률 청산
- **익절**: +1.5% 이상
- **손절**: -1.0% 이하

### 3. 차트 신호
- RSI 과매수 (>70) + MACD 하락
- RSI 과매도 (<30) + MACD 하락 + 거래량 감소

## 💡 재발 방지

앞으로 코드 업데이트 후 **반드시**:

1. 봇 종료 (Ctrl+C)
2. **EMERGENCY_CACHE_CLEAR.bat** 실행
3. `[EXECUTE-SELL]` 로그 확인

또는 봇 시작 시 항상 **-B 플래그** 사용:
```batch
python -B -u -m src.main --mode paper
```
(-B = bytecode 생성 안함)

## 📥 다운로드 링크

- **ZIP (최신버전)**: https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
- **GitHub**: https://github.com/lee-jungkil/Lj
- **긴급 스크립트**: https://raw.githubusercontent.com/lee-jungkil/Lj/main/EMERGENCY_CACHE_CLEAR.bat

## ❓ 여전히 안 될 때

1. **EMERGENCY_CACHE_CLEAR.bat 다시 실행**
2. PC 재부팅
3. ZIP 새로 다운로드 → 압축 해제 → EMERGENCY_CACHE_CLEAR.bat
4. 스크린샷 공유:
   - 봇 시작 로그 (처음 10줄)
   - VERSION.txt 내용
   - `[EXECUTE-SELL]` 검색 결과

## 📞 Support

- **GitHub Issues**: https://github.com/lee-jungkil/Lj/issues
- **Release Notes**: RELEASE_NOTES_v6.30.61.md

---

**Version**: v6.30.61-EMERGENCY-CACHE-FIX  
**Release Date**: 2026-02-15  
**Priority**: 🚨 CRITICAL - 매도 기능 복구
