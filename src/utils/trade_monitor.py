"""
실시간 체결 데이터 모니터링 및 학습 시스템

기능:
- 실시간 체결 내역 수집
- 대량 거래 감지
- 매수/매도 강도 분석
- 체결 패턴 학습
"""

import time
import json
from typing import Dict, List, Optional
from datetime import datetime
from collections import deque
import os


class TradeMonitor:
    """실시간 체결 데이터 모니터링 및 학습 시스템"""
    
    def __init__(self, upbit_api, logger):
        """
        초기화
        
        Args:
            upbit_api: UpbitAPI 인스턴스
            logger: TradingLogger 인스턴스
        """
        self.api = upbit_api
        self.logger = logger
        
        # 설정
        self.max_history = 500  # 최대 저장 개수
        self.large_trade_threshold = 1000000  # 대량 거래 기준 (100만원)
        
        # 데이터 저장
        self.trade_history = {}  # {ticker: deque([...], maxlen=500)}
        self.strength_patterns = {}  # {ticker: {pattern: count}}
        self.large_trades = {}  # {ticker: [대량 거래 목록]}
        
        # 학습 데이터 경로
        self.data_dir = "learning_data/trades"
        os.makedirs(self.data_dir, exist_ok=True)
        
        # 기존 학습 데이터 로드
        self._load_learning_data()
    
    def monitor_trades(self, ticker: str, count: int = 100) -> Optional[Dict]:
        """
        특정 코인의 체결 내역 모니터링
        
        Args:
            ticker: 코인 티커
            count: 조회할 체결 개수
        
        Returns:
            체결 분석 결과
        """
        try:
            # 체결 내역 조회
            trades = self.api.get_recent_trades(ticker, count)
            
            if not trades:
                return None
            
            # 체결 분석
            analysis = self._analyze_trades(ticker, trades)
            
            if analysis:
                # 이력 저장
                self._save_to_history(ticker, analysis)
                
                # 패턴 학습
                self._learn_pattern(ticker, analysis)
                
                # 대량 거래 감지
                self._detect_large_trades(ticker, trades)
            
            return analysis
            
        except Exception as e:
            self.logger.log_error("TRADE_MONITOR", f"{ticker} 체결 모니터링 실패", e)
            return None
    
    def _analyze_trades(self, ticker: str, trades: List[Dict]) -> Dict:
        """
        체결 데이터 분석
        
        Args:
            ticker: 코인 티커
            trades: 체결 내역 리스트
        
        Returns:
            분석 결과
        """
        try:
            # 매수/매도 분리
            buy_trades = [t for t in trades if t.get('ask_bid') == 'BID']
            sell_trades = [t for t in trades if t.get('ask_bid') == 'ASK']
            
            # 총 거래량 및 금액
            total_buy_volume = sum(float(t.get('trade_volume', 0)) for t in buy_trades)
            total_sell_volume = sum(float(t.get('trade_volume', 0)) for t in sell_trades)
            
            total_buy_amount = sum(
                float(t.get('trade_price', 0)) * float(t.get('trade_volume', 0))
                for t in buy_trades
            )
            total_sell_amount = sum(
                float(t.get('trade_price', 0)) * float(t.get('trade_volume', 0))
                for t in sell_trades
            )
            
            # 매수/매도 강도 계산
            total_volume = total_buy_volume + total_sell_volume
            total_amount = total_buy_amount + total_sell_amount
            
            buy_strength = (total_buy_amount / total_amount * 100) if total_amount > 0 else 50
            sell_strength = 100 - buy_strength
            
            # 평균 체결가
            avg_price = (
                sum(float(t.get('trade_price', 0)) for t in trades) / len(trades)
                if trades else 0
            )
            
            # 가격 변동
            if len(trades) >= 2:
                first_price = float(trades[0].get('trade_price', 0))
                last_price = float(trades[-1].get('trade_price', 0))
                price_change = ((last_price - first_price) / first_price * 100) if first_price > 0 else 0
            else:
                price_change = 0
            
            # 체결 강도 판단
            if buy_strength >= 65:
                strength_signal = "STRONG_BUY"
            elif buy_strength >= 55:
                strength_signal = "BUY"
            elif buy_strength <= 35:
                strength_signal = "STRONG_SELL"
            elif buy_strength <= 45:
                strength_signal = "SELL"
            else:
                strength_signal = "NEUTRAL"
            
            return {
                'ticker': ticker,
                'timestamp': datetime.now().isoformat(),
                'total_trades': len(trades),
                'buy_trades': len(buy_trades),
                'sell_trades': len(sell_trades),
                'buy_strength': round(buy_strength, 2),
                'sell_strength': round(sell_strength, 2),
                'total_buy_amount': total_buy_amount,
                'total_sell_amount': total_sell_amount,
                'avg_price': avg_price,
                'price_change': round(price_change, 2),
                'strength_signal': strength_signal
            }
            
        except Exception as e:
            self.logger.log_error("TRADE_ANALYZE", f"{ticker} 체결 분석 실패", e)
            return {}
    
    def _detect_large_trades(self, ticker: str, trades: List[Dict]):
        """대량 거래 감지"""
        try:
            if ticker not in self.large_trades:
                self.large_trades[ticker] = deque(maxlen=100)
            
            for trade in trades:
                trade_price = float(trade.get('trade_price', 0))
                trade_volume = float(trade.get('trade_volume', 0))
                trade_amount = trade_price * trade_volume
                
                # 대량 거래 감지
                if trade_amount >= self.large_trade_threshold:
                    large_trade_info = {
                        'timestamp': trade.get('timestamp', datetime.now().isoformat()),
                        'price': trade_price,
                        'volume': trade_volume,
                        'amount': trade_amount,
                        'side': trade.get('ask_bid', 'UNKNOWN')
                    }
                    
                    self.large_trades[ticker].append(large_trade_info)
                    
                    self.logger.log_info(
                        f"🐋 대량 거래 감지: {ticker} "
                        f"{large_trade_info['side']} "
                        f"{trade_amount:,.0f}원"
                    )
        
        except Exception as e:
            self.logger.log_error("LARGE_TRADE_DETECT", f"{ticker} 대량 거래 감지 실패", e)
    
    def _save_to_history(self, ticker: str, analysis: Dict):
        """이력에 저장"""
        if ticker not in self.trade_history:
            self.trade_history[ticker] = deque(maxlen=self.max_history)
        
        self.trade_history[ticker].append({
            'timestamp': analysis['timestamp'],
            'buy_strength': analysis['buy_strength'],
            'sell_strength': analysis['sell_strength'],
            'strength_signal': analysis['strength_signal'],
            'price_change': analysis['price_change']
        })
    
    def _learn_pattern(self, ticker: str, analysis: Dict):
        """
        체결 패턴 학습
        
        패턴 종류:
        - strong_buy_pressure: 강한 매수 압력
        - strong_sell_pressure: 강한 매도 압력
        - balanced: 균형
        - accumulation: 누적 (가격 안정 + 매수 우세)
        - distribution: 분산 (가격 안정 + 매도 우세)
        """
        if ticker not in self.strength_patterns:
            self.strength_patterns[ticker] = {
                'strong_buy_pressure': 0,
                'strong_sell_pressure': 0,
                'balanced': 0,
                'accumulation': 0,
                'distribution': 0
            }
        
        buy_strength = analysis['buy_strength']
        price_change = analysis['price_change']
        
        # 패턴 분류
        if buy_strength >= 65:
            self.strength_patterns[ticker]['strong_buy_pressure'] += 1
        elif buy_strength <= 35:
            self.strength_patterns[ticker]['strong_sell_pressure'] += 1
        elif 45 <= buy_strength <= 55:
            self.strength_patterns[ticker]['balanced'] += 1
        
        # 누적/분산 패턴
        if abs(price_change) < 0.5 and buy_strength >= 55:
            self.strength_patterns[ticker]['accumulation'] += 1
        elif abs(price_change) < 0.5 and buy_strength <= 45:
            self.strength_patterns[ticker]['distribution'] += 1
    
    def get_buy_sell_strength(self, ticker: str) -> Dict:
        """
        매수/매도 강도 조회 (최근 이력 기반)
        
        Args:
            ticker: 코인 티커
        
        Returns:
            강도 정보
        """
        if ticker not in self.trade_history or not self.trade_history[ticker]:
            return {
                'buy_strength': 50,
                'sell_strength': 50,
                'signal': 'NEUTRAL'
            }
        
        # 최근 10개 데이터 평균
        recent = list(self.trade_history[ticker])[-10:]
        
        avg_buy_strength = sum(t['buy_strength'] for t in recent) / len(recent)
        avg_sell_strength = 100 - avg_buy_strength
        
        # 신호 결정
        if avg_buy_strength >= 60:
            signal = "BUY"
        elif avg_buy_strength <= 40:
            signal = "SELL"
        else:
            signal = "NEUTRAL"
        
        return {
            'buy_strength': round(avg_buy_strength, 2),
            'sell_strength': round(avg_sell_strength, 2),
            'signal': signal
        }
    
    def get_strength_pattern(self, ticker: str) -> Dict:
        """
        학습된 강도 패턴 조회
        
        Args:
            ticker: 코인 티커
        
        Returns:
            패턴 통계
        """
        if ticker not in self.strength_patterns:
            return {}
        
        patterns = self.strength_patterns[ticker]
        total = sum(patterns.values())
        
        if total == 0:
            return {}
        
        # 비율로 변환
        return {
            pattern: (count / total) * 100
            for pattern, count in patterns.items()
        }
    
    def has_large_trades(self, ticker: str, time_window: int = 300) -> bool:
        """
        최근 대량 거래 존재 여부 확인
        
        Args:
            ticker: 코인 티커
            time_window: 시간 윈도우 (초)
        
        Returns:
            대량 거래 존재 여부
        """
        if ticker not in self.large_trades:
            return False
        
        now = datetime.now()
        
        for trade in self.large_trades[ticker]:
            timestamp = trade.get('timestamp')
            if isinstance(timestamp, str):
                trade_time = datetime.fromisoformat(timestamp)
            elif isinstance(timestamp, datetime):
                trade_time = timestamp
            else:
                continue
            
            elapsed = (now - trade_time).total_seconds()
            
            if elapsed <= time_window:
                return True
        
        return False
    
    def should_enter_trade(self, ticker: str) -> Dict:
        """
        진입 여부 결정 (AI 학습 기반)
        
        Args:
            ticker: 코인 티커
        
        Returns:
            진입 신호 및 이유
        """
        # 매수/매도 강도 조회
        strength = self.get_buy_sell_strength(ticker)
        
        # 학습된 패턴 조회
        pattern = self.get_strength_pattern(ticker)
        
        # 대량 거래 확인
        has_large = self.has_large_trades(ticker, time_window=300)
        
        # 결정 로직
        should_enter = False
        confidence = 0
        reason = []
        
        # 1. 강한 매수 압력
        if strength['buy_strength'] >= 60:
            should_enter = True
            confidence += 30
            reason.append(f"강한 매수 압력 ({strength['buy_strength']:.1f}%)")
        
        # 2. 누적 패턴
        if pattern.get('accumulation', 0) > 50:
            should_enter = True
            confidence += 20
            reason.append("누적 패턴 감지")
        
        # 3. 대량 매수 거래
        if has_large:
            confidence += 15
            reason.append("대량 거래 감지")
        
        # 4. 학습된 매수 패턴
        if pattern.get('strong_buy_pressure', 0) > 40:
            confidence += 10
            reason.append("학습된 매수 패턴")
        
        return {
            'should_enter': should_enter,
            'confidence': min(confidence, 100),
            'reason': ', '.join(reason) if reason else '진입 신호 없음',
            'buy_strength': strength['buy_strength'],
            'signal': strength['signal']
        }
    
    def _load_learning_data(self):
        """저장된 학습 데이터 로드"""
        try:
            patterns_file = os.path.join(self.data_dir, "strength_patterns.json")
            
            if os.path.exists(patterns_file):
                with open(patterns_file, 'r', encoding='utf-8') as f:
                    self.strength_patterns = json.load(f)
                    self.logger.log_info(f"✅ 체결 패턴 학습 데이터 로드 완료: {len(self.strength_patterns)}개")
        
        except Exception as e:
            self.logger.log_error("TRADE_LOAD", "학습 데이터 로드 실패", e)
    
    def save_learning_data(self):
        """학습 데이터 저장"""
        try:
            patterns_file = os.path.join(self.data_dir, "strength_patterns.json")
            
            with open(patterns_file, 'w', encoding='utf-8') as f:
                json.dump(self.strength_patterns, f, ensure_ascii=False, indent=2)
            
            self.logger.log_info(f"✅ 체결 학습 데이터 저장 완료: {len(self.strength_patterns)}개")
        
        except Exception as e:
            self.logger.log_error("TRADE_SAVE", "학습 데이터 저장 실패", e)
    
    def get_statistics(self) -> Dict:
        """통계 정보 조회"""
        return {
            'monitored_tickers': len(self.trade_history),
            'total_patterns': sum(sum(p.values()) for p in self.strength_patterns.values()),
            'total_large_trades': sum(len(t) for t in self.large_trades.values()),
            'history_size': sum(len(h) for h in self.trade_history.values())
        }
