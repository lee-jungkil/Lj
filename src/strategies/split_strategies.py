"""
20가지 분할 매수/매도 전략
시장 상황에 따라 최적의 분할 전략 자동 선택
"""

from typing import Dict, List, Tuple
from datetime import datetime
import math


class SplitStrategies:
    """분할 매수/매도 전략 관리자"""
    
    # 전략 정의
    STRATEGIES = {
        # === 매수 전략 (1-10) ===
        1: {
            'name': '일괄 매수',
            'type': 'BUY',
            'splits': 1,
            'distribution': [1.0],
            'use_case': '강한 상승 시그널, 급등 포착'
        },
        2: {
            'name': '2분할 균등 매수',
            'type': 'BUY',
            'splits': 2,
            'distribution': [0.5, 0.5],
            'use_case': '중간 신뢰도 신호'
        },
        3: {
            'name': '3분할 피라미딩',
            'type': 'BUY',
            'splits': 3,
            'distribution': [0.5, 0.3, 0.2],
            'use_case': '추세 초기 진입'
        },
        4: {
            'name': '3분할 역피라미딩',
            'type': 'BUY',
            'splits': 3,
            'distribution': [0.2, 0.3, 0.5],
            'use_case': '하락장 분할 매수'
        },
        5: {
            'name': '4분할 균등 매수',
            'type': 'BUY',
            'splits': 4,
            'distribution': [0.25, 0.25, 0.25, 0.25],
            'use_case': '불확실한 시장'
        },
        6: {
            'name': '5분할 적립식',
            'type': 'BUY',
            'splits': 5,
            'distribution': [0.3, 0.25, 0.2, 0.15, 0.1],
            'use_case': '장기 횡보 예상'
        },
        7: {
            'name': '피보나치 매수 (3단계)',
            'type': 'BUY',
            'splits': 3,
            'distribution': [0.382, 0.382, 0.236],
            'use_case': '기술적 지지선 활용'
        },
        8: {
            'name': '비율 조정 매수 (2:3:5)',
            'type': 'BUY',
            'splits': 3,
            'distribution': [0.2, 0.3, 0.5],
            'use_case': '하락 시 비중 확대'
        },
        9: {
            'name': '계단식 매수 (4단계)',
            'type': 'BUY',
            'splits': 4,
            'distribution': [0.1, 0.2, 0.3, 0.4],
            'use_case': '저점 탐색 매수'
        },
        10: {
            'name': '탄력적 매수 (5단계)',
            'type': 'BUY',
            'splits': 5,
            'distribution': [0.15, 0.15, 0.2, 0.25, 0.25],
            'use_case': '변동성 큰 시장'
        },
        
        # === 매도 전략 (11-20) ===
        11: {
            'name': '일괄 매도',
            'type': 'SELL',
            'splits': 1,
            'distribution': [1.0],
            'use_case': '급락 위험, 강한 매도 시그널'
        },
        12: {
            'name': '2분할 균등 매도',
            'type': 'SELL',
            'splits': 2,
            'distribution': [0.5, 0.5],
            'use_case': '중간 신뢰도 매도'
        },
        13: {
            'name': '3분할 익절 매도',
            'type': 'SELL',
            'splits': 3,
            'distribution': [0.3, 0.3, 0.4],
            'use_case': '수익 실현 단계'
        },
        14: {
            'name': '피라미딩 매도',
            'type': 'SELL',
            'splits': 3,
            'distribution': [0.5, 0.3, 0.2],
            'use_case': '상승장 익절'
        },
        15: {
            'name': '트레일링 매도 (4단계)',
            'type': 'SELL',
            'splits': 4,
            'distribution': [0.2, 0.2, 0.3, 0.3],
            'use_case': '추세 전환 대비'
        },
        16: {
            'name': '안전 우선 매도',
            'type': 'SELL',
            'splits': 3,
            'distribution': [0.6, 0.25, 0.15],
            'use_case': '고점 인식 시'
        },
        17: {
            'name': '단계적 이익 실현',
            'type': 'SELL',
            'splits': 5,
            'distribution': [0.15, 0.2, 0.25, 0.2, 0.2],
            'use_case': '큰 수익 시 단계 매도'
        },
        18: {
            'name': '손절 전용 매도',
            'type': 'SELL',
            'splits': 2,
            'distribution': [0.7, 0.3],
            'use_case': '손실 최소화'
        },
        19: {
            'name': '반반 나눔 매도',
            'type': 'SELL',
            'splits': 2,
            'distribution': [0.5, 0.5],
            'use_case': '횡보 전환 시'
        },
        20: {
            'name': '보수적 매도 (5단계)',
            'type': 'SELL',
            'splits': 5,
            'distribution': [0.1, 0.15, 0.2, 0.25, 0.3],
            'use_case': '긴 상승 추세 유지'
        }
    }
    
    def __init__(self):
        """분할 전략 관리자 초기화"""
        self.execution_history = []  # 실행 히스토리
        
    def select_buy_strategy(
        self, 
        scenario_id: int, 
        confidence: float,
        volatility: float,
        available_capital: float
    ) -> Dict:
        """
        매수 전략 자동 선택
        
        Args:
            scenario_id: 시장 시나리오 ID (1-45)
            confidence: 신호 신뢰도 (0-100)
            volatility: 변동성 (0-10)
            available_capital: 사용 가능 자금
        
        Returns:
            선택된 전략 정보
        """
        # 신뢰도 기반 전략 선택
        if confidence > 80 and volatility < 2:
            # 높은 신뢰도 + 낮은 변동성 → 일괄 매수
            strategy_id = 1
        elif confidence > 70:
            # 높은 신뢰도 → 2분할
            strategy_id = 2
        elif confidence > 60:
            # 중간 신뢰도 → 3분할 피라미딩
            strategy_id = 3
        elif volatility > 4:
            # 고변동성 → 탄력적 매수
            strategy_id = 10
        else:
            # 기본: 4분할 균등
            strategy_id = 5
        
        # 시나리오별 조정
        if scenario_id in [3, 4, 9, 10]:  # 하락/급락
            strategy_id = 4  # 역피라미딩
        elif scenario_id in [11, 12]:  # 초고변동성
            strategy_id = 9  # 계단식
        elif scenario_id in [1, 2]:  # 강한 상승
            strategy_id = 1  # 일괄
        
        return self._create_execution_plan(strategy_id, available_capital, 'BUY')
    
    def select_sell_strategy(
        self,
        scenario_id: int,
        profit_ratio: float,
        holding_time: int,
        position_size: float
    ) -> Dict:
        """
        매도 전략 자동 선택
        
        Args:
            scenario_id: 시장 시나리오 ID
            profit_ratio: 현재 수익률 (%)
            holding_time: 보유 시간 (초)
            position_size: 포지션 크기 (원화)
        
        Returns:
            선택된 전략 정보
        """
        # 손실 상황
        if profit_ratio < -2:
            # 큰 손실 → 손절 전용
            strategy_id = 18
        elif profit_ratio < 0:
            # 소폭 손실 → 2분할
            strategy_id = 12
        
        # 수익 상황
        elif profit_ratio > 5:
            # 큰 수익 → 단계적 이익 실현
            strategy_id = 17
        elif profit_ratio > 2:
            # 중간 수익 → 피라미딩 매도
            strategy_id = 14
        elif profit_ratio > 1:
            # 소폭 수익 → 3분할 익절
            strategy_id = 13
        else:
            # 기본
            strategy_id = 12
        
        # 시나리오별 조정
        if scenario_id in [3, 7, 34]:  # 강한 하락, 추세 전환
            strategy_id = 11  # 일괄 매도
        elif scenario_id in [31, 42]:  # 과매수, 천장 패턴
            strategy_id = 16  # 안전 우선
        elif scenario_id in [1, 2, 33]:  # 강한 상승, 골든크로스
            strategy_id = 20  # 보수적 매도
        
        return self._create_execution_plan(strategy_id, position_size, 'SELL')
    
    def _create_execution_plan(
        self, 
        strategy_id: int, 
        total_amount: float,
        action: str
    ) -> Dict:
        """
        실행 계획 생성
        
        Returns:
            {
                'strategy_id': int,
                'strategy_name': str,
                'total_amount': float,
                'splits': int,
                'distribution': List[float],
                'amounts': List[float],
                'intervals': List[int],  # 각 분할 간 대기 시간 (초)
                'use_case': str
            }
        """
        strategy = self.STRATEGIES[strategy_id]
        distribution = strategy['distribution']
        splits = strategy['splits']
        
        # 금액 분할
        amounts = [total_amount * ratio for ratio in distribution]
        
        # 최소 거래 금액 체크 (5,000원)
        min_trade = 5000
        valid_amounts = [amt for amt in amounts if amt >= min_trade]
        
        if len(valid_amounts) < splits:
            # 일부 분할이 최소 금액 미만 → 통합
            amounts = self._merge_small_splits(amounts, min_trade)
            splits = len(amounts)
        
        # 실행 간격 (초)
        intervals = self._calculate_intervals(splits, action)
        
        plan = {
            'strategy_id': strategy_id,
            'strategy_name': strategy['name'],
            'total_amount': total_amount,
            'splits': splits,
            'distribution': distribution[:splits],
            'amounts': amounts,
            'intervals': intervals,
            'use_case': strategy['use_case'],
            'action': action,
            'timestamp': datetime.now()
        }
        
        # 히스토리 저장
        self.execution_history.append(plan)
        if len(self.execution_history) > 100:
            self.execution_history.pop(0)
        
        return plan
    
    def _merge_small_splits(self, amounts: List[float], min_trade: float) -> List[float]:
        """
        최소 거래 금액 미만 분할 통합
        """
        merged = []
        accumulator = 0.0
        
        for amount in amounts:
            accumulator += amount
            if accumulator >= min_trade:
                merged.append(accumulator)
                accumulator = 0.0
        
        # 남은 금액 마지막에 합산
        if accumulator > 0 and merged:
            merged[-1] += accumulator
        
        return merged if merged else [sum(amounts)]
    
    def _calculate_intervals(self, splits: int, action: str) -> List[int]:
        """
        분할 실행 간격 계산 (초)
        
        매수: 더 긴 간격 (신중)
        매도: 더 짧은 간격 (빠름)
        """
        if splits == 1:
            return [0]
        
        base_interval = 30 if action == 'BUY' else 15
        
        # 분할 수가 많을수록 간격 증가
        intervals = [base_interval * i for i in range(splits)]
        
        return intervals
    
    def get_strategy_info(self, strategy_id: int) -> Dict:
        """전략 정보 조회"""
        return self.STRATEGIES.get(strategy_id, {})
    
    def get_all_strategies(self, action: str = None) -> Dict:
        """
        전체 전략 목록
        
        Args:
            action: 'BUY', 'SELL', None (전체)
        """
        if action:
            return {
                k: v for k, v in self.STRATEGIES.items() 
                if v['type'] == action
            }
        return self.STRATEGIES.copy()
    
    def calculate_optimal_split_count(
        self,
        confidence: float,
        volatility: float,
        capital: float
    ) -> int:
        """
        최적 분할 수 계산
        
        낮은 신뢰도 + 높은 변동성 → 많은 분할
        높은 신뢰도 + 낮은 변동성 → 적은 분할
        """
        if confidence > 80 and volatility < 2:
            return 1  # 일괄
        elif confidence > 70 and volatility < 3:
            return 2
        elif confidence > 60:
            return 3
        elif confidence > 50:
            return 4
        else:
            return 5
    
    def get_execution_summary(self) -> Dict:
        """실행 히스토리 요약"""
        if not self.execution_history:
            return {'total_executions': 0}
        
        buy_count = sum(1 for h in self.execution_history if h['action'] == 'BUY')
        sell_count = sum(1 for h in self.execution_history if h['action'] == 'SELL')
        
        avg_splits_buy = sum(
            h['splits'] for h in self.execution_history if h['action'] == 'BUY'
        ) / max(buy_count, 1)
        
        avg_splits_sell = sum(
            h['splits'] for h in self.execution_history if h['action'] == 'SELL'
        ) / max(sell_count, 1)
        
        return {
            'total_executions': len(self.execution_history),
            'buy_count': buy_count,
            'sell_count': sell_count,
            'avg_splits_buy': round(avg_splits_buy, 2),
            'avg_splits_sell': round(avg_splits_sell, 2),
            'last_execution': self.execution_history[-1]['timestamp']
        }
