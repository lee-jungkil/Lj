"""
보수적 단타 전략 (Conservative Scalping)
안정적인 작은 수익 누적
AI 학습 기능 통합 - 경험을 통해 성장하는 전략
"""

from typing import Dict, Tuple
import pandas as pd
from .base_strategy import BaseStrategy


class ConservativeScalping(BaseStrategy):
    """보수적 단타 전략 (AI 학습 통합)"""
    
    def __init__(self, config: Dict, learning_engine=None):
        super().__init__("ConservativeScalping", config)
        
        # AI 학습 엔진
        self.learning_engine = learning_engine
        
        # 전략 파라미터 (기본값)
        self.stop_loss = config.get('stop_loss', 0.015)  # 1.5%
        self.take_profit = config.get('take_profit', 0.01)  # 1%
        self.rsi_min = config.get('rsi_min', 40)
        self.rsi_max = config.get('rsi_max', 60)
        self.bb_threshold = config.get('bb_threshold', 0.95)  # 볼린저 밴드 하단 95%
        
        # 학습된 파라미터 적용
        if self.learning_engine:
            optimized = self.learning_engine.get_optimized_params('ConservativeScalping')
            if optimized:
                self.stop_loss = optimized.get('stop_loss', self.stop_loss)
                self.take_profit = optimized.get('take_profit', self.take_profit)
                self.rsi_min = optimized.get('rsi_low', self.rsi_min)
                self.rsi_max = optimized.get('rsi_high', self.rsi_max)
                print(f"🎓 AI 최적화 파라미터 적용: ConservativeScalping")
    
    def generate_signal(self, df: pd.DataFrame, ticker: str) -> Tuple[str, str, Dict]:
        """
        매매 신호 생성 (AI 학습 통합)
        
        조건:
        - RSI 40-60 (중립 구간)
        - 볼린저 밴드 하단 근접 시 매수
        - 거래량 안정적
        - AI 분석: 과거 유사 상황에서의 성과 반영
        
        Returns:
            (신호, 사유, 지표)
        """
        if not self.enabled or not self.is_valid_data(df):
            return 'HOLD', 'Invalid data', {}
        
        # 기술적 지표 계산
        rsi = self.calculate_rsi(df)
        bb_upper, bb_middle, bb_lower = self.calculate_bollinger_bands(df)
        volume_ratio = self.calculate_volume_ratio(df)
        
        current_rsi = rsi.iloc[-1]
        current_price = df['close'].iloc[-1]
        current_bb_lower = bb_lower.iloc[-1]
        current_bb_upper = bb_upper.iloc[-1]
        current_bb_middle = bb_middle.iloc[-1]
        
        # 볼린저 밴드 내 위치 계산 (0 = 하단, 1 = 상단)
        bb_position = (current_price - current_bb_lower) / (current_bb_upper - current_bb_lower) if (current_bb_upper - current_bb_lower) > 0 else 0.5
        
        indicators = {
            'rsi': current_rsi,
            'bb_position': bb_position,
            'bb_lower': current_bb_lower,
            'bb_middle': current_bb_middle,
            'bb_upper': current_bb_upper,
            'current_price': current_price,
            'volume_ratio': volume_ratio,
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
                    strategy='ConservativeScalping',
                    current_indicators=indicators
                )
                
                if ai_decision == 'AVOID' and ai_confidence >= 0.7:
                    return 'HOLD', f"🧠 AI 회피 권고: {ai_reason}", indicators
                    
            except Exception:
                pass
        
        # === 기본 매수 신호 ===
        basic_buy = (self.rsi_min <= current_rsi <= self.rsi_max and 
                     bb_position <= (1 - self.bb_threshold))
        
        if basic_buy:
            reason = f"볼린저 하단 근접 + RSI 중립 (BB위치: {bb_position:.2f}, RSI: {current_rsi:.1f})"
            
            if ai_decision in ['STRONG_BUY', 'BUY'] and ai_confidence >= 0.65:
                reason += f" | 🧠 AI 확신: {ai_confidence*100:.0f}%"
            
            return 'BUY', reason, indicators
        
        # === 매도 신호 ===
        if bb_position >= self.bb_threshold:
            reason = f"볼린저 상단 근접 (BB위치: {bb_position:.2f})"
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
                    ticker='',
                    strategy='ConservativeScalping',
                    entry_price=entry_price,
                    current_price=current_price,
                    holding_duration=holding_duration,
                    market_snapshot=market_snapshot
                )
                
                if should_exit_ai and confidence >= 0.75:
                    return True, f"🧠 AI 청산 권고: {exit_reason}"
                    
            except Exception:
                pass
        
        # === 기본 손절/익절 ===
        if profit_loss_ratio <= -self.stop_loss:
            return True, f"손절 ({profit_loss_ratio*100:.2f}%)"
        
        if profit_loss_ratio >= self.take_profit:
            return True, f"익절 ({profit_loss_ratio*100:.2f}%)"
        
        return False, "Hold position"
