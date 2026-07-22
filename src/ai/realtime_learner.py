"""
실시간 학습 시스템 (Realtime Learning System)
============================================

매 거래마다 학습하여 전략 파라미터를 실시간 최적화
"""

import json
import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from pathlib import Path
import logging
from collections import deque

logger = logging.getLogger(__name__)


class RealtimeLearner:
    """실시간 학습 및 파라미터 최적화"""
    
    def __init__(self, learning_data_dir: str = "src/learning_data"):
        self.learning_data_dir = Path(learning_data_dir)
        self.learning_data_dir.mkdir(parents=True, exist_ok=True)
        
        # 거래 기록 (최근 100개)
        self.trade_history = deque(maxlen=100)
        
        # 성과 메트릭
        self.win_rate = 0.5  # 초기 승률 50%
        self.avg_profit = 0.0
        self.avg_loss = 0.0
        self.profit_factor = 1.0
        
        # 학습 파라미터
        self.learning_rate = 0.05  # 학습 속도 (5%)
        self.min_trades_for_learning = 10  # 최소 10건 거래 후 학습 시작
        
        # 최적화할 파라미터들
        self.params = {
            'volume_spike_threshold': 2.5,
            'price_momentum_min': 0.15,
            'target_profit': 0.5,
            'stop_loss': -0.5,
            'time_based_exit': 180,
        }
        
        # 파라미터 범위
        self.param_bounds = {
            'volume_spike_threshold': (1.5, 4.0),
            'price_momentum_min': (0.1, 0.5),
            'target_profit': (0.3, 1.0),
            'stop_loss': (-1.0, -0.3),
            'time_based_exit': (120, 300),
        }
        
        # 저장된 학습 데이터 로드
        self.load_learning_data()
    
    def record_trade(self, trade_data: Dict[str, Any]):
        """
        거래 기록
        
        trade_data:
            ticker: str
            entry_price: float
            exit_price: float
            entry_time: datetime
            exit_time: datetime
            profit_pct: float
            exit_reason: str
            market_conditions: dict
        """
        try:
            # 거래 데이터 저장
            trade_record = {
                'timestamp': datetime.now().isoformat(),
                **trade_data,
                'current_params': self.params.copy()
            }
            
            self.trade_history.append(trade_record)
            
            # 메트릭 업데이트
            self._update_metrics()
            
            # 학습 실행 (10건 이상일 때)
            if len(self.trade_history) >= self.min_trades_for_learning:
                self._perform_learning()
            
            # 파일에 저장
            self._save_trade_to_file(trade_record)
            
            logger.info(f"[REALTIME-LEARNER] 거래 기록됨: {trade_data['ticker']} {trade_data['profit_pct']:.2f}%")
            
        except Exception as e:
            logger.error(f"[REALTIME-LEARNER] 거래 기록 실패: {e}")
    
    def _update_metrics(self):
        """성과 메트릭 업데이트"""
        if not self.trade_history:
            return
        
        profits = [t['profit_pct'] for t in self.trade_history if t['profit_pct'] > 0]
        losses = [t['profit_pct'] for t in self.trade_history if t['profit_pct'] < 0]
        
        # 승률
        total_trades = len(self.trade_history)
        winning_trades = len(profits)
        self.win_rate = winning_trades / total_trades if total_trades > 0 else 0.5
        
        # 평균 수익/손실
        self.avg_profit = sum(profits) / len(profits) if profits else 0
        self.avg_loss = sum(losses) / len(losses) if losses else 0
        
        # Profit Factor
        total_profit = sum(profits)
        total_loss = abs(sum(losses))
        self.profit_factor = total_profit / total_loss if total_loss > 0 else 1.0
    
    def _perform_learning(self):
        """실시간 학습 및 파라미터 최적화"""
        try:
            logger.info(f"[REALTIME-LEARNER] 학습 시작... (거래: {len(self.trade_history)}건)")
            
            # 최근 20건 분석
            recent_trades = list(self.trade_history)[-20:]
            
            # 1. 승률 기반 조정
            if self.win_rate < 0.4:  # 승률 40% 미만
                logger.warning(f"[REALTIME-LEARNER] 낮은 승률 감지: {self.win_rate:.1%}")
                
                # 진입 조건 강화
                self._adjust_param('volume_spike_threshold', increase=True)
                self._adjust_param('price_momentum_min', increase=True)
                
                # 손절 완화
                self._adjust_param('stop_loss', increase=True)  # -0.5 → -0.4
            
            elif self.win_rate > 0.6:  # 승률 60% 이상
                logger.info(f"[REALTIME-LEARNER] 높은 승률: {self.win_rate:.1%}")
                
                # 진입 조건 완화 (더 많은 기회)
                self._adjust_param('volume_spike_threshold', increase=False)
                self._adjust_param('price_momentum_min', increase=False)
            
            # 2. Profit Factor 기반 조정
            if self.profit_factor < 1.0:  # 손실 > 수익
                logger.warning(f"[REALTIME-LEARNER] 낮은 PF: {self.profit_factor:.2f}")
                
                # 익절 목표 상향
                self._adjust_param('target_profit', increase=True)
                
                # 보유 시간 단축
                self._adjust_param('time_based_exit', increase=False)
            
            # 3. 시간 초과 청산 비율 분석
            timeout_exits = [t for t in recent_trades if t.get('exit_reason') == 'TIME_EXCEEDED']
            timeout_rate = len(timeout_exits) / len(recent_trades) if recent_trades else 0
            
            if timeout_rate > 0.5:  # 50% 이상이 시간 초과
                logger.warning(f"[REALTIME-LEARNER] 높은 시간초과율: {timeout_rate:.1%}")
                
                # 시간 제한 단축
                self._adjust_param('time_based_exit', increase=False)
            
            # 4. 손절 비율 분석
            stop_loss_exits = [t for t in recent_trades if t.get('exit_reason') == 'STOP_LOSS']
            stop_loss_rate = len(stop_loss_exits) / len(recent_trades) if recent_trades else 0
            
            if stop_loss_rate > 0.3:  # 30% 이상이 손절
                logger.warning(f"[REALTIME-LEARNER] 높은 손절율: {stop_loss_rate:.1%}")
                
                # 손절 라인 완화
                self._adjust_param('stop_loss', increase=True)
            
            # 학습 결과 저장
            self.save_learning_data()
            
            logger.info(f"[REALTIME-LEARNER] 학습 완료! 승률:{self.win_rate:.1%}, PF:{self.profit_factor:.2f}")
            
        except Exception as e:
            logger.error(f"[REALTIME-LEARNER] 학습 실패: {e}")
    
    def _adjust_param(self, param_name: str, increase: bool):
        """파라미터 조정"""
        if param_name not in self.params:
            return
        
        current_value = self.params[param_name]
        min_val, max_val = self.param_bounds[param_name]
        
        # 조정 비율 (학습률)
        adjustment = self.learning_rate * (1 if increase else -1)
        
        # 새 값 계산
        if param_name == 'stop_loss':
            # 손절은 음수이므로 반대로 (increase=True면 -0.5 → -0.4)
            new_value = current_value * (1 - adjustment)
        else:
            new_value = current_value * (1 + adjustment)
        
        # 범위 제한
        new_value = max(min_val, min(max_val, new_value))
        
        if new_value != current_value:
            logger.info(f"[REALTIME-LEARNER] {param_name}: {current_value:.3f} → {new_value:.3f}")
            self.params[param_name] = new_value
    
    def get_optimized_params(self) -> Dict[str, Any]:
        """최적화된 파라미터 반환"""
        return self.params.copy()
    
    def get_performance_report(self) -> Dict[str, Any]:
        """성과 리포트"""
        recent_trades = list(self.trade_history)[-20:]
        
        return {
            'total_trades': len(self.trade_history),
            'win_rate': f"{self.win_rate:.1%}",
            'avg_profit': f"{self.avg_profit:.2f}%",
            'avg_loss': f"{self.avg_loss:.2f}%",
            'profit_factor': f"{self.profit_factor:.2f}",
            'recent_trades': len(recent_trades),
            'current_params': self.params,
        }
    
    def save_learning_data(self):
        """학습 데이터 저장"""
        try:
            data = {
                'timestamp': datetime.now().isoformat(),
                'params': self.params,
                'metrics': {
                    'win_rate': self.win_rate,
                    'avg_profit': self.avg_profit,
                    'avg_loss': self.avg_loss,
                    'profit_factor': self.profit_factor,
                },
                'trade_count': len(self.trade_history),
            }
            
            filepath = self.learning_data_dir / 'realtime_learning.json'
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"[REALTIME-LEARNER] 학습 데이터 저장 실패: {e}")
    
    def load_learning_data(self):
        """저장된 학습 데이터 로드"""
        try:
            filepath = self.learning_data_dir / 'realtime_learning.json'
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.params = data.get('params', self.params)
                metrics = data.get('metrics', {})
                self.win_rate = metrics.get('win_rate', 0.5)
                self.avg_profit = metrics.get('avg_profit', 0.0)
                self.avg_loss = metrics.get('avg_loss', 0.0)
                self.profit_factor = metrics.get('profit_factor', 1.0)
                
                logger.info(f"[REALTIME-LEARNER] 학습 데이터 로드 완료 (거래: {data.get('trade_count', 0)}건)")
        
        except Exception as e:
            logger.error(f"[REALTIME-LEARNER] 학습 데이터 로드 실패: {e}")
    
    def _save_trade_to_file(self, trade_record: Dict[str, Any]):
        """개별 거래를 파일에 저장"""
        try:
            today = datetime.now().strftime('%Y%m%d')
            filepath = self.learning_data_dir / f'trades_{today}.jsonl'
            
            # datetime 객체를 문자열로 변환
            record_copy = trade_record.copy()
            if 'entry_time' in record_copy and hasattr(record_copy['entry_time'], 'isoformat'):
                record_copy['entry_time'] = record_copy['entry_time'].isoformat()
            if 'exit_time' in record_copy and hasattr(record_copy['exit_time'], 'isoformat'):
                record_copy['exit_time'] = record_copy['exit_time'].isoformat()
            
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(json.dumps(record_copy, ensure_ascii=False) + '\n')
        
        except Exception as e:
            logger.error(f"[REALTIME-LEARNER] 거래 파일 저장 실패: {e}")
