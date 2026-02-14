#!/bin/bash

echo "========================================"
echo "Batch File Verification Script"
echo "========================================"
echo ""

# Check encoding
echo "[1/4] Checking file encodings..."
for file in setup.bat RUN_PAPER_CLEAN.bat RUN_LIVE_CLEAN.bat; do
    encoding=$(file -b --mime-encoding "$file")
    if [[ "$encoding" == "us-ascii" || "$encoding" == "ascii" ]]; then
        echo "  ✓ $file: $encoding (OK)"
    else
        echo "  ✗ $file: $encoding (WRONG - should be ASCII)"
    fi
done
echo ""

# Check for Korean characters (UTF-8 bytes)
echo "[2/4] Checking for Korean characters..."
for file in setup.bat RUN_PAPER_CLEAN.bat RUN_LIVE_CLEAN.bat; do
    if grep -qP '[\x80-\xFF]' "$file"; then
        echo "  ✗ $file: Contains non-ASCII characters"
    else
        echo "  ✓ $file: Pure ASCII (OK)"
    fi
done
echo ""

# Check version strings
echo "[3/4] Checking version strings..."
for file in setup.bat RUN_PAPER_CLEAN.bat RUN_LIVE_CLEAN.bat; do
    version=$(grep -oP 'v\d+\.\d+\.\d+' "$file" | head -1)
    echo "  $file: $version"
done
echo ""

# Check for common batch file errors
echo "[4/4] Checking for syntax issues..."
for file in setup.bat RUN_PAPER_CLEAN.bat RUN_LIVE_CLEAN.bat; do
    # Check for 'cho' error (broken echo)
    if grep -q "^cho " "$file"; then
        echo "  ✗ $file: Contains 'cho' (broken echo command)"
    else
        echo "  ✓ $file: No 'cho' errors"
    fi
done
echo ""

echo "========================================"
echo "Verification Complete"
echo "========================================"
