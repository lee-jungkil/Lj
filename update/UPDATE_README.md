# UPDATE Guide - v6.16-SELLHISTORY

## How to Update (Windows)

### Method 1: Double-click (Recommended)
```
1. Navigate to: Lj-main\update\
2. Double-click: UPDATE.bat
3. Wait for completion
4. Done!
```

### Method 2: Command Prompt
```batch
cd Lj-main\update
UPDATE.bat
```

---

## What's Updated?

### v6.16-SELLHISTORY Features
- ✅ Screen scroll completely removed
- ✅ Profit/Loss sync improved  
- ✅ Risk management: auto-stop at -10% loss
- ✅ Debug output minimized
- ⭐ **NEW: Sell history permanent storage**
  - Keep up to 10 records
  - Display last 5 on screen
  - Persist like buy positions

---

## Troubleshooting

### Korean characters broken (한글 깨짐)
**Solution**: The UPDATE.bat file uses English for compatibility.
All functionality works the same!

### "File not found" error
**Cause**: Running from wrong directory
**Solution**: 
```batch
cd Lj-main
cd update
UPDATE.bat
```

### "Permission denied" error
**Solution 1**: Run Command Prompt as Administrator
```
Right-click Command Prompt → Run as Administrator
cd path\to\Lj-main\update
UPDATE.bat
```

**Solution 2**: Close Python processes
```
Task Manager → Find python.exe → End Task
```

### Update failed
**Rollback**: Backup files are in `backup\backup_YYYYMMDD_HHMMSS\`
```batch
copy backup\backup_*\fixed_screen_display.py.bak src\utils\fixed_screen_display.py
```

---

## After Update

### Run the Bot
```batch
# Backtest mode
run.bat

# Paper trading (recommended for testing)
run_paper.bat

# Live trading
run_live.bat
```

### Verify Update
Check screen header shows: **v6.16-SELLHISTORY**

### Test Sell History
1. Buy → Sell a position
2. Check "📜 매도 기록" section at bottom
3. Verify records persist (don't disappear after 5 seconds)

---

## Files Changed
- `src/utils/fixed_screen_display.py` (main update)

## Backup Location
`backup/backup_YYYYMMDD_HHMMSS/`

---

## Need Help?
GitHub: https://github.com/lee-jungkil/Lj/issues

---

**Update completed! Sell records now persist like buy positions!** 🎉
