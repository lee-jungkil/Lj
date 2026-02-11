"""
리스크 관리 시스템
손실 한도, 수익 관리, 포지션 관리
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
    entry_time_id: str = ""  # AI 학습용 진입 시간 ID
    
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
    """리스크 관리 클래스"""
    
    def __init__(self, 
                 initial_capital: float,
                 max_daily_loss: float,
                 max_cumulative_loss: float,
                 max_positions: int = 3,
                 max_position_ratio: float = 0.3,
                 upbit_api = None):
        """
        초기화
        
        Args:
            initial_capital: 초기 자본
            max_daily_loss: 일일 최대 손실 한도
            max_cumulative_loss: 누적 최대 손실 한도
            max_positions: 최대 동시 포지션 수
            max_position_ratio: 단일 포지션 최대 비율
            upbit_api: UpbitAPI 인스턴스 (실시간 잔고 동기화용)
        """
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
        
        # 월간 수익 (수익 관리용)
        self.monthly_profit = 0.0
        self.last_profit_check_date = date.today()
        
        # 정지 플래그
        self.is_trading_stopped = False
        self.stop_reason = ""
    
    def sync_balance_from_exchange(self) -> bool:
        """
        거래소의 실제 잔고와 동기화
        사용자가 직접 입출금한 경우를 대응
        
        Returns:
            동기화 성공 여부
        """
        if self.upbit_api is None:
            return False
        
        try:
            # 실제 업비트 잔고 조회
            actual_balance = self.upbit_api.get_balance('KRW')
            
            if actual_balance is None or actual_balance == 0:
                return False
            
            # 잔고 차이 계산
            balance_diff = actual_balance - self.current_balance
            
            # 차이가 1000원 이상이면 동기화 (작은 오차는 무시)
            if abs(balance_diff) >= 1000:
                print(f"\n⚠️  잔고 불일치 감지!")
                print(f"   봇 추적 잔고: {self.current_balance:,.0f}원")
                print(f"   실제 거래소 잔고: {actual_balance:,.0f}원")
                print(f"   차이: {balance_diff:+,.0f}원")
                
                if balance_diff > 0:
                    print(f"   → 외부 입금 감지: +{balance_diff:,.0f}원")
                else:
                    print(f"   → 외부 출금 감지: {balance_diff:,.0f}원")
                
                # 잔고 동기화
                self.current_balance = actual_balance
                print(f"✅ 잔고 동기화 완료: {self.current_balance:,.0f}원\n")
                
                # 초기 자본도 조정 (수익률 계산 정확도 유지)
                # 단, 누적 손익은 유지 (실제 거래 성과 추적)
                self.initial_capital = actual_balance - self.cumulative_profit_loss
                
            return True
            
        except Exception as e:
            print(f"⚠️  잔고 동기화 실패: {e}")
            return False
    
    def reset_daily_stats(self):
        """일일 통계 초기화"""
        today = date.today()
        if today > self.last_reset_date:
            # 잔고 동기화 (매일 초 실행)
            self.sync_balance_from_exchange()
            
            self.daily_profit_loss = 0.0
            self.last_reset_date = today
            self.is_trading_stopped = False
            self.stop_reason = ""
    
    def can_open_position(self, ticker: str) -> tuple[bool, str]:
        """
        새 포지션 개설 가능 여부
        
        Args:
            ticker: 코인 티커
        
        Returns:
            (가능 여부, 사유)
        """
        # 거래 정지 확인
        if self.is_trading_stopped:
            return False, f"거래 정지됨: {self.stop_reason}"
        
        # 이미 보유 중인지 확인
        if ticker in self.positions:
            return False, f"{ticker}는 이미 보유 중입니다"
        
        # 최대 포지션 수 확인
        if len(self.positions) >= self.max_positions:
            return False, f"최대 포지션 수({self.max_positions}) 도달"
        
        # 일일 손실 한도 확인
        if self.daily_profit_loss <= -self.max_daily_loss:
            self.stop_trading("일일 손실 한도 초과")
            return False, "일일 손실 한도 초과"
        
        # 누적 손실 한도 확인
        if self.cumulative_profit_loss <= -self.max_cumulative_loss:
            self.stop_trading("누적 손실 한도 초과")
            return False, "누적 손실 한도 초과"
        
        return True, "OK"
    
    def calculate_position_size(self, price: float, force_sync: bool = False) -> float:
        """
        포지션 크기 계산
        
        Args:
            price: 현재 가격
            force_sync: 강제 잔고 동기화 여부
        
        Returns:
            투자 가능 금액 (KRW)
        """
        # 필요시 잔고 동기화
        if force_sync:
            self.sync_balance_from_exchange()
        
        # 사용 가능한 잔고
        available_balance = self.current_balance
        
        # 포지션 비율 적용
        max_investment = available_balance * self.max_position_ratio
        
        # 최소 5000원 이상
        if max_investment < 5000:
            return 0.0
        
        return max_investment
    
    def add_position(self, 
                    ticker: str, 
                    amount: float, 
                    price: float, 
                    strategy: str = "") -> bool:
        """
        포지션 추가
        
        Args:
            ticker: 코인 티커
            amount: 수량
            price: 매수 가격
            strategy: 전략 이름
        
        Returns:
            성공 여부
        """
        can_open, reason = self.can_open_position(ticker)
        if not can_open:
            return False
        
        position = Position(
            ticker=ticker,
            amount=amount,
            avg_buy_price=price,
            current_price=price,
            strategy=strategy,
            entry_time=datetime.now()
        )
        
        self.positions[ticker] = position
        self.current_balance -= (price * amount)
        self.total_trades += 1
        
        return True
    
    def close_position(self, ticker: str, price: float) -> Optional[float]:
        """
        포지션 청산
        
        Args:
            ticker: 코인 티커
            price: 매도 가격
        
        Returns:
            손익 금액
        """
        if ticker not in self.positions:
            return None
        
        position = self.positions[ticker]
        
        # 손익 계산
        buy_value = position.avg_buy_price * position.amount
        sell_value = price * position.amount
        profit_loss = sell_value - buy_value
        
        # 수수료 고려 (0.05% x 2)
        fee = (buy_value + sell_value) * 0.0005
        profit_loss -= fee
        
        # 통계 업데이트
        if profit_loss > 0:
            self.winning_trades += 1
        else:
            self.losing_trades += 1
        
        self.daily_profit_loss += profit_loss
        self.cumulative_profit_loss += profit_loss
        self.monthly_profit += profit_loss
        self.current_balance += sell_value
        
        # 포지션 제거
        del self.positions[ticker]
        
        return profit_loss
    
    def update_positions(self, prices: Dict[str, float]):
        """
        포지션 가격 업데이트
        
        Args:
            prices: {ticker: current_price} 딕셔너리
        """
        for ticker, position in self.positions.items():
            if ticker in prices:
                position.current_price = prices[ticker]
    
    def check_stop_loss(self, ticker: str, current_price: float, stop_loss_ratio: float) -> bool:
        """
        손절 확인
        
        Args:
            ticker: 코인 티커
            current_price: 현재 가격
            stop_loss_ratio: 손절 비율 (예: 0.02 = 2%)
        
        Returns:
            손절 필요 여부
        """
        if ticker not in self.positions:
            return False
        
        position = self.positions[ticker]
        loss_ratio = (current_price - position.avg_buy_price) / position.avg_buy_price
        
        return loss_ratio <= -stop_loss_ratio
    
    def check_take_profit(self, ticker: str, current_price: float, take_profit_ratio: float) -> bool:
        """
        익절 확인
        
        Args:
            ticker: 코인 티커
            current_price: 현재 가격
            take_profit_ratio: 익절 비율 (예: 0.015 = 1.5%)
        
        Returns:
            익절 필요 여부
        """
        if ticker not in self.positions:
            return False
        
        position = self.positions[ticker]
        profit_ratio = (current_price - position.avg_buy_price) / position.avg_buy_price
        
        return profit_ratio >= take_profit_ratio
    
    def stop_trading(self, reason: str):
        """
        거래 정지
        
        Args:
            reason: 정지 사유
        """
        self.is_trading_stopped = True
        self.stop_reason = reason
    
    def resume_trading(self):
        """거래 재개"""
        self.is_trading_stopped = False
        self.stop_reason = ""
    
    def get_win_rate(self) -> float:
        """
        승률 계산
        
        Returns:
            승률 (%)
        """
        total = self.winning_trades + self.losing_trades
        if total == 0:
            return 0.0
        return (self.winning_trades / total) * 100
    
    def get_total_position_value(self) -> float:
        """총 포지션 가치"""
        return sum(pos.total_value for pos in self.positions.values())
    
    def get_total_equity(self) -> float:
        """총 자산 (잔고 + 포지션)"""
        return self.current_balance + self.get_total_position_value()
    
    def should_withdraw_profit(self) -> tuple[bool, float]:
        """
        수익 출금 여부 확인 (월 1회)
        
        Returns:
            (출금 필요 여부, 출금 금액)
        """
        today = date.today()
        
        # 매월 1일 체크
        if today.day == 1 and today > self.last_profit_check_date:
            if self.monthly_profit > 0:
                withdrawal_amount = self.monthly_profit * 0.5  # 50% 출금
                self.last_profit_check_date = today
                return True, withdrawal_amount
        
        return False, 0.0
    
    def process_profit_withdrawal(self, amount: float):
        """
        수익 출금 처리
        
        Args:
            amount: 출금 금액
        """
        if amount > 0:
            self.current_balance -= amount
            self.monthly_profit = 0.0  # 월간 수익 초기화
    
    def get_risk_status(self) -> Dict[str, any]:
        """
        리스크 상태 조회
        
        Returns:
            리스크 상태 딕셔너리
        """
        total_equity = self.get_total_equity()
        total_pl_ratio = ((total_equity - self.initial_capital) / self.initial_capital) * 100
        
        return {
            'is_trading_stopped': self.is_trading_stopped,
            'stop_reason': self.stop_reason,
            'current_balance': self.current_balance,
            'total_equity': total_equity,
            'positions_count': len(self.positions),
            'daily_profit_loss': self.daily_profit_loss,
            'daily_loss_ratio': (self.daily_profit_loss / self.max_daily_loss) * 100,
            'cumulative_profit_loss': self.cumulative_profit_loss,
            'cumulative_loss_ratio': (self.cumulative_profit_loss / self.max_cumulative_loss) * 100,
            'total_profit_loss_ratio': total_pl_ratio,
            'win_rate': self.get_win_rate(),
            'total_trades': self.total_trades,
            'monthly_profit': self.monthly_profit,
        }
    
    def get_positions_summary(self) -> List[Dict[str, any]]:
        """포지션 요약 정보"""
        return [
            {
                'ticker': pos.ticker,
                'amount': pos.amount,
                'avg_buy_price': pos.avg_buy_price,
                'current_price': pos.current_price,
                'profit_loss': pos.profit_loss,
                'profit_loss_ratio': pos.profit_loss_ratio,
                'strategy': pos.strategy,
                'entry_time': pos.entry_time.isoformat(),
            }
            for pos in self.positions.values()
        ]
