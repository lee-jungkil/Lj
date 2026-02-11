"""
손실 분석 및 학습 시스템

기능:
- 손실 발생 시 자동 분석
- 손실 원인 분류 (시나리오/전략/타이밍)
- 대안 전략 자동 생성
- 실패 패턴 학습 및 회피
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from collections import defaultdict


class LossAnalyzer:
    """손실 분석 및 대응 시스템"""
    
    def __init__(
        self,
        learning_engine,
        scenario_identifier,
        strategy_selector,
        data_dir: str = "learning_data/losses"
    ):
        """
        초기화
        
        Args:
            learning_engine: 학습 엔진
            scenario_identifier: 시나리오 식별기
            strategy_selector: 전략 선택기
            data_dir: 데이터 디렉토리
        """
        self.learning_engine = learning_engine
        self.scenario_identifier = scenario_identifier
        self.strategy_selector = strategy_selector
        
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        # 손실 케이스 저장
        self.loss_cases = []
        self.loss_patterns = defaultdict(int)
        
        # 학습 데이터 로드
        self._load_loss_data()
    
    def analyze_loss(
        self,
        ticker: str,
        entry_price: float,
        exit_price: float,
        entry_scenario: str,
        selected_strategy: str,
        hold_time: float,
        profit_loss: float,
        market_data: Dict = None
    ) -> Dict:
        """
        손실 발생 시 자동 분석
        
        Args:
            ticker: 코인 티커
            entry_price: 진입 가격
            exit_price: 청산 가격
            entry_scenario: 진입 시 예측 시나리오
            selected_strategy: 선택된 전략
            hold_time: 보유 시간 (초)
            profit_loss: 손익 금액
            market_data: 시장 데이터 (OHLCV DataFrame)
        
        Returns:
            분석 결과 딕셔너리
        """
        try:
            # 1. 실제 시나리오 분석
            actual_scenario = "UNKNOWN"
            if market_data is not None and hasattr(self.scenario_identifier, 'identify_scenario'):
                scenarios = self.scenario_identifier.identify_scenario(market_data, ticker)
                if scenarios:
                    actual_scenario = scenarios[0]['scenario']  # 최상위 시나리오
            
            # 2. 손실 원인 분류
            loss_category = self._categorize_loss(
                entry_scenario,
                actual_scenario,
                selected_strategy,
                hold_time,
                profit_loss
            )
            
            # 3. 근본 원인 파악
            root_cause = self._identify_root_cause(
                loss_category,
                entry_scenario,
                actual_scenario,
                selected_strategy
            )
            
            # 4. 대안 전략 생성
            alternatives = self._generate_alternatives(
                entry_scenario,
                actual_scenario,
                selected_strategy
            )
            
            # 5. 신뢰도 계산
            confidence = self._calculate_confidence(
                loss_category,
                len(self.loss_cases)
            )
            
            analysis_result = {
                'timestamp': datetime.now().isoformat(),
                'ticker': ticker,
                'entry_price': entry_price,
                'exit_price': exit_price,
                'profit_loss': profit_loss,
                'profit_loss_ratio': ((exit_price - entry_price) / entry_price) * 100,
                'hold_time': hold_time,
                'entry_scenario': entry_scenario,
                'actual_scenario': actual_scenario,
                'selected_strategy': selected_strategy,
                'loss_category': loss_category,
                'root_cause': root_cause,
                'alternative_strategies': alternatives,
                'confidence': confidence
            }
            
            # 6. 학습
            self.learn_from_loss(analysis_result)
            
            return analysis_result
            
        except Exception as e:
            print(f"⚠️ 손실 분석 실패: {e}")
            return {}
    
    def _categorize_loss(
        self,
        entry_scenario: str,
        actual_scenario: str,
        selected_strategy: str,
        hold_time: float,
        profit_loss: float
    ) -> str:
        """손실 원인 분류"""
        
        # 1. 시나리오 불일치
        if entry_scenario != actual_scenario and actual_scenario != "UNKNOWN":
            return "SCENARIO_MISMATCH"
        
        # 2. 잘못된 전략 선택
        # (전략 선택기에서 최적 전략 확인 필요)
        if hasattr(self.strategy_selector, 'get_best_strategy'):
            best_strategy = self.strategy_selector.get_best_strategy_for_scenario(entry_scenario)
            if best_strategy and best_strategy != selected_strategy:
                return "WRONG_STRATEGY"
        
        # 3. 타이밍 문제
        if hold_time < 60:  # 1분 미만
            return "TOO_QUICK_EXIT"
        elif hold_time > 3600:  # 1시간 이상
            return "HELD_TOO_LONG"
        
        # 4. 큰 손실
        if profit_loss < -50000:  # 5만원 이상 손실
            return "LARGE_LOSS"
        
        # 5. 기타
        return "OTHER"
    
    def _identify_root_cause(
        self,
        loss_category: str,
        entry_scenario: str,
        actual_scenario: str,
        selected_strategy: str
    ) -> str:
        """근본 원인 파악"""
        
        if loss_category == "SCENARIO_MISMATCH":
            return f"시나리오 예측 실패: {entry_scenario} → {actual_scenario}"
        
        elif loss_category == "WRONG_STRATEGY":
            return f"부적절한 전략 선택: {selected_strategy} (시나리오: {entry_scenario})"
        
        elif loss_category == "TOO_QUICK_EXIT":
            return "조급한 청산 (충분한 시간 부여 필요)"
        
        elif loss_category == "HELD_TOO_LONG":
            return "과도한 보유 (빠른 손절 필요)"
        
        elif loss_category == "LARGE_LOSS":
            return "리스크 관리 실패 (포지션 크기 또는 손절 미흡)"
        
        else:
            return "원인 불명확 (추가 데이터 수집 필요)"
    
    def _generate_alternatives(
        self,
        entry_scenario: str,
        actual_scenario: str,
        selected_strategy: str
    ) -> List[str]:
        """대안 전략 생성"""
        alternatives = []
        
        # 1. 시나리오 기반 대안
        if actual_scenario != "UNKNOWN":
            # 실제 시나리오에 맞는 전략 추천
            if hasattr(self.strategy_selector, 'get_recommended_strategies'):
                recommended = self.strategy_selector.get_recommended_strategies(actual_scenario)
                alternatives.extend(recommended[:2])  # 상위 2개
        
        # 2. 보수적 전략 추천 (손실 후)
        conservative_strategies = ['conservative_scalping', 'mean_reversion']
        for strat in conservative_strategies:
            if strat != selected_strategy and strat not in alternatives:
                alternatives.append(strat)
        
        # 3. 최대 3개로 제한
        return alternatives[:3]
    
    def _calculate_confidence(self, loss_category: str, total_cases: int) -> float:
        """분석 신뢰도 계산"""
        
        # 기본 신뢰도
        base_confidence = 50.0
        
        # 케이스 수에 따른 신뢰도 증가
        if total_cases > 100:
            base_confidence += 30.0
        elif total_cases > 50:
            base_confidence += 20.0
        elif total_cases > 20:
            base_confidence += 10.0
        
        # 카테고리가 명확하면 신뢰도 증가
        if loss_category in ["SCENARIO_MISMATCH", "WRONG_STRATEGY", "LARGE_LOSS"]:
            base_confidence += 15.0
        
        return min(base_confidence, 95.0)
    
    def learn_from_loss(self, analysis_result: Dict):
        """손실로부터 학습"""
        
        # 1. 손실 케이스 저장
        self.loss_cases.append(analysis_result)
        
        # 2. 패턴 카운트
        loss_category = analysis_result.get('loss_category', 'OTHER')
        self.loss_patterns[loss_category] += 1
        
        # 3. 전략 선택기 업데이트 (실패한 조합 패널티)
        if hasattr(self.strategy_selector, 'penalize_combination'):
            self.strategy_selector.penalize_combination(
                scenario=analysis_result.get('entry_scenario'),
                strategy=analysis_result.get('selected_strategy'),
                penalty=0.9  # 10% 감소
            )
        
        # 4. 대안 전략 강화
        if hasattr(self.strategy_selector, 'boost_strategy'):
            for alt_strategy in analysis_result.get('alternative_strategies', []):
                self.strategy_selector.boost_strategy(
                    strategy=alt_strategy,
                    boost=1.1  # 10% 증가
                )
        
        # 5. 주기적 저장 (10건마다)
        if len(self.loss_cases) % 10 == 0:
            self._save_loss_data()
    
    def get_loss_summary(self) -> Dict:
        """손실 요약 통계"""
        
        if not self.loss_cases:
            return {
                'total_losses': 0,
                'total_loss_amount': 0.0,
                'avg_loss_amount': 0.0,
                'loss_by_category': {},
                'loss_by_scenario': {},
                'loss_by_strategy': {}
            }
        
        total_loss_amount = sum(case['profit_loss'] for case in self.loss_cases)
        avg_loss_amount = total_loss_amount / len(self.loss_cases)
        
        # 카테고리별 집계
        loss_by_category = defaultdict(int)
        for case in self.loss_cases:
            loss_by_category[case.get('loss_category', 'OTHER')] += 1
        
        # 시나리오별 집계
        loss_by_scenario = defaultdict(lambda: {'count': 0, 'amount': 0.0})
        for case in self.loss_cases:
            scenario = case.get('entry_scenario', 'UNKNOWN')
            loss_by_scenario[scenario]['count'] += 1
            loss_by_scenario[scenario]['amount'] += case['profit_loss']
        
        # 전략별 집계
        loss_by_strategy = defaultdict(lambda: {'count': 0, 'amount': 0.0})
        for case in self.loss_cases:
            strategy = case.get('selected_strategy', 'UNKNOWN')
            loss_by_strategy[strategy]['count'] += 1
            loss_by_strategy[strategy]['amount'] += case['profit_loss']
        
        return {
            'total_losses': len(self.loss_cases),
            'total_loss_amount': total_loss_amount,
            'avg_loss_amount': avg_loss_amount,
            'loss_by_category': dict(loss_by_category),
            'loss_by_scenario': dict(loss_by_scenario),
            'loss_by_strategy': dict(loss_by_strategy),
            'most_common_cause': max(loss_by_category.items(), key=lambda x: x[1])[0] if loss_by_category else None
        }
    
    def _load_loss_data(self):
        """저장된 손실 데이터 로드"""
        try:
            loss_file = os.path.join(self.data_dir, "loss_analysis.json")
            
            if os.path.exists(loss_file):
                with open(loss_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.loss_cases = data.get('cases', [])
                    self.loss_patterns = defaultdict(int, data.get('patterns', {}))
                    
                    print(f"✅ 손실 분석 데이터 로드 완료: {len(self.loss_cases)}건")
        
        except Exception as e:
            print(f"⚠️ 손실 데이터 로드 실패: {e}")
    
    def _save_loss_data(self):
        """손실 데이터 저장"""
        try:
            loss_file = os.path.join(self.data_dir, "loss_analysis.json")
            
            data = {
                'cases': self.loss_cases[-1000:],  # 최근 1000건만 저장
                'patterns': dict(self.loss_patterns),
                'last_updated': datetime.now().isoformat()
            }
            
            with open(loss_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 손실 분석 데이터 저장 완료: {len(self.loss_cases)}건")
        
        except Exception as e:
            print(f"⚠️ 손실 데이터 저장 실패: {e}")
