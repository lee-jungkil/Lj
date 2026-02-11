"""
그리드 거래 전략 (Grid Trading)
일정 구간에서 반복 매매로 수익
"""

from typing import Dict, Tuple, List
import pandas as pd
from .base_strategy import BaseStrategy


class GridTrading(BaseStrategy):
    """그리드 거래 전략"""
    
    def __init__(self, config: Dict):
        super().__init__("GridTrading", config)
        
        # 전략 파라미터
        self.stop_loss = config.get('stop_loss', 0.04)  # 4% (전체 그리드)
        self.grid_count = config.get('grid_count', 10)
        self.grid_spacing = config.get('grid_spacing', 0.005)  # 0.5% 간격
        self.max_volatility = config.get('max_volatility', 0.02)  # 2% 미만
        
        # 그리드 상태
        self.grids: List[Dict] = []
        self.base_price = 0.0
        self.grid_initialized = False
    
    def initialize_grids(self, current_price: float):
        """
        그리드 초기화
        
        Args:
            current_price: 현재 가격
        """
        self.base_price = current_price
        self.grids = []
        
        # 그리드 생성 (상하 각각)
        for i in range(-(self.grid_count // 2), (self.grid_count // 2) + 1):
            if i == 0:
                continue
            
            grid_price = current_price * (1 + (i * self.grid_spacing))
            
            self.grids.append({
                'level': i,
                'price': grid_price,
                'type': 'BUY' if i < 0 else 'SELL',
                'filled': False
            })
        
        self.grid_initialized = True
    
    def generate_signal(self, df: pd.DataFrame, ticker: str) -> Tuple[str, str, Dict]:
        """
        매매 신호 생성
        
        조건:
        - 변동성 < 2% (횡보장)
        - 0.5% 간격으로 매수/매도 주문
        - 최대 10개 그리드
        
        Returns:
            (신호, 사유, 지표)
        """
        if not self.enabled or not self.is_valid_data(df):
            return 'HOLD', 'Invalid data', {}
        
        current_price = df['close'].iloc[-1]
        volatility = self.get_volatility(df)
        
        indicators = {
            'current_price': current_price,
            'volatility': volatility,
            'grids_initialized': self.grid_initialized
        }
        
        # 변동성이 너무 크면 그리드 거래 중단
        if volatility > self.max_volatility:
            reason = f"변동성 과다 ({volatility:.2f}% > {self.max_volatility*100:.1f}%)"
            return 'HOLD', reason, indicators
        
        # 그리드 초기화
        if not self.grid_initialized:
            self.initialize_grids(current_price)
            indicators['grids'] = self.grids
            return 'HOLD', f'그리드 초기화 완료 (기준가: {self.base_price:,.0f}원)', indicators
        
        # 그리드 체크
        for grid in self.grids:
            if grid['filled']:
                continue
            
            price_diff = abs(current_price - grid['price']) / grid['price']
            
            # 매수 그리드 도달
            if grid['type'] == 'BUY' and current_price <= grid['price'] and price_diff < 0.001:
                grid['filled'] = True
                reason = f"그리드 매수 레벨 {grid['level']} 도달 (가격: {grid['price']:,.0f}원)"
                indicators['grid_level'] = grid['level']
                indicators['grids'] = self.grids
                return 'BUY', reason, indicators
            
            # 매도 그리드 도달
            if grid['type'] == 'SELL' and current_price >= grid['price'] and price_diff < 0.001:
                grid['filled'] = True
                reason = f"그리드 매도 레벨 {grid['level']} 도달 (가격: {grid['price']:,.0f}원)"
                indicators['grid_level'] = grid['level']
                indicators['grids'] = self.grids
                return 'SELL', reason, indicators
        
        indicators['grids'] = self.grids
        return 'HOLD', 'No grid level reached', indicators
    
    def should_exit(self, entry_price: float, current_price: float) -> Tuple[bool, str]:
        """
        청산 여부 확인 (전체 그리드 청산)
        
        Args:
            entry_price: 진입 가격 (기준가)
            current_price: 현재 가격
        
        Returns:
            (청산 여부, 사유)
        """
        if self.base_price == 0:
            return False, "No base price"
        
        profit_loss_ratio = (current_price - self.base_price) / self.base_price
        
        # 전체 그리드 손절
        if profit_loss_ratio <= -self.stop_loss:
            self.grid_initialized = False
            self.grids = []
            return True, f"전체 그리드 손절 ({profit_loss_ratio*100:.2f}%)"
        
        return False, "Hold grids"
    
    def reset_grids(self):
        """그리드 리셋"""
        self.grids = []
        self.base_price = 0.0
        self.grid_initialized = False
    
    def get_grid_status(self) -> Dict:
        """그리드 상태 조회"""
        if not self.grid_initialized:
            return {'initialized': False}
        
        filled_count = sum(1 for g in self.grids if g['filled'])
        
        return {
            'initialized': True,
            'base_price': self.base_price,
            'total_grids': len(self.grids),
            'filled_grids': filled_count,
            'remaining_grids': len(self.grids) - filled_count,
            'grids': self.grids
        }
