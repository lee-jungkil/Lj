# 🚨 Phase 3 청산 체크 미작동 해결 가이드

## 📋 문제 상황

**증상:**
- ✅ 봇 실행 중
- ✅ 포지션 보유 중 (예: DEEP +9.00%)
- ❌ `[DEBUG-LOOP]` 로그 없음
- ❌ `⚡ 포지션 청산 체크` 로그 없음
- ❌ 자동 매도 실행 안됨

**원인:**
사용자가 **구버전 (v6.25) main.py**를 실행 중입니다.
- GitHub에는 **v6.30.40** (Phase 3 청산 체크 포함)이 있음
- 사용자 로컬에는 **v6.25** (Phase 3 청산 체크 없음)이 실행 중

---

## ✅ 즉시 해결 방법

### 🚀 방법 1: 긴급 업데이트 배치 파일 (권장)

**1단계: 배치 파일 다운로드**
```batch
curl -o EMERGENCY_UPDATE_MAIN.bat https://raw.githubusercontent.com/lee-jungkil/Lj/main/EMERGENCY_UPDATE_MAIN.bat
```

**2단계: 실행**
```batch
EMERGENCY_UPDATE_MAIN.bat
```

**3단계: 봇 재시작**
```batch
python -B -u -m src.main --mode paper
```

---

### 🔧 방법 2: 수동 업데이트

**1단계: 현재 봇 중지**
```
Ctrl + C
```

**2단계: 프로젝트 폴더로 이동**
```batch
cd C:\Users\admin\Downloads\Lj-FRESH\Lj-main
```
(또는 본인의 프로젝트 폴더 경로)

**3단계: 기존 main.py 백업**
```batch
copy src\main.py src\main_backup.py
```

**4단계: 최신 main.py 다운로드**

**Option A: curl 사용 (빠름)**
```batch
curl -o src\main.py https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py
```

**Option B: PowerShell 사용**
```batch
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py' -OutFile 'src\main.py' -UseBasicParsing"
```

**5단계: 코드 검증**
```batch
findstr /C:"Phase 3 체크" src\main.py
findstr /C:"DEBUG-LOOP" src\main.py
```

**예상 출력:**
```
2147:                print(f"\n[DEBUG] Phase 3 체크 - 현재시간: {current_time:.2f}...
1986:                print(f"\n[DEBUG-LOOP] 메인 루프 #{monitor_count} 시작...
```

**6단계: 캐시 정리**
```batch
del /s /q *.pyc
for /d /r . %d in (__pycache__) do @rd /s /q "%d"
```

**7단계: 봇 재시작**
```batch
python -B -u -m src.main --mode paper
```

---

## 📊 정상 작동 확인

**메인 루프가 실행되면 이런 로그가 나타납니다 (3-5초마다 반복):**

```
[2026-02-14 21:30:00] 🤖 봇 가동 시작!
Paper Trading Mode (Simulation)
Initial Capital: 5,000,000 KRW

[DEBUG-LOOP] 메인 루프 #1 시작 - 시간: 1771067600.12

[DEBUG] Phase 3 체크 - 현재시간: 1771067600.12, 마지막체크: 0.00, 경과: 1771067600.12초, 포지션: 0개
[DEBUG] ✅ 시간 조건 충족! (>= 3초)
[DEBUG] ⚠️ 포지션 없음, Phase 3 스킵

[DEBUG-SLEEP] 5.00초 대기 중... (다음: 급등감지)
```

**포지션을 보유하고 있을 때 (예: DEEP +9.00%):**

```
[DEBUG-LOOP] 메인 루프 #5 시작 - 시간: 1771067615.34

[DEBUG] Phase 3 체크 - 현재시간: 1771067615.34, 마지막체크: 1771067612.12, 경과: 3.22초, 포지션: 1개
[DEBUG] ✅ 시간 조건 충족! (>= 3초)
[DEBUG] ✅ 포지션 있음! Phase 3 실행!

--- ⚡ 포지션 청산 체크 #1 - 21:30:15 ---
📊 KRW-DEEP 손익률: +9.00% (보유 240초)
   익절 목표: +1.5% | 손절 목표: -1.0%
   ✅ 익절 조건 충족! (+9.00% >= +1.5%)
   💰 익절 매도 주문 실행 중...

[DEBUG] ✅ Phase 3 완료! 마지막 체크 시간 업데이트: 1771067615.34

[DEBUG-SLEEP] 3.00초 대기 중... (다음: 포지션체크 OR 급등감지)
```

---

## 🔍 트러블슈팅

### ❌ 문제 1: "파일을 찾을 수 없습니다"

**해결:**
```batch
cd C:\Users\admin\Downloads\Lj-FRESH\Lj-main
dir src
```
`src` 폴더가 없으면 상위 폴더로 이동:
```batch
cd ..
dir
```

---

### ❌ 문제 2: "Phase 3 체크" 문자열을 찾을 수 없음

**다운로드한 파일이 잘못되었습니다.**

**해결: 특정 커밋에서 다운로드**
```batch
curl -o src\main.py https://raw.githubusercontent.com/lee-jungkil/Lj/3eb45c6/src/main.py
```

---

### ❌ 문제 3: SyntaxError / ParserError

**파일이 손상되었습니다.**

**해결:**
```batch
del src\main.py
curl -o src\main.py https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py
python -c "import sys; sys.path.insert(0, 'src'); from main import AutoProfitBot; print('OK')"
```

---

### ❌ 문제 4: "ModuleNotFoundError: No module named 'main'"

**Python 경로 문제입니다.**

**해결: 직접 실행**
```batch
cd src
python -B -u -c "from main import AutoProfitBot; bot = AutoProfitBot(); bot.run()"
```

---

## 📌 핵심 포인트

1. **GitHub 저장소에는 최신 코드가 있습니다.**
   - 파일: `src/main.py`
   - 버전: v6.30.40
   - Phase 3 청산 체크: ✅ 있음
   - DEBUG 로그: ✅ 있음

2. **사용자 로컬에는 구버전이 실행 중입니다.**
   - 버전: v6.25
   - Phase 3 청산 체크: ❌ 없음
   - DEBUG 로그: ❌ 없음

3. **해결 방법: main.py 파일만 교체하면 됩니다.**
   - 다른 파일은 건드릴 필요 없음
   - .env 설정은 그대로 유지
   - 캐시만 정리하면 OK

---

## 🎯 즉시 실행 명령어 (한 줄 복붙)

**전체 과정을 한 번에 실행:**

```batch
cd C:\Users\admin\Downloads\Lj-FRESH\Lj-main && copy src\main.py src\main_backup.py && curl -o src\main.py https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py && del /s /q *.pyc && for /d /r . %d in (__pycache__) do @rd /s /q "%d" && findstr /C:"Phase 3 체크" src\main.py && python -B -u -m src.main --mode paper
```

**또는 간단 버전 (캐시 정리 + 다운로드 + 실행):**

```batch
del /s /q *.pyc && curl -o src\main.py https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py && python -B -u -m src.main --mode paper
```

---

## 📞 도움이 필요하면

1. **현재 버전 확인:**
   ```batch
   findstr /C:"버전:" src\main.py | findstr /N "."
   ```

2. **파일 크기 확인:**
   ```batch
   dir src\main.py
   ```
   예상 크기: **약 118,000 ~ 120,000 bytes**

3. **클래스 확인:**
   ```batch
   findstr /C:"class AutoProfitBot" src\main.py
   ```
   예상 출력: `92:class AutoProfitBot:`

4. **Phase 3 코드 라인 확인:**
   ```batch
   findstr /N /C:"Phase 3 체크" src\main.py
   ```
   예상 출력: `2147:...Phase 3 체크...`

---

## ✅ 최종 확인 체크리스트

- [ ] `EMERGENCY_UPDATE_MAIN.bat` 실행 완료
- [ ] `findstr /C:"Phase 3 체크" src\main.py` → 결과 있음
- [ ] `findstr /C:"DEBUG-LOOP" src\main.py` → 결과 있음
- [ ] 캐시 정리 완료 (*.pyc, __pycache__ 삭제)
- [ ] 봇 재시작: `python -B -u -m src.main --mode paper`
- [ ] 콘솔에 `[DEBUG-LOOP]` 로그 출력됨
- [ ] 포지션 보유 시 `⚡ 포지션 청산 체크` 로그 출력됨

**모든 항목이 체크되면 문제 해결 완료입니다!** 🎉

---

## 📚 관련 문서

- GitHub 저장소: https://github.com/lee-jungkil/Lj
- 최신 릴리스: v6.30.40-EMERGENCY-UPDATE-MAIN
- 커밋: 3eb45c6
