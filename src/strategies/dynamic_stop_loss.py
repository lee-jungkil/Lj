"""
Dynamic Stop Loss System (동적 손절 시스템)
- 학습된 패턴 기반 최적 손절가 계산
- 시장 변동성에 따른 손절 조정
- 전략별 성과 기반 손절 최적화
- 시간대별 손절 조정

⭐ v6.30 Integration Phase 2B
"""

from typing import Dict, Optional, List
from dataclasses import dataclass
from datetime import datetime
import os


@dataclass
class StopLossConfig:
    """손절 설정"""
    base_stop_pct: float  # 기본 손절 비율
    min_stop_pct: float   # 최소 손절 비율
    max_stop_pct: float   # 최대 손절 비율
    volatility_multiplier: float  # 변동성 배율
    time_decay_factor: float  # 시간 감쇠 계수


class DynamicStopLoss:
    """동적 손절 관리 시스템"""
    
    def __init__(self, learning_engine, config):
        """
        초기화
        
        Args:
            learning_engine: AI 학습 엔진
            config: Config 객체
        """
        self.learning_engine = learning_engine
        self.config = config
        self.enabled = os.getenv('ENABLE_DYNAMIC_STOP_LOSS', 'true').lower() == 'true'
        
        # 전략별 손절 설정
        self.strategy_configs = self._init_strategy_configs()
    
    def _init_strategy_configs(self) -> Dict[str, StopLossConfig]:
        """전략별 손절 설정 초기화"""
        return {
            'ULTRA_SCALPING': StopLossConfig(
                base_stop_pct=0.01,   # 1%
                min_stop_pct=0.005,   # 0.5%
                max_stop_pct=0.02,    # 2%
                volatility_multiplier=1.5,
                time_decay_factor=0.9
            ),
            'AGGRESSIVE_SCALPING': StopLossConfig(
                base_stop_pct=0.03,   # 3%
                min_stop_pct=0.015,   # 1.5%
                max_stop_pct=0.05,    # 5%
                volatility_multiplier=1.3,
                time_decay_factor=0.95
            ),
            'CONSERVATIVE_SCALPING': StopLossConfig(
                base_stop_pct=0.02,   # 2%
                min_stop_pct=0.01,    # 1%
                max_stop_pct=0.04,    # 4%
                volatility_multiplier=1.2,
                time_decay_factor=0.98
            ),
            'MEAN_REVERSION': StopLossConfig(
                base_stop_pct=0.04,   # 4%
                min_stop_pct=0.02,    # 2%
                max_stop_pct=0.06,    # 6%
                volatility_multiplier=1.4,
                time_decay_factor=0.92
            ),
            'GRID_TRADING': StopLossConfig(
                base_stop_pct=0.05,   # 5%
                min_stop_pct=0.03,    # 3%
                max_stop_pct=0.08,    # 8%
                volatility_multiplier=1.1,
                time_decay_factor=1.0  # No decay
            )
        }
    
    def calculate_optimal_stop_loss(self, ticker: str, strategy: str, 
                                    entry_price: float, 
                                    market_condition: Dict) -> float:
        """
        동적 손절가 계산
        
        Args:
            ticker: 코인 티커
            strategy: 전략 이름
            entry_price: 진입 가격
            market_condition: 시장 조건 {'volatility', 'trend', 'volume_ratio'}
        
        Returns:
            최적 손절 가격
        """
        if not self.enabled:
            # 동적 손절 비활성화 시 기본값 사용
            return self._get_static_stop_loss(ticker, strategy, entry_price)
        
        # 1. 전략별 기본 손절 비율
        config = self.strategy_configs.get(
            strategy.upper(), 
            self.strategy_configs['CONSERVATIVE_SCALPING']
        )
        base_stop_pct = config.base_stop_pct
        
        # 2. 학습된 데이터 기반 조정
        learned_stop_pct = self._get_learned_stop_loss(ticker, strategy)
        if learned_stop_pct:
            # 학습된 값과 기본값의 가중 평균 (70% 학습, 30% 기본)
            adjusted_stop_pct = (learned_stop_pct * 0.7) + (base_stop_pct * 0.3)
        else:
            adjusted_stop_pct = base_stop_pct
        
        # 3. 변동성 조정
        volatility = market_condition.get('volatility', 'medium')
        if volatility == 'high':
            # 고변동성 → 손절 폭 넓힘 (변동성 배율 적용)
            adjusted_stop_pct *= config.volatility_multiplier
        elif volatility == 'low':
            # 저변동성 → 손절 폭 좁힘
            adjusted_stop_pct *= 0.8
        
        # 4. 추세 조정
        trend = market_condition.get('trend', 'sideways')
        if trend == 'down':
            # 하락 추세 → 손절 폭 좁힘 (빠른 탈출)
            adjusted_stop_pct *= 0.9
        elif trend == 'up':
            # 상승 추세 → 손절 폭 약간 넓힘 (여유 부여)
            adjusted_stop_pct *= 1.1
        
        # 5. 거래량 조정
        volume_ratio = market_condition.get('volume_ratio', 1.0)
        if volume_ratio < 0.5:
            # 저거래량 → 손절 폭 좁힘 (유동성 리스크)
            adjusted_stop_pct *= 0.85
        
        # 6. 시간대 조정 (야간 시간대는 변동성 고려)
        hour = datetime.now().hour
        if hour < 9 or hour > 22:
            # 야간 시간대 → 손절 폭 약간 넓힘
            adjusted_stop_pct *= 1.05
        
        # 7. 최소/최대 제한 적용
        final_stop_pct = max(config.min_stop_pct, 
                            min(adjusted_stop_pct, config.max_stop_pct))
        
        # 손절 가격 계산
        stop_loss_price = entry_price * (1 - final_stop_pct)
        
        return stop_loss_price
    
    def _get_learned_stop_loss(self, ticker: str, strategy: str) -> Optional[float]:
        """
        학습된 최적 손절 비율 조회
        
        Args:
            ticker: 코인 티커
            strategy: 전략 이름
        
        Returns:
            학습된 손절 비율 (없으면 None)
        """
        try:
            # 과거 손실 거래 분석
            experiences = self.learning_engine.experiences[-100:]  # 최근 100개
            
            # 동일 티커 + 전략의 손실 거래 필터링
            loss_trades = [
                exp for exp in experiences
                if exp.ticker == ticker
                and exp.strategy == strategy
                and exp.profit_loss < 0
                and exp.profit_loss_ratio is not None
            ]
            
            if len(loss_trades) < 3:
                return None  # 데이터 부족
            
            # 최대 손실 비율 계산
            max_loss_ratio = max(abs(exp.profit_loss_ratio) for exp in loss_trades)
            
            # 평균 손실 비율
            avg_loss_ratio = sum(abs(exp.profit_loss_ratio) for exp in loss_trades) / len(loss_trades)
            
            # 최적 손절 = 최대 손실의 120% (안전 마진)
            optimal_stop = max_loss_ratio * 1.2
            
            # 하지만 평균 손실의 150% 이하로 제한
            optimal_stop = min(optimal_stop, avg_loss_ratio * 1.5)
            
            return optimal_stop
        
        except Exception as e:
            print(f"⚠️ 학습 데이터 조회 오류: {e}")
            return None
    
    def _get_static_stop_loss(self, ticker: str, strategy: str, 
                             entry_price: float) -> float:
        """
        정적 손절가 계산 (기본값)
        
        Args:
            ticker: 코인 티커
            strategy: 전략 이름
            entry_price: 진입 가격
        
        Returns:
            정적 손절 가격
        """
        config = self.strategy_configs.get(
            strategy.upper(), 
            self.strategy_configs['CONSERVATIVE_SCALPING']
        )
        
        return entry_price * (1 - config.base_stop_pct)
    
    def update_stop_loss_trailing(self, current_price: float, entry_price: float,
                                  current_stop: float, strategy: str, 
                                  profit_ratio: float) -> float:
        """
        트레일링 스탑 업데이트
        
        Args:
            current_price: 현재 가격
            entry_price: 진입 가격
            current_stop: 현재 손절가
            strategy: 전략 이름
            profit_ratio: 현재 수익률 (%)
        
        Returns:
            업데이트된 손절 가격
        """
        if not self.config.ENABLE_TRAILING_STOP:
            return current_stop
        
        # 최소 수익 달성 시에만 트레일링 시작
        min_profit = self.config.TRAILING_STOP_MIN_PROFIT
        if profit_ratio < min_profit:
            return current_stop
        
        # 트레일링 오프셋 (수익에서 몇 % 떨어지면 청산)
        offset_pct = self.config.TRAILING_STOP_OFFSET / 100
        
        # 새 손절가 = 현재가 - 오프셋
        new_stop = current_price * (1 - offset_pct)
        
        # 손절가는 올라가기만 함 (내려가지 않음)
        return max(new_stop, current_stop)
    
    def should_trigger_stop_loss(self, current_price: float, 
                                 stop_loss_price: float) -> bool:
        """
        손절 트리거 여부 확인
        
        Args:
            current_price: 현재 가격
            stop_loss_price: 손절 가격
        
        Returns:
            손절 트리거 여부
        """
        return current_price <= stop_loss_price
    
    def get_stop_loss_reason(self, current_price: float, entry_price: float,
                            stop_loss_price: float, profit_ratio: float) -> str:
        """
        손절 사유 생성
        
        Args:
            current_price: 현재 가격
            entry_price: 진입 가격
            stop_loss_price: 손절 가격
            profit_ratio: 수익률 (%)
        
        Returns:
            손절 사유 문자열
        """
        if profit_ratio > 0:
            return f"트레일링 스탑 ({profit_ratio:+.2f}% → {(current_price/entry_price-1)*100:+.2f}%)"
        else:
            return f"손절 ({profit_ratio:+.2f}%, 현재가 {current_price:,.0f} ≤ 손절가 {stop_loss_price:,.0f})"
    
    def analyze_stop_loss_performance(self, ticker: str, strategy: str) -> Dict:
        """
        손절 성과 분석
        
        Args:
            ticker: 코인 티커
            strategy: 전략 이름
        
        Returns:
            성과 분석 결과
        """
        experiences = self.learning_engine.experiences[-100:]
        
        # 손절 거래 필터링
        stop_loss_trades = [
            exp for exp in experiences
            if exp.ticker == ticker
            and exp.strategy == strategy
            and hasattr(exp, 'exit_reason')
            and exp.exit_reason == 'stop_loss'
        ]
        
        if not stop_loss_trades:
            return {}
        
        total_stop_loss = len(stop_loss_trades)
        avg_loss = sum(exp.profit_loss for exp in stop_loss_trades) / total_stop_loss
        avg_hold_time = sum(exp.holding_duration for exp in stop_loss_trades if exp.holding_duration) / total_stop_loss
        
        # 손절 후 가격 회복 체크 (손절이 너무 빨랐는지)
        premature_stops = 0  # 구현 복잡도로 인해 생략
        
        return {
            'total_stop_loss_count': total_stop_loss,
            'avg_loss_amount': avg_loss,
            'avg_hold_time': avg_hold_time,
            'premature_stops': premature_stops
        }
