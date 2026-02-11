"""
동적 청산 관리자
트레일링 스톱, 부분 익절, 시장 상황 기반 청산
"""

from typing import Dict, List, Tuple, Optional
from datetime import datetime
import time


class DynamicExitManager:
    """동적 청산 관리"""
    
    def __init__(self, mode: str = 'moderate'):
        """
        Args:
            mode: 'aggressive', 'moderate', 'conservative'
        """
        self.mode = mode
        
        # 모드별 트레일링 스톱 설정
        self.trailing_stop_configs = {
            'aggressive': 0.005,   # 0.5%
            'moderate': 0.01,      # 1.0%
            'conservative': 0.02   # 2.0%
        }
        
        self.trailing_stop_ratio = self.trailing_stop_configs.get(mode, 0.01)
        
        # 포지션별 추적 데이터
        self.position_data = {}  # {ticker: {highest_price, trailing_stop_price, entry_time, ...}}
        
        # 부분 익절 계획
        self.partial_exit_plan = [
            {'profit_ratio': 0.01, 'exit_ratio': 0.2},  # +1%에 20% 매도
            {'profit_ratio': 0.02, 'exit_ratio': 0.3},  # +2%에 30% 매도
            {'profit_ratio': 0.03, 'exit_ratio': 0.3},  # +3%에 30% 매도
            {'profit_ratio': 0.05, 'exit_ratio': 0.2},  # +5%에 20% 매도
        ]
    
    def register_position(
        self,
        ticker: str,
        entry_price: float,
        entry_time: datetime,
        strategy: str,
        scenario_id: int
    ):
        """
        포지션 등록
        
        Args:
            ticker: 티커
            entry_price: 진입가
            entry_time: 진입 시간
            strategy: 전략 이름
            scenario_id: 시나리오 ID
        """
        self.position_data[ticker] = {
            'entry_price': entry_price,
            'entry_time': entry_time,
            'highest_price': entry_price,
            'trailing_stop_price': entry_price * (1 - self.trailing_stop_ratio),
            'strategy': strategy,
            'scenario_id': scenario_id,
            'partial_exits': [],  # 부분 익절 기록
            'last_check_time': datetime.now()
        }
    
    def update_position(self, ticker: str, current_price: float):
        """
        포지션 업데이트 (최고가 및 트레일링 스톱 갱신)
        
        Args:
            ticker: 티커
            current_price: 현재가
        """
        if ticker not in self.position_data:
            return
        
        data = self.position_data[ticker]
        
        # 최고가 갱신
        if current_price > data['highest_price']:
            data['highest_price'] = current_price
            # 트레일링 스톱 가격 상향 조정
            data['trailing_stop_price'] = current_price * (1 - self.trailing_stop_ratio)
        
        data['last_check_time'] = datetime.now()
    
    def should_exit(
        self,
        ticker: str,
        current_price: float,
        current_scenario: Dict,
        market_condition: Dict
    ) -> Tuple[bool, str, float]:
        """
        청산 여부 판단
        
        Args:
            ticker: 티커
            current_price: 현재가
            current_scenario: 현재 시나리오 정보
            market_condition: 시장 상황
        
        Returns:
            (청산 여부, 청산 사유, 매도 비율)
        """
        if ticker not in self.position_data:
            return False, "", 0.0
        
        data = self.position_data[ticker]
        entry_price = data['entry_price']
        profit_ratio = (current_price - entry_price) / entry_price
        
        # 1. 손절 (-2%)
        if profit_ratio <= -0.02:
            return True, "손절 -2% 도달", 1.0
        
        # 2. 트레일링 스톱
        if current_price <= data['trailing_stop_price']:
            return True, f"트레일링 스톱 (최고가: {data['highest_price']:,.0f}원)", 1.0
        
        # 3. 부분 익절 체크
        for plan in self.partial_exit_plan:
            if profit_ratio >= plan['profit_ratio']:
                # 이미 이 구간 익절 완료 여부 체크
                if plan['profit_ratio'] not in data['partial_exits']:
                    data['partial_exits'].append(plan['profit_ratio'])
                    return True, f"부분 익절 +{plan['profit_ratio']*100:.0f}%", plan['exit_ratio']
        
        # 4. 시장 상황 기반 청산
        # 추세 약화
        if market_condition.get('trend_strength', 0) < -0.5:
            return True, "추세 약화 감지", 1.0
        
        # 변동성 급증
        if market_condition.get('volatility', 0) > 0.05:  # 5% 이상
            return True, "변동성 급증", 0.5  # 50% 매도
        
        # 거래량 급감
        if market_condition.get('volume_ratio', 1.0) < 0.5:
            return True, "거래량 급감", 0.5
        
        # 5. 시간 기반 청산
        holding_time = (datetime.now() - data['entry_time']).total_seconds()
        
        # 최대 보유 시간 (전략별)
        max_holding_times = {
            'UltraScalping': 300,       # 5분
            'AggressiveScalping': 900,  # 15분
            'ConservativeScalping': 1800,  # 30분
            'MeanReversion': 3600,      # 1시간
            'GridTrading': 7200         # 2시간
        }
        
        max_time = max_holding_times.get(data['strategy'], 1800)
        if holding_time > max_time:
            return True, f"최대 보유 시간 초과 ({holding_time//60}분)", 1.0
        
        # 야간 시간대 (23:00~07:00) 리스크 감소
        current_hour = datetime.now().hour
        if (current_hour >= 23 or current_hour < 7) and profit_ratio > 0:
            return True, "야간 시간대 이익 보호", 0.7
        
        return False, "홀딩 유지", 0.0
    
    def should_add_position(
        self,
        ticker: str,
        current_price: float,
        current_scenario: Dict,
        market_condition: Dict,
        ai_confidence: float
    ) -> Tuple[bool, str, float]:
        """
        추가 매수 여부 판단
        
        Returns:
            (추가 매수 여부, 사유, 추가 비율)
        """
        if ticker not in self.position_data:
            return False, "", 0.0
        
        data = self.position_data[ticker]
        entry_price = data['entry_price']
        profit_ratio = (current_price - entry_price) / entry_price
        
        # 수익 중인 포지션만 추가 매수 고려
        if profit_ratio <= 0:
            return False, "손실 중", 0.0
        
        # 초단타는 추가 매수 없음
        if data['strategy'] == 'UltraScalping':
            return False, "초단타 전략", 0.0
        
        # AI 신뢰도 높음 + 강한 상승 추세
        if ai_confidence > 0.8 and market_condition.get('trend_strength', 0) > 0.7:
            # 거래량 지속 증가
            if market_condition.get('volume_ratio', 1.0) > 1.5:
                # RSI 과열 미도달 (< 70)
                if market_condition.get('rsi', 50) < 70:
                    return True, "강한 상승 모멘텀 + AI 고신뢰도", 0.3
        
        return False, "추가 매수 조건 미충족", 0.0
    
    def remove_position(self, ticker: str):
        """포지션 제거"""
        if ticker in self.position_data:
            del self.position_data[ticker]
    
    def get_position_summary(self, ticker: str) -> Optional[Dict]:
        """포지션 요약 정보"""
        return self.position_data.get(ticker)
