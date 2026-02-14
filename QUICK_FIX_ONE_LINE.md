# 🚀 Phase 3 청산 체크 한 줄 해결 명령어

## 📋 현재 상황
- ❌ 포지션 보유 중인데 `⚡ 포지션 청산 체크` 로그가 안 나옴
- ❌ `[DEBUG-LOOP]` 로그가 안 나옴  
- ✅ **원인: 구버전 (v6.25) main.py 실행 중**

---

## ✅ 즉시 해결 (복붙 한 줄)

### 방법 1: 긴급 업데이트 배치 파일 (가장 쉬움)

```batch
curl -o EMERGENCY_UPDATE_MAIN.bat https://raw.githubusercontent.com/lee-jungkil/Lj/main/EMERGENCY_UPDATE_MAIN.bat && EMERGENCY_UPDATE_MAIN.bat
```

배치 파일이 실행되면 **Y** 입력 후 엔터

---

### 방법 2: 한 줄 직접 업데이트

**프로젝트 폴더에서 실행:**

```batch
del /s /q *.pyc && for /d /r . %d in (__pycache__) do @rd /s /q "%d" && curl -o src\main.py https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py && python -B -u -m src.main --mode paper
```

---

### 방법 3: PowerShell 버전

```powershell
Get-ChildItem -Recurse -Filter *.pyc | Remove-Item -Force; Get-ChildItem -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force; Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py' -OutFile 'src\main.py' -UseBasicParsing; python -B -u -m src.main --mode paper
```

---

## 📊 정상 작동 확인

**이런 로그가 3-5초마다 출력되면 성공:**

```
[DEBUG-LOOP] 메인 루프 #1 시작 - 시간: 1771067600.12
[DEBUG] Phase 3 체크 - 현재시간: 1771067600.12, 마지막체크: 0.00, 경과: 1771067600.12초, 포지션: 1개
[DEBUG] ✅ 시간 조건 충족! (>= 3초)
[DEBUG] ✅ 포지션 있음! Phase 3 실행!

--- ⚡ 포지션 청산 체크 #1 - 21:30:15 ---
📊 KRW-DEEP 손익률: +9.00% (보유 240초)
   익절 목표: +1.5% | 손절 목표: -1.0%
```

---

## 🔧 여전히 안 된다면?

**1. 현재 디렉토리 확인**
```batch
cd
dir src
```

**2. 프로젝트 폴더로 이동**
```batch
cd C:\Users\admin\Downloads\Lj-FRESH\Lj-main
```
(본인의 실제 경로로 변경)

**3. 다시 한 줄 명령어 실행**

---

## 📞 추가 도움

- 전체 가이드: `PHASE3_FIX_GUIDE.md` 참고
- GitHub: https://github.com/lee-jungkil/Lj
- 버전: v6.30.40-EMERGENCY-UPDATE-MAIN
