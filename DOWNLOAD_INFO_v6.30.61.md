# 📦 Upbit AutoProfit Bot v6.30.61 - 긴급 수정 버전

## 🚨 Critical Fix: 매도 안되는 문제 완전 해결

**문제**: Python 캐시(.pyc) 파일이 오래된 코드를 실행하여 매도가 작동하지 않음  
**해결**: EMERGENCY_CACHE_CLEAR.bat 스크립트로 완전한 캐시 삭제

---

## 📥 다운로드 링크

### 🎯 Option 1: ZIP 다운로드 (추천)
```
https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
```

**설치 방법**:
1. ZIP 다운로드 및 압축 해제
2. `EMERGENCY_CACHE_CLEAR.bat` 더블클릭
3. 로그에서 `[EXECUTE-SELL]` 확인

### 🔄 Option 2: Git Clone
```bash
git clone https://github.com/lee-jungkil/Lj.git
cd Lj
EMERGENCY_CACHE_CLEAR.bat
```

### 📝 Option 3: 개별 파일 다운로드

**필수 파일**:
- main.py: https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py
- EMERGENCY_CACHE_CLEAR.bat: https://raw.githubusercontent.com/lee-jungkil/Lj/main/EMERGENCY_CACHE_CLEAR.bat
- VERSION.txt: https://raw.githubusercontent.com/lee-jungkil/Lj/main/VERSION.txt

---

## 🔧 긴급 수정 스크립트

### EMERGENCY_CACHE_CLEAR.bat

이 스크립트는:
- ✅ 실행 중인 Python 프로세스 강제 종료
- ✅ 모든 `__pycache__` 폴더 삭제
- ✅ 모든 `.pyc` 바이트코드 파일 삭제
- ✅ VERSION 확인 (v6.30.61)
- ✅ `[EXECUTE-SELL]` 로그 존재 확인
- ✅ 봇 자동 재시작

**사용법**:
```batch
# 기존 설치가 있다면
cd C:\Users\YourName\Lj
git pull origin main
EMERGENCY_CACHE_CLEAR.bat

# 새로 설치한다면
# ZIP 압축 해제 후
EMERGENCY_CACHE_CLEAR.bat
```

---

## ✅ 성공 확인

봇 재시작 후 **반드시** 다음 로그가 보여야 합니다:

```
[EXECUTE-SELL] execute_sell() 호출됨 - ticker: KRW-XXX
[EXECUTE-SELL] 포지션 존재 여부 체크: True
[EXECUTE-SELL] ✅ 포지션 찾음: KRW-XXX
[EXECUTE-SELL] 모의거래 모드: 매도 주문 시뮬레이션
[EXECUTE-SELL] risk_manager 청산 완료
```

**만약 `[EXECUTE-SELL]` 로그가 없다면**:
- 아직 오래된 캐시 사용 중
- EMERGENCY_CACHE_CLEAR.bat 다시 실행
- PC 재부팅 후 재시도

---

## 📋 주요 변경사항

### v6.30.61 (2026-02-15)
- 🚨 **CRITICAL**: EMERGENCY_CACHE_CLEAR.bat 추가
- 🐛 Python 캐시 문제로 인한 매도 미실행 해결
- 📝 `[EXECUTE-SELL]` 디버그 로그 추가 (v6.30.60)
- 🔧 DataFrame boolean 평가 오류 수정 (v6.30.58)
- 🔧 DataFrame indexing KeyError 수정 (v6.30.59)

### 매도 조건 (정상 작동 시)
- **시간 초과**: Aggressive 4분, Conservative 8분
- **익절**: +1.5%
- **손절**: -1.0%
- **차트 신호**: RSI, MACD, 거래량 기반

---

## 🎯 사용 시나리오

### 시나리오 1: 처음 설치
```batch
# 1. ZIP 다운로드
https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip

# 2. 압축 해제

# 3. .env 파일 생성 (또는 .env.example 복사)
copy .env.example .env
notepad .env

# 4. 캐시 삭제 및 시작
EMERGENCY_CACHE_CLEAR.bat
```

### 시나리오 2: 기존 버전 업데이트
```batch
# 1. 기존 폴더로 이동
cd C:\Users\YourName\Lj

# 2. 최신 코드 받기
git pull origin main

# 3. 캐시 삭제 및 재시작
EMERGENCY_CACHE_CLEAR.bat
```

### 시나리오 3: 매도 안될 때 긴급 조치
```batch
# 1. 봇 종료 (Ctrl+C)

# 2. 캐시 삭제
EMERGENCY_CACHE_CLEAR.bat

# 3. [EXECUTE-SELL] 로그 확인
```

---

## 🔍 문제 진단

### 증상 A: `[EXECUTE-SELL]` 로그 없음
**원인**: 오래된 캐시 사용  
**해결**: EMERGENCY_CACHE_CLEAR.bat 실행

### 증상 B: `[FORCE-SELL] ✅ 매도 주문 완료!`만 나오고 실제 매도 안됨
**원인**: execute_sell() 함수가 호출되지 않음 (캐시 문제)  
**해결**: EMERGENCY_CACHE_CLEAR.bat 실행

### 증상 C: 시간 초과 조건 충족했는데 매도 안됨
**원인**: check_positions() 함수가 오류로 중단됨 (캐시 문제)  
**해결**: EMERGENCY_CACHE_CLEAR.bat 실행

---

## 📊 테스트 결과

### Before (v6.30.57, 캐시 있음)
- KRW-BORA: 697초 보유 (11분 37초)
- 강제 매도 기준: 240초 (4분)
- 조건 충족: ✅ (697 > 240)
- 로그: `[FORCE-SELL] ✅ 매도 주문 완료!`
- 실제 매도: ❌ **안됨**
- `[EXECUTE-SELL]` 로그: ❌ **없음**

### After (v6.30.61, 캐시 삭제)
- 동일 조건
- 로그: `[EXECUTE-SELL]` 출력 ✅
- 실제 매도: ✅ **정상 작동**
- 포지션 청산: ✅ **완료**

---

## 📚 참고 문서

- **EMERGENCY_FIX_GUIDE.md**: 상세 해결 가이드
- **RELEASE_NOTES_v6.30.61.md**: 릴리스 노트
- **README.md**: 전체 사용 설명서

---

## 💡 예방 조치

앞으로 코드 업데이트 시:

1. ✅ **항상 EMERGENCY_CACHE_CLEAR.bat 사용**
2. ✅ `[EXECUTE-SELL]` 로그 확인
3. ✅ 캐시 자동 생성 방지: `python -B ...`

---

## 📞 지원

- **GitHub**: https://github.com/lee-jungkil/Lj
- **Issues**: https://github.com/lee-jungkil/Lj/issues
- **Discussions**: https://github.com/lee-jungkil/Lj/discussions

---

**Version**: v6.30.61-EMERGENCY-CACHE-FIX  
**Release Date**: 2026-02-15  
**Priority**: 🚨 CRITICAL

**다운로드**: https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
