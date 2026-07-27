"""
수익 최적화 전략 (Profit-Optimized Strategy)
==============================================

검증된 스캘핑 원칙:
1. 거래량 급증 + 가격 모멘텀 확인
2. 빠른 진입/청산 (목표: 0.3-0.8%)
3. 엄격한 손절 (-0.5%)
4. 시간 제한 (최대 300초, 5분)
5. 포지션 관리 (기본 5개, 최대 10개)
"""

import time
from typing import Dict, Any, Optional, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ProfitOptimizedStrategy:
    """수익 창출에 최적화된 스캘핑 전략"""
    
    def __init__(self):
        # 진입 조건
        self.volume_spike_threshold = 2.5  # 평균 대비 2.5배 이상
        self.price_momentum_min = 0.15  # 최소 0.15% 상승 중
        self.price_momentum_max = 1.5   # 최대 1.5% (과열 방지)
        
        # 청산 조건
        self.quick_profit_target = 0.3  # 빠른 익절: 0.3%
        self.target_profit = 0.5        # 목표 익절: 0.5%
        self.trailing_profit = 0.8      # 트레일링 시작: 0.8%
        self.trailing_stop = 0.15       # 트레일링 하락폭: 0.15%
        
        self.stop_loss = -0.5           # 손절: -0.5%
        self.time_based_exit = 300      # 시간 청산: 300초 (5분)
        self.time_exit_min_profit = 0.2 # 시간청산 최소 익절: 0.2%
        
        # 상태 추적
        self.max_profit_seen = {}       # 각 포지션의 최고 수익률
        self.entry_times = {}            # 진입 시간
        
    def should_enter(self, ticker: str, market_data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        진입 조건 검사
        
        Returns:
            (진입여부, 이유)
        """
        try:
            # 1. 거래량 급증 확인
            current_volume = market_data.get('current_volume', 0)
            avg_volume = market_data.get('avg_volume_5m', 0)
            
            if avg_volume <= 0:
                return False, "평균 거래량 데이터 없음"
            
            volume_ratio = current_volume / avg_volume
            
            if volume_ratio < self.volume_spike_threshold:
                return False, f"거래량 부족 ({volume_ratio:.2f}x < {self.volume_spike_threshold}x)"
            
            # 2. 가격 모멘텀 확인
            price_change_1m = market_data.get('price_change_1m', 0)
            
            if price_change_1m < self.price_momentum_min:
                return False, f"모멘텀 부족 ({price_change_1m:.2f}% < {self.price_momentum_min}%)"
            
            if price_change_1m > self.price_momentum_max:
                return False, f"과열 상태 ({price_change_1m:.2f}% > {self.price_momentum_max}%)"
            
            # 3. RSI 과매수 확인 (70 이하)
            rsi = market_data.get('rsi', 50)
            if rsi > 70:
                return False, f"RSI 과매수 ({rsi:.1f} > 70)"
            
            # 4. 매도벽 확인 (호가창)
            sell_pressure = market_data.get('sell_pressure', 1.0)
            if sell_pressure > 1.5:  # 매도벽이 매수벽보다 1.5배 큼
                return False, f"강한 매도벽 ({sell_pressure:.2f}x)"
            
            # 5. 볼린저 밴드 + 스토캐스틱 확인 (과매도 반등)
            # 5-1. 볼린저 밴드 하단 근처 (±5%)
            bb_lower = market_data.get('bb_lower', 0)
            current_price = market_data.get('current_price', 0)
            
            if bb_lower > 0 and current_price > 0:
                bb_position_pct = ((current_price - bb_lower) / bb_lower) * 100
                if not (-5 <= bb_position_pct <= 5):
                    return False, f"BB 위치 부적절 ({bb_position_pct:.1f}%, 하단 ±5% 필요)"
            else:
                # BB 데이터 없으면 이 조건 스킵
                pass
            
            # 5-2. 스토캐스틱 과매도 탈출 (20-40 구간 & 상승 중)
            stoch_k = market_data.get('stoch_k', 50)
            stoch_d = market_data.get('stoch_d', 50)
            
            if not (20 < stoch_k < 40 and stoch_k > stoch_d):
                return False, f"Stoch 부적절 (K:{stoch_k:.1f}, D:{stoch_d:.1f}, 20-40 & K>D 필요)"
            
            # 모든 조건 통과 (6가지)
            reason = f"✅ 진입! 거래량:{volume_ratio:.2f}x, 모멘텀:{price_change_1m:.2f}%, RSI:{rsi:.1f}, Stoch:{stoch_k:.1f}"
            logger.info(f"[PROFIT-STRATEGY] {ticker} {reason}")
            
            # 진입 시간 기록
            self.entry_times[ticker] = time.time()
            self.max_profit_seen[ticker] = 0
            
            return True, reason
            
        except Exception as e:
            logger.error(f"[PROFIT-STRATEGY] 진입 조건 검사 실패: {e}")
            return False, f"오류: {e}"
    
    def should_exit(self, ticker: str, entry_price: float, current_price: float, 
                   hold_time: float, market_data: Dict[str, Any]) -> Tuple[bool, str, str]:
        """
        청산 조건 검사
        
        Returns:
            (청산여부, 이유, 청산타입)
        """
        try:
            # 현재 수익률 계산
            profit_pct = ((current_price - entry_price) / entry_price) * 100
            
            # 최고 수익률 업데이트
            if ticker not in self.max_profit_seen:
                self.max_profit_seen[ticker] = profit_pct
            else:
                self.max_profit_seen[ticker] = max(self.max_profit_seen[ticker], profit_pct)
            
            # 1. 손절 조건 (최우선)
            if profit_pct <= self.stop_loss:
                return True, f"🚨 손절: {profit_pct:.2f}% (기준: {self.stop_loss}%)", "STOP_LOSS"
            
            # 2. 시간 초과 청산 (5분 경과 + 0.2% 이상 익절)
            if hold_time >= self.time_based_exit:
                if profit_pct >= self.time_exit_min_profit:
                    return True, f"⏰ 시간초과 익절: {hold_time:.0f}초 (수익: {profit_pct:.2f}%)", "TIME_EXCEEDED"
                # 익절 미달 시 계속 보유 (다른 청산 조건 대기)
                # 손실 상태면 손절 조건(-0.5%)이 먼저 작동
            
            # 3. 빠른 익절 (30초 이내 0.3% 달성)
            if hold_time <= 30 and profit_pct >= self.quick_profit_target:
                return True, f"⚡ 빠른익절: {profit_pct:.2f}% (30초내)", "QUICK_PROFIT"
            
            # 4. 목표 익절 (0.5%)
            if profit_pct >= self.target_profit:
                return True, f"💰 목표익절: {profit_pct:.2f}%", "TAKE_PROFIT"
            
            # 5. 트레일링 스톱 (0.8% 도달 후 최고점 대비 0.15% 하락 시)
            # 작동 방식:
            # - 수익률이 0.8%에 도달하면 트레일링 시작
            # - 이후 최고 수익률을 계속 추적
            # - 현재 수익률이 최고점 대비 0.15% 하락하면 매도
            # 예: 최고 1.0% 도달 → 0.85% 하락 시 매도 (0.85% 익절 확보)
            max_profit = self.max_profit_seen.get(ticker, 0)
            if max_profit >= self.trailing_profit:
                profit_drop = max_profit - profit_pct
                if profit_drop >= self.trailing_stop:
                    return True, f"📉 트레일링스톱: 최고{max_profit:.2f}% → 현재{profit_pct:.2f}% (하락: {profit_drop:.2f}%)", "TRAILING_STOP"
            
            # 6. 거래량 급감 (진입 시 대비 50% 이하)
            if hold_time > 60:  # 1분 이상 보유 시
                current_volume = market_data.get('current_volume', 0)
                entry_volume = market_data.get('entry_volume', current_volume)
                if entry_volume > 0 and current_volume < entry_volume * 0.5:
                    return True, f"📊 거래량급감: {profit_pct:.2f}% (거래량 50%↓)", "VOLUME_DROP"
            
            # 7. 급락 감지 (1분 내 -1% 이상)
            price_change_1m = market_data.get('price_change_1m', 0)
            if price_change_1m <= -1.0:
                return True, f"💥 급락감지: {price_change_1m:.2f}% (수익: {profit_pct:.2f}%)", "SUDDEN_DROP"
            
            # 청산 조건 미충족
            return False, f"보유중: {profit_pct:.2f}% (최고: {max_profit:.2f}%, 시간: {hold_time:.0f}초)", "HOLD"
            
        except Exception as e:
            logger.error(f"[PROFIT-STRATEGY] 청산 조건 검사 실패: {e}")
            # 오류 시 안전하게 청산
            return True, f"오류로 청산: {e}", "ERROR"
    
    def get_position_size(self, available_krw: float, current_price: float, 
                         confidence: float = 1.0) -> float:
        """
        포지션 크기 계산 (Kelly Criterion 기반)
        
        Args:
            available_krw: 사용 가능한 원화
            current_price: 현재 가격
            confidence: 신뢰도 (0~1, 기본 1.0)
        
        Returns:
            매수할 코인 수량
        """
        # 기본: 가용 자금의 15% 사용 (보수적)
        base_allocation = 0.15
        
        # 신뢰도에 따라 조정 (최대 25%)
        adjusted_allocation = min(base_allocation * confidence, 0.25)
        
        position_krw = available_krw * adjusted_allocation
        quantity = position_krw / current_price
        
        return quantity
    
    def cleanup(self, ticker: str):
        """포지션 종료 후 정리"""
        if ticker in self.max_profit_seen:
            del self.max_profit_seen[ticker]
        if ticker in self.entry_times:
            del self.entry_times[ticker]
    
    def get_stats(self) -> Dict[str, Any]:
        """전략 통계"""
        return {
            'name': 'ProfitOptimized',
            'type': 'SCALPING',
            'target_profit': f"{self.target_profit}%",
            'stop_loss': f"{self.stop_loss}%",
            'max_hold_time': f"{self.time_based_exit}s",
            'active_positions': len(self.max_profit_seen),
        }
