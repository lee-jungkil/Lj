@echo off
chcp 65001 > nul
title Upbit AutoProfit Bot v6.30.61 - COMPLETE REINSTALL
color 0E

echo.
echo ========================================
echo  Upbit AutoProfit Bot v6.30.61
echo  COMPLETE REINSTALL (긴급 캐시 수정)
echo ========================================
echo.
echo 이 스크립트는 다음을 수행합니다:
echo   1. .env 파일 백업
echo   2. 모든 Python 캐시 파일 삭제 (⭐ v6.30.61)
echo   3. GitHub에서 최신 코드 다운로드
echo   4. 모든 필수 패키지 설치
echo   5. .env 파일 복원
echo   6. 봇 시작
echo.
echo This script will:
echo   1. Backup your .env file
echo   2. Delete all Python cache files (⭐ v6.30.61)
echo   3. Download fresh code from GitHub
echo   4. Install all dependencies
echo   5. Restore your .env file
echo   6. Start the bot
echo.
echo 경고: 로컬 변경사항이 모두 삭제됩니다!
echo WARNING: This will delete ALL local changes!
echo.
set /p CONFIRM="계속하시겠습니까? Continue? (Y/N): "
if /i not "%CONFIRM%"=="Y" (
    echo.
    echo 사용자에 의해 취소됨. Cancelled by user.
    echo.
    pause
    exit /b 0
)

echo.
echo ========================================
echo  STEP 1/9: 설정 백업 (Backup Configuration)
echo ========================================
echo.

REM Change to script directory
cd /d "%~dp0"
echo 현재 디렉토리 Current directory: %cd%
echo.

REM Backup .env file
if exist ".env" (
    echo .env 파일 백업 중... Backing up .env file...
    copy /Y .env .env.backup > nul
    if errorlevel 1 (
        echo [오류 ERROR] .env 파일 백업 실패! Failed to backup .env file!
        pause
        exit /b 1
    )
    echo [확인 OK] .env backed up to .env.backup
) else (
    echo [경고 WARN] 백업할 .env 파일이 없습니다. No .env file found to backup
)
echo.

echo ========================================
echo  STEP 2/9: 실행 중인 프로세스 중지 (Stop Running Processes)
echo ========================================
echo.

echo 모든 Python 프로세스 중지 중... Stopping all Python processes...
taskkill /F /IM python.exe /T > nul 2>&1
if errorlevel 1 (
    echo [정보 INFO] 실행 중인 Python 프로세스 없음. No Python processes running
) else (
    echo [확인 OK] Python 프로세스 중지됨. Python processes stopped
    timeout /t 2 /nobreak > nul
)

taskkill /F /IM pythonw.exe /T > nul 2>&1
echo.

echo ========================================
echo  STEP 3/9: ⭐ Python 캐시 완전 삭제 (Delete Python Cache) v6.30.61
echo ========================================
echo.

echo 모든 .pyc 파일 삭제 중... Deleting all .pyc files...
del /s /q *.pyc > nul 2>&1
echo [확인 OK] .pyc 파일 삭제됨. .pyc files deleted
echo.

echo 모든 __pycache__ 폴더 삭제 중... Deleting all __pycache__ folders...
for /d /r . %%d in (__pycache__) do @if exist "%%d" (
    echo   삭제 Deleting: %%d
    rd /s /q "%%d" 2>nul
)
echo [확인 OK] __pycache__ 폴더 삭제됨. __pycache__ folders deleted
echo.

echo 특정 캐시 디렉토리 삭제 중... Deleting specific cache directories...
if exist "src\__pycache__" (
    rd /s /q "src\__pycache__" 2>nul
    echo   [확인 OK] src\__pycache__ 삭제됨
)
if exist "src\ai\__pycache__" (
    rd /s /q "src\ai\__pycache__" 2>nul
    echo   [확인 OK] src\ai\__pycache__ 삭제됨
)
if exist "src\strategies\__pycache__" (
    rd /s /q "src\strategies\__pycache__" 2>nul
    echo   [확인 OK] src\strategies\__pycache__ 삭제됨
)
if exist "src\utils\__pycache__" (
    rd /s /q "src\utils\__pycache__" 2>nul
    echo   [확인 OK] src\utils\__pycache__ 삭제됨
)
echo [확인 OK] 특정 캐시 디렉토리 삭제됨. Specific cache directories deleted
echo.

echo ========================================
echo  STEP 4/9: Python 설치 확인 (Check Python Installation)
echo ========================================
echo.

python --version > nul 2>&1
if errorlevel 1 (
    echo [오류 ERROR] Python이 설치되지 않았습니다! Python is not installed!
    echo.
    echo https://www.python.org/ 에서 Python 3.8+ 를 설치하세요.
    echo Please install Python 3.8+ from https://www.python.org/
    echo 설치 시 "Add Python to PATH" 를 체크하세요.
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

python --version
echo [확인 OK] Python 설치 확인됨. Python installation confirmed
echo.

echo ========================================
echo  STEP 5/9: 최신 코드 다운로드 (Download Fresh Code)
echo ========================================
echo.

echo Git 설치 확인 중... Checking Git installation...
git --version > nul 2>&1
if errorlevel 1 (
    echo [경고 WARN] Git을 찾을 수 없습니다. 대체 다운로드 방법 사용...
    echo [WARN] Git not found. Using alternative download method...
    echo.
    
    echo PowerShell로 main.py 다운로드 중... Downloading main.py using PowerShell...
    powershell -Command "try { Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py' -OutFile 'src\main.py' -UseBasicParsing; Write-Host '[OK] main.py downloaded'; exit 0 } catch { Write-Host '[ERROR] Download failed'; exit 1 }"
    
    if errorlevel 1 (
        echo.
        echo [오류 ERROR] 코드 다운로드 실패! Failed to download code!
        echo.
        echo 다음 방법 중 하나를 시도하세요. Please try one of these methods:
        echo   1. Git 설치 후 스크립트 재실행. Install Git and run this script again
        echo   2. 수동 다운로드: https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
        echo   3. curl 사용: curl -o src\main.py https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py
        echo.
        pause
        exit /b 1
    )
) else (
    echo [확인 OK] Git 발견됨. Git found: 
    git --version
    echo.
    
    echo Git 저장소 초기화 중... Initializing Git repository...
    if not exist ".git" (
        git init
    )
    echo.
    
    echo 원격 저장소 추가 중... Adding remote repository...
    git remote remove origin > nul 2>&1
    git remote add origin https://github.com/lee-jungkil/Lj.git
    echo.
    
    echo 최신 코드 가져오는 중... Fetching latest code...
    git fetch origin main
    if errorlevel 1 (
        echo [오류 ERROR] GitHub에서 코드 가져오기 실패! Failed to fetch code from GitHub!
        echo.
        echo 인터넷 연결을 확인하고 다시 시도하세요.
        echo Please check your internet connection and try again.
        echo.
        pause
        exit /b 1
    )
    echo.
    
    echo 최신 버전으로 리셋 중... Resetting to latest version...
    git reset --hard origin/main
    if errorlevel 1 (
        echo [경고 WARN] 리셋 실패, 클린 체크아웃 시도 중... Reset failed, trying clean checkout...
        git checkout -f main
    )
    echo [확인 OK] 코드가 최신 버전으로 업데이트됨. Code updated to latest version
)
echo.

echo ========================================
echo  STEP 6/9: 코드 무결성 확인 (Verify Code Integrity)
echo ========================================
echo.

echo main.py 확인 중... Checking main.py...
if not exist "src\main.py" (
    echo [오류 ERROR] src\main.py를 찾을 수 없습니다! src\main.py not found!
    pause
    exit /b 1
)

findstr /C:"class AutoProfitBot" src\main.py > nul
if errorlevel 1 (
    echo [오류 ERROR] main.py에서 AutoProfitBot 클래스를 찾을 수 없습니다!
    echo [ERROR] AutoProfitBot class not found in main.py!
    echo 다운로드된 파일이 손상되었을 수 있습니다.
    echo The downloaded file may be corrupted.
    pause
    exit /b 1
)
echo [확인 OK] AutoProfitBot 클래스 발견됨. AutoProfitBot class found
echo.

echo ⭐ v6.30.61 코드 확인 중... Checking v6.30.61 code...
findstr /C:"[EXECUTE-SELL]" src\main.py > nul
if errorlevel 1 (
    echo [경고 WARN] [EXECUTE-SELL] 로그를 찾을 수 없습니다! [EXECUTE-SELL] logs not found!
    echo 구버전일 수 있습니다. This may be an old version.
) else (
    echo [확인 OK] [EXECUTE-SELL] 디버그 로그 발견됨 (v6.30.60+)
    echo [OK] [EXECUTE-SELL] debug logs found (v6.30.60+)
)
echo.

findstr /C:"if ohlcv is not None and len" src\main.py > nul
if errorlevel 1 (
    echo [경고 WARN] DataFrame 수정 코드를 찾을 수 없습니다!
    echo [WARN] DataFrame fix code not found!
) else (
    echo [확인 OK] DataFrame 수정 코드 발견됨 (v6.30.58+)
    echo [OK] DataFrame fix code found (v6.30.58+)
)
echo.

echo VERSION.txt 확인 중... Checking VERSION.txt...
if exist "VERSION.txt" (
    echo 현재 버전 Current version:
    type VERSION.txt
    echo.
) else (
    echo [경고 WARN] VERSION.txt를 찾을 수 없습니다.
)
echo.

echo 파일 크기 확인 중... Checking file size...
for %%A in ("src\main.py") do (
    set size=%%~zA
    echo 파일 크기 File size: %%~zA bytes
    if %%~zA LSS 50000 (
        echo [경고 WARN] 파일이 너무 작습니다. 불완전할 수 있습니다.
        echo [WARN] File seems too small, may be incomplete
    ) else (
        echo [확인 OK] 파일 크기 정상. File size looks good
    )
)
echo.

echo ========================================
echo  STEP 7/9: 의존성 설치 (Install Dependencies)
echo ========================================
echo.

echo pip 업그레이드 중... Upgrading pip...
python -m pip install --upgrade pip > nul 2>&1
echo [확인 OK] pip 업그레이드됨. pip upgraded
echo.

echo 필수 패키지 설치 중... Installing required packages...
echo 몇 분 걸릴 수 있습니다. 기다려주세요...
echo This may take a few minutes, please wait...
echo.

if exist "requirements.txt" (
    echo requirements.txt에서 설치 중... Installing from requirements.txt...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo [경고 WARN] 일부 패키지 실패, 필수 패키지만 설치 시도...
        echo [WARN] Some packages failed, trying essentials...
        python -m pip install pyupbit pandas numpy requests python-dotenv colorlog ta
    )
) else (
    echo 필수 패키지 설치 중... Installing essential packages...
    python -m pip install pyupbit pandas numpy requests python-dotenv colorlog ta
)

if errorlevel 1 (
    echo.
    echo [오류 ERROR] 패키지 설치 실패! Package installation failed!
    echo.
    echo 수동 설치를 시도하세요. Please try installing manually:
    echo   pip install pyupbit pandas numpy requests python-dotenv colorlog ta
    echo.
    pause
    exit /b 1
)
echo.
echo [확인 OK] 모든 패키지 설치 성공. All packages installed successfully
echo.

echo ========================================
echo  STEP 8/9: 설정 복원 (Restore Configuration)
echo ========================================
echo.

if exist ".env.backup" (
    echo .env 파일 복원 중... Restoring .env file...
    copy /Y .env.backup .env > nul
    echo [확인 OK] .env 파일 백업에서 복원됨. .env file restored from backup
) else if exist ".env" (
    echo [확인 OK] .env 파일이 이미 존재합니다. .env file already exists
) else (
    echo 새 .env 파일 생성 중... Creating new .env file...
    (
        echo # Upbit AutoProfit Bot v6.30.61
        echo # 업비트 자동 수익 봇 v6.30.61
        echo.
        echo # 거래 모드 Trading Mode
        echo TRADING_MODE=paper
        echo.
        echo # 초기 자본 및 리스크 관리 Capital and Risk Management
        echo INITIAL_CAPITAL=5000000
        echo MAX_DAILY_LOSS=500000
        echo MAX_CUMULATIVE_LOSS=1000000
        echo MAX_POSITIONS=5
        echo MAX_POSITION_RATIO=0.3
        echo.
        echo # AI 시스템 AI System
        echo ENABLE_ADVANCED_AI=true
        echo ENABLE_ORDERBOOK_ANALYSIS=true
        echo ENABLE_SCENARIO_DETECTION=true
        echo ENABLE_SMART_SPLIT=true
        echo ENABLE_HOLDING_TIME_AI=true
        echo ENABLE_DYNAMIC_EXIT=true
        echo EXIT_MODE=aggressive
        echo.
        echo # 로깅 Logging
        echo LOG_LEVEL=INFO
        echo ENABLE_TRADING_LOG=true
        echo ENABLE_ERROR_LOG=true
        echo.
        echo # 업비트 API 키 (실거래용) Upbit API Keys (for live trading)
        echo UPBIT_ACCESS_KEY=
        echo UPBIT_SECRET_KEY=
    ) > .env
    echo [확인 OK] 기본 .env 파일 생성됨. Default .env file created
)
echo.

echo ========================================
echo  STEP 9/9: 최종 검증 (Final Verification) ⭐ v6.30.61
echo ========================================
echo.

echo 캐시 삭제 확인 중... Verifying cache deletion...
if exist "src\__pycache__" (
    echo [경고 WARN] src\__pycache__ 여전히 존재함!
) else (
    echo [확인 OK] src\__pycache__ 삭제 확인
)

if exist "src\strategies\__pycache__" (
    echo [경고 WARN] src\strategies\__pycache__ 여전히 존재함!
) else (
    echo [확인 OK] src\strategies\__pycache__ 삭제 확인
)
echo.

echo 핵심 코드 검증 중... Verifying critical code...
findstr /C:"[EXECUTE-SELL]" src\main.py > nul
if errorlevel 1 (
    echo [경고 WARN] 최신 코드가 아닐 수 있습니다!
    echo [WARN] May not be the latest code!
) else (
    echo [확인 OK] v6.30.60+ 코드 검증됨
)
echo.

echo ========================================
echo  재설치 완료! REINSTALL COMPLETE!
echo ========================================
echo.
echo 현재 버전 Current version: v6.30.61 (Emergency Cache Fix)
echo 저장소 Repository: https://github.com/lee-jungkil/Lj
echo.
echo ⭐ 중요한 변경사항 Important Changes:
echo   - Python 캐시 완전 삭제 Complete Python cache deletion
echo   - [EXECUTE-SELL] 디버그 로그 추가 [EXECUTE-SELL] debug logs added
echo   - DataFrame 오류 수정 DataFrame error fixed
echo   - 매도 로직 정상화 Sell logic normalized
echo.
echo 다음 단계 Next steps:
echo   1. .env 파일 설정 검토 Review your .env file settings
echo   2. 실거래용: .env에 업비트 API 키 추가 For live trading: Add Upbit API keys to .env
echo   3. 아무 키나 눌러 모의거래 시작 Press any key to start the bot in paper mode
echo.
echo 예상되는 로그 Expected logs:
echo   [EXECUTE-SELL] execute_sell() 호출됨
echo   [EXECUTE-SELL] 포지션 존재 여부 체크
echo   [EXECUTE-SELL] ✅ 포지션 찾음
echo.
echo.
set /p START="봇을 지금 시작하시겠습니까? Start bot now? (Y/N): "
if /i "%START%"=="Y" (
    echo.
    echo ========================================
    echo  봇 시작 중... STARTING BOT...
    echo ========================================
    echo.
    echo -B -u 플래그로 시작합니다 (캐시 비활성화, 버퍼링 제거)...
    echo Starting with -B -u flags (disable cache, unbuffered output)...
    echo 3-5초마다 DEBUG 로그가 보여야 합니다.
    echo You should see DEBUG logs every 3-5 seconds
    echo.
    echo [EXECUTE-SELL] 로그를 확인하세요!
    echo Watch for [EXECUTE-SELL] logs!
    echo.
    timeout /t 2 /nobreak > nul
    python -B -u -m src.main --mode paper
) else (
    echo.
    echo 수동으로 봇을 시작하려면 다음을 실행하세요:
    echo To start the bot manually, run:
    echo   python -B -u -m src.main --mode paper
    echo.
    echo 또는 다음을 사용하세요:
    echo Or use:
    echo   RUN_PAPER_CLEAN.bat
    echo.
)

echo.
echo 아무 키나 눌러 종료... Press any key to exit...
pause > nul
exit /b 0
