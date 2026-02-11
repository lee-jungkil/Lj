"""
시장 상황 분석기
변동성, 추세, 거래량 등을 분석하여 시장 상태 분류
"""

import pandas as pd
import numpy as np
from typing import Tuple


def analyze_market_condition(df: pd.DataFrame, sentiment_score: float = 0.5) -> Tuple[str, str, str, str]:
    """
    시장 상황 분석
    
    Args:
        df: OHLCV 데이터프레임
        sentiment_score: 감정 점수 (0~1)
    
    Returns:
        (volatility, trend, volume, sentiment)
    """
    if df is None or df.empty or len(df) < 20:
        return 'medium', 'sideways', 'medium', 'neutral'
    
    # 1. 변동성 분석
    volatility = _analyze_volatility(df)
    
    # 2. 추세 분석
    trend = _analyze_trend(df)
    
    # 3. 거래량 분석
    volume = _analyze_volume(df)
    
    # 4. 감정 분석
    sentiment = _classify_sentiment(sentiment_score)
    
    return volatility, trend, volume, sentiment


def _analyze_volatility(df: pd.DataFrame) -> str:
    """
    변동성 분석
    
    Returns:
        'high', 'medium', 'low'
    """
    try:
        # ATR (Average True Range) 계산
        high = df['high']
        low = df['low']
        close = df['close']
        
        # True Range 계산
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(14).mean().iloc[-1]
        
        # 현재가 대비 ATR 비율
        current_price = close.iloc[-1]
        atr_ratio = (atr / current_price) * 100
        
        if atr_ratio > 3.0:
            return 'high'
        elif atr_ratio > 1.5:
            return 'medium'
        else:
            return 'low'
            
    except:
        return 'medium'


def _analyze_trend(df: pd.DataFrame) -> str:
    """
    추세 분석
    
    Returns:
        'uptrend', 'downtrend', 'sideways'
    """
    try:
        close = df['close']
        
        # 이동평균선
        ma20 = close.rolling(20).mean()
        ma50 = close.rolling(50).mean()
        
        current_price = close.iloc[-1]
        ma20_current = ma20.iloc[-1]
        ma50_current = ma50.iloc[-1]
        
        # 선형 회귀로 추세 강도 계산
        recent = close.tail(20).values
        x = np.arange(len(recent))
        slope = np.polyfit(x, recent, 1)[0]
        
        # 추세 분류
        if current_price > ma20_current > ma50_current and slope > 0:
            return 'uptrend'
        elif current_price < ma20_current < ma50_current and slope < 0:
            return 'downtrend'
        else:
            return 'sideways'
            
    except:
        return 'sideways'


def _analyze_volume(df: pd.DataFrame) -> str:
    """
    거래량 분석
    
    Returns:
        'high', 'medium', 'low'
    """
    try:
        volume = df['volume']
        
        # 최근 20봉 평균 거래량
        avg_volume = volume.rolling(20).mean().iloc[-1]
        
        # 현재 거래량
        current_volume = volume.iloc[-1]
        
        # 비율
        ratio = current_volume / avg_volume if avg_volume > 0 else 1.0
        
        if ratio > 1.5:
            return 'high'
        elif ratio > 0.7:
            return 'medium'
        else:
            return 'low'
            
    except:
        return 'medium'


def _classify_sentiment(score: float) -> str:
    """
    감정 점수 분류
    
    Args:
        score: 0~1 사이 점수
    
    Returns:
        'positive', 'neutral', 'negative'
    """
    if score > 0.6:
        return 'positive'
    elif score > 0.4:
        return 'neutral'
    else:
        return 'negative'


def get_market_description(volatility: str, trend: str, volume: str, sentiment: str) -> str:
    """
    시장 상황 설명 생성
    
    Returns:
        한글 설명
    """
    desc_map = {
        'volatility': {
            'high': '고변동성',
            'medium': '중변동성',
            'low': '저변동성'
        },
        'trend': {
            'uptrend': '상승 추세',
            'downtrend': '하락 추세',
            'sideways': '횡보 추세'
        },
        'volume': {
            'high': '고거래량',
            'medium': '보통거래량',
            'low': '저거래량'
        },
        'sentiment': {
            'positive': '긍정적 심리',
            'neutral': '중립적 심리',
            'negative': '부정적 심리'
        }
    }
    
    parts = [
        desc_map['volatility'][volatility],
        desc_map['trend'][trend],
        desc_map['volume'][volume],
        desc_map['sentiment'][sentiment]
    ]
    
    return " / ".join(parts)


def recommend_strategy_for_condition(volatility: str, trend: str, volume: str) -> str:
    """
    시장 상황에 따른 전략 추천 (경험 규칙)
    
    Returns:
        추천 전략 이름
    """
    # 고변동성 + 상승 = 공격적 단타
    if volatility == 'high' and trend == 'uptrend':
        return 'aggressive_scalping'
    
    # 고변동성 + 하락 = 평균회귀
    if volatility == 'high' and trend == 'downtrend':
        return 'mean_reversion'
    
    # 저변동성 + 횡보 = 그리드
    if volatility == 'low' and trend == 'sideways':
        return 'grid_trading'
    
    # 중변동성 + 횡보 = 보수적 단타
    if trend == 'sideways':
        return 'conservative_scalping'
    
    # 상승 추세 = 공격적
    if trend == 'uptrend':
        return 'aggressive_scalping'
    
    # 하락 추세 = 평균회귀
    if trend == 'downtrend':
        return 'mean_reversion'
    
    # 기본값
    return 'conservative_scalping'
