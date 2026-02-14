# Obsolete Batch Files (v5.x)

## Why These Files Are Here

These batch files are **obsolete versions (v5.x)** that have been replaced by newer, more stable versions in v6.30.25.

**Date Moved**: 2026-02-14  
**Reason**: Encoding issues (UTF-8 with Korean characters) and outdated functionality

---

## Files in This Directory

### Replaced by New CLEAN Versions

1. **run_paper.bat** (v5.2)
   - **Replaced by**: `RUN_PAPER_CLEAN.bat` (v6.30.25)
   - **Why replaced**: No Python cache cleaning, encoding issues, old version

2. **run_live.bat** (v5.2)
   - **Replaced by**: `RUN_LIVE_CLEAN.bat` (v6.30.25)
   - **Why replaced**: No Python cache cleaning, encoding issues, old version

3. **run_backtest.bat** (v5.2)
   - **Replaced by**: None yet
   - **Status**: Obsolete, backtest mode can be run with: `python -m src.main --mode backtest`

4. **run.bat** (v5.x, lowercase)
   - **Replaced by**: `RUN.bat` (v6.30.x, uppercase)
   - **Why replaced**: Naming convention change

### Utility Files (Obsolete)

5. **run_test.bat** (v5.2)
   - **Status**: Test mode obsolete
   
6. **run_dynamic.bat** (v5.3)
   - **Status**: Dynamic coin selection obsolete

7. **change_coin_count.bat** (v5.x)
   - **Status**: Functionality moved to config

8. **fix_logs.bat** (v5.x)
   - **Status**: No longer needed

9. **test_install.bat** (v5.x)
   - **Status**: Replaced by `setup.bat` (v6.30.25)

10. **verify_setup.bat** (v5.x)
    - **Status**: Functionality included in `setup.bat`

---

## Should You Use These Files?

**❌ NO!** Do not use these files.

**Problems with these files**:
- ✗ Old version (v5.x)
- ✗ UTF-8 encoding issues
- ✗ No Python cache cleaning
- ✗ Window closing bugs
- ✗ Korean character encoding errors

---

## What Should You Use Instead?

### Current Version: v6.30.25

**For setup**:
```batch
setup.bat
```

**For paper trading (recommended)**:
```batch
RUN_PAPER_CLEAN.bat
```

**For live trading (real money)**:
```batch
RUN_LIVE_CLEAN.bat
```

**For updates**:
```batch
QUICK_UPDATE.bat
UPDATE.bat
```

---

## Can These Files Be Deleted?

**Yes, they can be safely deleted.**

They are kept here for reference only. If you need to free up disk space, you can delete this entire `old_batch_files/` directory:

```batch
cd C:\Users\admin\Downloads\Lj-main\Lj-main
rmdir /s /q old_batch_files
```

---

## Migration Guide

If you were using old batch files:

### Before (v5.x)
```batch
run_paper.bat     ← OLD, don't use
run_live.bat      ← OLD, don't use
```

### After (v6.30.25)
```batch
RUN_PAPER_CLEAN.bat    ← NEW, use this
RUN_LIVE_CLEAN.bat     ← NEW, use this
```

---

## Key Improvements in v6.30.25

1. ✅ **ASCII Encoding**: Pure ASCII, no encoding errors
2. ✅ **Python Cache Cleaning**: Automatic cache cleanup
3. ✅ **Window Stays Open**: Always shows errors
4. ✅ **Version Display**: Shows v6.30.25
5. ✅ **English Messages**: Universal compatibility

---

**Last Updated**: 2026-02-14  
**Version**: v6.30.25-BATCH-ENCODING-FIX
