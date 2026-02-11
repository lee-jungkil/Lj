"""
매매 전략 베이스 클래스
모든 전략이 상속받는 추상 클래스
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional, Tuple
import pandas as pd
import numpy as np


class BaseStrategy(ABC):
    """전략 베이스 클래스"""
    
    def __init__(self, name: str, config: Dict):
        """
        초기화
        
        Args:
            name: 전략 이름
            config: 전략 설정
        """
        self.name = name
        self.config = config
        self.enabled = config.get('enabled', True)
    
    @abstractmethod
    def generate_signal(self, df: pd.DataFrame, ticker: str) -> Tuple[str, str, Dict]:
        """
        매매 신호 생성
        
        Args:
            df: OHLCV 데이터프레임
            ticker: 코인 티커
        
        Returns:
            (신호, 사유, 지표) 튜플
            - 신호: 'BUY', 'SELL', 'HOLD'
            - 사유: 매매 사유
            - 지표: 기술적 지표 딕셔너리
        """
        pass
    
    @abstractmethod
    def should_exit(self, entry_price: float, current_price: float) -> Tuple[bool, str]:
        """
        청산 여부 확인
        
        Args:
            entry_price: 진입 가격
            current_price: 현재 가격
        
        Returns:
            (청산 여부, 사유)
        """
        pass
    
    def calculate_rsi(self, df: pd.DataFrame, period: int = 14) -> pd.Series:
        """
        RSI (Relative Strength Index) 계산
        
        Args:
            df: OHLCV 데이터프레임
            period: RSI 기간
        
        Returns:
            RSI 시리즈
        """
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_bollinger_bands(self, df: pd.DataFrame, period: int = 20, std: float = 2.0) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        볼린저 밴드 계산
        
        Args:
            df: OHLCV 데이터프레임
            period: 이동평균 기간
            std: 표준편차 배수
        
        Returns:
            (상단, 중단, 하단) 튜플
        """
        middle = df['close'].rolling(window=period).mean()
        std_dev = df['close'].rolling(window=period).std()
        
        upper = middle + (std_dev * std)
        lower = middle - (std_dev * std)
        
        return upper, middle, lower
    
    def calculate_macd(self, df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        MACD 계산
        
        Args:
            df: OHLCV 데이터프레임
            fast: 빠른 EMA 기간
            slow: 느린 EMA 기간
            signal: 시그널 기간
        
        Returns:
            (MACD, Signal, Histogram) 튜플
        """
        exp1 = df['close'].ewm(span=fast, adjust=False).mean()
        exp2 = df['close'].ewm(span=slow, adjust=False).mean()
        
        macd = exp1 - exp2
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        histogram = macd - signal_line
        
        return macd, signal_line, histogram
    
    def calculate_moving_average(self, df: pd.DataFrame, period: int) -> pd.Series:
        """
        이동평균 계산
        
        Args:
            df: OHLCV 데이터프레임
            period: 기간
        
        Returns:
            이동평균 시리즈
        """
        return df['close'].rolling(window=period).mean()
    
    def calculate_volume_ratio(self, df: pd.DataFrame, period: int = 20) -> float:
        """
        거래량 비율 계산 (현재 거래량 / 평균 거래량)
        
        Args:
            df: OHLCV 데이터프레임
            period: 평균 기간
        
        Returns:
            거래량 비율
        """
        if len(df) < period:
            return 1.0
        
        avg_volume = df['volume'].iloc[-period:].mean()
        current_volume = df['volume'].iloc[-1]
        
        if avg_volume == 0:
            return 1.0
        
        return current_volume / avg_volume
    
    def get_price_change(self, df: pd.DataFrame, periods: int = 1) -> float:
        """
        가격 변동률 계산
        
        Args:
            df: OHLCV 데이터프레임
            periods: 기간
        
        Returns:
            변동률 (%)
        """
        if len(df) < periods + 1:
            return 0.0
        
        current_price = df['close'].iloc[-1]
        prev_price = df['close'].iloc[-(periods + 1)]
        
        if prev_price == 0:
            return 0.0
        
        return ((current_price - prev_price) / prev_price) * 100
    
    def get_volatility(self, df: pd.DataFrame, period: int = 20) -> float:
        """
        변동성 계산 (표준편차 기반)
        
        Args:
            df: OHLCV 데이터프레임
            period: 기간
        
        Returns:
            변동성 (%)
        """
        if len(df) < period:
            return 0.0
        
        returns = df['close'].pct_change().iloc[-period:]
        volatility = returns.std() * 100
        
        return volatility
    
    def is_valid_data(self, df: pd.DataFrame, min_length: int = 50) -> bool:
        """
        데이터 유효성 검사
        
        Args:
            df: OHLCV 데이터프레임
            min_length: 최소 길이
        
        Returns:
            유효 여부
        """
        if df is None or df.empty:
            return False
        
        if len(df) < min_length:
            return False
        
        if df['close'].iloc[-1] == 0:
            return False
        
        return True
    
    def __str__(self):
        return f"{self.name} Strategy"
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(name='{self.name}', enabled={self.enabled})>"
