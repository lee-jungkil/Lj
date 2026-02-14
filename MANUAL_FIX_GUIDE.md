# 🚨 긴급 수정 가이드 - 배치 파일이 작동하지 않을 때

## 문제: FIX_POSITION_CHECK_URGENT.bat 실행 시 창이 바로 사라짐

이것은 Windows 시스템 설정 문제일 수 있습니다.

---

## ✅ 해결 방법 1: 명령 프롬프트에서 직접 실행 (추천)

### 1단계: 명령 프롬프트 열기
```
1. Windows 키 + R
2. "cmd" 입력
3. Enter
```

### 2단계: 폴더 이동
```batch
cd C:\Users\admin\Downloads\Lj-main\Lj-main
```

### 3단계: 다음 명령어들을 **하나씩** 복사해서 실행

```batch
REM 1. Python 프로세스 종료
taskkill /F /IM python.exe

REM 2. 캐시 폴더 삭제
for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"

REM 3. .pyc 파일 삭제
del /s /q *.pyc

REM 4. 캐시 삭제 확인 (아무것도 안 나와야 정상)
dir /s /b __pycache__

REM 5. Git 리셋
git reset --hard HEAD

REM 6. Git 최신 코드 받기
git pull origin main

REM 7. 버전 확인
type VERSION.txt

REM 8. 봇 실행
RUN_PAPER_CLEAN.bat
```

---

## ✅ 해결 방법 2: PowerShell 스크립트 사용

### 1단계: 메모장 열기

### 2단계: 다음 내용을 복사해서 붙여넣기

```powershell
# Move to bot directory
Set-Location "C:\Users\admin\Downloads\Lj-main\Lj-main"

# Stop Python
Write-Host "[1/7] Stopping Python processes..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
Write-Host "OK" -ForegroundColor Green
Start-Sleep -Seconds 1

# Delete cache
Write-Host "[2/7] Deleting Python cache..." -ForegroundColor Yellow
Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
Get-ChildItem -Path . -Recurse -File -Filter "*.pyc" | Remove-Item -Force
Write-Host "OK" -ForegroundColor Green
Start-Sleep -Seconds 1

# Verify cache deleted
Write-Host "[3/7] Verifying cache deletion..." -ForegroundColor Yellow
$cacheExists = Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue
if ($null -eq $cacheExists) {
    Write-Host "OK - No cache found" -ForegroundColor Green
} else {
    Write-Host "WARNING - Cache still exists" -ForegroundColor Red
}
Start-Sleep -Seconds 1

# Git reset
Write-Host "[4/7] Resetting git..." -ForegroundColor Yellow
git reset --hard HEAD
Write-Host "OK" -ForegroundColor Green
Start-Sleep -Seconds 1

# Git pull
Write-Host "[5/7] Pulling latest code..." -ForegroundColor Yellow
git pull origin main
Write-Host "OK" -ForegroundColor Green
Start-Sleep -Seconds 1

# Check version
Write-Host "[6/7] Checking version..." -ForegroundColor Yellow
Get-Content VERSION.txt | Select-Object -First 1
Start-Sleep -Seconds 1

# Verify code
Write-Host "[7/7] Verifying Phase 3 code..." -ForegroundColor Yellow
Select-String -Path "src\main.py" -Pattern "if current_time - self.last_position_check_time" | Where-Object { $_.LineNumber -eq 2143 }
Write-Host "OK" -ForegroundColor Green

Write-Host ""
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "                    ALL STEPS COMPLETE                                  " -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Now run: RUN_PAPER_CLEAN.bat" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to start the bot..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Start bot
.\RUN_PAPER_CLEAN.bat
```

### 3단계: 파일 저장
```
파일명: FIX_MANUAL.ps1
저장 위치: C:\Users\admin\Downloads\Lj-main\Lj-main\
```

### 4단계: PowerShell에서 실행
```
1. 파일을 우클릭
2. "PowerShell로 실행" 선택
```

---

## ✅ 해결 방법 3: 한 줄 명령어 (가장 빠름)

명령 프롬프트를 열고 다음 **한 줄**을 복사해서 실행:

```batch
cd C:\Users\admin\Downloads\Lj-main\Lj-main && taskkill /F /IM python.exe && for /d /r . %d in (__pycache__) do @rd /s /q "%d" && del /s /q *.pyc && git reset --hard HEAD && git pull origin main && type VERSION.txt && RUN_PAPER_CLEAN.bat
```

---

## 🔍 예상 결과

봇이 시작되면 **3초마다** 다음 로그가 나와야 합니다:

```
[16:30:00] ⚡ 포지션 청산 체크 #1 (보유: 1/5)
[16:30:00] 📊 KRW-CBK 손익률: -0.61% (보유 228초)
[16:30:00]    익절 목표: +1.5% | 손절 목표: -1.0%
[16:30:00]    📊 보유 유지

[16:30:03] ⚡ 포지션 청산 체크 #2 (보유: 1/5)
[16:30:03] 📊 KRW-CBK 손익률: -0.58% (보유 231초)
...
```

---

## ❓ 여전히 로그가 안 나온다면?

### 1. 버전 확인
```batch
type VERSION.txt
```
**기대값**: v6.30.31 이상

### 2. 코드 확인
```batch
findstr /N "if current_time - self.last_position_check_time" src\main.py
```
**기대값**: `2143:    if current_time - self.last_position_check_time >= self.position_check_interval:`

### 3. 캐시 확인
```batch
dir /s /b __pycache__
```
**기대값**: "찾을 수 없습니다" 또는 빈 결과

### 4. 마지막 방법: 완전 재설치
```batch
cd C:\Users\admin\Downloads
rename Lj-main Lj-main-backup
git clone https://github.com/lee-jungkil/Lj.git Lj-main
cd Lj-main\Lj-main
copy ..\Lj-main-backup\.env .env
setup.bat
RUN_PAPER_CLEAN.bat
```

---

## 📞 추가 도움

위의 방법들을 모두 시도해도 해결되지 않으면:

1. **스크린샷 공유**:
   - 명령 프롬프트에서 명령어 실행 결과
   - 봇 실행 화면
   - VERSION.txt 내용

2. **확인 사항**:
   - Python 버전 (`python --version`)
   - Git 버전 (`git --version`)
   - 현재 폴더 위치 (`cd`)

---

## 📝 요약

**가장 쉬운 방법**:
```batch
cd C:\Users\admin\Downloads\Lj-main\Lj-main
taskkill /F /IM python.exe
for /d /r . %d in (__pycache__) do @rd /s /q "%d"
del /s /q *.pyc
git pull origin main
RUN_PAPER_CLEAN.bat
```

**이것만 기억하세요**:
1. Python 프로세스 종료
2. __pycache__ 폴더 삭제
3. .pyc 파일 삭제
4. 최신 코드 받기
5. 봇 실행

**3초마다 "⚡ 포지션 청산 체크" 로그가 나와야 합니다!**
