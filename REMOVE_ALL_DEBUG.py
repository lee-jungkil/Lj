#!/usr/bin/env python3
"""
Remove All Debug Outputs v6.30.71
Removes all DEBUG, CHECK, verification related outputs
ASCII-safe version
"""
import os
import re

def remove_debug_outputs(file_path):
    """Remove all debug-related outputs"""
    print(f"Processing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    original_count = len(lines)
    new_lines = []
    removed_count = 0
    
    # Patterns to remove (ASCII-safe)
    remove_patterns = [
        r'_original_print\(.*?\[DEBUG.*?\)',       # [DEBUG-*] messages
        r'_original_print\(.*?check.*?\)',         # check related
        r'_original_print\(.*?verify.*?\)',        # verify related
        r'_original_print\(.*?CHECK.*?\)',         # CHECK related
        r'_original_print\(.*?position.*?check.*?\)',  # position check
        r'_original_print\(.*?liquidation.*?check.*?\)',  # liquidation check
        r'self\.logger\.log_info\(.*?check.*?\)',      # logger check
        r'self\.logger\.log_info\(.*?verify.*?\)',     # logger verify
        r'print\(.*?check.*?\)',                       # print check
        r'print\(.*?verify.*?\)',                      # print verify
    ]
    
    skip_next_line = False
    
    for i, line in enumerate(lines):
        # Skip if previous line set the flag
        if skip_next_line:
            skip_next_line = False
            removed_count += 1
            continue
        
        # Check patterns
        should_remove = False
        for pattern in remove_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                should_remove = True
                removed_count += 1
                
                # Handle multi-line function calls
                if line.rstrip().endswith('('):
                    skip_next_line = True
                break
        
        if not should_remove:
            new_lines.append(line)
    
    # Write file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    new_count = len(new_lines)
    
    return {
        'original': original_count,
        'new': new_count,
        'removed': removed_count
    }

def main():
    print("=" * 60)
    print("Remove All Debug Outputs Tool v6.30.71")
    print("=" * 60)
    
    files_to_process = [
        'src/main.py',
        'src/utils/fixed_screen_display.py'
    ]
    
    total_removed = 0
    
    for file_path in files_to_process:
        if not os.path.exists(file_path):
            print(f"[WARNING] File not found: {file_path}")
            continue
        
        result = remove_debug_outputs(file_path)
        total_removed += result['removed']
        
        print(f"[OK] {file_path}")
        print(f"   Original: {result['original']} lines")
        print(f"   Removed:  {result['removed']} lines")
        print(f"   Result:   {result['new']} lines")
        print()
    
    print("=" * 60)
    print(f"[OK] Total {total_removed} debug outputs removed!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Stop bot: Ctrl+C")
    print("2. Clear cache: del /s /q *.pyc")
    print("3. Restart: python -B -u -m src.main --mode paper")

if __name__ == '__main__':
    main()
