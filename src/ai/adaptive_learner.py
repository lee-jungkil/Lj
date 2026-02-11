"""
통합 AI 학습 시스템 (Adaptive Learner)
모든 AI 컴포넌트를 통합하여 지속적으로 학습하고 진화하는 시스템
"""

from typing import Dict, List, Optional
from datetime import datetime
import json
import os


class AdaptiveLearner:
    """통합 AI 학습 및 최적화 시스템"""
    
    def __init__(
        self,
        learning_engine,
        scenario_identifier,
        strategy_selector,
        holding_time_optimizer,
        data_dir: str = "trading_logs/learning"
    ):
        """
        Args:
            learning_engine: 기존 학습 엔진
            scenario_identifier: 시장 상황 식별기
            strategy_selector: 전략 선택기
            holding_time_optimizer: 보유 시간 최적화
            data_dir: 데이터 디렉토리
        """
        self.learning_engine = learning_engine
        self.scenario_identifier = scenario_identifier
        self.strategy_selector = strategy_selector
        self.holding_optimizer = holding_time_optimizer
        
        self.data_dir = data_dir
        self.adaptive_stats_file = os.path.join(data_dir, "adaptive_stats.json")
        
        # 통합 통계
        self.adaptive_stats = self._load_adaptive_stats()
        
        # 학습 단계
        self.learning_phase = self._determine_learning_phase()
        
    def _load_adaptive_stats(self) -> Dict:
        """통합 통계 로드"""
        if os.path.exists(self.adaptive_stats_file):
            try:
                with open(self.adaptive_stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self._init_adaptive_stats()
        return self._init_adaptive_stats()
    
    def _init_adaptive_stats(self) -> Dict:
        """통합 통계 초기화"""
        return {
            'total_trades': 0,
            'total_learning_cycles': 0,
            'scenario_accuracy': 0.0,
            'strategy_selection_accuracy': 0.0,
            'holding_time_accuracy': 0.0,
            'overall_win_rate': 0.0,
            'overall_profit': 0.0,
            'phase_history': [],
            'milestones': [],
            'last_updated': datetime.now().isoformat()
        }
    
    def _save_adaptive_stats(self):
        """통합 통계 저장"""
        try:
            os.makedirs(self.data_dir, exist_ok=True)
            with open(self.adaptive_stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.adaptive_stats, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ 통합 통계 저장 실패: {e}")
    
    def _determine_learning_phase(self) -> str:
        """
        현재 학습 단계 판단
        
        Phase 2-A: 규칙 기반 (0-20 거래)
        Phase 2-B: 학습 데이터 수집 (20-100 거래)
        Phase 2-C: 고급 최적화 (100+ 거래)
        """
        total_trades = self.adaptive_stats.get('total_trades', 0)
        
        if total_trades < 20:
            return 'Phase 2-A: 규칙 기반'
        elif total_trades < 100:
            return 'Phase 2-B: 학습 데이터 수집'
        else:
            return 'Phase 2-C: 고급 최적화'
    
    def analyze_and_decide(
        self,
        ticker: str,
        df,
        current_price: float,
        available_capital: float
    ) -> Dict:
        """
        종합 분석 및 의사결정
        
        프로세스:
        1. 시장 상황 식별 (45가지 시나리오)
        2. 최적 전략 선택
        3. 분할 방식 결정
        4. 신호 생성
        
        Returns:
            {
                'action': 'BUY'|'HOLD'|'SKIP',
                'scenario': Dict,
                'strategy': Dict,
                'confidence': float,
                'reason': str,
                'split_plan': Dict (if BUY)
            }
        """
        print(f"\n{'='*70}")
        print(f"🧠 AI 종합 분석 시작: {ticker}")
        print(f"   현재가: {current_price:,.0f}원")
        print(f"   가용 자금: {available_capital:,.0f}원")
        print(f"   학습 단계: {self.learning_phase}")
        print(f"{'='*70}")
        
        # 1. 시장 상황 식별
        scenario = self.scenario_identifier.identify(df, ticker)
        
        print(f"\n📊 시장 상황:")
        print(f"   주요 시나리오: #{scenario['primary_scenario']} - {scenario['scenario_names'][0]}")
        if scenario['secondary_scenarios']:
            print(f"   부가 시나리오: {', '.join([f'#{s}' for s in scenario['secondary_scenarios']])}")
        print(f"   신뢰도: {scenario['confidence']:.1f}%")
        
        # 변동성, 추세 추출
        indicators = scenario['indicators']
        volatility = indicators.get('volatility', 2.0)
        
        # 추세 판단
        price_change_4h = indicators.get('price_change_4h', 0)
        if price_change_4h > 2:
            trend = 'UP'
        elif price_change_4h < -2:
            trend = 'DOWN'
        else:
            trend = 'SIDEWAYS'
        
        volume_ratio = indicators.get('volume_ratio', 1.0)
        
        # 2. 최적 전략 선택
        strategy_selection = self.strategy_selector.select_strategy(
            scenario_id=scenario['primary_scenario'],
            scenario_name=scenario['scenario_names'][0],
            volatility=volatility,
            trend=trend,
            volume_ratio=volume_ratio,
            confidence=scenario['confidence']
        )
        
        # 3. 기존 학습 엔진 통합
        market_decision = self.learning_engine.analyze_market_decision(
            scenario['primary_scenario'],
            scenario['confidence']
        )
        
        print(f"\n🤖 AI 학습 엔진 의견:")
        print(f"   권장 액션: {market_decision['action']}")
        print(f"   AI 신뢰도: {market_decision['confidence']:.1f}%")
        print(f"   사유: {market_decision['reason']}")
        
        # 4. 최종 의사결정
        final_confidence = (scenario['confidence'] + strategy_selection['confidence'] + market_decision['confidence']) / 3
        
        # 매수 조건 판단
        should_buy = False
        reason = ""
        
        if market_decision['action'] == 'STRONG_BUY' and final_confidence > 70:
            should_buy = True
            reason = "AI 강력 매수 신호 + 높은 종합 신뢰도"
        elif market_decision['action'] == 'CONSIDER_BUY' and final_confidence > 65:
            should_buy = True
            reason = "AI 매수 고려 + 유리한 시장 상황"
        elif market_decision['action'] == 'AVOID':
            should_buy = False
            reason = "AI 매수 회피 권장"
        else:
            should_buy = final_confidence > 60
            reason = f"종합 신뢰도 {final_confidence:.1f}% 기반 판단"
        
        result = {
            'action': 'BUY' if should_buy else 'HOLD',
            'scenario': scenario,
            'strategy': strategy_selection,
            'market_decision': market_decision,
            'confidence': final_confidence,
            'reason': reason,
            'volatility': volatility,
            'trend': trend,
            'volume_ratio': volume_ratio,
            'timestamp': datetime.now()
        }
        
        print(f"\n{'='*70}")
        print(f"✅ 최종 결정: {result['action']}")
        print(f"   종합 신뢰도: {final_confidence:.1f}%")
        print(f"   사유: {reason}")
        print(f"{'='*70}\n")
        
        return result
    
    def analyze_exit_decision(
        self,
        ticker: str,
        df,
        entry_price: float,
        current_price: float,
        holding_time: int,
        strategy: str,
        scenario_id: int
    ) -> Dict:
        """
        청산 의사결정
        
        Returns:
            {
                'should_exit': bool,
                'confidence': float,
                'reason': str,
                'holding_analysis': Dict
            }
        """
        profit_ratio = (current_price - entry_price) / entry_price * 100
        
        print(f"\n🔍 청산 분석: {ticker}")
        print(f"   보유 시간: {holding_time}초 ({holding_time//60}분)")
        print(f"   현재 수익: {profit_ratio:+.2f}%")
        
        # 1. 보유 시간 AI 분석
        holding_analysis = self.holding_optimizer.predict_optimal_holding_time(
            scenario_id=scenario_id,
            strategy=strategy,
            current_profit=profit_ratio
        )
        
        should_exit_by_time, time_reason = self.holding_optimizer.should_exit_now(
            scenario_id=scenario_id,
            strategy=strategy,
            current_holding_time=holding_time,
            current_profit=profit_ratio
        )
        
        # 2. 시장 상황 재분석
        current_scenario = self.scenario_identifier.identify(df, ticker)
        
        # 3. 종합 판단
        exit_signals = []
        
        if should_exit_by_time:
            exit_signals.append(f"보유시간AI: {time_reason}")
        
        # 추세 반전
        if current_scenario['primary_scenario'] in [7, 34]:  # 추세 전환
            exit_signals.append("추세 전환 감지")
        
        # 손실 확대
        if profit_ratio < -1.5:
            exit_signals.append(f"손실 확대 ({profit_ratio:.2f}%)")
        
        # 목표 수익 달성
        expected_profit = holding_analysis['expected_profit']
        if profit_ratio >= expected_profit * 1.2:
            exit_signals.append(f"목표 수익 초과 달성 ({profit_ratio:.2f}% > {expected_profit * 1.2:.2f}%)")
        
        should_exit = len(exit_signals) >= 2 or should_exit_by_time
        confidence = min(100, len(exit_signals) * 30 + (50 if should_exit_by_time else 0))
        
        result = {
            'should_exit': should_exit,
            'confidence': confidence,
            'reason': "; ".join(exit_signals) if exit_signals else "홀딩 유지",
            'holding_analysis': holding_analysis,
            'current_scenario': current_scenario,
            'profit_ratio': profit_ratio,
            'timestamp': datetime.now()
        }
        
        print(f"   청산 권장: {'✅ 예' if should_exit else '❌ 아니오'}")
        print(f"   신뢰도: {confidence:.1f}%")
        print(f"   사유: {result['reason']}\n")
        
        return result
    
    def record_full_trade_cycle(
        self,
        ticker: str,
        entry_scenario: Dict,
        exit_scenario: Dict,
        strategy: str,
        entry_price: float,
        exit_price: float,
        holding_time: int,
        profit_ratio: float
    ):
        """
        전체 거래 사이클 기록 및 학습
        
        모든 AI 컴포넌트에 학습 데이터 전달
        """
        success = profit_ratio > 0
        
        print(f"\n{'='*70}")
        print(f"📚 거래 학습 기록 중...")
        print(f"   티커: {ticker}")
        print(f"   수익률: {profit_ratio:+.2f}%")
        print(f"   보유 시간: {holding_time}초")
        print(f"{'='*70}")
        
        # 1. 전략 선택기 학습
        self.strategy_selector.record_trade_result(
            strategy=strategy,
            scenario_id=entry_scenario['primary_scenario'],
            profit_ratio=profit_ratio,
            success=success
        )
        
        # 2. 보유 시간 최적화 학습
        self.holding_optimizer.record_trade(
            ticker=ticker,
            scenario_id=entry_scenario['primary_scenario'],
            entry_price=entry_price,
            exit_price=exit_price,
            holding_time=holding_time,
            profit_ratio=profit_ratio,
            strategy=strategy
        )
        
        # 3. 통합 통계 업데이트
        self.adaptive_stats['total_trades'] += 1
        self.adaptive_stats['total_learning_cycles'] += 1
        self.adaptive_stats['overall_profit'] += profit_ratio
        
        # 승률 계산
        if success:
            wins = self.adaptive_stats.get('total_wins', 0) + 1
            self.adaptive_stats['total_wins'] = wins
        
        total = self.adaptive_stats['total_trades']
        self.adaptive_stats['overall_win_rate'] = (
            self.adaptive_stats.get('total_wins', 0) / total * 100
        )
        
        # 학습 단계 업데이트
        old_phase = self.learning_phase
        self.learning_phase = self._determine_learning_phase()
        
        if old_phase != self.learning_phase:
            milestone = {
                'phase': self.learning_phase,
                'trade_count': total,
                'win_rate': self.adaptive_stats['overall_win_rate'],
                'timestamp': datetime.now().isoformat()
            }
            self.adaptive_stats['milestones'].append(milestone)
            print(f"\n🎉 학습 단계 업그레이드: {self.learning_phase}")
        
        self.adaptive_stats['last_updated'] = datetime.now().isoformat()
        self._save_adaptive_stats()
        
        print(f"✅ 학습 완료")
        print(f"   총 거래 수: {total}")
        print(f"   전체 승률: {self.adaptive_stats['overall_win_rate']:.2f}%")
        print(f"   학습 단계: {self.learning_phase}\n")
    
    def get_comprehensive_report(self) -> Dict:
        """종합 리포트 생성"""
        return {
            'learning_phase': self.learning_phase,
            'adaptive_stats': self.adaptive_stats,
            'strategy_performance': self.strategy_selector.get_all_strategies_performance(),
            'holding_time_stats': self.holding_optimizer.get_stats_report(),
            'learning_engine_stats': self.learning_engine.get_recent_performance(days=30),
            'timestamp': datetime.now()
        }
    
    def print_status(self):
        """현재 상태 출력"""
        stats = self.adaptive_stats
        
        print(f"\n{'='*70}")
        print(f"🧠 AI 통합 학습 시스템 상태")
        print(f"{'='*70}")
        print(f"학습 단계: {self.learning_phase}")
        print(f"총 거래 수: {stats['total_trades']}")
        print(f"학습 사이클: {stats['total_learning_cycles']}")
        print(f"전체 승률: {stats['overall_win_rate']:.2f}%")
        print(f"누적 수익: {stats['overall_profit']:+.2f}%")
        
        if stats.get('milestones'):
            print(f"\n📈 달성한 마일스톤:")
            for milestone in stats['milestones'][-3:]:
                print(f"   - {milestone['phase']}: 거래 {milestone['trade_count']}회, 승률 {milestone['win_rate']:.1f}%")
        
        print(f"{'='*70}\n")
