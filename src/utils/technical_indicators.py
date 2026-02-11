"""
간단한 기술적 분석 유틸리티
pandas만 사용하여 기본적인 지표 계산
"""

import pandas as pd
import numpy as np


def calculate_rsi(df: pd.DataFrame, period: int = 14, price_col: str = 'close') -> pd.Series:
    """
    RSI (Relative Strength Index) 계산
    
    Args:
        df: OHLCV 데이터프레임
        period: RSI 기간 (기본값: 14)
        price_col: 가격 컬럼명 (기본값: 'close')
    
    Returns:
        RSI 시리즈
    """
    delta = df[price_col].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


def calculate_sma(df: pd.DataFrame, period: int = 20, price_col: str = 'close') -> pd.Series:
    """
    SMA (Simple Moving Average) 계산
    
    Args:
        df: OHLCV 데이터프레임
        period: 이동평균 기간 (기본값: 20)
        price_col: 가격 컬럼명 (기본값: 'close')
    
    Returns:
        SMA 시리즈
    """
    return df[price_col].rolling(window=period).mean()


def calculate_ema(df: pd.DataFrame, period: int = 20, price_col: str = 'close') -> pd.Series:
    """
    EMA (Exponential Moving Average) 계산
    
    Args:
        df: OHLCV 데이터프레임
        period: 이동평균 기간 (기본값: 20)
        price_col: 가격 컬럼명 (기본값: 'close')
    
    Returns:
        EMA 시리즈
    """
    return df[price_col].ewm(span=period, adjust=False).mean()


def calculate_bollinger_bands(df: pd.DataFrame, period: int = 20, std_dev: int = 2, 
                               price_col: str = 'close') -> tuple:
    """
    볼린저 밴드 계산
    
    Args:
        df: OHLCV 데이터프레임
        period: 이동평균 기간 (기본값: 20)
        std_dev: 표준편차 배수 (기본값: 2)
        price_col: 가격 컬럼명 (기본값: 'close')
    
    Returns:
        (상단밴드, 중간밴드, 하단밴드) 튜플
    """
    sma = calculate_sma(df, period, price_col)
    std = df[price_col].rolling(window=period).std()
    
    upper_band = sma + (std * std_dev)
    lower_band = sma - (std * std_dev)
    
    return upper_band, sma, lower_band


def calculate_macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9,
                   price_col: str = 'close') -> tuple:
    """
    MACD (Moving Average Convergence Divergence) 계산
    
    Args:
        df: OHLCV 데이터프레임
        fast: 빠른 EMA 기간 (기본값: 12)
        slow: 느린 EMA 기간 (기본값: 26)
        signal: 시그널 라인 기간 (기본값: 9)
        price_col: 가격 컬럼명 (기본값: 'close')
    
    Returns:
        (MACD, Signal, Histogram) 튜플
    """
    ema_fast = calculate_ema(df, fast, price_col)
    ema_slow = calculate_ema(df, slow, price_col)
    
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    
    return macd_line, signal_line, histogram


def calculate_stochastic(df: pd.DataFrame, period: int = 14, smooth_k: int = 3,
                         smooth_d: int = 3) -> tuple:
    """
    스토캐스틱 오실레이터 계산
    
    Args:
        df: OHLCV 데이터프레임
        period: 기간 (기본값: 14)
        smooth_k: %K 스무딩 (기본값: 3)
        smooth_d: %D 스무딩 (기본값: 3)
    
    Returns:
        (%K, %D) 튜플
    """
    low_min = df['low'].rolling(window=period).min()
    high_max = df['high'].rolling(window=period).max()
    
    k = 100 * (df['close'] - low_min) / (high_max - low_min)
    k = k.rolling(window=smooth_k).mean()
    d = k.rolling(window=smooth_d).mean()
    
    return k, d


def calculate_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    ATR (Average True Range) 계산
    
    Args:
        df: OHLCV 데이터프레임
        period: 기간 (기본값: 14)
    
    Returns:
        ATR 시리즈
    """
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())
    
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = true_range.rolling(window=period).mean()
    
    return atr


def calculate_obv(df: pd.DataFrame) -> pd.Series:
    """
    OBV (On Balance Volume) 계산
    
    Args:
        df: OHLCV 데이터프레임
    
    Returns:
        OBV 시리즈
    """
    obv = (np.sign(df['close'].diff()) * df['volume']).fillna(0).cumsum()
    return obv


def calculate_momentum(df: pd.DataFrame, period: int = 10, price_col: str = 'close') -> pd.Series:
    """
    모멘텀 계산
    
    Args:
        df: OHLCV 데이터프레임
        period: 기간 (기본값: 10)
        price_col: 가격 컬럼명 (기본값: 'close')
    
    Returns:
        모멘텀 시리즈
    """
    return df[price_col].diff(period)


def calculate_roc(df: pd.DataFrame, period: int = 12, price_col: str = 'close') -> pd.Series:
    """
    ROC (Rate of Change) 계산
    
    Args:
        df: OHLCV 데이터프레임
        period: 기간 (기본값: 12)
        price_col: 가격 컬럼명 (기본값: 'close')
    
    Returns:
        ROC 시리즈 (%)
    """
    roc = ((df[price_col] - df[price_col].shift(period)) / df[price_col].shift(period)) * 100
    return roc


def add_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    모든 기술적 지표를 데이터프레임에 추가
    
    Args:
        df: OHLCV 데이터프레임
    
    Returns:
        지표가 추가된 데이터프레임
    """
    df = df.copy()
    
    # RSI
    df['rsi'] = calculate_rsi(df)
    
    # 이동평균
    df['sma_20'] = calculate_sma(df, 20)
    df['sma_50'] = calculate_sma(df, 50)
    df['ema_12'] = calculate_ema(df, 12)
    df['ema_26'] = calculate_ema(df, 26)
    
    # 볼린저 밴드
    df['bb_upper'], df['bb_middle'], df['bb_lower'] = calculate_bollinger_bands(df)
    
    # MACD
    df['macd'], df['macd_signal'], df['macd_hist'] = calculate_macd(df)
    
    # 스토캐스틱
    df['stoch_k'], df['stoch_d'] = calculate_stochastic(df)
    
    # ATR
    df['atr'] = calculate_atr(df)
    
    # OBV
    df['obv'] = calculate_obv(df)
    
    # 모멘텀
    df['momentum'] = calculate_momentum(df)
    
    # ROC
    df['roc'] = calculate_roc(df)
    
    return df


# 편의 함수: 빠른 지표 계산
def quick_indicators(df: pd.DataFrame) -> dict:
    """
    주요 지표를 빠르게 계산하여 딕셔너리로 반환
    
    Args:
        df: OHLCV 데이터프레임
    
    Returns:
        지표 딕셔너리
    """
    if len(df) < 50:
        return {}
    
    latest = df.iloc[-1]
    
    indicators = {
        'rsi': calculate_rsi(df).iloc[-1],
        'sma_20': calculate_sma(df, 20).iloc[-1],
        'current_price': latest['close'],
        'volume': latest['volume'],
    }
    
    # 볼린저 밴드
    bb_upper, bb_middle, bb_lower = calculate_bollinger_bands(df)
    indicators['bb_position'] = (latest['close'] - bb_lower.iloc[-1]) / (bb_upper.iloc[-1] - bb_lower.iloc[-1])
    
    # MACD
    macd, signal, hist = calculate_macd(df)
    indicators['macd_signal'] = 'bullish' if hist.iloc[-1] > 0 else 'bearish'
    
    return indicators
