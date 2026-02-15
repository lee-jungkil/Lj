# TROUBLESHOOTING GUIDE - Sell Order Not Executing

## Problem Description
- Bot shows position for 75+ minutes
- Logs show "[FORCE-SELL] Order completed" but position remains
- NO "[EXECUTE-SELL]" logs appear
- Sell count does not increase

## Root Cause
**Python Cache Issue**: The bot is executing OLD compiled bytecode (.pyc files) instead of the new code.

---

## SOLUTION 1: Emergency Cache Clear (RECOMMENDED)

### Step 1: Run Emergency Fix
```batch
EMERGENCY_FIX_SIMPLE.bat
```

This will:
1. Stop all Python processes
2. Delete ALL .pyc files
3. Delete ALL __pycache__ folders
4. Verify cache is gone

### Step 2: Start Bot with -B Flag
```batch
python -B -u -m src.main --mode paper
```

The `-B` flag prevents Python from creating new cache files.

### Step 3: Verify Success
Look for these logs:
```
[EXECUTE-SELL] execute_sell() called - ticker: KRW-AAVE
[EXECUTE-SELL] ========== Position cleanup start ==========
[EXECUTE-SELL] holding_protector.close_bot_position() called...
[EXECUTE-SELL] ✅ holding_protector cleanup complete
[EXECUTE-SELL] risk_manager.close_position() called...
[EXECUTE-SELL] ✅ risk_manager cleanup complete
```

---

## SOLUTION 2: Complete Reinstall

If Solution 1 doesn't work, do a complete reinstall:

### Step 1: Download Fresh Code
https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip

### Step 2: Extract to New Folder
Extract to: `C:\Lj-v6.30.62\`

### Step 3: Copy Your Config
```batch
copy "C:\Users\admin\Downloads\Lj-main\.env" "C:\Lj-v6.30.62\.env"
```

### Step 4: Run Complete Reinstall
```batch
cd C:\Lj-v6.30.62
COMPLETE_REINSTALL.bat
```

---

## SOLUTION 3: Manual Fix (if batch files fail)

### Step 1: Stop Python
Open Command Prompt as Administrator:
```batch
taskkill /F /IM python.exe /T
taskkill /F /IM pythonw.exe /T
```

### Step 2: Delete Cache Manually
```batch
cd C:\Users\admin\Downloads\Lj-main

del /s /q *.pyc
for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"

rd /s /q src\__pycache__
rd /s /q src\ai\__pycache__
rd /s /q src\strategies\__pycache__
rd /s /q src\utils\__pycache__
```

### Step 3: Verify Cache is Gone
```batch
dir /s /b src\__pycache__
```
Should show: "File Not Found"

### Step 4: Start Bot
```batch
python -B -u -m src.main --mode paper
```

---

## Verification Checklist

After applying the fix, verify:

✅ **VERSION.txt** shows: `v6.30.62-NO-CHCP-ASCII-ONLY`

✅ **No __pycache__** exists:
```batch
dir /s /b src\__pycache__
```
Should show "File Not Found"

✅ **Logs show [EXECUTE-SELL]**:
```
[EXECUTE-SELL] execute_sell() called
[EXECUTE-SELL] cleanup start
[EXECUTE-SELL] protector called
```

✅ **Position disappears** after 4-8 minutes

✅ **Sell count increases** in the UI

---

## Still Not Working?

### Run Diagnostic Check
```batch
DIAGNOSTIC_CHECK.bat
```

This will show:
- Current version
- Whether cache exists
- Whether debug logs are in code
- Whether Python is running
- File sizes and timestamps

### If Diagnostic Shows Cache Exists
1. Reboot your PC
2. Run `EMERGENCY_FIX_SIMPLE.bat` again
3. Start bot with `-B` flag

### If Diagnostic Shows Old Code
1. Download fresh ZIP from GitHub
2. Extract to new folder
3. Run `COMPLETE_REINSTALL.bat`

---

## Understanding the Logs

### ✅ SUCCESS - Sell Working
```
[EXECUTE-SELL] execute_sell() called - ticker: KRW-AAVE
[EXECUTE-SELL] Position exists: True
[EXECUTE-SELL] ✅ Found position: KRW-AAVE, amount: 60.6
[EXECUTE-SELL] ========== Position cleanup start ==========
[EXECUTE-SELL] holding_protector.close_bot_position() called...
[EXECUTE-SELL] ✅ holding_protector cleanup complete, P/L: +84
[EXECUTE-SELL] risk_manager.close_position() called...
[EXECUTE-SELL] ✅ risk_manager cleanup complete, P/L: +84
[EXECUTE-SELL] ========== UI update start ==========
[EXECUTE-SELL] ✅ Position removed from UI
```

### ❌ FAILURE - Old Cache Running
```
[FORCE-SELL] ✅ Sell order completed!
```
(No [EXECUTE-SELL] logs appear)

---

## Prevention - Avoid Future Issues

### Always Use -B Flag
```batch
python -B -u -m src.main --mode paper
```

### Create a Clean Start Script
Save as `START_CLEAN.bat`:
```batch
@echo off
taskkill /F /IM python.exe 2>nul
del /s /q *.pyc 2>nul
for /d /r . %%d in (__pycache__) do @rd /s /q "%%d" 2>nul
python -B -u -m src.main --mode paper
pause
```

### After Every Code Update
1. Stop bot (Ctrl+C)
2. Run `EMERGENCY_FIX_SIMPLE.bat`
3. Start bot with `-B` flag

---

## Download Links

- **Latest Code (ZIP)**: https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip
- **Repository**: https://github.com/lee-jungkil/Lj
- **Issues Page**: https://github.com/lee-jungkil/Lj/issues

---

## Contact Support

If none of these solutions work:

1. Run `DIAGNOSTIC_CHECK.bat`
2. Take screenshot of the output
3. Take screenshot of bot startup logs (first 50 lines)
4. Take screenshot of any position held >10 minutes
5. Post to: https://github.com/lee-jungkil/Lj/issues

Include:
- VERSION.txt content
- Whether cache exists (from diagnostic)
- Whether [EXECUTE-SELL] appears in logs
- Operating system version
- Python version

---

**Last Updated**: 2026-02-15  
**Version**: v6.30.62-NO-CHCP-ASCII-ONLY
