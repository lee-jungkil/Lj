"""
자동 최적화 시스템

기능:
- 최대 손실 도달 시 자동 분석
- 파라미터 자동 최적화
- 복구 계획 생성
- 재시작 조건 학습
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from collections import defaultdict


class AutoOptimizer:
    """자동 최적화 시스템"""
    
    def __init__(
        self,
        risk_manager,
        learning_engine,
        loss_analyzer,
        strategy_selector,
        data_dir: str = "learning_data/optimization"
    ):
        """
        초기화
        
        Args:
            risk_manager: 리스크 관리자
            learning_engine: 학습 엔진
            loss_analyzer: 손실 분석기
            strategy_selector: 전략 선택기
            data_dir: 데이터 디렉토리
        """
        self.risk_manager = risk_manager
        self.learning_engine = learning_engine
        self.loss_analyzer = loss_analyzer
        self.strategy_selector = strategy_selector
        
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        # 최적화 이력
        self.optimization_history = []
        
        # 복구 모드 상태
        self.is_recovery_mode = False
        self.recovery_trades = 0
        self.recovery_stats = {
            'wins': 0,
            'losses': 0,
            'total_profit': 0.0
        }
        
        # 로드
        self._load_optimization_data()
    
    def on_max_loss_reached(self, logger=None) -> Dict:
        """
        최대 손실 도달 시 자동 실행
        
        Args:
            logger: 로거 (선택)
        
        Returns:
            최적화 결과
        """
        if logger:
            logger.log_warning("🚨 최대 손실 도달 - 자동 분석 및 최적화 시작")
        else:
            print("🚨 최대 손실 도달 - 자동 분석 및 최적화 시작")
        
        # 1. 전체 거래 이력 분석
        analysis = self._analyze_trade_history()
        
        # 2. 자동 파라미터 최적화
        optimized_params = self._optimize_parameters(analysis)
        
        # 3. 복구 계획 생성
        recovery_plan = self._generate_recovery_plan(analysis, optimized_params)
        
        # 4. 재시작 조건 정의
        restart_conditions = self._define_restart_conditions(analysis)
        
        # 5. 결과 저장
        optimization_result = {
            'timestamp': datetime.now().isoformat(),
            'trigger': 'MAX_LOSS_REACHED',
            'analysis': analysis,
            'optimized_params': optimized_params,
            'recovery_plan': recovery_plan,
            'restart_conditions': restart_conditions
        }
        
        self._save_optimization_result(optimization_result)
        
        # 6. 복구 모드 활성화
        self.activate_recovery_mode(recovery_plan)
        
        if logger:
            logger.log_info("✅ 자동 최적화 완료 - 복구 모드 진입")
            logger.log_info(f"📊 분석 결과: {analysis.get('summary', {})}")
            logger.log_info(f"🔧 최적화된 파라미터: {optimized_params}")
            logger.log_info(f"📋 복구 계획: {recovery_plan}")
        
        return optimization_result
    
    def _analyze_trade_history(self) -> Dict:
        """전체 거래 이력 분석"""
        
        # 학습 엔진에서 거래 이력 가져오기
        if hasattr(self.learning_engine, 'trade_history'):
            trade_history = list(self.learning_engine.trade_history.values())
        else:
            trade_history = []
        
        if not trade_history:
            return {
                'summary': {
                    'total_trades': 0,
                    'total_profit': 0.0,
                    'win_rate': 0.0
                },
                'loss_analysis': {},
                'by_scenario': {},
                'by_strategy': {},
                'common_mistakes': []
            }
        
        # 손실 거래 필터
        loss_trades = [t for t in trade_history if t.get('profit_loss', 0) < 0]
        win_trades = [t for t in trade_history if t.get('profit_loss', 0) > 0]
        
        # 기본 통계
        total_trades = len(trade_history)
        total_profit = sum(t.get('profit_loss', 0) for t in trade_history)
        win_rate = (len(win_trades) / total_trades * 100) if total_trades > 0 else 0
        
        # 손실 분석 (LossAnalyzer 활용)
        loss_summary = self.loss_analyzer.get_loss_summary() if self.loss_analyzer else {}
        
        # 시나리오별 분석
        by_scenario = self._analyze_by_group(trade_history, 'scenario')
        
        # 전략별 분석
        by_strategy = self._analyze_by_group(trade_history, 'strategy')
        
        # 공통 실수 식별
        common_mistakes = self._identify_common_mistakes(loss_trades)
        
        return {
            'summary': {
                'total_trades': total_trades,
                'win_trades': len(win_trades),
                'loss_trades': len(loss_trades),
                'total_profit': total_profit,
                'avg_profit': total_profit / total_trades if total_trades > 0 else 0,
                'win_rate': win_rate
            },
            'loss_analysis': loss_summary,
            'by_scenario': by_scenario,
            'by_strategy': by_strategy,
            'common_mistakes': common_mistakes
        }
    
    def _analyze_by_group(self, trades: List[Dict], group_key: str) -> Dict:
        """그룹별 분석 (시나리오 또는 전략)"""
        
        grouped = defaultdict(lambda: {
            'trades': 0,
            'wins': 0,
            'losses': 0,
            'total_profit': 0.0,
            'win_rate': 0.0
        })
        
        for trade in trades:
            group = trade.get(group_key, 'UNKNOWN')
            profit = trade.get('profit_loss', 0)
            
            grouped[group]['trades'] += 1
            grouped[group]['total_profit'] += profit
            
            if profit > 0:
                grouped[group]['wins'] += 1
            else:
                grouped[group]['losses'] += 1
        
        # 승률 계산
        for group in grouped:
            total = grouped[group]['trades']
            wins = grouped[group]['wins']
            grouped[group]['win_rate'] = (wins / total * 100) if total > 0 else 0
            grouped[group]['avg_profit'] = grouped[group]['total_profit'] / total if total > 0 else 0
        
        return dict(grouped)
    
    def _identify_common_mistakes(self, loss_trades: List[Dict]) -> List[str]:
        """공통 실수 식별"""
        mistakes = []
        
        if not loss_trades:
            return mistakes
        
        # 1. 큰 손실 체크
        large_losses = [t for t in loss_trades if t.get('profit_loss', 0) < -50000]
        if len(large_losses) > len(loss_trades) * 0.2:  # 20% 이상
            mistakes.append("대형 손실 발생 빈도 높음 - 손절 기준 강화 필요")
        
        # 2. 빠른 청산
        quick_exits = [t for t in loss_trades if t.get('hold_time', 0) < 60]
        if len(quick_exits) > len(loss_trades) * 0.3:  # 30% 이상
            mistakes.append("조급한 청산 빈번 - 보유 시간 여유 필요")
        
        # 3. 과도한 보유
        long_holds = [t for t in loss_trades if t.get('hold_time', 0) > 3600]
        if len(long_holds) > len(loss_trades) * 0.2:
            mistakes.append("과도한 보유로 손실 확대 - 빠른 손절 필요")
        
        # 4. 특정 시나리오 반복 실패
        scenario_losses = defaultdict(int)
        for trade in loss_trades:
            scenario = trade.get('scenario', 'UNKNOWN')
            scenario_losses[scenario] += 1
        
        if scenario_losses:
            worst_scenario = max(scenario_losses.items(), key=lambda x: x[1])
            if worst_scenario[1] > 5:
                mistakes.append(f"'{worst_scenario[0]}' 시나리오에서 반복 실패 - 진입 회피 권장")
        
        return mistakes
    
    def _optimize_parameters(self, analysis: Dict) -> Dict:
        """파라미터 자동 최적화"""
        optimized = {}
        
        summary = analysis.get('summary', {})
        by_strategy = analysis.get('by_strategy', {})
        by_scenario = analysis.get('by_scenario', {})
        
        # 1. 리스크 파라미터 조정
        avg_loss = abs(summary.get('avg_profit', 0)) if summary.get('avg_profit', 0) < 0 else 0
        
        if avg_loss > 20000:  # 평균 손실이 2만원 이상
            optimized['max_position_ratio'] = 0.15  # 30% → 15%
            optimized['stop_loss_ratio'] = 0.01  # 손절 강화 1%
        elif avg_loss > 10000:
            optimized['max_position_ratio'] = 0.20
            optimized['stop_loss_ratio'] = 0.015
        else:
            optimized['max_position_ratio'] = 0.25
            optimized['stop_loss_ratio'] = 0.02
        
        # 2. 전략 가중치 조정
        strategy_adjustments = {}
        for strategy, stats in by_strategy.items():
            win_rate = stats.get('win_rate', 0)
            
            if win_rate < 40:
                strategy_adjustments[strategy] = 0.3  # 가중치 70% 감소
            elif win_rate < 50:
                strategy_adjustments[strategy] = 0.5  # 가중치 50% 감소
            elif win_rate > 70:
                strategy_adjustments[strategy] = 1.3  # 가중치 30% 증가
        
        if strategy_adjustments:
            optimized['strategy_weights'] = strategy_adjustments
        
        # 3. 시나리오별 진입 조건 강화
        scenario_thresholds = {}
        for scenario, stats in by_scenario.items():
            win_rate = stats.get('win_rate', 0)
            
            if win_rate < 40:
                scenario_thresholds[scenario] = 80  # 신뢰도 80% 이상 필요
            elif win_rate < 50:
                scenario_thresholds[scenario] = 70
            else:
                scenario_thresholds[scenario] = 60  # 기본값
        
        if scenario_thresholds:
            optimized['scenario_confidence_thresholds'] = scenario_thresholds
        
        return optimized
    
    def _generate_recovery_plan(self, analysis: Dict, optimized_params: Dict) -> Dict:
        """복구 계획 생성"""
        
        summary = analysis.get('summary', {})
        win_rate = summary.get('win_rate', 0)
        
        # 승률에 따라 복구 계획 수준 결정
        if win_rate < 40:
            # 심각한 상태 - 매우 보수적
            return {
                'mode': 'ULTRA_CONSERVATIVE',
                'max_positions': 1,
                'position_size_ratio': 0.10,  # 10%만 사용
                'target_profit_ratio': 0.3,  # 0.3% 목표
                'stop_loss_ratio': 0.005,  # 0.5% 손절
                'allowed_strategies': ['conservative_scalping'],
                'observation_period': 20,  # 20회 거래
                'success_criteria': {
                    'min_win_rate': 70,
                    'min_avg_profit': 0.2,
                    'max_consecutive_losses': 2
                }
            }
        
        elif win_rate < 55:
            # 보통 상태 - 보수적
            return {
                'mode': 'CONSERVATIVE',
                'max_positions': 2,
                'position_size_ratio': 0.15,
                'target_profit_ratio': 0.5,
                'stop_loss_ratio': 0.01,
                'allowed_strategies': ['conservative_scalping', 'mean_reversion'],
                'observation_period': 15,
                'success_criteria': {
                    'min_win_rate': 65,
                    'min_avg_profit': 0.3,
                    'max_consecutive_losses': 3
                }
            }
        
        else:
            # 양호 상태 - 점진적 회복
            return {
                'mode': 'GRADUAL_RECOVERY',
                'max_positions': 2,
                'position_size_ratio': 0.20,
                'target_profit_ratio': 0.8,
                'stop_loss_ratio': 0.015,
                'allowed_strategies': ['conservative_scalping', 'mean_reversion', 'aggressive_scalping'],
                'observation_period': 10,
                'success_criteria': {
                    'min_win_rate': 60,
                    'min_avg_profit': 0.5,
                    'max_consecutive_losses': 3
                }
            }
    
    def _define_restart_conditions(self, analysis: Dict) -> List[str]:
        """재시작 조건 정의"""
        
        summary = analysis.get('summary', {})
        win_rate = summary.get('win_rate', 0)
        
        conditions = [
            "복구 계획의 관찰 기간 완료",
            "복구 모드에서 설정된 성공 기준 달성"
        ]
        
        if win_rate < 50:
            conditions.extend([
                "승률 65% 이상 달성",
                "평균 수익률 +0.5% 이상",
                "연속 손실 2회 이하 유지"
            ])
        else:
            conditions.extend([
                "승률 60% 이상 유지",
                "평균 수익률 +0.3% 이상",
                "연속 손실 3회 이하 유지"
            ])
        
        return conditions
    
    def activate_recovery_mode(self, recovery_plan: Dict):
        """복구 모드 활성화"""
        self.is_recovery_mode = True
        self.recovery_trades = 0
        self.recovery_stats = {
            'wins': 0,
            'losses': 0,
            'total_profit': 0.0,
            'consecutive_losses': 0
        }
        self.current_recovery_plan = recovery_plan
        
        print(f"🔄 복구 모드 활성화: {recovery_plan['mode']}")
        print(f"📋 관찰 기간: {recovery_plan['observation_period']}회 거래")
    
    def check_recovery_progress(self, trade_result: Dict) -> Dict:
        """복구 진행 상황 체크"""
        
        if not self.is_recovery_mode:
            return {'status': 'NOT_IN_RECOVERY'}
        
        # 거래 기록
        self.recovery_trades += 1
        profit = trade_result.get('profit_loss', 0)
        self.recovery_stats['total_profit'] += profit
        
        if profit > 0:
            self.recovery_stats['wins'] += 1
            self.recovery_stats['consecutive_losses'] = 0
        else:
            self.recovery_stats['losses'] += 1
            self.recovery_stats['consecutive_losses'] += 1
        
        # 성공 기준 체크
        plan = self.current_recovery_plan
        criteria = plan['success_criteria']
        
        total_trades = self.recovery_trades
        win_rate = (self.recovery_stats['wins'] / total_trades * 100) if total_trades > 0 else 0
        avg_profit = self.recovery_stats['total_profit'] / total_trades if total_trades > 0 else 0
        
        # 관찰 기간 완료 체크
        if total_trades >= plan['observation_period']:
            # 성공 기준 달성 여부
            success = (
                win_rate >= criteria['min_win_rate'] and
                avg_profit >= criteria['min_avg_profit'] and
                self.recovery_stats['consecutive_losses'] <= criteria['max_consecutive_losses']
            )
            
            if success:
                self.deactivate_recovery_mode()
                return {
                    'status': 'RECOVERY_COMPLETE',
                    'win_rate': win_rate,
                    'avg_profit': avg_profit,
                    'message': '복구 완료 - 정상 모드 복귀'
                }
            else:
                # 연장 필요
                return {
                    'status': 'RECOVERY_EXTENDED',
                    'win_rate': win_rate,
                    'avg_profit': avg_profit,
                    'message': f'기준 미달성 - {plan["observation_period"]}회 추가 관찰'
                }
        
        # 진행 중
        return {
            'status': 'IN_PROGRESS',
            'trades': f"{total_trades}/{plan['observation_period']}",
            'win_rate': win_rate,
            'avg_profit': avg_profit,
            'consecutive_losses': self.recovery_stats['consecutive_losses']
        }
    
    def deactivate_recovery_mode(self):
        """복구 모드 비활성화"""
        self.is_recovery_mode = False
        print("✅ 복구 모드 종료 - 정상 모드 복귀")
    
    def _save_optimization_result(self, result: Dict):
        """최적화 결과 저장"""
        try:
            self.optimization_history.append(result)
            
            opt_file = os.path.join(self.data_dir, "optimization_history.json")
            
            with open(opt_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'history': self.optimization_history[-100:],  # 최근 100건
                    'last_updated': datetime.now().isoformat()
                }, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 최적화 결과 저장 완료")
        
        except Exception as e:
            print(f"⚠️ 최적화 결과 저장 실패: {e}")
    
    def _load_optimization_data(self):
        """최적화 데이터 로드"""
        try:
            opt_file = os.path.join(self.data_dir, "optimization_history.json")
            
            if os.path.exists(opt_file):
                with open(opt_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.optimization_history = data.get('history', [])
                    
                    print(f"✅ 최적화 이력 로드 완료: {len(self.optimization_history)}건")
        
        except Exception as e:
            print(f"⚠️ 최적화 데이터 로드 실패: {e}")
