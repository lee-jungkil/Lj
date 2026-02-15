# QUICK FIX - Sell Not Working

## 🚨 PROBLEM
- Position stuck for 75+ minutes
- Logs show "[FORCE-SELL] completed" but position remains
- NO "[EXECUTE-SELL]" logs

## ✅ SOLUTION (3 STEPS)

### Step 1: Download Latest Code
Click here to download:
**https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip**

### Step 2: Extract and Copy Config
1. Extract ZIP to: `C:\Lj-FIXED\`
2. Copy your `.env` file:
   ```batch
   copy "C:\Users\admin\Downloads\Lj-main\.env" "C:\Lj-FIXED\.env"
   ```

### Step 3: Run Fix Script
```batch
cd C:\Lj-FIXED
EMERGENCY_FIX_SIMPLE.bat
```

Then start bot:
```batch
python -B -u -m src.main --mode paper
```

---

## ✅ SUCCESS CHECK

You should see these logs:
```
[EXECUTE-SELL] execute_sell() called - ticker: KRW-XXX
[EXECUTE-SELL] cleanup start
[EXECUTE-SELL] protector called
[EXECUTE-SELL] ✅ cleanup complete
```

Position should disappear within 4-8 minutes.
Sell count should increase.

---

## ❌ STILL NOT WORKING?

Run diagnostic:
```batch
DIAGNOSTIC_CHECK.bat
```

Or read full guide:
**TROUBLESHOOTING_ENGLISH.md**

---

## 📞 SUPPORT

GitHub Issues: https://github.com/lee-jungkil/Lj/issues

Include:
- Screenshot of `DIAGNOSTIC_CHECK.bat` output
- Screenshot of bot startup logs
- VERSION.txt content

---

**Version**: v6.30.63-DIAGNOSTIC-TOOLS  
**Updated**: 2026-02-15
