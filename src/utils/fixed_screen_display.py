"""
실시간 고정 화면 표시 시스템
한 화면에서 스크롤 없이 모든 정보를 표시
"""
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional
from colorama import init, Fore, Back, Style
import time

# Windows 콘솔 ANSI 지원 활성화
if os.name == 'nt':
    import ctypes
    kernel32 = ctypes.windll.kernel32
    # ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

# Colorama 초기화
init(autoreset=True, strip=False)


class FixedScreenDisplay:
    """고정 화면 표시 시스템"""
    
    def __init__(self, max_positions: int = 7):
        """
        초기화
        
        Args:
            max_positions: 최대 포지션 수 (기본 7개)
        """
        self.max_positions = max_positions
        self.positions = {}  # {slot: position_data}
        self.scan_status = "대기 중..."
        self.bot_status = "초기화 중..."
        self.market_summary = "시장 분석 중..."
        
        # AI 학습 상태 (매도 결과 제외)
        self.ai_learning_count = 0
        self.ai_win_rate = 0.0
        self.ai_total_trades = 0
        self.ai_profit_trades = 0  # 수익 거래 수
        self.ai_loss_trades = 0    # 손실 거래 수
        
        # 자본금 및 손익 상태
        self.initial_capital = 0
        self.current_balance = 0
        self.total_profit = 0.0
        self.profit_ratio = 0.0
        
        # 진입 조건 상태
        self.market_phase = "분석 중"  # 강세장/약세장/횡보장
        self.entry_condition = "기본"  # 완화/기본/강화
        
        # 1줄 요약
        self.coin_summary = "코인 시장 분석 중..."
        
        # ⭐ 시장 조건 이유
        self.market_phase_reason = ""  # 강세장 이유, 횡보장 이유
        
        # ⭐ 거래 통계 (매수/매도 횟수)
        self.buy_count = 0
        self.sell_count = 0
        
        # ⭐ 스캔 시간 기록
        self.last_full_scan_time = None
        self.last_position_check_time = None
        self.last_surge_scan_time = None
        
        # ⭐ 모니터링 상태 (3줄) - 간단한 표현만
        self.monitor_line1 = "대기 중..."
        self.monitor_line2 = ""
        self.monitor_line3 = ""
        
        # 매도 결과 (임시 표시용)
        self.last_trade_result = None
        self.last_trade_time = 0
        
        # ⭐ 매도 기록 영구 저장 (최대 10개)
        self.sell_history = []  # [{ticker, profit_loss, profit_ratio, strategy, hold_time, time}]
        self.max_sell_history = 10
        
        # ⭐ 화면 크기: 중앙 정렬 + 80% 크기
        import os
        try:
            # 터미널 크기 감지
            terminal_size = os.get_terminal_size()
            terminal_width = terminal_size.columns
            terminal_height = terminal_size.rows
            
            # 80% 너비 계산
            self.screen_width = min(int(terminal_width * 0.8), 120)  # 최대 120
            
            # 중앙 정렬을 위한 왼쪽 여백
            self.left_margin = (terminal_width - self.screen_width) // 2
            
            # ⭐ 고정 높이: 터미널 높이 - 2 (여유 공간)
            self.screen_height = terminal_height - 2
        except:
            # 기본값
            self.screen_width = 96  # 120의 80%
            self.left_margin = 12   # (120 - 96) // 2
            self.screen_height = 40  # 기본 높이
        
        # ⭐ 첫 화면 초기화
        self._first_render = True
        
        # 커서 숨기기 (Windows)
        if os.name == 'nt':
            # 커서 숨기기
            sys.stdout.write('\033[?25l')
            sys.stdout.flush()
    
    def clear_screen(self):
        """화면 전체 클리어"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def cleanup(self):
        """종료 시 정리 작업 (커서 표시)"""
        if os.name == 'nt':
            # 커서 다시 표시
            sys.stdout.write('\033[?25h')
            sys.stdout.flush()
    
    def move_cursor(self, row: int, col: int = 0):
        """커서 이동 (ANSI 코드)"""
        sys.stdout.write(f'\033[{row};{col}H')
        sys.stdout.flush()
    
    def _format_hold_time(self, seconds: float) -> str:
        """
        초를 사람이 읽기 쉬운 형식으로 변환
        
        Args:
            seconds: 초 단위 시간
        
        Returns:
            "3분 24초" 형식의 문자열
        """
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        
        if minutes > 0:
            return f"{minutes}분 {secs}초"
        else:
            return f"{secs}초"
    
    def update_position(self, slot: int, ticker: str, entry_price: float, 
                       current_price: float, amount: float, strategy: str,
                       entry_time: datetime):
        """
        포지션 업데이트
        
        Args:
            slot: 슬롯 번호 (1~7)
            ticker: 코인 티커
            entry_price: 진입 가격
            current_price: 현재 가격
            amount: 수량
            strategy: 전략
            entry_time: 진입 시간
        """
        if slot < 1 or slot > self.max_positions:
            return
        
        # ⭐ 손익 계산
        profit_loss = (current_price - entry_price) * amount
        profit_ratio = ((current_price - entry_price) / entry_price) * 100
        
        # ⭐ 보유 시간 계산 및 형식화
        hold_seconds = (datetime.now() - entry_time).total_seconds()
        hold_time = self._format_hold_time(hold_seconds)
        
        # ⭐ 투자금 및 현재 가치 계산
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
            'hold_seconds': hold_seconds,  # ⭐ 추가: 초 단위 저장
            'entry_time': entry_time,  # ⭐ 추가: 원본 시간 저장
            'strategy': strategy
        }
    
    def update_position_price(self, slot: int, current_price: float):
        """
        포지션의 현재 가격만 업데이트 (실시간 동기화용)
        
        Args:
            slot: 슬롯 번호
            current_price: 새 현재 가격
        """
        if slot not in self.positions:
            return
        
        pos = self.positions[slot]
        
        # 가격 업데이트
        pos['current_price'] = current_price
        
        # 손익 재계산
        pos['profit_loss'] = (current_price - pos['entry_price']) * pos['amount']
        pos['profit_ratio'] = ((current_price - pos['entry_price']) / pos['entry_price']) * 100
        
        # 현재 가치 재계산
        pos['current_value'] = current_price * pos['amount']
        
        # ⭐ 보유 시간 재계산 (entry_time 활용)
        if 'entry_time' in pos:
            hold_seconds = (datetime.now() - pos['entry_time']).total_seconds()
            pos['hold_time'] = self._format_hold_time(hold_seconds)
            pos['hold_seconds'] = hold_seconds
    
    def remove_position(self, slot: int, exit_price: float, profit_loss: float, 
                       profit_ratio: float):
        """
        포지션 제거 및 결과 표시
        
        Args:
            slot: 슬롯 번호
            exit_price: 청산 가격
            profit_loss: 손익 금액
            profit_ratio: 손익 비율
        """
        if slot not in self.positions:
            return
        
        position = self.positions[slot]
        
        # ⭐ 매도 기록 영구 저장
        sell_record = {
            'ticker': position['ticker'],
            'profit_loss': profit_loss,
            'profit_ratio': profit_ratio,
            'strategy': position['strategy'],
            'hold_time': position['hold_time'],
            'time': datetime.now().strftime('%H:%M:%S')
        }
        
        # 최대 개수 제한 (FIFO)
        if len(self.sell_history) >= self.max_sell_history:
            self.sell_history.pop(0)
        
        self.sell_history.append(sell_record)
        
        # 임시 표시용 (5초간)
        emoji = "💰" if profit_loss > 0 else "📉"
        self.last_trade_result = (
            f"{emoji} {slot}️⃣ {position['ticker']} 매도 완료: "
            f"{profit_loss:+,.0f}원 ({profit_ratio:+.2f}%) | "
            f"보유: {position['hold_time']:.0f}초"
        )
        self.last_trade_time = time.time()
        
        # 매도 횟수 증가
        self.sell_count += 1
        
        # 포지션 제거
        del self.positions[slot]
    
    def update_scan_status(self, status: str):
        """스캔 상태 업데이트"""
        self.scan_status = status
    
    def update_bot_status(self, status: str):
        """봇 상태 업데이트"""
        self.bot_status = status
    
    def update_ai_learning(self, total_trades: int, profit_trades: int, 
                          loss_trades: int):
        """
        AI 학습 상태 업데이트
        
        Args:
            total_trades: 총 거래 수
            profit_trades: 수익 거래 수
            loss_trades: 손실 거래 수
        """
        self.ai_total_trades = total_trades
        self.ai_profit_trades = profit_trades
        self.ai_loss_trades = loss_trades
        self.ai_learning_count = total_trades
        
        if total_trades > 0:
            self.ai_win_rate = (profit_trades / total_trades) * 100
        else:
            self.ai_win_rate = 0.0
    
    def sync_with_risk_manager(self, risk_manager):
        """
        RiskManager와 자동 동기화
        
        Args:
            risk_manager: RiskManager 인스턴스
        """
        # 자본금 동기화
        risk_status = risk_manager.get_risk_status()
        self.update_capital_status(
            initial=risk_manager.initial_capital,
            current=risk_status['current_balance'],
            profit=risk_status['cumulative_profit_loss']
        )
    
    def update_capital_status(self, initial: int, current: int, profit: float):
        """
        자본금 및 손익 상태 업데이트
        
        Args:
            initial: 초기 자본금
            current: 현재 잔고
            profit: 누적 손익
        """
        self.initial_capital = initial
        self.current_balance = current
        self.total_profit = profit
        
        if initial > 0:
            self.profit_ratio = (profit / initial) * 100
        else:
            self.profit_ratio = 0.0
    
    def update_market_condition(self, phase: str, entry_condition: str, reason: str = ""):
        """
        시장 조건 및 진입 조건 업데이트
        
        Args:
            phase: 시장 국면 (강세장/약세장/횡보장)
            entry_condition: 진입 조건 (완화/기본/강화)
            reason: 시장 조건 이유 (예: "BTC +3.5%", "거래량 감소")
        """
        self.market_phase = phase
        self.entry_condition = entry_condition
        self.market_phase_reason = reason
    
    def update_trade_stats(self, buy_count: int, sell_count: int):
        """
        거래 통계 업데이트
        
        Args:
            buy_count: 매수 횟수
            sell_count: 매도 횟수
        """
        self.buy_count = buy_count
        self.sell_count = sell_count
    
    def update_scan_times(self, full_scan_time=None, position_check_time=None, surge_scan_time=None):
        """
        스캔 시간 업데이트
        
        Args:
            full_scan_time: 전체 스캔 시간
            position_check_time: 포지션 체크 시간
            surge_scan_time: 초단타 스캔 시간
        """
        if full_scan_time:
            self.last_full_scan_time = full_scan_time
        if position_check_time:
            self.last_position_check_time = position_check_time
        if surge_scan_time:
            self.last_surge_scan_time = surge_scan_time
    
    def update_coin_summary(self, summary: str):
        """
        코인 상황 한 줄 요약 업데이트
        
        Args:
            summary: 요약 텍스트
        """
        self.coin_summary = summary
    
    def update_monitoring(self, line1: str, line2: str = "", line3: str = ""):
        """
        모니터링 상태 업데이트 (3줄)
        
        Args:
            line1: 첫 번째 줄 (필수)
            line2: 두 번째 줄 (선택)
            line3: 세 번째 줄 (선택)
        """
        self.monitor_line1 = line1
        self.monitor_line2 = line2
        self.monitor_line3 = line3
    
    def update_position_details(self, ticker: str, action: str, reason: str):
        """
        포지션 처리 상세 정보 업데이트
        
        Args:
            ticker: 코인 티커
            action: 처리 내용 (익절 확인 중, 손절 확인 중, 보유 중 등)
            reason: 상세 이유
        """
        coin_short = ticker.split('-')[1] if '-' in ticker else ticker
        self.monitor_line1 = f"📊 {coin_short}: {action}"
        self.monitor_line2 = f"상세: {reason}"
        self.monitor_line3 = ""
    
    def render(self):
        """전체 화면 렌더링 (고정 화면, 스크롤 없음)"""
        # ⭐ 터미널 크기 재계산
        try:
            terminal_size = os.get_terminal_size()
            terminal_width = terminal_size.columns
            terminal_height = terminal_size.rows
            self.screen_width = min(int(terminal_width * 0.8), 120)
            self.left_margin = max(0, (terminal_width - self.screen_width) // 2)
            self.screen_height = terminal_height - 2  # 여유 공간
        except:
            pass
        
        # ⭐ 첫 렌더링 시 화면 클리어
        if self._first_render:
            sys.stdout.write('\033[2J\033[H')  # 화면 클리어 + 커서 홈
            sys.stdout.flush()
            self._first_render = False
        
        # ⭐ 모든 라인 생성
        output_lines = []
        margin = " " * self.left_margin
        
        # 헤더 (3줄)
        for line in self._render_header().split('\n'):
            output_lines.append(margin + line)
        output_lines.append(margin + "━" * self.screen_width)
        
        # 매수 포지션 (가변)
        for line in self._render_positions().split('\n'):
            output_lines.append(margin + line)
        output_lines.append(margin + "━" * self.screen_width)
        
        # 매도 결과 (3줄 or 빈 줄)
        trade_result = self._render_trade_result()
        if trade_result:
            for line in trade_result.split('\n'):
                output_lines.append(margin + line)
            output_lines.append(margin + "━" * self.screen_width)
        else:
            output_lines.append(margin)
            output_lines.append(margin)
            output_lines.append(margin + "━" * self.screen_width)
        
        # 스캔 상태 (4줄)
        for line in self._render_scan_status().split('\n'):
            output_lines.append(margin + line)
        output_lines.append(margin + "━" * self.screen_width)
        
        # 봇 상태 (2줄)
        output_lines.append(margin + self._render_bot_status())
        output_lines.append(margin + "━" * self.screen_width)
        
        # 모니터링 상태 (4-5줄)
        for line in self._render_monitoring().split('\n'):
            output_lines.append(margin + line)
        output_lines.append(margin + "━" * self.screen_width)
        
        # ⭐ 매도 기록 (6-8줄)
        for line in self._render_sell_history().split('\n'):
            output_lines.append(margin + line)
        output_lines.append(margin + "━" * self.screen_width)
        output_lines.append(margin)  # 마지막 빈 줄
        
        # ⭐ 고정 높이 제한: 화면 높이를 초과하면 잘라냄
        if len(output_lines) > self.screen_height:
            output_lines = output_lines[:self.screen_height]
        
        # ⭐ 부족한 줄은 빈 줄로 채움 (화면 고정)
        while len(output_lines) < self.screen_height:
            output_lines.append(margin)
        
        # ⭐ 커서를 홈으로 이동 후 한 줄씩 덮어쓰기
        sys.stdout.write('\033[H')  # 커서를 (1, 1)로 이동
        
        for i, line in enumerate(output_lines, start=1):
            # 각 줄을 지우고 쓰기
            sys.stdout.write('\033[2K')  # 현재 줄 지우기
            sys.stdout.write(line)
            
            # 마지막 줄이 아니면 다음 줄로 이동
            if i < len(output_lines):
                sys.stdout.write('\n')
        
        sys.stdout.flush()
    
    def _render_header(self) -> str:
        """헤더 렌더링 (실시간 시계)"""
        # ⭐ 실시간 시계
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        title = "Upbit AutoProfit Bot v6.14-FIXED"
        
        # AI 학습 상태 표시 (매도 결과 제외)
        ai_status = (
            f"AI학습: {self.ai_learning_count}회 | "
            f"승률: {self.ai_win_rate:.1f}%"
        )
        
        # 자본금 및 손익 상태
        profit_color = Fore.GREEN if self.total_profit >= 0 else Fore.RED
        capital_status = (
            f"자본: {self.current_balance:,.0f}원 | "
            f"{profit_color}손익: {self.total_profit:+,.0f}원 ({self.profit_ratio:+.2f}%){Style.RESET_ALL}"
        )
        
        return (
            f"{Fore.CYAN}{Style.BRIGHT}{title}{Style.RESET_ALL} | "
            f"{Fore.GREEN}⏰ {now}{Style.RESET_ALL}\n"  # ⭐ 시계 아이콘
            f"{Fore.YELLOW}📊 {ai_status}{Style.RESET_ALL} | "
            f"{capital_status}"
        )
    
    def _render_positions(self) -> str:
        """포지션 영역 렌더링 (실시간 가격/손익 표시)"""
        lines = [f"{Fore.YELLOW}{Style.BRIGHT}[ 💼 보유 포지션 ({len(self.positions)}/{self.max_positions}) ]{Style.RESET_ALL}"]
        lines.append("")
        
        if not self.positions:
            lines.append(f"{Fore.CYAN}  대기 중... 매수 신호 분석 중{Style.RESET_ALL}")
        else:
            for slot in range(1, self.max_positions + 1):
                if slot in self.positions:
                    pos = self.positions[slot]
                    
                    # 코인 이름 (짧게)
                    coin = pos['ticker'].replace('KRW-', '')
                    
                    # 투자 금액 계산
                    investment = pos['entry_price'] * pos['amount']
                    
                    # 현재 가치 계산
                    current_value = pos['current_price'] * pos['amount']
                    
                    # 손익 금액
                    profit_loss = pos['profit_loss']
                    
                    # 손익률
                    profit_ratio = pos['profit_ratio']
                    
                    # 손익률에 따른 색상
                    if profit_ratio >= 2.0:
                        color = Fore.GREEN + Style.BRIGHT
                        emoji = "🚀"
                    elif profit_ratio >= 0.5:
                        color = Fore.GREEN
                        emoji = "💰"
                    elif profit_ratio > 0:
                        color = Fore.CYAN
                        emoji = "📈"
                    elif profit_ratio > -0.5:
                        color = Fore.YELLOW
                        emoji = "⚠️"
                    else:
                        color = Fore.RED
                        emoji = "📉"
                    
                    # 보유 시간
                    hold_seconds = int(pos['hold_time'])
                    hold_minutes = hold_seconds // 60
                    hold_secs = hold_seconds % 60
                    
                    if hold_minutes > 0:
                        hold_str = f"{hold_minutes}분{hold_secs}초"
                    else:
                        hold_str = f"{hold_secs}초"
                    
                    # 전략 표시 (간단하게)
                    strategy_map = {
                        'aggressive_scalping': '⚡스캘핑',
                        'medium_term': '📊중기',
                        'value_investing': '💎가치',
                        'ultra_scalping': '🔥초단타',
                        '⚡초단타': '🔥초단타',
                        '⚡초': '🔥초단타'
                    }
                    strategy_short = strategy_map.get(pos['strategy'], pos['strategy'][:4])
                    
                    # ⭐ 가격 포맷 (업비트 실제 가격 그대로)
                    # 큰 금액(1000원 이상): 정수로 표시
                    # 작은 금액(1000원 미만): 소수점 그대로 표시
                    def format_price(price):
                        if price >= 1000:
                            return f"{price:,.0f}"
                        elif price >= 100:
                            return f"{price:,.1f}"
                        elif price >= 10:
                            return f"{price:,.2f}"
                        elif price >= 1:
                            return f"{price:,.3f}"
                        else:
                            return f"{price:,.8f}"  # 매우 작은 코인
                    
                    # 투자 금액과 현재 가치
                    investment_str = format_price(investment)
                    current_value_str = format_price(current_value)
                    
                    # 진입가와 현재가
                    entry_price_str = format_price(pos['entry_price'])
                    current_price_str = format_price(pos['current_price'])
                    
                    # 손익 금액
                    profit_loss_str = f"{profit_loss:+,.0f}" if abs(profit_loss) >= 1 else f"{profit_loss:+,.2f}"
                    
                    # ⭐ 실시간 정보 표시
                    lines.append(
                        f"  {emoji} 슬롯{slot} │ {Fore.CYAN}{Style.BRIGHT}{coin:8s}{Style.RESET_ALL} │ "
                        f"{strategy_short}"
                    )
                    lines.append(
                        f"     투자: {Fore.WHITE}{investment_str:>15s}원{Style.RESET_ALL} → "
                        f"현재: {Fore.YELLOW}{current_value_str:>15s}원{Style.RESET_ALL}"
                    )
                    lines.append(
                        f"     진입: {entry_price_str:>15s}원 → "
                        f"현재: {color}{current_price_str:>15s}원{Style.RESET_ALL}"
                    )
                    lines.append(
                        f"     손익: {color}{profit_loss_str:>15s}원 ({profit_ratio:>+6.2f}%){Style.RESET_ALL} │ "
                        f"보유: {hold_str}"
                    )
                    lines.append("")  # 빈 줄
        
        return '\n'.join(lines)
    
    def _render_trade_result(self) -> Optional[str]:
        """매도 결과 렌더링 (5초간만)"""
        if not self.last_trade_result:
            return None
        
        # 5초 경과 확인
        if time.time() - self.last_trade_time > 5:
            self.last_trade_result = None
            return None
        
        return f"{Fore.CYAN}{Style.BRIGHT}[ 매도 결과 ]{Style.RESET_ALL}\n{self.last_trade_result}"
    
    def _render_scan_status(self) -> str:
        """스캔 상태 렌더링 + 시간 + 시장 분석"""
        now = datetime.now().strftime('%H:%M:%S')
        
        # ⭐ 스캔 시간 표시
        scan_times = []
        if self.last_full_scan_time:
            scan_times.append(f"전체: {self.last_full_scan_time.strftime('%H:%M:%S')}")
        if self.last_position_check_time:
            scan_times.append(f"포지션: {self.last_position_check_time.strftime('%H:%M:%S')}")
        if self.last_surge_scan_time:
            scan_times.append(f"초단타: {self.last_surge_scan_time.strftime('%H:%M:%S')}")
        
        scan_time_str = " | ".join(scan_times) if scan_times else "대기 중"
        
        # 시장 조건 및 진입 조건 표시
        condition_color = {
            '완화': Fore.GREEN,
            '기본': Fore.YELLOW,
            '강화': Fore.RED
        }.get(self.entry_condition, Fore.WHITE)
        
        # ⭐ 시장 이유 표시
        market_reason = f" ({self.market_phase_reason})" if self.market_phase_reason else ""
        
        return (
            f"{Fore.BLUE}🔍 스캔{Style.RESET_ALL} | "
            f"{self.scan_status} | "
            f"{Fore.CYAN}⏰ {now}{Style.RESET_ALL}\n"
            f"{Fore.GREEN}⏱️ {scan_time_str}{Style.RESET_ALL}\n"
            f"{Fore.MAGENTA}📈 시장{Style.RESET_ALL}: {self.market_phase}{market_reason} | "
            f"{condition_color}진입: {self.entry_condition}{Style.RESET_ALL} | "
            f"{self.coin_summary}"
        )
    
    def _render_bot_status(self) -> str:
        """봇 상태 렌더링 + 거래 통계"""
        # ⭐ 매수/매도 횟수 표시
        trade_stats = f"매수 {self.buy_count}회 | 매도 {self.sell_count}회"
        
        return (
            f"{Fore.MAGENTA}🤖 상태{Style.RESET_ALL} | {self.bot_status} | "
            f"{Fore.CYAN}{trade_stats}{Style.RESET_ALL}"
        )
    
    def _render_monitoring(self) -> str:
        """모니터링 상태 렌더링 (3줄, 간단한 표현)"""
        lines = [f"{Fore.CYAN}{Style.BRIGHT}[ 🔍 작업 상태 ]{Style.RESET_ALL}"]
        
        # 간단하게만 표시
        if self.monitor_line1:
            # 너무 긴 텍스트 자르기 (화면 너비 - 10)
            line1 = self.monitor_line1[:self.screen_width - 10]
            lines.append(f"{Fore.GREEN}▸ {line1}{Style.RESET_ALL}")
        if self.monitor_line2:
            line2 = self.monitor_line2[:self.screen_width - 10]
            lines.append(f"{Fore.YELLOW}▸ {line2}{Style.RESET_ALL}")
        if self.monitor_line3:
            line3 = self.monitor_line3[:self.screen_width - 10]
            lines.append(f"{Fore.BLUE}▸ {line3}{Style.RESET_ALL}")
        
        return '\n'.join(lines)
    
    def _render_sell_history(self) -> str:
        """매도 기록 렌더링 (최근 5개)"""
        lines = [f"{Fore.YELLOW}{Style.BRIGHT}[ 📜 매도 기록 ({len(self.sell_history)}건) ]{Style.RESET_ALL}"]
        
        if not self.sell_history:
            lines.append("  기록 없음")
        else:
            # 최근 5개만 표시 (스크롤 방지)
            recent_sells = self.sell_history[-5:]
            
            for record in reversed(recent_sells):  # 최신순
                profit_loss = record['profit_loss']
                profit_ratio = record['profit_ratio']
                color = Fore.GREEN if profit_loss >= 0 else Fore.RED
                emoji = "✅" if profit_loss >= 0 else "❌"
                
                lines.append(
                    f"  {emoji} {record['time']} | {record['ticker']} | "
                    f"{color}{profit_loss:+,.0f}원 ({profit_ratio:+.2f}%){Style.RESET_ALL} | "
                    f"{record['strategy'][:8]}"
                )
        
        return '\n'.join(lines)
    
    def get_available_slot(self) -> Optional[int]:
        """
        사용 가능한 슬롯 번호 반환
        
        Returns:
            슬롯 번호 (1~5) 또는 None
        """
        for slot in range(1, self.max_positions + 1):
            if slot not in self.positions:
                return slot
        return None
    
    def get_slot_by_ticker(self, ticker: str) -> Optional[int]:
        """
        티커로 슬롯 번호 찾기
        
        Args:
            ticker: 코인 티커
        
        Returns:
            슬롯 번호 또는 None
        """
        for slot, pos in self.positions.items():
            if pos['ticker'] == ticker:
                return slot
        return None
    
    def get_position_count(self) -> int:
        """현재 포지션 수"""
        return len(self.positions)
    
    def is_slot_available(self) -> bool:
        """슬롯 사용 가능 여부"""
        return len(self.positions) < self.max_positions


# 전역 인스턴스
display = FixedScreenDisplay(max_positions=7)


if __name__ == "__main__":
    # 테스트
    display.clear_screen()
    display.update_bot_status("테스트 모드 실행 중")
    display.update_scan_status("코인 20개 스캔 중...")
    
    # 포지션 추가
    display.update_position(
        slot=1,
        ticker="KRW-BTC",
        entry_price=50000000,
        current_price=50600000,
        amount=0.001,
        strategy="ultra_scalping",
        entry_time=datetime.now()
    )
    
    display.update_position(
        slot=2,
        ticker="KRW-ETH",
        entry_price=3000000,
        current_price=2985000,
        amount=0.01,
        strategy="aggressive_scalping",
        entry_time=datetime.now()
    )
    
    # 렌더링
    for i in range(10):
        display.render()
        time.sleep(1)
        
        # 가격 변동 시뮬레이션
        if 1 in display.positions:
            current = display.positions[1]['current_price']
            display.update_position(
                slot=1,
                ticker="KRW-BTC",
                entry_price=50000000,
                current_price=current + 10000,
                amount=0.001,
                strategy="ultra_scalping",
                entry_time=display.positions[1]['hold_time']
            )
    
    # 매도 시뮬레이션
    display.remove_position(1, 50600000, 600, 1.2)
    display.render()
    
    time.sleep(5)
    display.render()
    
    print("\n테스트 완료!")
