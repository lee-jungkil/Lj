"""
Remove DEBUG logs from main.py v6.30.70
Removes all _original_print statements containing [DEBUG]
"""

import re

def remove_debug_logs():
    """Remove all DEBUG log statements from main.py"""
    
    print("="*60)
    print("  DEBUG Log Removal Tool v6.30.70")
    print("="*60)
    print()
    
    # Read main.py
    print("[1/3] Reading src/main.py...")
    with open('src/main.py', 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    original_line_count = len(lines)
    print(f"      Total lines: {original_line_count}")
    
    # Find DEBUG lines
    debug_lines = [i for i, line in enumerate(lines) if '_original_print' in line and '[DEBUG' in line]
    print(f"      DEBUG lines found: {len(debug_lines)}")
    
    if not debug_lines:
        print("\n✓ No DEBUG logs found. Already clean!")
        return
    
    # Show examples
    print("\n      Examples of DEBUG logs to remove:")
    for i in debug_lines[:3]:
        preview = lines[i].strip()[:80]
        print(f"        Line {i+1}: {preview}...")
    if len(debug_lines) > 3:
        print(f"        ... and {len(debug_lines)-3} more")
    
    # Remove DEBUG lines
    print("\n[2/3] Removing DEBUG logs...")
    filtered_lines = []
    removed_count = 0
    
    for i, line in enumerate(lines):
        # Skip lines with DEBUG
        if '_original_print' in line and '[DEBUG' in line:
            removed_count += 1
            continue
        filtered_lines.append(line)
    
    new_content = '\n'.join(filtered_lines)
    
    print(f"      Removed: {removed_count} lines")
    print(f"      Remaining: {len(filtered_lines)} lines")
    
    # Write back
    print("\n[3/3] Writing changes...")
    with open('src/main.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("      ✓ File updated")
    
    # Update version
    with open('VERSION.txt', 'w', encoding='utf-8') as f:
        f.write('v6.30.70-NO-DEBUG\n')
    
    print("\n" + "="*60)
    print("  ✅ DEBUG logs removed successfully!")
    print("="*60)
    print()
    print(f"  Removed: {removed_count} DEBUG log lines")
    print(f"  Clean output: No more [DEBUG] messages")
    print()
    print("  Next steps:")
    print("    1. Stop the bot (Ctrl+C)")
    print("    2. Clear cache: del /s /q *.pyc")
    print("    3. Restart: python -B -u -m src.main --mode paper")
    print()
    print("="*60)

if __name__ == '__main__':
    try:
        remove_debug_logs()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
