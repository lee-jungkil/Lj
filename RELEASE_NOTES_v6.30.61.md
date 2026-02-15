# Release Notes v6.30.61 - 긴급 캐시 문제 해결

## 🚨 Critical Issue Fixed

**문제**: 매도가 실행되지 않는 문제가 Python 캐시(.pyc 파일) 때문에 발생했습니다.

- ✅ 코드에는 매도 로직이 정상적으로 있음
- ✅ GitHub에는 최신 코드가 올라가 있음
- ❌ **봇이 오래된 캐시(.pyc) 파일을 사용하여 구 코드 실행**

## 🔧 Solution

### 1. 긴급 캐시 삭제 스크립트 추가
- **EMERGENCY_CACHE_CLEAR.bat** 생성
- Python 프로세스 강제 종료
- 모든 `__pycache__` 폴더 삭제
- 모든 `.pyc` 파일 삭제
- 버전 확인 및 디버그 로그 존재 여부 체크
- 봇 자동 재시작

### 2. 사용 방법

**방법 1: 긴급 캐시 삭제 (추천)**
```batch
# 봇이 실행 중이라면 Ctrl+C로 먼저 종료
EMERGENCY_CACHE_CLEAR.bat
```

**방법 2: 수동 캐시 삭제**
```batch
taskkill /F /IM python.exe
del /s /q *.pyc
for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"
RUN_PAPER_CLEAN.bat
```

**방법 3: 전체 재설치**
```batch
COMPLETE_REINSTALL.bat
```

## 📋 Symptoms

다음 증상이 나타나면 반드시 캐시를 삭제해야 합니다:

- [FORCE-SELL] ✅ 매도 주문 완료! 로그는 나오지만 실제로 매도되지 않음
- [EXECUTE-SELL] 로그가 전혀 보이지 않음
- 시간 초과(4분, 8분) 조건을 충족했는데도 매도 안됨
- 손익률 조건(+1.5%, -1.0%)을 충족했는데도 매도 안됨

## ✅ Expected Behavior After Fix

캐시 삭제 후 봇을 재시작하면 다음 로그가 **반드시** 나타나야 합니다:

```
[DEBUG-CHECK] 조건 1: 시간 초과 체크
[DEBUG-CHECK] - 보유 시간: 697초 (11분 37초)
[DEBUG-CHECK] - 강제 매도 기준: 240초 (4분)
[DEBUG-CHECK] ⚠️ 시간 초과 청산 조건 충족!
[FORCE-SELL] 🚨 강제 매도 실행 시작!
[EXECUTE-SELL] execute_sell() 호출됨 - ticker: KRW-BORA, reason: 시간초과청산
[EXECUTE-SELL] 포지션 존재 여부 체크: True
[EXECUTE-SELL] ✅ 포지션 찾음: KRW-BORA, amount=60.6, avg_price=16000
[EXECUTE-SELL] 모의거래 모드: 매도 주문 시뮬레이션
[EXECUTE-SELL] risk_manager 청산 완료, P/L: +84
[EXECUTE-SELL] 화면에서 포지션 제거 완료
[FORCE-SELL] ✅ 매도 주문 완료!
```

## 🔍 Verification Checklist

캐시 삭제 후 확인사항:

1. ✅ VERSION.txt에 v6.30.61 표시
2. ✅ src/main.py에 [EXECUTE-SELL] 로그 존재
3. ✅ __pycache__ 폴더 모두 삭제됨
4. ✅ 봇 시작 시 [EXECUTE-SELL] 로그 출력됨
5. ✅ 4분 이상 보유 시 자동 매도됨

## 📥 Download Links

- **GitHub Repository**: https://github.com/lee-jungkil/Lj
- **ZIP Download**: https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
- **Direct Script**: https://raw.githubusercontent.com/lee-jungkil/Lj/main/EMERGENCY_CACHE_CLEAR.bat

## 🎯 Summary

| Before | After |
|--------|-------|
| ❌ Old cached code running | ✅ Latest code running |
| ❌ No [EXECUTE-SELL] logs | ✅ [EXECUTE-SELL] logs visible |
| ❌ Sells not executing | ✅ Sells execute properly |
| ❌ Positions stuck | ✅ Positions close on time |

## 💡 Important Notes

- **Always run EMERGENCY_CACHE_CLEAR.bat after updating code from GitHub**
- **Python bytecode cache (.pyc) can persist even after git pull**
- **Use `-B` flag when running Python to disable bytecode generation**
- **Check for [EXECUTE-SELL] logs to confirm new code is running**

## 🔄 Version History

- v6.30.59: Fixed DataFrame indexing KeyError
- v6.30.60: Added extensive [EXECUTE-SELL] debug logs
- **v6.30.61**: Added EMERGENCY_CACHE_CLEAR.bat to force new code execution

---

**Release Date**: 2026-02-15  
**Critical Priority**: HIGH - Required for sell functionality
