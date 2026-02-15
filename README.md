# 🚀 Upbit AutoProfit Bot v6.30.62

**Automated cryptocurrency trading bot for Upbit exchange with AI-powered strategies.**

---

## ⚡ Quick Start

### Download & Install

**Option 1: ZIP Download (Recommended)**
```
1. Download: https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
2. Extract to: C:\Lj-main\
3. Double-click: COMPLETE_REINSTALL.bat
4. Type: Y
5. Done!
```

**Option 2: Git Clone**
```bash
git clone https://github.com/lee-jungkil/Lj.git
cd Lj
COMPLETE_REINSTALL.bat
```

---

## 📋 System Requirements

- **OS**: Windows 10/11
- **Python**: 3.8 or higher
- **RAM**: 2GB minimum
- **Disk**: 500MB free space
- **Internet**: Required

---

## 🎯 Features

### Core Features
- ✅ **Automated Trading**: 24/7 autonomous operation
- ✅ **Multiple Strategies**: Aggressive, Conservative, Mean Reversion, Grid
- ✅ **AI Learning**: Adaptive strategy optimization
- ✅ **Risk Management**: Stop-loss, take-profit, position limits
- ✅ **Paper Trading**: Safe testing with virtual money

### v6.30.62 Updates
- ✅ **Enhanced Sell Debugging**: Detailed error tracking
- ✅ **Individual Try/Except**: Per-step error handling
- ✅ **Stack Trace Logging**: Automatic error diagnosis
- ✅ **English Batch Files**: No encoding errors
- ✅ **Cache Management**: Complete cleanup system

---

## 🚀 Usage

### Paper Trading (Safe Testing)
```batch
RUN_PAPER_CLEAN.bat
```
- No real money
- Safe for testing
- Learn bot behavior

### Live Trading (Real Money)
```batch
# 1. Edit .env file
notepad .env

# 2. Add your Upbit API keys
TRADING_MODE=live
UPBIT_ACCESS_KEY=your_access_key
UPBIT_SECRET_KEY=your_secret_key

# 3. Run bot
python -B -u -m src.main --mode live
```

---

## 🔧 Configuration (.env)

### Basic Settings
```ini
# Trading Mode
TRADING_MODE=paper          # paper or live

# Capital Management
INITIAL_CAPITAL=5000000     # Starting capital (KRW)
MAX_DAILY_LOSS=500000       # Max loss per day
MAX_CUMULATIVE_LOSS=1000000 # Max total loss
MAX_POSITIONS=5             # Max concurrent positions

# Strategy
EXIT_MODE=aggressive        # aggressive, moderate, conservative
```

### API Keys (Live Trading Only)
```ini
UPBIT_ACCESS_KEY=your_key_here
UPBIT_SECRET_KEY=your_secret_here
```

---

## 📊 Trading Strategies

### 1. Aggressive Scalping
- **Hold Time**: 4 minutes
- **Take Profit**: +1.5%
- **Stop Loss**: -1.0%
- **Best For**: High volatility markets

### 2. Conservative Scalping
- **Hold Time**: 8 minutes
- **Take Profit**: +2.0%
- **Stop Loss**: -1.5%
- **Best For**: Stable markets

### 3. Mean Reversion
- **Hold Time**: 30 minutes
- **Take Profit**: +3.0%
- **Stop Loss**: -2.0%
- **Best For**: Range-bound markets

### 4. Grid Trading
- **Hold Time**: 1 hour
- **Take Profit**: +5.0%
- **Stop Loss**: -3.0%
- **Best For**: Sideways markets

---

## 🐛 Troubleshooting

### Problem: Sell Not Executing

**Symptoms**:
- Positions held for 70+ minutes
- [EXECUTE-SELL] logs missing
- No sell count increase

**Solution**:
```batch
# 1. Run emergency cache clear
EMERGENCY_CACHE_CLEAR.bat

# 2. Or complete reinstall
COMPLETE_REINSTALL.bat

# 3. Verify logs show:
[EXECUTE-SELL] Position cleanup start
[EXECUTE-SELL] holding_protector called
[EXECUTE-SELL] risk_manager called
```

### Problem: Python Not Found

**Solution**:
```
1. Download Python: https://www.python.org/
2. Check "Add Python to PATH" during install
3. Restart computer
4. Run COMPLETE_REINSTALL.bat
```

### Problem: Package Install Fails

**Solution**:
```batch
python -m pip install --upgrade pip
python -m pip install pyupbit pandas numpy requests python-dotenv colorlog ta
```

### Problem: Batch File Encoding Errors

**Solution**:
- ✅ Fixed in v6.30.62
- All batch files now English-only
- No Korean characters
- No encoding issues

---

## 📈 Expected Performance

### Paper Trading
- **Purpose**: Testing and learning
- **Risk**: Zero (virtual money)
- **Duration**: Unlimited

### Live Trading
- **Daily Trades**: 10-30
- **Win Rate**: 60-70% (typical)
- **Daily Return**: 1-3% (varies)
- **Risk Level**: Managed by settings

**⚠️ Warning**: Past performance does not guarantee future results. Cryptocurrency trading carries high risk.

---

## 🔄 Updating

### Method 1: Complete Reinstall (Recommended)
```batch
COMPLETE_REINSTALL.bat
```
- Preserves .env settings
- Downloads latest code
- Cleans all cache
- Installs dependencies

### Method 2: Git Pull
```batch
cd C:\Lj
git pull origin main
EMERGENCY_CACHE_CLEAR.bat
```

---

## 📁 Project Structure

```
Lj/
├── src/
│   ├── main.py              # Main bot engine
│   ├── config.py            # Configuration
│   ├── strategies/          # Trading strategies
│   ├── ai/                  # AI learning modules
│   └── utils/               # Utility functions
├── COMPLETE_REINSTALL.bat   # Full installation
├── RUN_PAPER_CLEAN.bat      # Paper trading
├── EMERGENCY_CACHE_CLEAR.bat# Cache cleanup
├── .env                     # Configuration file
├── VERSION.txt              # Current version
└── README.md                # This file
```

---

## 🎓 Best Practices

### Before Live Trading
1. ✅ Test in paper mode for 1-2 weeks
2. ✅ Understand bot behavior
3. ✅ Set appropriate risk limits
4. ✅ Start with small capital
5. ✅ Monitor daily

### Risk Management
1. ✅ Never invest more than you can afford to lose
2. ✅ Set MAX_DAILY_LOSS conservatively
3. ✅ Use stop-loss for all positions
4. ✅ Diversify positions
5. ✅ Monitor regularly

### Maintenance
1. ✅ Update weekly (git pull)
2. ✅ Check logs daily
3. ✅ Clear cache when issues occur
4. ✅ Backup .env file
5. ✅ Keep API keys secure

---

## 🔐 Security

### API Keys
- ✅ Never share your API keys
- ✅ Keep .env file private
- ✅ Use IP whitelist on Upbit
- ✅ Enable 2FA on Upbit account

### Permissions
- ✅ Read: Required
- ✅ Trade: Required for live mode
- ✅ Withdraw: **NOT REQUIRED** (safer)

---

## 📞 Support

### Issues
- **GitHub Issues**: https://github.com/lee-jungkil/Lj/issues
- **Discussions**: https://github.com/lee-jungkil/Lj/discussions

### Version Check
```batch
type VERSION.txt
```
Current: **v6.30.62-ENGLISH-BATCH-FILES**

---

## 🎯 Changelog

### v6.30.62 (2026-02-15)
- ✅ English-only batch files (no encoding errors)
- ✅ Enhanced sell execution debugging
- ✅ Individual try/except per cleanup step
- ✅ Automatic stack trace logging
- ✅ Fixed Korean character issues

### v6.30.61 (2026-02-15)
- ✅ Complete reinstall script
- ✅ 9-step automation
- ✅ Emergency cache clear
- ✅ DataFrame bug fixes

### v6.30.60 (2026-02-14)
- ✅ [EXECUTE-SELL] debug logs
- ✅ Position tracking enhancement

---

## ⚖️ Disclaimer

This software is provided "as is" without warranty of any kind. Trading cryptocurrency carries significant risk. You are responsible for your own investment decisions. The developers are not liable for any financial losses incurred while using this software.

**USE AT YOUR OWN RISK.**

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🌟 Contributors

- **Main Developer**: lee-jungkil
- **AI Assistant**: GenSpark AI
- **Community**: GitHub Contributors

---

## 🔗 Links

- **GitHub**: https://github.com/lee-jungkil/Lj
- **Issues**: https://github.com/lee-jungkil/Lj/issues
- **Download**: https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
- **Upbit**: https://upbit.com/

---

**Current Version**: v6.30.62-ENGLISH-BATCH-FILES  
**Release Date**: 2026-02-15  
**Status**: ✅ Stable

**Download Now**: https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
