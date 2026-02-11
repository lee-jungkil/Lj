"""
극공격적 단타 전략 (Aggressive Scalping)
짧은 시간 내 작은 가격 변동으로 수익 추구
AI 학습 기능 통합 - 경험을 통해 성장하는 전략
"""

from typing import Dict, Tuple, Optional
import pandas as pd
from .base_strategy import BaseStrategy


class AggressiveScalping(BaseStrategy):
    """극공격적 단타 전략 (AI 학습 통합)"""
    
    def __init__(self, config: Dict, learning_engine=None):
        super().__init__("AggressiveScalping", config)
        
        # AI 학습 엔진
        self.learning_engine = learning_engine
        
        # 전략 파라미터 (기본값)
        self.stop_loss = config.get('stop_loss', 0.02)  # 2%
        self.take_profit = config.get('take_profit', 0.015)  # 1.5%
        self.rsi_oversold = config.get('rsi_oversold', 30)
        self.rsi_overbought = config.get('rsi_overbought', 70)
        self.volume_threshold = config.get('volume_threshold', 1.5)
        self.min_price_change = config.get('min_price_change', 0.01)  # 1%
        
        # 학습된 파라미터 적용
        if self.learning_engine:
            optimized = self.learning_engine.get_optimized_params('AggressiveScalping')
            if optimized:
                self.stop_loss = optimized.get('stop_loss', self.stop_loss)
                self.take_profit = optimized.get('take_profit', self.take_profit)
                self.rsi_oversold = optimized.get('rsi_low', self.rsi_oversold)
                self.rsi_overbought = optimized.get('rsi_high', self.rsi_overbought)
                print(f"🎓 AI 최적화 파라미터 적용: AggressiveScalping")
                print(f"   손절: {self.stop_loss*100:.2f}% | 익절: {self.take_profit*100:.2f}%")
    
    def generate_signal(self, df: pd.DataFrame, ticker: str) -> Tuple[str, str, Dict]:
        """
        매매 신호 생성 (AI 학습 통합)
        
        조건:
        - RSI < 30 (과매도) 또는 RSI > 70 (과매수)
        - 5분봉 기준 1% 이상 급등/급락
        - 거래량 평균 대비 150% 이상
        - AI 분석: 과거 유사 상황에서의 성과 반영
        
        Returns:
            (신호, 사유, 지표)
        """
        if not self.enabled or not self.is_valid_data(df):
            return 'HOLD', 'Invalid data', {}
        
        # 기술적 지표 계산
        rsi = self.calculate_rsi(df)
        volume_ratio = self.calculate_volume_ratio(df)
        price_change = self.get_price_change(df, periods=1)
        bb_upper, bb_middle, bb_lower = self.calculate_bollinger_bands(df)
        
        current_rsi = rsi.iloc[-1]
        current_price = df['close'].iloc[-1]
        current_bb_lower = bb_lower.iloc[-1]
        current_bb_upper = bb_upper.iloc[-1]
        
        # 볼린저 밴드 내 위치 계산
        bb_position = (current_price - current_bb_lower) / (current_bb_upper - current_bb_lower) if (current_bb_upper - current_bb_lower) > 0 else 0.5
        
        indicators = {
            'rsi': current_rsi,
            'volume_ratio': volume_ratio,
            'price_change': price_change,
            'current_price': current_price,
            'bb_position': bb_position,
            'volatility': df['close'].pct_change().std() * 100 if len(df) > 1 else 0
        }
        
        # === AI 의사결정 분석 ===
        ai_decision = 'NEUTRAL'
        ai_confidence = 0.5
        ai_reason = ""
        
        if self.learning_engine:
            try:
                ai_decision, ai_confidence, ai_reason = self.learning_engine.analyze_market_decision(
                    ticker=ticker,
                    df=df,
                    strategy='AggressiveScalping',
                    current_indicators=indicators
                )
                
                # AI가 회피를 권고하는 경우
                if ai_decision == 'AVOID' and ai_confidence >= 0.7:
                    return 'HOLD', f"🧠 AI 회피 권고: {ai_reason}", indicators
                
            except Exception as e:
                # 학습 엔진 오류 시 기본 로직 사용
                pass
        
        # === 기본 매수 신호 ===
        basic_buy_signal = (
            current_rsi < self.rsi_oversold and 
            volume_ratio >= self.volume_threshold and
            abs(price_change) >= self.min_price_change
        )
        
        if basic_buy_signal:
            reason = f"과매도 + 거래량 급증 (RSI: {current_rsi:.1f}, 거래량: {volume_ratio:.2f}x, 변동: {price_change:+.2f}%)"
            
            # AI 강화 신호
            if ai_decision in ['STRONG_BUY', 'BUY'] and ai_confidence >= 0.65:
                reason += f" | 🧠 AI 확신: {ai_confidence*100:.0f}% ({ai_reason})"
                return 'BUY', reason, indicators
            
            # AI 중립이면 기본 신호 유지
            elif ai_decision == 'NEUTRAL' or not self.learning_engine:
                return 'BUY', reason, indicators
            
            # AI가 회의적이면 보류
            else:
                return 'HOLD', f"{reason} | ⚠️ AI 회의적 ({ai_reason})", indicators
        
        # === 매도 신호 (이미 보유 중일 때) ===
        if current_rsi > self.rsi_overbought:
            reason = f"과매수 영역 (RSI: {current_rsi:.1f})"
            return 'SELL', reason, indicators
        
        return 'HOLD', 'No clear signal', indicators
    
    def should_exit(self, entry_price: float, current_price: float, holding_duration: float = 0, market_snapshot=None) -> Tuple[bool, str]:
        """
        청산 여부 확인 (AI 학습 통합)
        
        Args:
            entry_price: 진입 가격
            current_price: 현재 가격
            holding_duration: 보유 시간 (초)
            market_snapshot: 현재 시장 상황
        
        Returns:
            (청산 여부, 사유)
        """
        profit_loss_ratio = (current_price - entry_price) / entry_price
        
        # === AI 청산 판단 ===
        if self.learning_engine and market_snapshot and holding_duration > 0:
            try:
                should_exit_ai, exit_reason, confidence = self.learning_engine.should_exit_position(
                    ticker='',  # ticker는 호출 시점에 전달
                    strategy='AggressiveScalping',
                    entry_price=entry_price,
                    current_price=current_price,
                    holding_duration=holding_duration,
                    market_snapshot=market_snapshot
                )
                
                # AI가 강하게 청산 권고하면 우선 적용
                if should_exit_ai and confidence >= 0.75:
                    return True, f"🧠 AI 청산 권고 (신뢰도: {confidence*100:.0f}%): {exit_reason}"
                
            except Exception as e:
                # 학습 엔진 오류 시 기본 로직 사용
                pass
        
        # === 기본 손절 ===
        if profit_loss_ratio <= -self.stop_loss:
            return True, f"손절 ({profit_loss_ratio*100:.2f}%)"
        
        # === 기본 익절 ===
        if profit_loss_ratio >= self.take_profit:
            return True, f"익절 ({profit_loss_ratio*100:.2f}%)"
        
        return False, "Hold position"
