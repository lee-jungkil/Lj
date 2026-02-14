"""
초단타 전략 (Ultra Scalping) - 스마트 버전
급등/급락 감지 시 즉시 진입하는 공격적 전략

특징:
- 목표: 0.5~1% 빠른 수익
- 손절: -0.3~0.5% 빠른 손절
- 보유 시간: 1~5분
- 조건: 급등/급락 + 거래량 폭증
- 스마트 매도: 수익 시 추세 재확인 후 결정 🔄
"""

from typing import Dict, Tuple
import pandas as pd
from .base_strategy import BaseStrategy


class UltraScalping(BaseStrategy):
    """초단타 전략 (스마트 버전)"""
    
    def __init__(self, config: Dict):
        super().__init__("UltraScalping", config)
        
        # 초단타 전용 파라미터 (v6.30.20: 손절 강화 1% → 0.8%)
        self.stop_loss = config.get('stop_loss', 0.008)  # 0.8% 손절 (강화)
        self.take_profit = config.get('take_profit', 0.015)  # 1.5% 익절 (유지)
        self.min_price_surge = config.get('min_price_surge', 0.015)  # 1.5% 이상 급등 (완화)
        self.volume_spike = config.get('volume_spike', 2.0)  # 거래량 2배 이상 (완화)
        self.max_hold_time = config.get('max_hold_time', 300)  # 최대 5분 보유
        
        # ⭐ 스마트 매도 설정
        self.smart_exit = config.get('smart_exit', True)  # 스마트 매도 활성화
        self.profit_recheck_threshold = config.get('profit_recheck_threshold', 0.005)  # 0.5% 이상부터 재확인
        self.momentum_threshold = config.get('momentum_threshold', 0.001)  # 0.1% 모멘텀
    
    def generate_signal(self, df: pd.DataFrame, ticker: str) -> Tuple[str, str, Dict]:
        """
        초단타 매매 신호 생성
        
        조건:
        - 1분 이내 2% 이상 급등/급락
        - 거래량 평균 대비 3배 이상
        - RSI 극단값 (< 25 or > 75)
        
        Returns:
            (신호, 사유, 지표)
        """
        if not self.enabled or not self.is_valid_data(df):
            return 'HOLD', 'Invalid data', {}
        
        # 최근 1분 가격 변동 (5분봉의 마지막 캔들)
        price_change_1min = self.get_price_change(df, periods=1)
        
        # 거래량 급증 확인
        volume_ratio = self.calculate_volume_ratio(df)
        
        # RSI 계산
        rsi = self.calculate_rsi(df, period=6)  # 짧은 기간 RSI
        current_rsi = rsi.iloc[-1]
        
        current_price = df['close'].iloc[-1]
        
        indicators = {
            'price_change_1min': price_change_1min,
            'volume_ratio': volume_ratio,
            'rsi': current_rsi,
            'current_price': current_price
        }
        
        # 🔥 급등 + 거래량 폭증 감지 (매수) - 조건 완화
        if (abs(price_change_1min) >= self.min_price_surge and 
            volume_ratio >= self.volume_spike):
            
            # 급락 후 반등 (RSI < 35로 완화)
            if price_change_1min < 0 and current_rsi < 35:
                reason = (f"급락 후 반등 기회! "
                         f"(가격: {price_change_1min:+.2f}%, "
                         f"거래량: {volume_ratio:.1f}x, RSI: {current_rsi:.1f})")
                return 'BUY', reason, indicators
            
            # 급등 추격 매수 (RSI < 80으로 완화)
            elif price_change_1min > 0 and current_rsi < 80:
                reason = (f"급등 추격 진입! "
                         f"(가격: {price_change_1min:+.2f}%, "
                         f"거래량: {volume_ratio:.1f}x, RSI: {current_rsi:.1f})")
                return 'BUY', reason, indicators
        
        # 🔥 추가 진입 조건: 거래량만 폭증 (가격 변동 1% 이상)
        if (abs(price_change_1min) >= 0.01 and  # 1% 이상
            volume_ratio >= 2.5):  # 거래량 2.5배 이상
            
            if price_change_1min > 0 and 40 < current_rsi < 75:  # 상승 + 중립~과매수 직전
                reason = (f"거래량 폭증 진입! "
                         f"(가격: {price_change_1min:+.2f}%, "
                         f"거래량: {volume_ratio:.1f}x, RSI: {current_rsi:.1f})")
                return 'BUY', reason, indicators
        
        # 🔥 과매수 영역 (매도)
        if current_rsi > 80:
            reason = f"과매수 청산 (RSI: {current_rsi:.1f})"
            return 'SELL', reason, indicators
        
        return 'HOLD', 'No ultra signal', indicators
    
    def should_exit(self, entry_price: float, current_price: float, hold_time: float = 0, 
                    price_history: list = None) -> Tuple[bool, str]:
        """
        청산 여부 확인 (초단타 전용 - 스마트 버전)
        
        Args:
            entry_price: 진입 가격
            current_price: 현재 가격
            hold_time: 보유 시간 (초)
            price_history: 최근 가격 이력 (스마트 판단용, 선택적)
        
        Returns:
            (청산 여부, 사유)
        """
        profit_loss_ratio = (current_price - entry_price) / entry_price
        
        # 빠른 손절 (0.8%) - 무조건! (v6.30.21: 디버그 로그)
        if profit_loss_ratio <= -self.stop_loss:
            return True, f"초단타 손절 ({profit_loss_ratio*100:.2f}%)"
        
        # ⭐ 스마트 익절 로직 (v6.30.21: price_history None 처리 추가)
        if profit_loss_ratio >= self.profit_recheck_threshold:  # 0.5% 이상 수익
            # price_history가 있을 때만 스마트 로직 실행
            if self.smart_exit and price_history is not None and len(price_history) >= 3:
                # 추세 분석
                trend_decision = self._analyze_profit_trend(
                    entry_price, 
                    current_price, 
                    price_history, 
                    profit_loss_ratio
                )
                
                if trend_decision['should_exit']:
                    return True, trend_decision['reason']
                else:
                    # 추세 지속 중 - 홀딩 계속
                    return False, trend_decision['reason']
            
            # 기본 익절 (1.5%) 또는 price_history 없을 때
            elif profit_loss_ratio >= self.take_profit:
                return True, f"초단타 익절 ({profit_loss_ratio*100:.2f}%)"
        
        # 시간 초과 (5분)
        if hold_time >= self.max_hold_time:
            return True, f"시간 초과 청산 (보유: {hold_time:.0f}초, {profit_loss_ratio*100:+.2f}%)"
        
        # 소폭 손실 + 시간 경과 (3분 + -0.2%)
        if hold_time >= 180 and profit_loss_ratio <= -0.002:
            return True, f"시간손실 청산 (3분 경과, {profit_loss_ratio*100:+.2f}%)"
        
        return False, "Hold position"
    
    def _analyze_profit_trend(self, entry_price: float, current_price: float, 
                              price_history: list, current_profit: float) -> Dict:
        """
        수익 상태에서 추세 분석 (매도 vs 홀딩 판단)
        
        Args:
            entry_price: 진입가
            current_price: 현재가
            price_history: 최근 가격 이력 [p1, p2, p3, ...] (시간 순)
            current_profit: 현재 수익률
        
        Returns:
            {'should_exit': bool, 'reason': str}
        """
        # 최근 3~5개 가격으로 추세 판단
        recent_prices = price_history[-5:] if len(price_history) >= 5 else price_history[-3:]
        
        if len(recent_prices) < 2:
            # 데이터 부족 - 기본 익절
            if current_profit >= self.take_profit:
                return {
                    'should_exit': True,
                    'reason': f"데이터 부족 익절 ({current_profit*100:.2f}%)"
                }
            return {'should_exit': False, 'reason': "데이터 수집 중"}
        
        # 1. 모멘텀 분석 (최근 추세)
        price_changes = []
        for i in range(1, len(recent_prices)):
            change = (recent_prices[i] - recent_prices[i-1]) / recent_prices[i-1]
            price_changes.append(change)
        
        avg_momentum = sum(price_changes) / len(price_changes)
        last_momentum = price_changes[-1] if price_changes else 0
        
        # 2. 최고가 대비 하락 확인
        max_price = max(price_history)
        drawdown_from_peak = (current_price - max_price) / max_price
        
        # 3. 진입가 대비 상승폭
        total_gain = current_profit
        
        # ⭐ 매도 조건 (추세 꺾임 감지)
        
        # 조건 1: 최고가에서 0.3% 이상 하락 (고점 대비 하락)
        if drawdown_from_peak <= -0.003:  # -0.3%
            return {
                'should_exit': True,
                'reason': f"고점 하락 매도 (고점 대비 {drawdown_from_peak*100:.2f}%, 수익 {total_gain*100:.2f}%)"
            }
        
        # 조건 2: 음의 모멘텀 + 수익 0.7% 이상 (추세 반전)
        if avg_momentum < -self.momentum_threshold and total_gain >= 0.007:
            return {
                'should_exit': True,
                'reason': f"추세 반전 매도 (모멘텀 {avg_momentum*100:.2f}%, 수익 {total_gain*100:.2f}%)"
            }
        
        # 조건 3: 2% 이상 수익 + 최근 하락 (고수익 확정)
        if total_gain >= 0.02 and last_momentum < -0.001:
            return {
                'should_exit': True,
                'reason': f"고수익 확정 매도 (수익 {total_gain*100:.2f}%, 최근 하락 중)"
            }
        
        # 조건 4: 기본 익절 목표 달성 + 모멘텀 약화
        if total_gain >= self.take_profit and avg_momentum < self.momentum_threshold * 0.5:
            return {
                'should_exit': True,
                'reason': f"목표 달성 매도 (수익 {total_gain*100:.2f}%, 모멘텀 약화)"
            }
        
        # ⭐ 홀딩 조건 (추세 지속 중)
        
        # 조건 1: 양의 모멘텀 + 수익 (상승 추세 지속)
        if avg_momentum > self.momentum_threshold:
            return {
                'should_exit': False,
                'reason': f"상승 추세 홀딩 (모멘텀 +{avg_momentum*100:.2f}%, 수익 {total_gain*100:.2f}%)"
            }
        
        # 조건 2: 고점 근처 + 횡보 (추가 상승 대기)
        if abs(drawdown_from_peak) < 0.001 and abs(avg_momentum) < self.momentum_threshold:
            return {
                'should_exit': False,
                'reason': f"고점 횡보 홀딩 (고점 유지, 수익 {total_gain*100:.2f}%)"
            }
        
        # 기본: 목표 미달 시 홀딩
        if total_gain < self.take_profit:
            return {
                'should_exit': False,
                'reason': f"목표 미달 홀딩 (수익 {total_gain*100:.2f}%, 목표 {self.take_profit*100:.1f}%)"
            }
        
        # 애매한 상황: 기본 익절
        return {
            'should_exit': True,
            'reason': f"기본 익절 ({total_gain*100:.2f}%)"
        }
