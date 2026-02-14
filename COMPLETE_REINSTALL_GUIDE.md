# Complete Reinstall Guide - v6.30.38

## 🚨 Problem: Bot Not Working / No DEBUG Logs

If you're experiencing:
- No "⚡ 포지션 청산 체크" logs appearing
- Bot runs but doesn't show position checks
- ImportError or module not found errors
- Corrupted or outdated code

**→ Use COMPLETE_REINSTALL.bat**

---

## 📋 What's New in v6.30.38

### New Features
1. **COMPLETE_REINSTALL.bat** - Full automated reinstallation
2. **Enhanced setup.bat** - Better error handling and verification
3. **Improved RUN_PAPER_CLEAN.bat** - Code verification before start
4. **Better error messages** - Clear troubleshooting steps

### Bug Fixes
- Fixed Python cache causing old code execution
- Fixed code download issues (Git + PowerShell fallback)
- Fixed TradingBot class import errors
- Added comprehensive code verification

---

## 🚀 Quick Start

### Method 1: Complete Reinstall (Recommended)

1. **Download latest batch file:**
   ```batch
   curl -o COMPLETE_REINSTALL.bat https://raw.githubusercontent.com/lee-jungkil/Lj/main/COMPLETE_REINSTALL.bat
   ```

2. **Run it:**
   ```batch
   COMPLETE_REINSTALL.bat
   ```

3. **Follow prompts:**
   - Confirm reinstall (Y)
   - Wait for completion (2-5 minutes)
   - Choose to start bot (Y)

### Method 2: Manual Setup

1. **Install Python 3.8+** from https://www.python.org/
   - Check "Add Python to PATH"

2. **Download project:**
   ```batch
   git clone https://github.com/lee-jungkil/Lj.git
   cd Lj
   ```

3. **Run setup:**
   ```batch
   setup.bat
   ```

4. **Start bot:**
   ```batch
   RUN_PAPER_CLEAN.bat
   ```

---

## 📂 Batch Files Overview

### COMPLETE_REINSTALL.bat
**Purpose:** Full clean reinstallation  
**When to use:**
- Bot not working at all
- Code corruption suspected
- ImportError or class not found
- Persistent cache issues

**What it does:**
1. Backs up .env configuration
2. Stops all Python processes
3. Deletes all cache files
4. Downloads fresh code from GitHub
5. Installs all dependencies
6. Restores configuration
7. Starts the bot

**Time:** 2-5 minutes

---

### setup.bat
**Purpose:** Initial setup and package installation  
**When to use:**
- First time installation
- After downloading project
- Package installation needed

**What it does:**
1. Verifies Python installation
2. Cleans cache
3. Checks Git (optional)
4. Verifies project structure
5. Installs dependencies
6. Creates .env configuration
7. Verifies code integrity

**Time:** 2-10 minutes (depending on internet speed)

---

### RUN_PAPER_CLEAN.bat
**Purpose:** Start bot in paper trading mode  
**When to use:**
- Normal bot startup
- Testing strategies
- Daily trading

**What it does:**
1. Verifies Python and packages
2. Verifies code integrity
3. Cleans cache (every run)
4. Checks configuration
5. Starts bot with debug flags

**Time:** <1 minute

---

## 🔧 Troubleshooting

### Problem: "ImportError: cannot import name 'TradingBot'"

**Solution:**
```batch
COMPLETE_REINSTALL.bat
```

### Problem: No DEBUG logs appearing

**Symptoms:**
- Bot runs but no `[DEBUG-LOOP]` logs
- No position check logs
- Seems frozen or slow

**Solution:**
```batch
# Method 1: Complete reinstall
COMPLETE_REINSTALL.bat

# Method 2: Manual cache clean
del /s /q *.pyc
for /d /r . %d in (__pycache__) do @rd /s /q "%d"
python -B -u -m src.main --mode paper
```

### Problem: "Python is not installed"

**Solution:**
1. Download Python 3.8+ from https://www.python.org/
2. **Important:** Check "Add Python to PATH" during installation
3. Restart command prompt
4. Verify: `python --version`

### Problem: Git not found

**Solution (Option 1):** Install Git
- Download from https://git-scm.com/
- Install with default settings
- Restart command prompt

**Solution (Option 2):** Use without Git
- COMPLETE_REINSTALL.bat will use PowerShell download as fallback
- Or manually download main.py:
  ```batch
  powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py' -OutFile 'src\main.py' -UseBasicParsing"
  ```

### Problem: Package installation fails

**Solution:**
```batch
# Upgrade pip first
python -m pip install --upgrade pip

# Install essential packages one by one
python -m pip install pyupbit
python -m pip install pandas
python -m pip install numpy
python -m pip install requests
python -m pip install python-dotenv
python -m pip install colorlog
python -m pip install ta
```

---

## ⚙️ Configuration (.env file)

### Default Settings (Paper Trading)
```env
TRADING_MODE=paper
INITIAL_CAPITAL=5000000
MAX_DAILY_LOSS=500000
MAX_CUMULATIVE_LOSS=1000000
MAX_POSITIONS=5
MAX_POSITION_RATIO=0.3
```

### For Live Trading
Add your Upbit API keys:
```env
TRADING_MODE=live
UPBIT_ACCESS_KEY=your_access_key_here
UPBIT_SECRET_KEY=your_secret_key_here
```

⚠️ **Warning:** Never share your API keys!

---

## 📊 Expected Logs

### Normal Startup
```
[2026-02-14 21:00:00] 🤖 봇 가동 시작!

[DEBUG-LOOP] 메인 루프 #1 시작 - 시간: 1771067600.12

[DEBUG] Phase 3 체크 - 현재시간: 1771067600.12, 마지막체크: 0.00, 경과: 1771067600.12초, 포지션: 0개
[DEBUG] ✅ 시간 조건 충족! (>= 3초)
[DEBUG] ⚠️ 포지션 없음, Phase 3 스킵

[DEBUG-SLEEP] 5.00초 대기 중... (다음: 급등감지)
[DEBUG-SLEEP] 포지션: 0개, 초단타: 0개
[DEBUG-SLEEP] 대기 완료! 루프 재시작...
```

### With Positions
```
[DEBUG-LOOP] 메인 루프 #15 시작 - 시간: 1771067645.23

[DEBUG] Phase 3 체크 - 현재시간: 1771067645.23, 마지막체크: 1771067642.10, 경과: 3.13초, 포지션: 2개
[DEBUG] ✅ 시간 조건 충족! (>= 3초)
[DEBUG] ✅ 포지션 있음! Phase 3 실행!

--- ⚡ 포지션 청산 체크 #5 - 21:00:45 ---
📊 KRW-BTC 손익률: +1.23% (보유 180초)
   익절 목표: +1.5% | 손절 목표: -1.0%
   📊 보유 유지

📊 KRW-ETH 손익률: +0.87% (보유 195초)
   익절 목표: +1.5% | 손절 목표: -1.0%
   📊 보유 유지

[DEBUG] ✅ Phase 3 완료! 마지막 체크 시간 업데이트: 1771067645.23

[DEBUG-SLEEP] 3.00초 대기 중... (다음: 포지션체크 OR 급등감지)
[DEBUG-SLEEP] 포지션: 2개, 초단타: 0개
[DEBUG-SLEEP] 대기 완료! 루프 재시작...
```

### Sell Execution
```
📊 KRW-BTC 손익률: +1.58% (보유 240초)
   익절 목표: +1.5% | 손절 목표: -1.0%
   ✅ 익절 트리거 발동! (+1.58% >= +1.5%)

[2026-02-14 21:01:00] 💰 매도 주문 체결 완료!
   코인: KRW-BTC
   매도가: 45,234,000 원
   수익: +358,920 원 (+1.58%)
```

---

## 🆘 Still Having Issues?

1. **Check GitHub Issues:**
   https://github.com/lee-jungkil/Lj/issues

2. **Verify System Requirements:**
   - Windows 10/11
   - Python 3.8 or higher
   - Internet connection
   - At least 2GB free disk space

3. **Try Fresh Installation:**
   ```batch
   # Move to parent directory
   cd C:\Users\admin\Downloads
   
   # Rename old folder
   ren Lj-main Lj-main-backup
   
   # Clone fresh
   git clone https://github.com/lee-jungkil/Lj.git Lj-main
   cd Lj-main
   
   # Copy old config if exists
   copy ..\Lj-main-backup\.env .env
   
   # Run setup
   setup.bat
   
   # Start bot
   RUN_PAPER_CLEAN.bat
   ```

4. **Manual Verification Commands:**
   ```batch
   # Check Python
   python --version
   where python
   
   # Check project structure
   dir src
   
   # Check TradingBot class
   findstr /C:"class TradingBot" src\main.py
   
   # Check DEBUG code
   findstr /C:"DEBUG-LOOP" src\main.py
   
   # Test import
   python -c "from src.main import TradingBot; print('OK')"
   ```

---

## 📌 Important Notes

1. **Cache Issues:** The most common problem is Python using cached .pyc files
   - Solution: Run COMPLETE_REINSTALL.bat

2. **Always Use -B Flag:** Prevents .pyc file creation
   ```batch
   python -B -m src.main --mode paper
   ```

3. **Backup Your .env:** Before any reinstall
   ```batch
   copy .env .env.backup
   ```

4. **Check Version:** After installation
   ```batch
   type VERSION.txt
   ```
   Should show: `v6.30.38-COMPLETE-REINSTALL-SYSTEM`

---

## 📞 Support

- **GitHub:** https://github.com/lee-jungkil/Lj
- **Issues:** https://github.com/lee-jungkil/Lj/issues
- **Current Version:** v6.30.38

---

**Last Updated:** 2026-02-14  
**Author:** lee-jungkil  
**License:** Check repository for details
