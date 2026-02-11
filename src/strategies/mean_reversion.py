"""
평균 회귀 전략 (Mean Reversion)
가격이 평균으로 회귀하는 특성 활용
"""

from typing import Dict, Tuple
import pandas as pd
from .base_strategy import BaseStrategy


class MeanReversion(BaseStrategy):
    """평균 회귀 전략"""
    
    def __init__(self, config: Dict):
        super().__init__("MeanReversion", config)
        
        # 전략 파라미터
        self.stop_loss = config.get('stop_loss', 0.03)  # 3%
        self.take_profit = config.get('take_profit', 0.025)  # 2.5%
        self.ma_period = config.get('ma_period', 20)
        self.deviation_threshold = config.get('deviation_threshold', 0.05)  # 5% 이탈
    
    def generate_signal(self, df: pd.DataFrame, ticker: str) -> Tuple[str, str, Dict]:
        """
        매매 신호 생성
        
        조건:
        - 가격이 20일 이동평균에서 ±5% 이상 이탈
        - MACD 다이버전스 확인
        
        Returns:
            (신호, 사유, 지표)
        """
        if not self.enabled or not self.is_valid_data(df, min_length=30):
            return 'HOLD', 'Invalid data', {}
        
        # 기술적 지표 계산
        ma = self.calculate_moving_average(df, self.ma_period)
        macd, macd_signal, macd_hist = self.calculate_macd(df)
        
        current_price = df['close'].iloc[-1]
        current_ma = ma.iloc[-1]
        current_macd = macd.iloc[-1]
        current_macd_signal = macd_signal.iloc[-1]
        current_macd_hist = macd_hist.iloc[-1]
        
        # 이동평균으로부터의 이탈률
        deviation = (current_price - current_ma) / current_ma
        
        indicators = {
            'current_price': current_price,
            'ma': current_ma,
            'deviation': deviation,
            'macd': current_macd,
            'macd_signal': current_macd_signal,
            'macd_hist': current_macd_hist
        }
        
        # 매수 신호: 하단 이탈 + MACD 상승 전환
        if (deviation <= -self.deviation_threshold and 
            current_macd > current_macd_signal and
            current_macd_hist > 0):
            reason = f"하단 이탈 + MACD 상승전환 (이탈: {deviation*100:.2f}%, MACD히스토그램: {current_macd_hist:.2f})"
            return 'BUY', reason, indicators
        
        # 매도 신호: 상단 이탈 + MACD 하락 전환
        if (deviation >= self.deviation_threshold and 
            current_macd < current_macd_signal and
            current_macd_hist < 0):
            reason = f"상단 이탈 + MACD 하락전환 (이탈: {deviation*100:.2f}%, MACD히스토그램: {current_macd_hist:.2f})"
            return 'SELL', reason, indicators
        
        # 평균 회귀 확인 (포지션 청산 신호)
        if abs(deviation) < 0.01:  # 평균 근처 복귀
            reason = f"평균 회귀 완료 (이탈: {deviation*100:.2f}%)"
            return 'SELL', reason, indicators
        
        return 'HOLD', 'No clear signal', indicators
    
    def should_exit(self, entry_price: float, current_price: float) -> Tuple[bool, str]:
        """
        청산 여부 확인
        
        Args:
            entry_price: 진입 가격
            current_price: 현재 가격
        
        Returns:
            (청산 여부, 사유)
        """
        profit_loss_ratio = (current_price - entry_price) / entry_price
        
        # 손절
        if profit_loss_ratio <= -self.stop_loss:
            return True, f"손절 ({profit_loss_ratio*100:.2f}%)"
        
        # 익절
        if profit_loss_ratio >= self.take_profit:
            return True, f"익절 ({profit_loss_ratio*100:.2f}%)"
        
        return False, "Hold position"
