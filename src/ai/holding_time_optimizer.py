"""
보유 시간 AI 최적화 시스템
과거 거래 데이터를 학습하여 최적의 보유 시간 예측
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import json
import os
import numpy as np


class HoldingTimeOptimizer:
    """보유 시간 최적화 AI"""
    
    def __init__(self, data_dir: str = "trading_logs/learning"):
        """
        Args:
            data_dir: 학습 데이터 저장 디렉토리
        """
        self.data_dir = data_dir
        self.holding_times_file = os.path.join(data_dir, "holding_times.json")
        
        # 학습 데이터
        self.holding_data = self._load_holding_data()
        
        # 시나리오별 최적 보유 시간 (초)
        self.optimal_times = {}
        
        # 통계
        self.stats = {
            'total_samples': 0,
            'avg_holding_time': 0,
            'win_rate_by_time': {},
            'profit_by_time': {}
        }
        
        self._initialize()
    
    def _initialize(self):
        """초기화 및 기존 데이터 로드"""
        os.makedirs(self.data_dir, exist_ok=True)
        if self.holding_data:
            self._calculate_stats()
    
    def _load_holding_data(self) -> List[Dict]:
        """보유 시간 학습 데이터 로드"""
        if os.path.exists(self.holding_times_file):
            try:
                with open(self.holding_times_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_holding_data(self):
        """학습 데이터 저장"""
        try:
            with open(self.holding_times_file, 'w', encoding='utf-8') as f:
                json.dump(self.holding_data, f, ensure_ascii=False, indent=2, default=str)
        except Exception as e:
            print(f"⚠️ 보유 시간 데이터 저장 실패: {e}")
    
    def record_trade(
        self,
        ticker: str,
        scenario_id: int,
        entry_price: float,
        exit_price: float,
        holding_time: int,
        profit_ratio: float,
        strategy: str
    ):
        """
        거래 기록 저장
        
        Args:
            ticker: 티커 심볼
            scenario_id: 진입 시 시나리오 ID
            entry_price: 진입 가격
            exit_price: 청산 가격
            holding_time: 보유 시간 (초)
            profit_ratio: 수익률 (%)
            strategy: 전략 이름
        """
        record = {
            'ticker': ticker,
            'scenario_id': scenario_id,
            'entry_price': entry_price,
            'exit_price': exit_price,
            'holding_time': holding_time,
            'profit_ratio': profit_ratio,
            'strategy': strategy,
            'success': profit_ratio > 0,
            'timestamp': datetime.now().isoformat()
        }
        
        self.holding_data.append(record)
        
        # 최대 5,000건 유지
        if len(self.holding_data) > 5000:
            self.holding_data.pop(0)
        
        # 저장
        self._save_holding_data()
        
        # 통계 업데이트
        self._calculate_stats()
    
    def predict_optimal_holding_time(
        self,
        scenario_id: int,
        strategy: str,
        current_profit: float = 0.0
    ) -> Dict:
        """
        최적 보유 시간 예측
        
        Args:
            scenario_id: 현재 시나리오 ID
            strategy: 사용 중인 전략
            current_profit: 현재 수익률 (%)
        
        Returns:
            {
                'optimal_time': int,  # 예측된 최적 보유 시간 (초)
                'min_time': int,      # 최소 보유 시간
                'max_time': int,      # 최대 보유 시간
                'confidence': float,  # 예측 신뢰도 (0-100)
                'expected_profit': float,  # 예상 수익률
                'sample_count': int   # 학습 샘플 수
            }
        """
        # 유사한 거래 찾기
        similar_trades = self._find_similar_trades(scenario_id, strategy)
        
        if len(similar_trades) < 3:
            # 데이터 부족 → 기본값
            return self._default_prediction(strategy)
        
        # 성공한 거래만 필터링
        successful_trades = [t for t in similar_trades if t['success']]
        
        if not successful_trades:
            return self._default_prediction(strategy)
        
        # 보유 시간 분석
        holding_times = [t['holding_time'] for t in successful_trades]
        profits = [t['profit_ratio'] for t in successful_trades]
        
        # 통계 계산
        optimal_time = int(np.median(holding_times))
        min_time = int(np.percentile(holding_times, 25))
        max_time = int(np.percentile(holding_times, 75))
        expected_profit = np.mean(profits)
        
        # 신뢰도 계산
        confidence = min(100, (len(successful_trades) / 10) * 100)
        
        return {
            'optimal_time': optimal_time,
            'min_time': min_time,
            'max_time': max_time,
            'confidence': round(confidence, 2),
            'expected_profit': round(expected_profit, 3),
            'sample_count': len(similar_trades),
            'timestamp': datetime.now()
        }
    
    def should_exit_now(
        self,
        scenario_id: int,
        strategy: str,
        current_holding_time: int,
        current_profit: float
    ) -> Tuple[bool, str]:
        """
        지금 청산해야 하는지 판단
        
        Args:
            scenario_id: 현재 시나리오
            strategy: 전략
            current_holding_time: 현재 보유 시간 (초)
            current_profit: 현재 수익률 (%)
        
        Returns:
            (청산 여부, 이유)
        """
        prediction = self.predict_optimal_holding_time(scenario_id, strategy, current_profit)
        
        optimal_time = prediction['optimal_time']
        max_time = prediction['max_time']
        expected_profit = prediction['expected_profit']
        
        # 1. 최적 시간 도달 + 목표 수익 달성
        if current_holding_time >= optimal_time and current_profit >= expected_profit * 0.8:
            return True, f"최적 시간 도달 ({current_holding_time}초) + 목표 수익 달성 ({current_profit:.2f}%)"
        
        # 2. 최대 시간 초과
        if current_holding_time >= max_time:
            return True, f"최대 보유 시간 초과 ({current_holding_time}초 > {max_time}초)"
        
        # 3. 수익 급증 (예상의 150% 이상)
        if current_profit >= expected_profit * 1.5:
            return True, f"목표 수익 대폭 초과 ({current_profit:.2f}% > {expected_profit * 1.5:.2f}%)"
        
        # 4. 보유 시간 길어짐 + 수익 감소
        if current_holding_time > optimal_time and current_profit < expected_profit * 0.5:
            return True, f"장기 보유 중 수익 부진 (보유: {current_holding_time}초, 수익: {current_profit:.2f}%)"
        
        return False, f"홀딩 유지 (목표: {optimal_time}초, 현재: {current_holding_time}초)"
    
    def _find_similar_trades(self, scenario_id: int, strategy: str) -> List[Dict]:
        """
        유사한 거래 찾기
        
        같은 시나리오 + 같은 전략
        """
        similar = [
            trade for trade in self.holding_data
            if trade['scenario_id'] == scenario_id and trade['strategy'] == strategy
        ]
        
        # 최근 100건만
        return similar[-100:] if len(similar) > 100 else similar
    
    def _default_prediction(self, strategy: str) -> Dict:
        """기본 예측값 (데이터 부족 시)"""
        # 전략별 기본 보유 시간
        default_times = {
            'UltraScalping': 180,       # 3분
            'AggressiveScalping': 300,  # 5분
            'ConservativeScalping': 600,  # 10분
            'MeanReversion': 900,       # 15분
            'GridTrading': 1800         # 30분
        }
        
        optimal = default_times.get(strategy, 300)
        
        return {
            'optimal_time': optimal,
            'min_time': optimal // 2,
            'max_time': optimal * 2,
            'confidence': 30.0,
            'expected_profit': 1.0,
            'sample_count': 0,
            'timestamp': datetime.now()
        }
    
    def _calculate_stats(self):
        """통계 계산"""
        if not self.holding_data:
            return
        
        total = len(self.holding_data)
        successful = [t for t in self.holding_data if t['success']]
        
        self.stats['total_samples'] = total
        self.stats['win_rate'] = len(successful) / total * 100 if total > 0 else 0
        
        # 평균 보유 시간
        all_times = [t['holding_time'] for t in self.holding_data]
        self.stats['avg_holding_time'] = np.mean(all_times) if all_times else 0
        
        # 시간대별 승률
        time_buckets = {
            '0-3분': (0, 180),
            '3-5분': (180, 300),
            '5-10분': (300, 600),
            '10-30분': (600, 1800),
            '30분+': (1800, 999999)
        }
        
        for bucket_name, (min_t, max_t) in time_buckets.items():
            trades_in_bucket = [
                t for t in self.holding_data 
                if min_t <= t['holding_time'] < max_t
            ]
            
            if trades_in_bucket:
                wins = sum(1 for t in trades_in_bucket if t['success'])
                self.stats['win_rate_by_time'][bucket_name] = wins / len(trades_in_bucket) * 100
                
                avg_profit = np.mean([t['profit_ratio'] for t in trades_in_bucket])
                self.stats['profit_by_time'][bucket_name] = avg_profit
    
    def get_stats_report(self) -> Dict:
        """통계 리포트 반환"""
        self._calculate_stats()
        return self.stats.copy()
    
    def get_scenario_performance(self, scenario_id: int) -> Dict:
        """
        특정 시나리오의 성과 분석
        
        Returns:
            {
                'scenario_id': int,
                'total_trades': int,
                'win_rate': float,
                'avg_profit': float,
                'avg_holding_time': int,
                'best_strategy': str
            }
        """
        scenario_trades = [t for t in self.holding_data if t['scenario_id'] == scenario_id]
        
        if not scenario_trades:
            return {
                'scenario_id': scenario_id,
                'total_trades': 0,
                'win_rate': 0.0,
                'avg_profit': 0.0,
                'avg_holding_time': 0,
                'best_strategy': 'N/A'
            }
        
        wins = sum(1 for t in scenario_trades if t['success'])
        win_rate = wins / len(scenario_trades) * 100
        
        avg_profit = np.mean([t['profit_ratio'] for t in scenario_trades])
        avg_time = np.mean([t['holding_time'] for t in scenario_trades])
        
        # 최고 성과 전략
        strategy_profits = {}
        for trade in scenario_trades:
            strat = trade['strategy']
            if strat not in strategy_profits:
                strategy_profits[strat] = []
            strategy_profits[strat].append(trade['profit_ratio'])
        
        best_strategy = max(
            strategy_profits.keys(), 
            key=lambda s: np.mean(strategy_profits[s])
        ) if strategy_profits else 'N/A'
        
        return {
            'scenario_id': scenario_id,
            'total_trades': len(scenario_trades),
            'win_rate': round(win_rate, 2),
            'avg_profit': round(avg_profit, 3),
            'avg_holding_time': int(avg_time),
            'best_strategy': best_strategy
        }
