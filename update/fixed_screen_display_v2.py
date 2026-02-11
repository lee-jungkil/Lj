"""
고정 화면 표시 시스템 v6.16-TRADE-HISTORY
- 완전 고정 화면 (스크롤 제거)
- 디버그 출력 억제
- 손익 동기화 개선
- ⭐ 매도 기록 영구 보관 (최대 10개)
"""
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional
from colorama import init, Fore, Back, Style
import time
from collections import deque

# Windows 콘솔 ANSI 지원 활성화
if os.name == 'nt':
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

# Colorama 초기화
init(autoreset=True, strip=False)


class FixedScreenDisplay:
    """고정 화면 표시 시스템 v6.16-TRADE-HISTORY"""
    
    def __init__(self, max_positions: int = 7, max_trade_history: int = 10):
        """초기화"""
        self.max_positions = max_positions
        self.max_trade_history = max_trade_history  # ⭐ 최대 매도 기록 수
        
        self.positions = {}
        self.scan_status = "대기 중..."
        self.bot_status = "초기화 중..."
        self.market_summary = "시장 분석 중..."
        
        # AI 학습 상태
        self.ai_learning_count = 0
        self.ai_win_rate = 0.0
        self.ai_total_trades = 0
        self.ai_profit_trades = 0
        self.ai_loss_trades = 0
        
        # 자본금 및 손익 상태
        self.initial_capital = 0
        self.current_balance = 0
        self.total_profit = 0.0
        self.profit_ratio = 0.0
        
        # 진입 조건 상태
        self.market_phase = "분석 중"
        self.entry_condition = "기본"
        
        # 코인 요약
        self.coin_summary = "코인 시장 분석 중..."
        self.market_phase_reason = ""
        
        # 거래 통계
        self.buy_count = 0
        self.sell_count = 0
        
        # 스캔 시간 기록
        self.last_full_scan_time = None
        self.last_position_check_time = None
        self.last_surge_scan_time = None
        
        # 모니터링 상태
        self.monitor_line1 = "대기 중..."
        self.monitor_line2 = ""
        self.monitor_line3 = ""
        
        # ⭐ 매도 기록 (영구 보관)
        self.trade_history = deque(maxlen=max_trade_history)
        
        # ⭐ 화면 크기 설정
        try:
            terminal_size = os.get_terminal_size()
            terminal_width = terminal_size.columns
            terminal_height = terminal_size.rows
            
            self.screen_width = min(int(terminal_width * 0.8), 120)
            self.left_margin = (terminal_width - self.screen_width) // 2
            self.screen_height = terminal_height - 2
        except:
            self.screen_width = 96
            self.left_margin = 12
            self.screen_height = 40
        
        # ⭐ 첫 렌더링 플래그
        self._first_render = True
        
        # ⭐ 커서 숨기기
        if os.name == 'nt':
            try:
                sys.stdout.write('\033[?25l')
                sys.stdout.flush()
            except:
                pass
    
    def cleanup(self):
        """종료 시 정리"""
        try:
            sys.stdout.write('\033[?25h')  # 커서 표시
            sys.stdout.flush()
        except:
            pass
    
    def render(self):
        """전체 화면 렌더링 (완전 고정, 스크롤 제거)"""
        # ⭐ 터미널 크기 재계산
        try:
            terminal_size = os.get_terminal_size()
            terminal_width = terminal_size.columns
            terminal_height = terminal_size.rows
            self.screen_width = min(int(terminal_width * 0.8), 120)
            self.left_margin = max(0, (terminal_width - self.screen_width) // 2)
            self.screen_height = terminal_height - 2
        except:
            pass
        
        # ⭐ 첫 렌더링 시 화면 클리어
        if self._first_render:
            sys.stdout.write('\033[2J\033[H')
            sys.stdout.flush()
            self._first_render = False
        
        # ⭐ 모든 라인 생성
        output_lines = []
        margin = " " * self.left_margin
        
        # 헤더
        for line in self._render_header().split('\n'):
            output_lines.append(margin + line)
        output_lines.append(margin + "━" * self.screen_width)
        
        # 포지션
        for line in self._render_positions().split('\n'):
            output_lines.append(margin + line)
        output_lines.append(margin + "━" * self.screen_width)
        
        # ⭐ 매도 기록 (영구 표시)
        trade_history = self._render_trade_history()
        if trade_history:
            for line in trade_history.split('\n'):
                output_lines.append(margin + line)
            output_lines.append(margin + "━" * self.screen_width)
        
        # 스캔 상태
        for line in self._render_scan_status().split('\n'):
            output_lines.append(margin + line)
        output_lines.append(margin + "━" * self.screen_width)
        
        # 봇 상태
        output_lines.append(margin + self._render_bot_status())
        output_lines.append(margin + "━" * self.screen_width)
        
        # 모니터링
        for line in self._render_monitoring().split('\n'):
            output_lines.append(margin + line)
        output_lines.append(margin + "━" * self.screen_width)
        output_lines.append(margin)
        
        # ⭐ 고정 높이 제한
        if len(output_lines) > self.screen_height:
            output_lines = output_lines[:self.screen_height]
        
        # ⭐ 부족한 줄은 빈 줄로 채움
        while len(output_lines) < self.screen_height:
            output_lines.append(margin)
        
        # ⭐ 커서 홈으로 이동 후 덮어쓰기
        sys.stdout.write('\033[H')
        
        for i, line in enumerate(output_lines, start=1):
            sys.stdout.write('\033[2K')  # 현재 줄 지우기
            sys.stdout.write(line)
            
            if i < len(output_lines):
                sys.stdout.write('\n')
        
        sys.stdout.flush()
    
    def _render_header(self) -> str:
        """헤더 렌더링"""
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        title = "Upbit AutoProfit Bot v6.16-TRADE-HISTORY"
        
        ai_status = f"AI학습: {self.ai_learning_count}회 | 승률: {self.ai_win_rate:.1f}%"
        
        # ⭐ 손익 동기화 개선: initial_capital 기준 계산
        if self.initial_capital > 0:
            self.total_profit = self.current_balance - self.initial_capital
            self.profit_ratio = (self.total_profit / self.initial_capital) * 100
        
        profit_color = Fore.GREEN if self.total_profit >= 0 else Fore.RED
        capital_status = (
            f"자본: {self.current_balance:,.0f}원 | "
            f"{profit_color}손익: {self.total_profit:+,.0f}원 ({self.profit_ratio:+.2f}%){Style.RESET_ALL}"
        )
        
        return f"""{title} | 🕐 {now}
📊 {ai_status} | 자본: {self.initial_capital:,.0f}원 → {capital_status}"""
    
    def _render_positions(self) -> str:
        """포지션 렌더링"""
        if not self.positions:
            return f"[ 💼 보유 포지션 (0/{self.max_positions}) ]\n\n  대기 중... 매수 신호 분석 중"
        
        lines = [f"[ 💼 보유 포지션 ({len(self.positions)}/{self.max_positions}) ]", ""]
        
        for slot in sorted(self.positions.keys()):
            pos = self.positions[slot]
            ticker = pos.get('ticker', 'UNKNOWN')
            profit_loss = pos.get('profit_loss', 0.0)
            profit_ratio = pos.get('profit_ratio', 0.0)
            
            color = Fore.GREEN if profit_loss >= 0 else Fore.RED
            emoji = "🟢" if profit_loss >= 0 else "🔴"
            
            # 4줄 상세 정보
            investment = pos.get('investment', 0.0)
            current_value = pos.get('current_value', 0.0)
            entry_price = pos.get('entry_price', 0.0)
            current_price = pos.get('current_price', 0.0)
            hold_time = pos.get('hold_time', '0분')
            strategy = pos.get('strategy', 'unknown')
            
            lines.extend([
                f"#{slot} {ticker} | {color}{emoji} {profit_ratio:+.2f}% ({profit_loss:+,.0f}원){Style.RESET_ALL}",
                f"   투자: {investment:,.0f}원 → 현재: {current_value:,.0f}원",
                f"   진입: {entry_price:,.0f}원 | 현재: {current_price:,.0f}원",
                f"   보유: {hold_time} | 전략: {strategy}",
                ""
            ])
        
        return '\n'.join(lines)
    
    def _render_trade_history(self) -> Optional[str]:
        """⭐ 매도 기록 렌더링 (영구 표시)"""
        if not self.trade_history:
            return None
        
        lines = [f"[ 📜 매도 기록 ({len(self.trade_history)}/{self.max_trade_history}) ]", ""]
        
        # 최근 매도부터 표시 (역순)
        for idx, trade in enumerate(reversed(list(self.trade_history)), start=1):
            ticker = trade.get('ticker', 'UNKNOWN')
            profit_loss = trade.get('profit_loss', 0.0)
            profit_ratio = trade.get('profit_ratio', 0.0)
            strategy = trade.get('strategy', 'unknown')
            hold_time = trade.get('hold_time', '0분')
            trade_time = trade.get('time', '')
            
            # 색상 및 이모지
            color = Fore.GREEN if profit_loss >= 0 else Fore.RED
            emoji = "✅" if profit_loss >= 0 else "❌"
            
            # 한 줄로 표시
            lines.append(
                f"{emoji} {ticker} | {color}{profit_loss:+,.0f}원 ({profit_ratio:+.2f}%){Style.RESET_ALL} "
                f"| {strategy} | {hold_time} | {trade_time}"
            )
        
        return '\n'.join(lines)
    
    def _render_scan_status(self) -> str:
        """스캔 상태 렌더링"""
        now_str = datetime.now().strftime('%H:%M:%S')
        return f"""🔍 스캔 | {self.scan_status} | ⏰ {now_str}"""
    
    def _render_bot_status(self) -> str:
        """봇 상태 렌더링"""
        now_str = datetime.now().strftime('%H:%M:%S')
        return f"🤖 봇 | {self.bot_status} | ⏰ {now_str}"
    
    def _render_monitoring(self) -> str:
        """모니터링 렌더링"""
        lines = ["[ 📊 모니터링 ]"]
        
        if self.monitor_line1:
            lines.append(self.monitor_line1)
        if self.monitor_line2:
            lines.append(self.monitor_line2)
        if self.monitor_line3:
            lines.append(self.monitor_line3)
        
        return '\n'.join(lines)
    
    # ⭐ 업데이트 메서드들
    def update_capital_status(self, initial_capital: float, current_balance: float, 
                            total_profit: float = None, profit_ratio: float = None):
        """자본금 및 손익 상태 업데이트 (동기화 개선)"""
        self.initial_capital = initial_capital
        self.current_balance = current_balance
        
        # ⭐ 자동 계산으로 동기화 보장
        if total_profit is None or profit_ratio is None:
            if initial_capital > 0:
                self.total_profit = current_balance - initial_capital
                self.profit_ratio = (self.total_profit / initial_capital) * 100
        else:
            self.total_profit = total_profit
            self.profit_ratio = profit_ratio
    
    def update_ai_learning(self, learning_count: int, profit_trades: int, loss_trades: int, 
                          win_rate: float = None, total_trades: int = None):
        """AI 학습 상태 업데이트"""
        self.ai_learning_count = learning_count
        self.ai_profit_trades = profit_trades
        self.ai_loss_trades = loss_trades
        
        if total_trades is None:
            self.ai_total_trades = profit_trades + loss_trades
        else:
            self.ai_total_trades = total_trades
        
        if win_rate is None and self.ai_total_trades > 0:
            self.ai_win_rate = (profit_trades / self.ai_total_trades) * 100
        else:
            self.ai_win_rate = win_rate if win_rate is not None else 0.0
    
    def update_position(self, slot: int, ticker: str, entry_price: float, 
                       current_price: float, amount: float, profit_loss: float, 
                       profit_ratio: float, hold_time: str, strategy: str):
        """포지션 업데이트"""
        investment = entry_price * amount
        current_value = current_price * amount
        
        self.positions[slot] = {
            'ticker': ticker,
            'entry_price': entry_price,
            'current_price': current_price,
            'amount': amount,
            'investment': investment,
            'current_value': current_value,
            'profit_loss': profit_loss,
            'profit_ratio': profit_ratio,
            'hold_time': hold_time,
            'strategy': strategy
        }
    
    def remove_position(self, slot: int, exit_price: float, profit_loss: float, 
                       profit_ratio: float):
        """⭐ 포지션 제거 (매도) + 기록 저장"""
        if slot in self.positions:
            pos = self.positions[slot]
            
            # ⭐ 매도 기록 저장 (영구 보관)
            trade_record = {
                'ticker': pos['ticker'],
                'profit_loss': profit_loss,
                'profit_ratio': profit_ratio,
                'strategy': pos['strategy'],
                'hold_time': pos['hold_time'],
                'time': datetime.now().strftime('%H:%M:%S')
            }
            
            self.trade_history.append(trade_record)
            
            # 포지션 제거
            del self.positions[slot]
    
    def update_scan_status(self, status: str):
        """스캔 상태 업데이트"""
        self.scan_status = status
    
    def update_bot_status(self, status: str):
        """봇 상태 업데이트"""
        self.bot_status = status
    
    def update_monitoring(self, line1: str = None, line2: str = None, line3: str = None):
        """모니터링 상태 업데이트"""
        if line1 is not None:
            self.monitor_line1 = line1
        if line2 is not None:
            self.monitor_line2 = line2
        if line3 is not None:
            self.monitor_line3 = line3
    
    def clear_trade_history(self):
        """⭐ 매도 기록 초기화"""
        self.trade_history.clear()
    
    def get_trade_history(self) -> List[Dict]:
        """⭐ 매도 기록 조회"""
        return list(self.trade_history)


# 전역 인스턴스
display = FixedScreenDisplay(max_positions=7, max_trade_history=10)
