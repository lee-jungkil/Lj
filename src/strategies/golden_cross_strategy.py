"""
골든크로스 매수 전략 (Golden Cross Strategy)
단기 이평선이 장기 이평선을 상향 돌파
"""

from typing import Dict, Tuple
import pandas as pd
import numpy as np
from .base_strategy import BaseStrategy


class GoldenCrossStrategy(BaseStrategy):
    """골든크로스 매수 전략"""
    
    def __init__(self, config: Dict):
        """
        초기화
        
        Args:
            config: 전략 설정
        """
        super().__init__('GOLDEN_CROSS', config)
        
        # 전략 파라미터
        self.fast_period = config.get('fast_period', 5)  # 단기 이평선
        self.slow_period = config.get('slow_period', 20)  # 장기 이평선
        self.cross_window = config.get('cross_window', 3)  # 크로스 확인 기간
        self.volume_multiplier = config.get('volume_multiplier', 1.3)  # 거래량 배수
        self.take_profit = config.get('take_profit', 0.08)  # 익절 8%
        self.stop_loss = config.get('stop_loss', -0.03)  # 손절 -3%
    
    def detect_golden_cross(self, df: pd.DataFrame) -> Tuple[bool, int]:
        """
        골든크로스 감지
        
        Args:
            df: OHLCV 데이터프레임
        
        Returns:
            (골든크로스 발생 여부, 몇 봉 전)
        """
        if len(df) < self.slow_period + self.cross_window:
            return False, -1
        
        ma_fast = self.calculate_moving_average(df, self.fast_period)
        ma_slow = self.calculate_moving_average(df, self.slow_period)
        
        # 최근 cross_window 봉 이내에 크로스 발생 확인
        for i in range(1, self.cross_window + 1):
            if ma_fast.iloc[-i-1] <= ma_slow.iloc[-i-1] and ma_fast.iloc[-i] > ma_slow.iloc[-i]:
                return True, i
        
        return False, -1
    
    def generate_signal(self, df: pd.DataFrame, ticker: str) -> Tuple[str, str, Dict]:
        """
        매매 신호 생성
        
        조건:
        1. 골든크로스 발생 (최근 3봉 이내)
        2. 거래량 증가 (1.3배 이상)
        3. MACD 양수 전환
        4. 현재가 > 20일 이평선
        
        Returns:
            (신호, 사유, 지표)
        """
        if not self.is_valid_data(df, self.slow_period + 10):
            return 'HOLD', 'Insufficient data', {}
        
        # 기술적 지표 계산
        current_price = df['close'].iloc[-1]
        
        # 이동평균
        ma_fast = self.calculate_moving_average(df, self.fast_period).iloc[-1]
        ma_slow = self.calculate_moving_average(df, self.slow_period).iloc[-1]
        
        # 골든크로스 감지
        is_golden_cross, bars_ago = self.detect_golden_cross(df)
        
        # 거래량
        volume_ratio = self.calculate_volume_ratio(df, self.slow_period)
        
        # MACD
        macd, signal, hist = self.calculate_macd(df)
        macd_positive = macd.iloc[-1] > 0 and signal.iloc[-1] > 0
        macd_hist_positive = hist.iloc[-1] > 0
        
        # RSI
        rsi = self.calculate_rsi(df).iloc[-1]
        
        # 현재가 vs 이평선
        price_above_ma = current_price > ma_slow
        
        # 추세 강도
        trend_strength = (ma_fast / ma_slow - 1) * 100
        
        # 지표 딕셔너리
        indicators = {
            'current_price': current_price,
            'ma_fast': ma_fast,
            'ma_slow': ma_slow,
            'is_golden_cross': is_golden_cross,
            'cross_bars_ago': bars_ago,
            'volume_ratio': volume_ratio,
            'macd_positive': macd_positive,
            'macd_hist_positive': macd_hist_positive,
            'rsi': rsi,
            'price_above_ma': price_above_ma,
            'trend_strength': trend_strength
        }
        
        # 골든크로스 매수 조건 체크
        golden_cross_ok = is_golden_cross and bars_ago <= self.cross_window
        volume_ok = volume_ratio >= self.volume_multiplier
        macd_ok = macd_positive or macd_hist_positive
        position_ok = price_above_ma
        
        if golden_cross_ok and volume_ok and macd_ok and position_ok:
            reason = f"골든크로스 | {self.fast_period}일×{self.slow_period}일 | {bars_ago}봉전 | 거래량{volume_ratio:.1f}배 | MACD↑"
            return 'BUY', reason, indicators
        
        # 추가 강화 조건 (강한 상승 추세)
        if golden_cross_ok and volume_ratio >= 1.0 and trend_strength > 2.0 and rsi < 70:
            reason = f"골든크로스(강화) | 추세강도{trend_strength:.1f}% | RSI{rsi:.0f}"
            return 'BUY', reason, indicators
        
        return 'HOLD', 'No golden cross signal', indicators
    
    def should_exit(self, entry_price: float, current_price: float, holding_duration: float = 0, market_snapshot=None) -> Tuple[bool, str]:
        """
        청산 여부 확인
        
        Args:
            entry_price: 진입 가격
            current_price: 현재 가격
            holding_duration: 보유 시간 (초)
            market_snapshot: 시장 스냅샷 (옵션)
        
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
        return f"Golden Cross Strategy (Fast: {self.fast_period}d, Slow: {self.slow_period}d)"
