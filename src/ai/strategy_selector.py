"""
AI 전략 선택기
시장 상황 + 과거 성과 + AI 학습을 기반으로 최적 전략 자동 선택
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json
import os


class StrategySelector:
    """AI 기반 전략 선택기"""
    
    # 전략 정의
    STRATEGIES = {
        'UltraScalping': {
            'name': '초단타 (Ultra Scalping)',
            'timeframe': '1-5분',
            'profit_target': '0.5-1.0%',
            'best_scenarios': [1, 9, 10, 21, 22],  # 강한 상승, 급등/락, 거래량 폭증
            'volatility_range': (3, 10),
            'description': '급등/급락 시 초고속 진입'
        },
        'AggressiveScalping': {
            'name': '공격적 스캘핑',
            'timeframe': '5-15분',
            'profit_target': '1.0-1.5%',
            'best_scenarios': [1, 2, 15, 22, 31],  # 상승 추세, 변동성 급증
            'volatility_range': (2, 5),
            'description': 'RSI + 거래량 기반 단타'
        },
        'ConservativeScalping': {
            'name': '보수적 스캘핑',
            'timeframe': '10-30분',
            'profit_target': '0.8-1.2%',
            'best_scenarios': [5, 6, 13, 14, 23],  # 횡보장, 중/저변동성
            'volatility_range': (1, 3),
            'description': '볼린저밴드 기반 안전 매매'
        },
        'MeanReversion': {
            'name': '평균 회귀',
            'timeframe': '30-60분',
            'profit_target': '1.5-2.5%',
            'best_scenarios': [17, 18, 32, 37, 39],  # BB 돌파, RSI 과매도, 지지선
            'volatility_range': (2, 5),
            'description': '평균 복귀 패턴 활용'
        },
        'GridTrading': {
            'name': '그리드 거래',
            'timeframe': '1시간+',
            'profit_target': '2.0-4.0%',
            'best_scenarios': [5, 6, 14, 19, 43],  # 횡보, 저변동성, 삼각수렴
            'volatility_range': (0.5, 2),
            'description': '구간 매매 전략'
        }
    }
    
    def __init__(self, data_dir: str = "trading_logs/learning"):
        """
        Args:
            data_dir: 학습 데이터 디렉토리
        """
        self.data_dir = data_dir
        self.performance_file = os.path.join(data_dir, "strategy_performance.json")
        
        # 전략별 성과 데이터
        self.performance_data = self._load_performance_data()
        
        # 선택 히스토리
        self.selection_history = []
        
    def _load_performance_data(self) -> Dict:
        """전략 성과 데이터 로드"""
        if os.path.exists(self.performance_file):
            try:
                with open(self.performance_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self._init_performance_data()
        return self._init_performance_data()
    
    def _init_performance_data(self) -> Dict:
        """성과 데이터 초기화"""
        data = {}
        for strategy_key in self.STRATEGIES.keys():
            data[strategy_key] = {
                'total_trades': 0,
                'wins': 0,
                'losses': 0,
                'win_rate': 0.0,
                'avg_profit': 0.0,
                'avg_loss': 0.0,
                'total_profit': 0.0,
                'scenario_performance': {},  # 시나리오별 성과
                'last_updated': datetime.now().isoformat()
            }
        return data
    
    def _save_performance_data(self):
        """성과 데이터 저장"""
        try:
            os.makedirs(self.data_dir, exist_ok=True)
            with open(self.performance_file, 'w', encoding='utf-8') as f:
                json.dump(self.performance_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ 전략 성과 저장 실패: {e}")
    
    def select_strategy(
        self,
        scenario_id: int,
        scenario_name: str,
        volatility: float,
        trend: str,
        volume_ratio: float,
        confidence: float
    ) -> Dict:
        """
        최적 전략 선택
        
        Args:
            scenario_id: 현재 시나리오 ID (1-45)
            scenario_name: 시나리오 이름
            volatility: 변동성 (%)
            trend: 추세 ('UP', 'DOWN', 'SIDEWAYS')
            volume_ratio: 거래량 비율
            confidence: 시나리오 신뢰도 (0-100)
        
        Returns:
            {
                'strategy': str,
                'strategy_name': str,
                'confidence': float,
                'reason': str,
                'alternative': str,
                'expected_profit': float,
                'expected_win_rate': float
            }
        """
        print(f"\n{'='*60}")
        print(f"🎯 AI 전략 선택 시작")
        print(f"   시나리오: #{scenario_id} - {scenario_name}")
        print(f"   변동성: {volatility:.2f}%")
        print(f"   추세: {trend}")
        print(f"   거래량: {volume_ratio:.2f}x")
        print(f"{'='*60}")
        
        # 각 전략 점수 계산
        strategy_scores = {}
        
        for strategy_key, strategy_info in self.STRATEGIES.items():
            score = self._calculate_strategy_score(
                strategy_key=strategy_key,
                scenario_id=scenario_id,
                volatility=volatility,
                trend=trend,
                volume_ratio=volume_ratio,
                confidence=confidence
            )
            strategy_scores[strategy_key] = score
        
        # 최고 점수 전략
        best_strategy = max(strategy_scores, key=strategy_scores.get)
        best_score = strategy_scores[best_strategy]
        
        # 두 번째 전략
        sorted_strategies = sorted(strategy_scores.items(), key=lambda x: x[1], reverse=True)
        alternative_strategy = sorted_strategies[1][0] if len(sorted_strategies) > 1 else best_strategy
        
        # 성과 예측
        performance = self.performance_data.get(best_strategy, {})
        expected_profit = performance.get('avg_profit', 1.0)
        expected_win_rate = performance.get('win_rate', 65.0)
        
        # 선택 이유
        reason = self._generate_selection_reason(
            best_strategy, scenario_id, volatility, trend, best_score
        )
        
        result = {
            'strategy': best_strategy,
            'strategy_name': self.STRATEGIES[best_strategy]['name'],
            'confidence': round(best_score, 2),
            'reason': reason,
            'alternative': alternative_strategy,
            'expected_profit': round(expected_profit, 3),
            'expected_win_rate': round(expected_win_rate, 2),
            'all_scores': strategy_scores,
            'timestamp': datetime.now()
        }
        
        # 히스토리 저장
        self.selection_history.append(result)
        if len(self.selection_history) > 100:
            self.selection_history.pop(0)
        
        print(f"\n✅ 선택된 전략: {result['strategy_name']}")
        print(f"   신뢰도: {result['confidence']:.1f}%")
        print(f"   사유: {result['reason']}")
        print(f"   예상 승률: {result['expected_win_rate']:.1f}%")
        print(f"   예상 수익: {result['expected_profit']:.2f}%\n")
        
        return result
    
    def _calculate_strategy_score(
        self,
        strategy_key: str,
        scenario_id: int,
        volatility: float,
        trend: str,
        volume_ratio: float,
        confidence: float
    ) -> float:
        """
        전략 점수 계산 (0-100)
        
        점수 구성:
        - 시나리오 적합도: 40점
        - 변동성 적합도: 20점
        - 과거 성과: 30점
        - 시장 조건: 10점
        """
        score = 0.0
        strategy_info = self.STRATEGIES[strategy_key]
        
        # 1. 시나리오 적합도 (40점)
        best_scenarios = strategy_info['best_scenarios']
        if scenario_id in best_scenarios:
            score += 40.0
        elif scenario_id in [s for s in range(1, 46) if abs(s - min(best_scenarios)) <= 2]:
            score += 20.0  # 인접 시나리오
        
        # 2. 변동성 적합도 (20점)
        vol_min, vol_max = strategy_info['volatility_range']
        if vol_min <= volatility <= vol_max:
            score += 20.0
        elif vol_min * 0.8 <= volatility <= vol_max * 1.2:
            score += 10.0  # 근접
        
        # 3. 과거 성과 (30점)
        performance = self.performance_data.get(strategy_key, {})
        if performance.get('total_trades', 0) >= 10:
            win_rate = performance.get('win_rate', 50.0)
            avg_profit = performance.get('avg_profit', 0.0)
            
            # 승률 점수
            score += (win_rate / 100) * 15
            
            # 평균 수익 점수
            if avg_profit > 0:
                score += min(avg_profit / 2 * 15, 15)
        else:
            # 데이터 부족 시 기본 점수
            score += 15.0
        
        # 4. 시장 조건 (10점)
        if trend == 'UP' and strategy_key in ['UltraScalping', 'AggressiveScalping']:
            score += 10.0
        elif trend == 'SIDEWAYS' and strategy_key in ['ConservativeScalping', 'GridTrading']:
            score += 10.0
        elif trend == 'DOWN' and strategy_key == 'MeanReversion':
            score += 10.0
        else:
            score += 5.0
        
        # 신뢰도 가중치
        score *= (confidence / 100)
        
        return min(score, 100.0)
    
    def _generate_selection_reason(
        self,
        strategy_key: str,
        scenario_id: int,
        volatility: float,
        trend: str,
        score: float
    ) -> str:
        """선택 이유 생성"""
        strategy_info = self.STRATEGIES[strategy_key]
        
        reasons = []
        
        # 시나리오 적합성
        if scenario_id in strategy_info['best_scenarios']:
            reasons.append(f"현재 시나리오에 최적화됨")
        
        # 변동성
        vol_min, vol_max = strategy_info['volatility_range']
        if vol_min <= volatility <= vol_max:
            reasons.append(f"적절한 변동성 범위")
        
        # 과거 성과
        performance = self.performance_data.get(strategy_key, {})
        if performance.get('win_rate', 0) > 70:
            reasons.append(f"높은 승률 ({performance['win_rate']:.1f}%)")
        
        # 추세
        if trend == 'UP' and strategy_key in ['UltraScalping', 'AggressiveScalping']:
            reasons.append("상승 추세에 강함")
        
        if not reasons:
            reasons.append(f"종합 점수 {score:.1f}점")
        
        return ", ".join(reasons)
    
    def record_trade_result(
        self,
        strategy: str,
        scenario_id: int,
        profit_ratio: float,
        success: bool
    ):
        """
        거래 결과 기록
        
        Args:
            strategy: 사용된 전략
            scenario_id: 시나리오 ID
            profit_ratio: 수익률 (%)
            success: 성공 여부
        """
        if strategy not in self.performance_data:
            self.performance_data[strategy] = self._init_performance_data()[strategy]
        
        perf = self.performance_data[strategy]
        
        # 전체 통계 업데이트
        perf['total_trades'] += 1
        if success:
            perf['wins'] += 1
            if perf['avg_profit'] == 0:
                perf['avg_profit'] = profit_ratio
            else:
                perf['avg_profit'] = (perf['avg_profit'] * (perf['wins'] - 1) + profit_ratio) / perf['wins']
        else:
            perf['losses'] += 1
            if perf['avg_loss'] == 0:
                perf['avg_loss'] = profit_ratio
            else:
                perf['avg_loss'] = (perf['avg_loss'] * (perf['losses'] - 1) + profit_ratio) / perf['losses']
        
        perf['win_rate'] = (perf['wins'] / perf['total_trades']) * 100
        perf['total_profit'] += profit_ratio
        
        # 시나리오별 성과
        scenario_key = str(scenario_id)
        if scenario_key not in perf['scenario_performance']:
            perf['scenario_performance'][scenario_key] = {
                'trades': 0,
                'wins': 0,
                'avg_profit': 0.0
            }
        
        scenario_perf = perf['scenario_performance'][scenario_key]
        scenario_perf['trades'] += 1
        if success:
            scenario_perf['wins'] += 1
        scenario_perf['avg_profit'] = (
            (scenario_perf['avg_profit'] * (scenario_perf['trades'] - 1) + profit_ratio) / 
            scenario_perf['trades']
        )
        
        perf['last_updated'] = datetime.now().isoformat()
        
        # 저장
        self._save_performance_data()
    
    def get_strategy_info(self, strategy_key: str) -> Dict:
        """전략 상세 정보 조회"""
        if strategy_key not in self.STRATEGIES:
            return {}
        
        strategy_info = self.STRATEGIES[strategy_key].copy()
        performance = self.performance_data.get(strategy_key, {})
        
        return {
            **strategy_info,
            'performance': performance
        }
    
    def get_all_strategies_performance(self) -> Dict:
        """전체 전략 성과 조회"""
        return self.performance_data.copy()
    
    def get_best_strategy_for_scenario(self, scenario_id: int) -> str:
        """특정 시나리오의 최고 성과 전략"""
        best_strategy = None
        best_win_rate = 0.0
        
        for strategy, perf in self.performance_data.items():
            scenario_key = str(scenario_id)
            if scenario_key in perf.get('scenario_performance', {}):
                scenario_perf = perf['scenario_performance'][scenario_key]
                win_rate = scenario_perf['wins'] / scenario_perf['trades'] * 100 if scenario_perf['trades'] > 0 else 0
                
                if win_rate > best_win_rate:
                    best_win_rate = win_rate
                    best_strategy = strategy
        
        return best_strategy or 'AggressiveScalping'
