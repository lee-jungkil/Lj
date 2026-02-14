#!/bin/bash

echo "=========================================="
echo "Batch File Execution Test"
echo "=========================================="
echo ""

# Test 1: Check for exit commands that skip pause
echo "[Test 1] Checking for problematic exit commands..."
for file in setup.bat RUN_PAPER_CLEAN.bat RUN_LIVE_CLEAN.bat; do
    # Count exit /b commands
    exit_count=$(grep -c "exit /b" "$file" || echo "0")
    # Count goto :END commands (safe)
    goto_count=$(grep -c "goto :END" "$file" || echo "0")
    # Check if :END label exists
    end_label=$(grep -c "^:END" "$file" || echo "0")
    
    echo "  $file:"
    echo "    exit /b commands: $exit_count"
    echo "    goto :END commands: $goto_count"
    echo "    :END label: $end_label"
    
    if [ "$exit_count" -eq 0 ] || [ "$goto_count" -gt 0 ]; then
        echo "    Status: OK (uses goto or no exit)"
    else
        echo "    Status: WARNING (may skip pause)"
    fi
    echo ""
done

# Test 2: Check pause commands
echo "[Test 2] Checking pause commands..."
for file in setup.bat RUN_PAPER_CLEAN.bat RUN_LIVE_CLEAN.bat; do
    pause_count=$(grep -c "^pause" "$file" || echo "0")
    echo "  $file: $pause_count pause command(s)"
done
echo ""

# Test 3: Simulate Windows batch execution logic
echo "[Test 3] Simulating batch file flow..."
echo "  Checking if pause is reachable in all paths..."
for file in setup.bat RUN_PAPER_CLEAN.bat RUN_LIVE_CLEAN.bat; do
    echo "  $file:"
    # Check if pause comes after goto :END label
    if grep -q "^:END" "$file"; then
        # Check if pause is before :END
        line_pause=$(grep -n "^pause" "$file" | head -1 | cut -d: -f1)
        line_end=$(grep -n "^:END" "$file" | head -1 | cut -d: -f1)
        if [ "$line_pause" -lt "$line_end" ]; then
            echo "    pause is BEFORE :END label - GOOD"
        else
            echo "    pause is AFTER :END label - BAD"
        fi
    else
        echo "    No :END label, checking for exit /b before pause..."
        if grep -B 50 "^pause" "$file" | grep -q "exit /b"; then
            echo "    exit /b found before pause - MAY SKIP PAUSE"
        else
            echo "    No exit /b before pause - OK"
        fi
    fi
done
echo ""

echo "=========================================="
echo "Test Complete"
echo "=========================================="
