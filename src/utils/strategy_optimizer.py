"""
적응형 전략 최적화 시스템
과거 성과 기반 실시간 전략 가중치 조정
"""

from typing import Dict, List, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from collections import defaultdict
import json
import os


@dataclass
class StrategyPerformance:
    """전략별 성과 추적"""
    strategy_name: str
    trades: int = 0
    wins: int = 0
    losses: int = 0
    total_profit: float = 0.0
    total_loss: float = 0.0
    avg_profit: float = 0.0
    avg_loss: float = 0.0
    win_rate: float = 0.0
    profit_factor: float = 0.0  # 총이익 / 총손실
    sharpe_ratio: float = 0.0
    max_drawdown: float = 0.0
    
    # 시장 상황별 성과
    market_conditions: Dict[str, Dict] = field(default_factory=dict)
    
    def calculate_metrics(self):
        """성과 지표 계산"""
        if self.trades == 0:
            return
        
        # 승률
        self.win_rate = (self.wins / self.trades) * 100
        
        # 평균 손익
        self.avg_profit = self.total_profit / self.wins if self.wins > 0 else 0
        self.avg_loss = abs(self.total_loss) / self.losses if self.losses > 0 else 0
        
        # Profit Factor
        if abs(self.total_loss) > 0:
            self.profit_factor = self.total_profit / abs(self.total_loss)
        else:
            self.profit_factor = float('inf') if self.total_profit > 0 else 0
    
    def get_score(self) -> float:
        """전략 점수 계산 (0~100)"""
        if self.trades < 5:  # 최소 거래 수 필요
            return 50.0  # 중립 점수
        
        score = 0.0
        
        # 승률 (40점)
        score += (self.win_rate / 100) * 40
        
        # Profit Factor (30점)
        pf_score = min(self.profit_factor / 2.0, 1.0) * 30
        score += pf_score
        
        # 평균 수익 대비 평균 손실 (30점)
        if self.avg_loss > 0:
            risk_reward = self.avg_profit / self.avg_loss
            rr_score = min(risk_reward / 2.0, 1.0) * 30
            score += rr_score
        
        return min(score, 100.0)


@dataclass
class MarketCondition:
    """시장 상황 분류"""
    volatility: str  # high, medium, low
    trend: str  # uptrend, downtrend, sideways
    volume: str  # high, medium, low
    sentiment: str  # positive, neutral, negative
    
    def to_key(self) -> str:
        """해시 키 생성"""
        return f"{self.volatility}_{self.trend}_{self.volume}_{self.sentiment}"


class StrategyOptimizer:
    """전략 최적화 엔진"""
    
    def __init__(self, data_dir: str = "trading_logs"):
        """
        초기화
        
        Args:
            data_dir: 데이터 저장 디렉토리
        """
        self.data_dir = data_dir
        self.performance_file = os.path.join(data_dir, "strategy_performance.json")
        
        # 전략별 성과 추적
        self.performances: Dict[str, StrategyPerformance] = {}
        
        # 시장 상황별 최적 전략 매핑
        self.market_strategy_map: Dict[str, Dict[str, float]] = defaultdict(dict)
        
        # 최근 거래 이력 (학습용)
        self.recent_trades: List[Dict] = []
        self.max_recent_trades = 100
        
        # 학습 파라미터
        self.learning_rate = 0.1  # 가중치 조정 속도
        self.min_trades_for_learning = 10  # 학습 최소 거래 수
        
        # 초기 전략 등록
        self._initialize_strategies()
        
        # 저장된 데이터 로드
        self.load_performance()
    
    def _initialize_strategies(self):
        """전략 초기화"""
        strategies = [
            'aggressive_scalping',
            'conservative_scalping',
            'mean_reversion',
            'grid_trading'
        ]
        
        for strategy in strategies:
            self.performances[strategy] = StrategyPerformance(strategy_name=strategy)
    
    def record_trade(self, 
                    strategy: str,
                    profit_loss: float,
                    market_condition: MarketCondition,
                    entry_price: float,
                    exit_price: float,
                    hold_time: float):
        """
        거래 기록 및 학습
        
        Args:
            strategy: 전략 이름
            profit_loss: 손익 금액
            market_condition: 시장 상황
            entry_price: 진입 가격
            exit_price: 청산 가격
            hold_time: 보유 시간 (초)
        """
        if strategy not in self.performances:
            return
        
        perf = self.performances[strategy]
        
        # 거래 기록
        perf.trades += 1
        
        if profit_loss > 0:
            perf.wins += 1
            perf.total_profit += profit_loss
        else:
            perf.losses += 1
            perf.total_loss += profit_loss
        
        # 시장 상황별 성과 기록
        condition_key = market_condition.to_key()
        if condition_key not in perf.market_conditions:
            perf.market_conditions[condition_key] = {
                'trades': 0,
                'wins': 0,
                'total_profit': 0.0
            }
        
        cond_perf = perf.market_conditions[condition_key]
        cond_perf['trades'] += 1
        if profit_loss > 0:
            cond_perf['wins'] += 1
        cond_perf['total_profit'] += profit_loss
        
        # 성과 지표 재계산
        perf.calculate_metrics()
        
        # 최근 거래 이력 추가
        self.recent_trades.append({
            'timestamp': datetime.now().isoformat(),
            'strategy': strategy,
            'profit_loss': profit_loss,
            'market_condition': condition_key,
            'entry_price': entry_price,
            'exit_price': exit_price,
            'hold_time': hold_time
        })
        
        # 최대 이력 수 유지
        if len(self.recent_trades) > self.max_recent_trades:
            self.recent_trades = self.recent_trades[-self.max_recent_trades:]
        
        # 시장 상황별 전략 매핑 업데이트
        self._update_market_strategy_map(market_condition, strategy, profit_loss)
        
        # 자동 저장
        self.save_performance()
    
    def _update_market_strategy_map(self, 
                                   condition: MarketCondition,
                                   strategy: str,
                                   profit_loss: float):
        """시장 상황별 전략 매핑 업데이트"""
        condition_key = condition.to_key()
        
        if condition_key not in self.market_strategy_map:
            # 초기화: 모든 전략 동일 가중치
            self.market_strategy_map[condition_key] = {
                s: 25.0 for s in self.performances.keys()
            }
        
        # 학습: 성공한 전략 가중치 증가, 실패한 전략 감소
        weights = self.market_strategy_map[condition_key]
        
        if profit_loss > 0:
            # 성공: 가중치 증가
            weights[strategy] += self.learning_rate * 5
        else:
            # 실패: 가중치 감소
            weights[strategy] = max(5.0, weights[strategy] - self.learning_rate * 3)
        
        # 가중치 정규화 (합 = 100)
        total = sum(weights.values())
        if total > 0:
            for s in weights:
                weights[s] = (weights[s] / total) * 100
    
    def get_optimized_weights(self, 
                            market_condition: MarketCondition,
                            base_weights: Dict[str, float]) -> Dict[str, float]:
        """
        최적화된 전략 가중치 계산
        
        Args:
            market_condition: 현재 시장 상황
            base_weights: 기본 가중치 (시간대별)
        
        Returns:
            최적화된 가중치
        """
        # 전체 성과 기반 점수
        strategy_scores = {}
        for strategy, perf in self.performances.items():
            strategy_scores[strategy] = perf.get_score()
        
        # 시장 상황별 가중치
        condition_key = market_condition.to_key()
        market_weights = self.market_strategy_map.get(condition_key, {})
        
        # 최적화된 가중치 계산
        optimized = {}
        for strategy in base_weights.keys():
            # 기본 가중치
            base = base_weights.get(strategy, 25.0)
            
            # 전체 성과 점수 (0~100)
            score = strategy_scores.get(strategy, 50.0)
            score_factor = score / 50.0  # 정규화 (1.0 = 평균)
            
            # 시장 상황별 가중치
            market_factor = market_weights.get(strategy, 25.0) / 25.0
            
            # 최종 가중치 = 기본 × 성과 × 시장적합도
            weight = base * score_factor * market_factor
            
            optimized[strategy] = weight
        
        # 정규화 (합 = 100)
        total = sum(optimized.values())
        if total > 0:
            optimized = {s: (w / total) * 100 for s, w in optimized.items()}
        
        return optimized
    
    def get_best_strategy(self, market_condition: MarketCondition) -> str:
        """
        현재 시장 상황에 최적인 전략 추천
        
        Args:
            market_condition: 시장 상황
        
        Returns:
            최적 전략 이름
        """
        condition_key = market_condition.to_key()
        
        # 시장 상황별 매핑이 있으면 사용
        if condition_key in self.market_strategy_map:
            weights = self.market_strategy_map[condition_key]
            best = max(weights.items(), key=lambda x: x[1])
            return best[0]
        
        # 없으면 전체 성과 기준
        best_strategy = None
        best_score = 0.0
        
        for strategy, perf in self.performances.items():
            score = perf.get_score()
            if score > best_score:
                best_score = score
                best_strategy = strategy
        
        return best_strategy or 'conservative_scalping'
    
    def get_strategy_rankings(self) -> List[Tuple[str, float, Dict]]:
        """
        전략 순위 반환
        
        Returns:
            [(전략명, 점수, 상세정보), ...]
        """
        rankings = []
        
        for strategy, perf in self.performances.items():
            score = perf.get_score()
            info = {
                'trades': perf.trades,
                'win_rate': perf.win_rate,
                'profit_factor': perf.profit_factor,
                'avg_profit': perf.avg_profit,
                'avg_loss': perf.avg_loss
            }
            rankings.append((strategy, score, info))
        
        # 점수 기준 정렬
        rankings.sort(key=lambda x: x[1], reverse=True)
        
        return rankings
    
    def should_disable_strategy(self, strategy: str) -> Tuple[bool, str]:
        """
        전략 비활성화 필요 여부 확인
        
        Args:
            strategy: 전략 이름
        
        Returns:
            (비활성화 여부, 사유)
        """
        if strategy not in self.performances:
            return False, ""
        
        perf = self.performances[strategy]
        
        # 최소 거래 수 미달
        if perf.trades < 20:
            return False, ""
        
        # 승률 30% 미만
        if perf.win_rate < 30:
            return True, f"승률 부족 ({perf.win_rate:.1f}%)"
        
        # Profit Factor 0.5 미만 (손실 2배)
        if perf.profit_factor < 0.5:
            return True, f"손실 과다 (PF: {perf.profit_factor:.2f})"
        
        # 최근 10거래 연속 손실
        recent = [t for t in self.recent_trades if t['strategy'] == strategy][-10:]
        if len(recent) == 10 and all(t['profit_loss'] < 0 for t in recent):
            return True, "최근 10거래 연속 손실"
        
        return False, ""
    
    def get_performance_report(self) -> str:
        """성과 리포트 생성"""
        report = []
        report.append("=" * 60)
        report.append("📊 전략 성과 리포트")
        report.append("=" * 60)
        report.append("")
        
        rankings = self.get_strategy_rankings()
        
        for i, (strategy, score, info) in enumerate(rankings, 1):
            report.append(f"{i}. {strategy.upper()}")
            report.append(f"   점수: {score:.1f}/100")
            report.append(f"   거래: {info['trades']}회")
            report.append(f"   승률: {info['win_rate']:.1f}%")
            report.append(f"   Profit Factor: {info['profit_factor']:.2f}")
            report.append(f"   평균 수익: {info['avg_profit']:,.0f}원")
            report.append(f"   평균 손실: {info['avg_loss']:,.0f}원")
            report.append("")
        
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def save_performance(self):
        """성과 데이터 저장"""
        try:
            data = {
                'performances': {
                    name: {
                        'strategy_name': perf.strategy_name,
                        'trades': perf.trades,
                        'wins': perf.wins,
                        'losses': perf.losses,
                        'total_profit': perf.total_profit,
                        'total_loss': perf.total_loss,
                        'avg_profit': perf.avg_profit,
                        'avg_loss': perf.avg_loss,
                        'win_rate': perf.win_rate,
                        'profit_factor': perf.profit_factor,
                        'market_conditions': perf.market_conditions
                    }
                    for name, perf in self.performances.items()
                },
                'market_strategy_map': dict(self.market_strategy_map),
                'recent_trades': self.recent_trades,
                'updated_at': datetime.now().isoformat()
            }
            
            with open(self.performance_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"⚠️  성과 데이터 저장 실패: {e}")
    
    def load_performance(self):
        """저장된 성과 데이터 로드"""
        try:
            if not os.path.exists(self.performance_file):
                return
            
            with open(self.performance_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 성과 데이터 복원
            for name, perf_data in data.get('performances', {}).items():
                perf = StrategyPerformance(strategy_name=name)
                perf.trades = perf_data.get('trades', 0)
                perf.wins = perf_data.get('wins', 0)
                perf.losses = perf_data.get('losses', 0)
                perf.total_profit = perf_data.get('total_profit', 0.0)
                perf.total_loss = perf_data.get('total_loss', 0.0)
                perf.avg_profit = perf_data.get('avg_profit', 0.0)
                perf.avg_loss = perf_data.get('avg_loss', 0.0)
                perf.win_rate = perf_data.get('win_rate', 0.0)
                perf.profit_factor = perf_data.get('profit_factor', 0.0)
                perf.market_conditions = perf_data.get('market_conditions', {})
                
                self.performances[name] = perf
            
            # 시장 매핑 복원
            self.market_strategy_map = defaultdict(dict, data.get('market_strategy_map', {}))
            
            # 최근 거래 복원
            self.recent_trades = data.get('recent_trades', [])
            
            print(f"✅ 전략 성과 데이터 로드 완료")
            
        except Exception as e:
            print(f"⚠️  성과 데이터 로드 실패: {e}")
