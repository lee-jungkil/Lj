"""
변동성 돌파 매수 전략 (Volatility Breakout Strategy)
래리 윌리엄스의 변동성 돌파 전략
"""

from typing import Dict, Tuple
import pandas as pd
import numpy as np
from .base_strategy import BaseStrategy


class VolatilityBreakoutStrategy(BaseStrategy):
    """변동성 돌파 매수 전략"""
    
    def __init__(self, config: Dict):
        """
        초기화
        
        Args:
            config: 전략 설정
        """
        super().__init__('VOLATILITY_BREAKOUT', config)
        
        # 전략 파라미터
        self.k_value = config.get('k_value', 0.4)  # 변동성 계수 (0.3~0.5)
        self.volume_multiplier = config.get('volume_multiplier', 1.5)  # 거래량 배수
        self.rsi_max = config.get('rsi_max', 75)  # RSI 상한
        self.take_profit = config.get('take_profit', 0.06)  # 익절 6%
        self.stop_loss = config.get('stop_loss', -0.025)  # 손절 -2.5%
    
    def calculate_target_price(self, df: pd.DataFrame) -> float:
        """
        변동성 돌파 목표가 계산
        
        공식: 금일 시가 + (전일 고가 - 전일 저가) × K
        
        Args:
            df: OHLCV 데이터프레임
        
        Returns:
            목표가
        """
        if len(df) < 2:
            return 0.0
        
        today_open = df['open'].iloc[-1]
        prev_high = df['high'].iloc[-2]
        prev_low = df['low'].iloc[-2]
        
        target_price = today_open + (prev_high - prev_low) * self.k_value
        return target_price
    
    def generate_signal(self, df: pd.DataFrame, ticker: str) -> Tuple[str, str, Dict]:
        """
        매매 신호 생성
        
        조건:
        1. 현재가가 목표가 돌파
        2. 거래량 1.5배 이상
        3. RSI < 75
        4. 전일 변동폭이 충분 (0.5% 이상)
        
        Returns:
            (신호, 사유, 지표)
        """
        if not self.is_valid_data(df, 30):
            return 'HOLD', 'Insufficient data', {}
        
        # 기술적 지표 계산
        current_price = df['close'].iloc[-1]
        
        # 목표가 계산
        target_price = self.calculate_target_price(df)
        
        # 전일 변동폭
        prev_high = df['high'].iloc[-2]
        prev_low = df['low'].iloc[-2]
        prev_range = (prev_high - prev_low) / prev_low * 100 if prev_low > 0 else 0
        
        # 거래량
        volume_ratio = self.calculate_volume_ratio(df)
        
        # RSI
        rsi = self.calculate_rsi(df).iloc[-1]
        
        # MACD
        macd, signal, hist = self.calculate_macd(df)
        macd_bullish = hist.iloc[-1] > 0
        
        # 20일 이동평균
        ma_20 = self.calculate_moving_average(df, 20).iloc[-1]
        above_ma = current_price > ma_20
        
        # 오늘 변동폭
        today_open = df['open'].iloc[-1]
        today_range = (current_price - today_open) / today_open * 100 if today_open > 0 else 0
        
        # 목표가 대비 비율
        breakout_ratio = (current_price / target_price - 1) * 100 if target_price > 0 else 0
        
        # 지표 딕셔너리
        indicators = {
            'current_price': current_price,
            'target_price': target_price,
            'breakout_ratio': breakout_ratio,
            'prev_range': prev_range,
            'today_range': today_range,
            'volume_ratio': volume_ratio,
            'rsi': rsi,
            'macd_bullish': macd_bullish,
            'above_ma': above_ma,
            'k_value': self.k_value
        }
        
        # 변동성 돌파 매수 조건 체크
        price_breakout = current_price > target_price  # 목표가 돌파
        volume_ok = volume_ratio >= self.volume_multiplier  # 거래량 증가
        not_overbought = rsi < self.rsi_max  # 과매수 아님
        sufficient_range = prev_range >= 0.5  # 전일 변동폭 충분
        
        if price_breakout and volume_ok and not_overbought and sufficient_range:
            reason = f"변동성돌파 | 목표가돌파 {breakout_ratio:.2f}% | K={self.k_value} | 거래량{volume_ratio:.1f}배 | RSI{rsi:.0f}"
            return 'BUY', reason, indicators
        
        # 추가 강화 조건 (MACD + 이평선 상향)
        if price_breakout and volume_ratio >= 1.2 and macd_bullish and above_ma and not_overbought:
            reason = f"변동성돌파(강화) | 목표가돌파 | MACD↑ | MA상향"
            return 'BUY', reason, indicators
        
        return 'HOLD', 'No volatility breakout signal', indicators
    
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
        return f"Volatility Breakout Strategy (K={self.k_value}, Volume: {self.volume_multiplier}x)"
