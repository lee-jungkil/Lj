"""
돌파 매수 전략 (Breakout Buy Strategy)
저항선 돌파 시 강한 상승 기대
"""

from typing import Dict, Tuple
import pandas as pd
import numpy as np
from .base_strategy import BaseStrategy


class BreakoutStrategy(BaseStrategy):
    """돌파 매수 전략"""
    
    def __init__(self, config: Dict):
        """
        초기화
        
        Args:
            config: 전략 설정
        """
        super().__init__('BREAKOUT', config)
        
        # 전략 파라미터
        self.lookback_period = config.get('lookback_period', 20)  # 저항선 확인 기간
        self.volume_multiplier = config.get('volume_multiplier', 2.0)  # 거래량 배수
        self.rsi_max = config.get('rsi_max', 70)  # RSI 상한
        self.take_profit = config.get('take_profit', 0.05)  # 익절 5%
        self.stop_loss = config.get('stop_loss', -0.02)  # 손절 -2%
    
    def generate_signal(self, df: pd.DataFrame, ticker: str) -> Tuple[str, str, Dict]:
        """
        매매 신호 생성
        
        조건:
        1. 20일 최고가 돌파
        2. 거래량 2배 이상
        3. RSI < 70 (과매수 아님)
        4. 최근 추세 상승
        
        Returns:
            (신호, 사유, 지표)
        """
        if not self.is_valid_data(df, self.lookback_period + 10):
            return 'HOLD', 'Insufficient data', {}
        
        # 기술적 지표 계산
        current_price = df['close'].iloc[-1]
        current_volume = df['volume'].iloc[-1]
        
        # 20일 최고가
        high_20d = df['high'].iloc[-self.lookback_period:-1].max()
        
        # 평균 거래량
        avg_volume = df['volume'].iloc[-self.lookback_period:].mean()
        volume_ratio = current_volume / avg_volume if avg_volume > 0 else 0
        
        # RSI
        rsi = self.calculate_rsi(df).iloc[-1]
        
        # MACD
        macd, signal, hist = self.calculate_macd(df)
        macd_bullish = macd.iloc[-1] > signal.iloc[-1]
        
        # 20일 이동평균
        ma_20 = self.calculate_moving_average(df, 20).iloc[-1]
        
        # 5일 추세
        trend_5d = self.get_price_change(df, 5)
        
        # 지표 딕셔너리
        indicators = {
            'current_price': current_price,
            'high_20d': high_20d,
            'breakout_ratio': (current_price / high_20d - 1) * 100,
            'volume_ratio': volume_ratio,
            'rsi': rsi,
            'macd_bullish': macd_bullish,
            'ma_20': ma_20,
            'trend_5d': trend_5d
        }
        
        # 돌파 매수 조건 체크
        breakout_confirmed = current_price > high_20d  # 저항선 돌파
        volume_surge = volume_ratio >= self.volume_multiplier  # 거래량 급증
        not_overbought = rsi < self.rsi_max  # 과매수 아님
        uptrend = current_price > ma_20  # 상승 추세
        
        if breakout_confirmed and volume_surge and not_overbought and uptrend:
            reason = f"돌파매수 | 20일고가돌파 {indicators['breakout_ratio']:.2f}% | 거래량 {volume_ratio:.1f}배 | RSI {rsi:.0f}"
            return 'BUY', reason, indicators
        
        # 추가 강화 조건 (MACD 골든크로스)
        if breakout_confirmed and volume_ratio >= 1.5 and macd_bullish and not_overbought:
            reason = f"돌파매수(MACD강화) | 20일고가돌파 | 거래량 {volume_ratio:.1f}배 | MACD↑"
            return 'BUY', reason, indicators
        
        return 'HOLD', 'No breakout signal', indicators
    
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
        return f"Breakout Strategy (Lookback: {self.lookback_period}d, Volume: {self.volume_multiplier}x)"
