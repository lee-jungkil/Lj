"""
더블바텀 매수 전략 (Double Bottom Strategy)
W자 패턴 형성 후 넥라인 돌파
"""

from typing import Dict, Tuple
import pandas as pd
import numpy as np
from .base_strategy import BaseStrategy


class DoubleBottomStrategy(BaseStrategy):
    """더블바텀 매수 전략"""
    
    def __init__(self, config: Dict):
        """
        초기화
        
        Args:
            config: 전략 설정
        """
        super().__init__('DOUBLE_BOTTOM', config)
        
        # 전략 파라미터
        self.lookback_period = config.get('lookback_period', 30)  # 패턴 확인 기간
        self.bottom_tolerance = config.get('bottom_tolerance', 0.02)  # 저점 오차 2%
        self.volume_multiplier = config.get('volume_multiplier', 1.8)  # 거래량 배수
        self.rsi_min = config.get('rsi_min', 40)  # RSI 하한 (과매도 탈출)
        self.take_profit = config.get('take_profit', 0.07)  # 익절 7%
        self.stop_loss = config.get('stop_loss', -0.03)  # 손절 -3%
    
    def detect_double_bottom(self, df: pd.DataFrame) -> Tuple[bool, float, float, float]:
        """
        더블바텀 패턴 감지
        
        Args:
            df: OHLCV 데이터프레임
        
        Returns:
            (패턴 발생 여부, 첫번째 저점, 두번째 저점, 넥라인)
        """
        if len(df) < self.lookback_period:
            return False, 0.0, 0.0, 0.0
        
        # 최근 기간 데이터
        recent_df = df.iloc[-self.lookback_period:]
        lows = recent_df['low'].values
        highs = recent_df['high'].values
        
        # 최저점 2개 찾기 (충분히 떨어져 있어야 함)
        min_distance = max(5, self.lookback_period // 6)  # 최소 간격
        
        # 첫 번째 저점 찾기
        first_bottom_idx = lows[:self.lookback_period//2].argmin()
        first_bottom = lows[first_bottom_idx]
        
        # 두 번째 저점 찾기 (첫 번째 이후)
        search_start = first_bottom_idx + min_distance
        if search_start >= len(lows):
            return False, 0.0, 0.0, 0.0
        
        second_bottom_idx = search_start + lows[search_start:].argmin()
        second_bottom = lows[second_bottom_idx]
        
        # 두 저점이 비슷한지 확인 (오차 범위 내)
        if abs(first_bottom - second_bottom) / first_bottom > self.bottom_tolerance:
            return False, 0.0, 0.0, 0.0
        
        # 넥라인 찾기 (두 저점 사이의 최고점)
        neckline_idx = first_bottom_idx + highs[first_bottom_idx:second_bottom_idx+1].argmax()
        neckline = highs[neckline_idx]
        
        # 넥라인이 저점보다 충분히 높아야 함 (최소 1%)
        if (neckline - first_bottom) / first_bottom < 0.01:
            return False, 0.0, 0.0, 0.0
        
        return True, first_bottom, second_bottom, neckline
    
    def generate_signal(self, df: pd.DataFrame, ticker: str) -> Tuple[str, str, Dict]:
        """
        매매 신호 생성
        
        조건:
        1. 더블바텀 패턴 형성
        2. 넥라인 돌파
        3. 거래량 1.8배 이상
        4. RSI > 40 (과매도 탈출)
        
        Returns:
            (신호, 사유, 지표)
        """
        if not self.is_valid_data(df, self.lookback_period + 10):
            return 'HOLD', 'Insufficient data', {}
        
        # 기술적 지표 계산
        current_price = df['close'].iloc[-1]
        
        # 더블바텀 감지
        has_pattern, first_bottom, second_bottom, neckline = self.detect_double_bottom(df)
        
        # 넥라인 돌파 여부
        neckline_breakout = current_price > neckline if has_pattern else False
        
        # 거래량
        volume_ratio = self.calculate_volume_ratio(df)
        
        # RSI
        rsi = self.calculate_rsi(df).iloc[-1]
        rsi_recovered = rsi > self.rsi_min
        
        # MACD
        macd, signal, hist = self.calculate_macd(df)
        macd_bullish = hist.iloc[-1] > 0
        macd_turning = hist.iloc[-1] > hist.iloc[-2]
        
        # 20일 이동평균
        ma_20 = self.calculate_moving_average(df, 20).iloc[-1]
        
        # 패턴 깊이 (저점 대비 현재가 상승률)
        if has_pattern and second_bottom > 0:
            pattern_depth = (current_price - second_bottom) / second_bottom * 100
        else:
            pattern_depth = 0.0
        
        # 넥라인 돌파 강도
        if has_pattern and neckline > 0:
            breakout_strength = (current_price / neckline - 1) * 100
        else:
            breakout_strength = 0.0
        
        # 지표 딕셔너리
        indicators = {
            'current_price': current_price,
            'has_pattern': has_pattern,
            'first_bottom': first_bottom,
            'second_bottom': second_bottom,
            'neckline': neckline,
            'neckline_breakout': neckline_breakout,
            'breakout_strength': breakout_strength,
            'pattern_depth': pattern_depth,
            'volume_ratio': volume_ratio,
            'rsi': rsi,
            'rsi_recovered': rsi_recovered,
            'macd_bullish': macd_bullish,
            'macd_turning': macd_turning
        }
        
        # 더블바텀 매수 조건 체크
        pattern_ok = has_pattern and neckline_breakout
        volume_ok = volume_ratio >= self.volume_multiplier
        rsi_ok = rsi_recovered
        momentum_ok = macd_turning or macd_bullish
        
        if pattern_ok and volume_ok and rsi_ok and momentum_ok:
            reason = f"더블바텀 | 넥라인돌파 {breakout_strength:.2f}% | 패턴깊이{pattern_depth:.1f}% | 거래량{volume_ratio:.1f}배 | RSI{rsi:.0f}"
            return 'BUY', reason, indicators
        
        # 추가 강화 조건 (강한 돌파)
        if has_pattern and neckline_breakout and breakout_strength > 1.0 and volume_ratio >= 1.5 and rsi > 35:
            reason = f"더블바텀(강화) | 강한돌파{breakout_strength:.2f}% | 거래량{volume_ratio:.1f}배"
            return 'BUY', reason, indicators
        
        return 'HOLD', 'No double bottom signal', indicators
    
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
        return f"Double Bottom Strategy (Lookback: {self.lookback_period}d, Tolerance: {self.bottom_tolerance*100:.0f}%)"
