"""
Display improvements v6.30.69
- Remove DEBUG logs
- Add 10-minute screen clear
- Expand work status display (5 lines)
- Increase sell history to 10
- Real-time position update only
"""

import re

def apply_improvements():
    """Apply all display improvements"""
    
    print("Applying display improvements v6.30.69...")
    
    # 1. Remove DEBUG and EXECUTE-SELL logs from main.py
    print("\n[1/5] Removing DEBUG logs...")
    with open('src/main.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove DEBUG prints
    content = re.sub(r'\s*_original_print\(f?\[DEBUG[^\)]*\)\)\n?', '', content)
    
    # Remove EXECUTE-SELL logs (keep only important ones)
    lines_to_keep = [
        'execute_sell() 호출됨',
        '포지션 찾음',
        '모의거래 모드: 포지션 전체 매도 허용',
        '포지션 청산 시작',
        '포지션 청산 완료'
    ]
    
    content_lines = content.split('\n')
    filtered_lines = []
    for line in content_lines:
        if '_original_print' in line and '[EXECUTE-SELL]' in line:
            # Keep only important logs
            if any(keyword in line for keyword in lines_to_keep):
                filtered_lines.append(line)
        else:
            filtered_lines.append(line)
    
    content = '\n'.join(filtered_lines)
    
    with open('src/main.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("   ✓ Removed DEBUG and verbose EXECUTE-SELL logs")
    
    # 2. Add 10-minute screen clear to main.py
    print("\n[2/5] Adding 10-minute screen clear...")
    with open('src/main.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the main loop and add screen clear logic
    if 'self.last_screen_clear_time' not in content:
        # Add initialization
        init_pattern = r'(self\.last_surge_scan_time = time\.time\(\))'
        init_replacement = r'\1\n        self.last_screen_clear_time = time.time()  # ⭐ v6.30.69: 화면 클리어'
        content = re.sub(init_pattern, init_replacement, content)
        
        # Add clear logic in main loop
        loop_pattern = r'(# ⭐ PHASE 1: 전체 스캔.*?\n.*?if current_time - self\.last_full_scan_time.*?:)'
        loop_replacement = r'''# ⭐ 10분마다 화면 클리어 (v6.30.69)
                if current_time - self.last_screen_clear_time >= 600:  # 10분 = 600초
                    os.system('cls' if os.name == 'nt' else 'clear')
                    self.display.render()
                    self.last_screen_clear_time = current_time
                
                \1'''
        content = re.sub(loop_pattern, loop_replacement, content, flags=re.DOTALL)
    
    with open('src/main.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("   ✓ Added 10-minute screen clear")
    
    # 3. Expand work status display to 5 lines
    print("\n[3/5] Expanding work status display...")
    with open('src/utils/fixed_screen_display.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update monitor lines count
    content = re.sub(
        r'self\.monitor_line3 = ""',
        '''self.monitor_line3 = ""
        self.monitor_line4 = ""  # ⭐ v6.30.69
        self.monitor_line5 = ""  # ⭐ v6.30.69''',
        content
    )
    
    # Update render method to show 5 lines
    content = re.sub(
        r'(if self\.monitor_line3:.*?self\.print_line\(self\.monitor_line3\))',
        r'''\1
            if self.monitor_line4:  # ⭐ v6.30.69
                self.print_line(self.monitor_line4)
            if self.monitor_line5:  # ⭐ v6.30.69
                self.print_line(self.monitor_line5)''',
        content,
        flags=re.DOTALL
    )
    
    with open('src/utils/fixed_screen_display.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("   ✓ Expanded work status to 5 lines")
    
    # 4. Increase sell history to 10
    print("\n[4/5] Increasing sell history to 10...")
    with open('src/utils/fixed_screen_display.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = re.sub(
        r'self\.max_sell_history = \d+',
        'self.max_sell_history = 10  # ⭐ v6.30.69',
        content
    )
    
    with open('src/utils/fixed_screen_display.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("   ✓ Increased sell history to 10")
    
    # 5. Add real-time position update method
    print("\n[5/5] Adding real-time position update...")
    with open('src/utils/fixed_screen_display.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add new method for position-only update
    if 'def update_position_only' not in content:
        method_code = '''
    def update_position_only(self, slot: int, ticker: str, entry_price: float, 
                            current_price: float, amount: float, investment: float,
                            strategy: str, hold_time: int, sell_reason: str = ""):
        """
        포지션 정보만 실시간 업데이트 (화면 전체 리렌더 없이)
        
        Args:
            slot: 슬롯 번호
            ticker: 티커
            entry_price: 진입 가격
            current_price: 현재 가격
            amount: 수량
            investment: 투자금
            strategy: 전략명
            hold_time: 보유 시간 (초)
            sell_reason: 매도 사유 (있으면 표시)
        """
        # Calculate profit/loss
        current_value = amount * current_price
        profit_loss = current_value - investment
        profit_ratio = (profit_loss / investment) * 100 if investment > 0 else 0
        
        # Format hold time
        hours = hold_time // 3600
        minutes = (hold_time % 3600) // 60
        seconds = hold_time % 60
        
        if hours > 0:
            hold_display = f"{hours}시간{minutes}분"
        elif minutes > 0:
            hold_display = f"{minutes}분{seconds}초"
        else:
            hold_display = f"{seconds}초"
        
        # Determine emoji and color
        if profit_ratio > 0:
            emoji = "📈"
            profit_color = Fore.GREEN
        elif profit_ratio < 0:
            emoji = "📉"
            profit_color = Fore.RED
        else:
            emoji = "⚠️"
            profit_color = Fore.YELLOW
        
        # Extract coin name
        coin = ticker.replace('KRW-', '')[:8]
        
        # Build strategy display
        strategy_display = {
            'AggressiveScalping': '⚡스캘핑',
            'ConservativeScalping': '🛡️보수',
            'ULTRA_SCALPING': '🔥초단타',
            'ultra_scalping': '🔥초단타',
            'chase': '🏃추격',
        }.get(strategy, strategy[:6])
        
        # Build sell reason display
        sell_display = ""
        if sell_reason:
            if '손절' in sell_reason:
                sell_display = f" → {Fore.RED}손절{Style.RESET_ALL}"
            elif '익절' in sell_reason or 'take_profit' in sell_reason.lower():
                sell_display = f" → {Fore.GREEN}익절{Style.RESET_ALL}"
            elif '시간' in sell_reason or 'time' in sell_reason.lower():
                sell_display = f" → {Fore.YELLOW}시간{Style.RESET_ALL}"
            elif 'AI' in sell_reason or '학습' in sell_reason:
                sell_display = f" → {Fore.CYAN}AI{Style.RESET_ALL}"
            else:
                sell_display = f" → {sell_reason[:6]}"
        
        # Move cursor to position line
        position_line = 15 + slot  # Adjust based on your layout
        sys.stdout.write(f"\\033[{position_line};0H")  # Move to line
        sys.stdout.write("\\033[K")  # Clear line
        
        # Print updated position
        line = (
            f"{' ' * self.left_margin}"
            f"  {emoji} 슬롯{slot} │ {Fore.CYAN}{Style.BRIGHT}{coin:8s}{Style.RESET_ALL} │ "
            f"매수:{strategy_display}{sell_display} "
            f"│ 투자: {investment:,.0f}원 → 현재: {current_value:,.0f}원, "
            f"진입: {entry_price:.2f}원 → 현재: {current_price:.2f}원 "
            f"│ 손익: {profit_color}{profit_loss:+,.0f}원 ({profit_ratio:+.2f}%){Style.RESET_ALL} "
            f"│ 보유: {hold_display}"
        )
        
        sys.stdout.write(line)
        sys.stdout.flush()
'''
        
        # Insert before the last method
        content = content.replace(
            '    def is_slot_available',
            method_code + '\n    def is_slot_available'
        )
    
    with open('src/utils/fixed_screen_display.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("   ✓ Added real-time position update method")
    
    # Update VERSION.txt
    print("\n[6/6] Updating version...")
    with open('VERSION.txt', 'w', encoding='utf-8') as f:
        f.write('v6.30.69-DISPLAY-IMPROVEMENTS\n')
    
    print("   ✓ Updated version to v6.30.69")
    
    print("\n" + "="*50)
    print("✅ All improvements applied successfully!")
    print("="*50)
    print("\nChanges:")
    print("  1. ✓ Removed DEBUG and verbose logs")
    print("  2. ✓ Added 10-minute screen clear")
    print("  3. ✓ Expanded work status to 5 lines")
    print("  4. ✓ Increased sell history to 10")
    print("  5. ✓ Added real-time position update")
    print("\nNext steps:")
    print("  1. Stop the bot (Ctrl+C)")
    print("  2. Clear cache: del /s /q *.pyc")
    print("  3. Restart: python -B -u -m src.main --mode paper")
    print()

if __name__ == '__main__':
    try:
        apply_improvements()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
