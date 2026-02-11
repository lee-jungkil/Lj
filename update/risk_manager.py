"""
리스크 관리 시스템 v6.15-UPDATE
- 10% 손실 자동 중단 강화
- 손익 동기화 개선
"""

from typing import Dict, List, Optional
from datetime import datetime, date
from dataclasses import dataclass, field


@dataclass
class Position:
    """포지션 정보"""
    ticker: str
    amount: float
    avg_buy_price: float
    current_price: float = 0.0
    strategy: str = ""
    entry_time: datetime = field(default_factory=datetime.now)
    entry_time_id: str = ""
    
    @property
    def profit_loss(self) -> float:
        """손익 계산"""
        return (self.current_price - self.avg_buy_price) * self.amount
    
    @property
    def profit_loss_ratio(self) -> float:
        """손익률 계산 (%)"""
        if self.avg_buy_price == 0:
            return 0.0
        return ((self.current_price - self.avg_buy_price) / self.avg_buy_price) * 100
    
    @property
    def total_value(self) -> float:
        """현재 총 가치"""
        return self.current_price * self.amount


class RiskManager:
    """리스크 관리 클래스 v6.15-UPDATE"""
    
    def __init__(self, 
                 initial_capital: float,
                 max_daily_loss: float,
                 max_cumulative_loss: float,
                 max_positions: int = 3,
                 max_position_ratio: float = 0.3,
                 upbit_api = None):
        """초기화"""
        self.initial_capital = initial_capital
        self.max_daily_loss = max_daily_loss
        self.max_cumulative_loss = max_cumulative_loss
        self.max_positions = max_positions
        self.max_position_ratio = max_position_ratio
        self.upbit_api = upbit_api
        
        # 현재 상태
        self.current_balance = initial_capital
        self.positions: Dict[str, Position] = {}
        
        # 손익 추적
        self.daily_profit_loss = 0.0
        self.cumulative_profit_loss = 0.0
        self.last_reset_date = date.today()
        
        # 거래 통계
        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
        
        # 월간 수익
        self.monthly_profit = 0.0
        self.last_profit_check_date = date.today()
        
        # 정지 플래그
        self.is_trading_stopped = False
        self.stop_reason = ""
        
        # ⭐ 10% 손실 자동 중단
        self.loss_threshold_ratio = -10.0  # -10%
    
    def get_total_equity(self) -> float:
        """총 자산 (잔고 + 포지션)"""
        position_value = sum(pos.total_value for pos in self.positions.values())
        return self.current_balance + position_value
    
    def get_total_profit_loss(self) -> float:
        """총 손익 (초기 자본 대비)"""
        return self.get_total_equity() - self.initial_capital
    
    def get_total_profit_loss_ratio(self) -> float:
        """총 손익률 (%)"""
        if self.initial_capital == 0:
            return 0.0
        return (self.get_total_profit_loss() / self.initial_capital) * 100
    
    def check_loss_threshold(self) -> bool:
        """
        ⭐ 10% 손실 임계값 체크 (강화)
        
        Returns:
            True: 임계값 초과 (거래 중단 필요)
            False: 정상
        """
        total_pl_ratio = self.get_total_profit_loss_ratio()
        
        # ⭐ -10% 이하면 무조건 중단
        if total_pl_ratio <= self.loss_threshold_ratio:
            self.stop_trading(
                f"손실 임계값 초과: {total_pl_ratio:.2f}% (한도: {self.loss_threshold_ratio}%)"
            )
            return True
        
        return False
    
    def update_balance(self, new_balance: float):
        """
        잔고 업데이트 + 손익 동기화
        
        Args:
            new_balance: 새 잔고
        """
        self.current_balance = new_balance
        
        # ⭐ 매 업데이트마다 손실 임계값 체크
        self.check_loss_threshold()
    
    def update_position_price(self, ticker: str, current_price: float):
        """포지션 가격 업데이트"""
        if ticker in self.positions:
            self.positions[ticker].current_price = current_price
            
            # ⭐ 가격 업데이트 후에도 손실 임계값 체크
            self.check_loss_threshold()
    
    def add_position(self, ticker: str, amount: float, buy_price: float, 
                    strategy: str = "", entry_time_id: str = "") -> bool:
        """포지션 추가"""
        # 최대 포지션 수 확인
        if len(self.positions) >= self.max_positions:
            return False
        
        # 투자 금액 확인
        investment = amount * buy_price
        if investment > self.current_balance:
            return False
        
        # 단일 포지션 비율 확인
        if investment > self.initial_capital * self.max_position_ratio:
            return False
        
        # 포지션 추가
        self.positions[ticker] = Position(
            ticker=ticker,
            amount=amount,
            avg_buy_price=buy_price,
            current_price=buy_price,
            strategy=strategy,
            entry_time_id=entry_time_id
        )
        
        # 잔고 차감
        self.current_balance -= investment
        
        return True
    
    def close_position(self, ticker: str, sell_price: float) -> Optional[Dict]:
        """포지션 청산"""
        if ticker not in self.positions:
            return None
        
        pos = self.positions[ticker]
        
        # 매도 금액
        sell_amount = pos.amount * sell_price
        
        # 손익 계산
        buy_amount = pos.amount * pos.avg_buy_price
        profit_loss = sell_amount - buy_amount
        profit_loss_ratio = (profit_loss / buy_amount) * 100
        
        # 잔고 증가
        self.current_balance += sell_amount
        
        # 손익 누적
        self.daily_profit_loss += profit_loss
        self.cumulative_profit_loss += profit_loss
        self.monthly_profit += profit_loss
        
        # 거래 통계
        self.total_trades += 1
        if profit_loss > 0:
            self.winning_trades += 1
        else:
            self.losing_trades += 1
        
        # 포지션 제거
        result = {
            'ticker': ticker,
            'profit_loss': profit_loss,
            'profit_loss_ratio': profit_loss_ratio,
            'sell_price': sell_price,
            'strategy': pos.strategy,
            'holding_time': (datetime.now() - pos.entry_time).total_seconds()
        }
        
        del self.positions[ticker]
        
        # ⭐ 청산 후 손실 임계값 체크
        self.check_loss_threshold()
        
        return result
    
    def stop_trading(self, reason: str):
        """거래 정지"""
        self.is_trading_stopped = True
        self.stop_reason = reason
    
    def resume_trading(self):
        """거래 재개"""
        self.is_trading_stopped = False
        self.stop_reason = ""
    
    def get_win_rate(self) -> float:
        """승률 계산"""
        total = self.winning_trades + self.losing_trades
        if total == 0:
            return 0.0
        return (self.winning_trades / total) * 100
    
    def get_risk_status(self) -> Dict[str, any]:
        """리스크 상태 조회"""
        total_equity = self.get_total_equity()
        total_pl = self.get_total_profit_loss()
        total_pl_ratio = self.get_total_profit_loss_ratio()
        
        return {
            'is_trading_stopped': self.is_trading_stopped,
            'stop_reason': self.stop_reason,
            'current_balance': self.current_balance,
            'total_equity': total_equity,
            'total_profit_loss': total_pl,
            'total_profit_loss_ratio': total_pl_ratio,
            'positions_count': len(self.positions),
            'daily_profit_loss': self.daily_profit_loss,
            'cumulative_profit_loss': self.cumulative_profit_loss,
            'win_rate': self.get_win_rate(),
            'total_trades': self.total_trades,
            'monthly_profit': self.monthly_profit,
            'loss_threshold_status': 'DANGER' if total_pl_ratio < -8.0 else 'WARNING' if total_pl_ratio < -5.0 else 'SAFE'
        }
    
    def reset_daily_stats(self):
        """일일 통계 초기화"""
        today = date.today()
        if today > self.last_reset_date:
            self.daily_profit_loss = 0.0
            self.last_reset_date = today
    
    def can_open_new_position(self, investment_amount: float) -> bool:
        """신규 포지션 가능 여부"""
        # ⭐ 거래 정지 상태 확인
        if self.is_trading_stopped:
            return False
        
        # 최대 포지션 수
        if len(self.positions) >= self.max_positions:
            return False
        
        # 잔고 확인
        if investment_amount > self.current_balance:
            return False
        
        # 단일 포지션 비율
        if investment_amount > self.initial_capital * self.max_position_ratio:
            return False
        
        return True
