"""
되돌림 매수 전략 (Pullback Buy Strategy)
상승 추세 중 일시 조정 시 저점 매수
"""

from typing import Dict, Tuple
import pandas as pd
import numpy as np
from .base_strategy import BaseStrategy


class PullbackStrategy(BaseStrategy):
    """되돌림 매수 전략"""
    
    def __init__(self, config: Dict):
        """
        초기화
        
        Args:
            config: 전략 설정
        """
        super().__init__('PULLBACK', config)
        
        # 전략 파라미터
        self.trend_period = config.get('trend_period', 20)  # 추세 확인 기간
        self.trend_min = config.get('trend_min', 0.05)  # 최소 상승 추세 5%
        self.pullback_min = config.get('pullback_min', -0.02)  # 최소 되돌림 -2%
        self.pullback_max = config.get('pullback_max', -0.05)  # 최대 되돌림 -5%
        self.rsi_max = config.get('rsi_max', 35)  # RSI 상한 (과매도)
        self.fib_range = config.get('fib_range', (0.45, 0.55))  # 피보나치 50% 근처
        self.take_profit = config.get('take_profit', 0.04)  # 익절 4%
        self.stop_loss = config.get('stop_loss', -0.03)  # 손절 -3%
    
    def calculate_fibonacci_level(self, df: pd.DataFrame, period: int = 20) -> float:
        """
        피보나치 되돌림 레벨 계산
        
        Args:
            df: OHLCV 데이터프레임
            period: 기간
        
        Returns:
            현재 피보나치 레벨 (0~1)
        """
        if len(df) < period:
            return 0.5
        
        # 최근 기간의 최고/최저
        high = df['high'].iloc[-period:].max()
        low = df['low'].iloc[-period:].min()
        current = df['close'].iloc[-1]
        
        if high == low:
            return 0.5
        
        # 되돌림 레벨 (0 = 저점, 1 = 고점)
        fib_level = (current - low) / (high - low)
        return fib_level
    
    def generate_signal(self, df: pd.DataFrame, ticker: str) -> Tuple[str, str, Dict]:
        """
        매매 신호 생성
        
        조건:
        1. 전체 추세 상승 (20일 +5% 이상)
        2. 최근 3일 조정 (-2% ~ -5%)
        3. 피보나치 50% 근처
        4. RSI < 35 (과매도)
        
        Returns:
            (신호, 사유, 지표)
        """
        if not self.is_valid_data(df, self.trend_period + 10):
            return 'HOLD', 'Insufficient data', {}
        
        # 기술적 지표 계산
        current_price = df['close'].iloc[-1]
        
        # 장기 추세 (20일)
        trend_20d = self.get_price_change(df, self.trend_period)
        
        # 단기 조정 (3일)
        pullback_3d = self.get_price_change(df, 3)
        
        # RSI
        rsi = self.calculate_rsi(df).iloc[-1]
        
        # 피보나치 레벨
        fib_level = self.calculate_fibonacci_level(df, self.trend_period)
        
        # 볼린저 밴드
        bb_upper, bb_middle, bb_lower = self.calculate_bollinger_bands(df)
        bb_position = (current_price - bb_lower.iloc[-1]) / (bb_upper.iloc[-1] - bb_lower.iloc[-1]) if bb_upper.iloc[-1] != bb_lower.iloc[-1] else 0.5
        
        # MACD
        macd, signal, hist = self.calculate_macd(df)
        macd_turning = hist.iloc[-1] > hist.iloc[-2]  # 히스토그램 상승 전환
        
        # 거래량
        volume_ratio = self.calculate_volume_ratio(df)
        
        # 지표 딕셔너리
        indicators = {
            'current_price': current_price,
            'trend_20d': trend_20d,
            'pullback_3d': pullback_3d,
            'rsi': rsi,
            'fib_level': fib_level,
            'bb_position': bb_position,
            'macd_turning': macd_turning,
            'volume_ratio': volume_ratio
        }
        
        # 되돌림 매수 조건 체크
        uptrend = trend_20d >= self.trend_min  # 상승 추세
        pullback = self.pullback_max <= pullback_3d <= self.pullback_min  # 적정 조정
        oversold = rsi < self.rsi_max  # 과매도
        fib_ok = self.fib_range[0] <= fib_level <= self.fib_range[1]  # 피보나치 50% 근처
        
        if uptrend and pullback and oversold and fib_ok:
            reason = f"되돌림매수 | 추세↑{trend_20d:.1f}% | 조정{pullback_3d:.1f}% | RSI{rsi:.0f} | Fib{fib_level*100:.0f}%"
            return 'BUY', reason, indicators
        
        # 추가 강화 조건 (MACD 반등 + 볼린저 하단)
        if uptrend and pullback and macd_turning and bb_position < 0.3:
            reason = f"되돌림매수(강화) | 추세↑{trend_20d:.1f}% | MACD반등 | BB하단"
            return 'BUY', reason, indicators
        
        return 'HOLD', 'No pullback signal', indicators
    
    def should_exit(self, entry_price: float, current_price: float) -> Tuple[bool, str]:
        """
        청산 여부 확인
        
        Args:
            entry_price: 진입 가격
            current_price: 현재 가격
        
        Returns:
            (청산 여부, 사유)
        """
        profit_ratio = (current_price - entry_price) / entry_price
        
        # 익절
        if profit_ratio >= self.take_profit:
            return True, f"익절 {profit_ratio*100:.2f}% (목표 {self.take_profit*100:.0f}%)"
        
        # 손절
        if profit_ratio <= self.stop_loss:
            return True, f"손절 {profit_ratio*100:.2f}% (목표 {self.stop_loss*100:.0f}%)"
        
        return False, "Hold"
    
    def __str__(self):
        return f"Pullback Strategy (Trend: {self.trend_period}d, Pullback: {self.pullback_min*100:.0f}%~{self.pullback_max*100:.0f}%)"
