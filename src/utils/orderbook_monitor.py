"""
실시간 호가창 모니터링 및 학습 시스템

기능:
- 실시간 호가창 데이터 수집
- 매수/매도 벽 감지
- 유동성 패턴 학습
- 슬리피지 예측 모델 학습
"""

import time
import json
from typing import Dict, List, Optional
from datetime import datetime
from collections import deque
import os


class OrderbookMonitor:
    """실시간 호가창 모니터링 및 학습 시스템"""
    
    def __init__(self, upbit_api, logger, order_book_analyzer):
        """
        초기화
        
        Args:
            upbit_api: UpbitAPI 인스턴스
            logger: TradingLogger 인스턴스
            order_book_analyzer: OrderBookAnalyzer 인스턴스
        """
        self.api = upbit_api
        self.logger = logger
        self.analyzer = order_book_analyzer
        
        # 설정
        self.max_history = 1000  # 최대 저장 개수
        self.batch_size = 5  # 배치 조회 개수
        self.cache_duration = 3  # 캐시 유지 시간 (초)
        
        # 데이터 저장
        self.orderbook_history = {}  # {ticker: deque([...], maxlen=1000)}
        self.liquidity_patterns = {}  # {ticker: {pattern: count}}
        self.slippage_predictions = {}  # {ticker: {time: slippage}}
        
        # 캐시
        self.cache = {}  # {ticker: {data, timestamp}}
        
        # 학습 데이터 경로
        self.data_dir = "learning_data/orderbook"
        os.makedirs(self.data_dir, exist_ok=True)
        
        # 기존 학습 데이터 로드
        self._load_learning_data()
    
    def monitor_orderbook(self, tickers: List[str]) -> Dict[str, Dict]:
        """
        여러 코인의 호가창을 실시간으로 모니터링
        
        Args:
            tickers: 모니터링할 티커 리스트
        
        Returns:
            {ticker: orderbook_analysis} 딕셔너리
        """
        results = {}
        
        # 배치 단위로 분할 조회 (API 제한 고려)
        for i in range(0, len(tickers), self.batch_size):
            batch = tickers[i:i+self.batch_size]
            
            try:
                # 배치 API로 호가창 조회
                orderbooks = self.api.get_orderbooks(batch)
                
                for ticker in batch:
                    if ticker not in orderbooks:
                        continue
                    
                    # 호가창 분석
                    analysis = self._analyze_orderbook(ticker, orderbooks[ticker])
                    
                    if analysis:
                        results[ticker] = analysis
                        
                        # 이력 저장
                        self._save_to_history(ticker, analysis)
                        
                        # 패턴 학습
                        self._learn_pattern(ticker, analysis)
                
                # API 제한 고려 (0.2초 대기)
                time.sleep(0.2)
                
            except Exception as e:
                self.logger.log_error("ORDERBOOK_MONITOR", f"배치 조회 실패: {batch}", e)
        
        return results
    
    def get_cached_orderbook(self, ticker: str) -> Optional[Dict]:
        """
        캐시된 호가창 데이터 조회 (3초 이내)
        
        Args:
            ticker: 코인 티커
        
        Returns:
            캐시된 분석 데이터 또는 None
        """
        if ticker not in self.cache:
            return None
        
        cached = self.cache[ticker]
        elapsed = time.time() - cached['timestamp']
        
        # 캐시 유효 시간 확인
        if elapsed < self.cache_duration:
            return cached['data']
        
        return None
    
    def _analyze_orderbook(self, ticker: str, orderbook_data: Dict) -> Optional[Dict]:
        """
        호가창 데이터 분석
        
        Args:
            ticker: 코인 티커
            orderbook_data: 호가창 원본 데이터
        
        Returns:
            분석 결과
        """
        try:
            # OrderBookAnalyzer로 분석
            analysis = self.analyzer.analyze_orderbook(orderbook_data)
            
            if not analysis:
                return None
            
            # 추가 분석
            enhanced_analysis = {
                **analysis,
                'ticker': ticker,
                'timestamp': datetime.now().isoformat(),
                'buy_wall_detected': self._detect_buy_wall(orderbook_data),
                'sell_wall_detected': self._detect_sell_wall(orderbook_data),
                'imbalance_ratio': self._calculate_imbalance(orderbook_data),
                'spread_ratio': self._calculate_spread(orderbook_data)
            }
            
            # 캐시 업데이트
            self.cache[ticker] = {
                'data': enhanced_analysis,
                'timestamp': time.time()
            }
            
            return enhanced_analysis
            
        except Exception as e:
            self.logger.log_error("ORDERBOOK_ANALYZE", f"{ticker} 분석 실패", e)
            return None
    
    def _detect_buy_wall(self, orderbook_data: Dict) -> bool:
        """매수 벽 감지"""
        try:
            bids = orderbook_data[0]['orderbook_units']
            
            # 최상위 매수 호가의 수량
            top_bid_size = float(bids[0]['bid_size'])
            
            # 평균 매수 수량
            avg_bid_size = sum(float(b['bid_size']) for b in bids[:5]) / 5
            
            # 최상위가 평균의 3배 이상이면 매수 벽
            return top_bid_size > avg_bid_size * 3
            
        except:
            return False
    
    def _detect_sell_wall(self, orderbook_data: Dict) -> bool:
        """매도 벽 감지"""
        try:
            asks = orderbook_data[0]['orderbook_units']
            
            # 최상위 매도 호가의 수량
            top_ask_size = float(asks[0]['ask_size'])
            
            # 평균 매도 수량
            avg_ask_size = sum(float(a['ask_size']) for a in asks[:5]) / 5
            
            # 최상위가 평균의 3배 이상이면 매도 벽
            return top_ask_size > avg_ask_size * 3
            
        except:
            return False
    
    def _calculate_imbalance(self, orderbook_data: Dict) -> float:
        """
        매수/매도 불균형 비율 계산
        
        Returns:
            양수: 매수 우세, 음수: 매도 우세
        """
        try:
            units = orderbook_data[0]['orderbook_units']
            
            total_bid = sum(float(u['bid_size']) * float(u['bid_price']) for u in units)
            total_ask = sum(float(u['ask_size']) * float(u['ask_price']) for u in units)
            
            if total_bid + total_ask == 0:
                return 0.0
            
            return (total_bid - total_ask) / (total_bid + total_ask)
            
        except:
            return 0.0
    
    def _calculate_spread(self, orderbook_data: Dict) -> float:
        """
        스프레드 비율 계산
        
        Returns:
            스프레드 비율 (%)
        """
        try:
            units = orderbook_data[0]['orderbook_units']
            
            best_bid = float(units[0]['bid_price'])
            best_ask = float(units[0]['ask_price'])
            
            if best_bid == 0:
                return 0.0
            
            return ((best_ask - best_bid) / best_bid) * 100
            
        except:
            return 0.0
    
    def _save_to_history(self, ticker: str, analysis: Dict):
        """이력에 저장"""
        if ticker not in self.orderbook_history:
            self.orderbook_history[ticker] = deque(maxlen=self.max_history)
        
        self.orderbook_history[ticker].append({
            'timestamp': analysis['timestamp'],
            'liquidity_score': analysis.get('liquidity_score', 0),
            'slippage_risk': analysis.get('slippage_risk', 'UNKNOWN'),
            'buy_wall': analysis.get('buy_wall_detected', False),
            'sell_wall': analysis.get('sell_wall_detected', False),
            'imbalance': analysis.get('imbalance_ratio', 0),
            'spread': analysis.get('spread_ratio', 0)
        })
    
    def _learn_pattern(self, ticker: str, analysis: Dict):
        """
        호가창 패턴 학습
        
        패턴 종류:
        - high_liquidity_low_risk: 고유동성 + 저위험
        - low_liquidity_high_risk: 저유동성 + 고위험
        - buy_wall_detected: 매수 벽 존재
        - sell_wall_detected: 매도 벽 존재
        - balanced: 균형 잡힌 호가창
        """
        if ticker not in self.liquidity_patterns:
            self.liquidity_patterns[ticker] = {
                'high_liquidity_low_risk': 0,
                'low_liquidity_high_risk': 0,
                'buy_wall_detected': 0,
                'sell_wall_detected': 0,
                'balanced': 0
            }
        
        # 패턴 분류
        liquidity_score = analysis.get('liquidity_score', 0)
        slippage_risk = analysis.get('slippage_risk', 'UNKNOWN')
        buy_wall = analysis.get('buy_wall_detected', False)
        sell_wall = analysis.get('sell_wall_detected', False)
        imbalance = abs(analysis.get('imbalance_ratio', 0))
        
        # 패턴 카운트
        if liquidity_score >= 70 and slippage_risk == 'LOW':
            self.liquidity_patterns[ticker]['high_liquidity_low_risk'] += 1
        elif liquidity_score < 30 and slippage_risk == 'HIGH':
            self.liquidity_patterns[ticker]['low_liquidity_high_risk'] += 1
        
        if buy_wall:
            self.liquidity_patterns[ticker]['buy_wall_detected'] += 1
        
        if sell_wall:
            self.liquidity_patterns[ticker]['sell_wall_detected'] += 1
        
        if imbalance < 0.2:
            self.liquidity_patterns[ticker]['balanced'] += 1
    
    def get_liquidity_pattern(self, ticker: str) -> Dict:
        """
        학습된 유동성 패턴 조회
        
        Args:
            ticker: 코인 티커
        
        Returns:
            패턴 통계
        """
        if ticker not in self.liquidity_patterns:
            return {}
        
        patterns = self.liquidity_patterns[ticker]
        total = sum(patterns.values())
        
        if total == 0:
            return {}
        
        # 비율로 변환
        return {
            pattern: (count / total) * 100
            for pattern, count in patterns.items()
        }
    
    def predict_slippage(self, ticker: str, amount: float) -> float:
        """
        슬리피지 예측 (AI 학습 기반)
        
        Args:
            ticker: 코인 티커
            amount: 거래 금액
        
        Returns:
            예상 슬리피지 (%)
        """
        # 캐시된 호가창 조회
        cached = self.get_cached_orderbook(ticker)
        
        if not cached:
            # 기본값 반환
            return 0.5
        
        # 학습된 패턴 기반 예측
        pattern = self.get_liquidity_pattern(ticker)
        liquidity_score = cached.get('liquidity_score', 50)
        
        # 기본 슬리피지 계산
        base_slippage = 0.1
        
        # 유동성 점수에 따른 조정
        if liquidity_score >= 70:
            base_slippage *= 0.5  # 고유동성: 슬리피지 감소
        elif liquidity_score < 30:
            base_slippage *= 2.0  # 저유동성: 슬리피지 증가
        
        # 패턴에 따른 조정
        if pattern.get('high_liquidity_low_risk', 0) > 50:
            base_slippage *= 0.7
        elif pattern.get('low_liquidity_high_risk', 0) > 50:
            base_slippage *= 1.5
        
        # 금액에 따른 조정 (큰 금액일수록 슬리피지 증가)
        if amount > 1000000:  # 100만원 이상
            base_slippage *= 1.5
        elif amount > 500000:  # 50만원 이상
            base_slippage *= 1.2
        
        return round(base_slippage, 2)
    
    def should_use_limit_order(self, ticker: str, amount: float) -> bool:
        """
        지정가 주문 사용 여부 결정 (AI 학습 기반)
        
        Args:
            ticker: 코인 티커
            amount: 거래 금액
        
        Returns:
            True: 지정가 사용, False: 시장가 사용
        """
        # 슬리피지 예측
        predicted_slippage = self.predict_slippage(ticker, amount)
        
        # 캐시된 호가창 조회
        cached = self.get_cached_orderbook(ticker)
        
        if not cached:
            # 데이터 없으면 보수적으로 지정가 사용
            return True
        
        slippage_risk = cached.get('slippage_risk', 'MEDIUM')
        liquidity_score = cached.get('liquidity_score', 50)
        
        # 결정 로직
        # 1. 예상 슬리피지가 0.3% 이상이면 지정가
        if predicted_slippage >= 0.3:
            return True
        
        # 2. 슬리피지 위험이 HIGH이면 지정가
        if slippage_risk == 'HIGH':
            return True
        
        # 3. 유동성 점수가 50 미만이면 지정가
        if liquidity_score < 50:
            return True
        
        # 4. 큰 금액(50만원 이상)이면 지정가
        if amount >= 500000:
            return True
        
        # 나머지는 시장가
        return False
    
    def get_optimal_entry_price(self, ticker: str, action: str = "BUY") -> Optional[float]:
        """
        최적 진입 가격 추천
        
        Args:
            ticker: 코인 티커
            action: BUY 또는 SELL
        
        Returns:
            추천 가격
        """
        cached = self.get_cached_orderbook(ticker)
        
        if not cached:
            return None
        
        if 'recommended_price' in cached:
            return cached['recommended_price']
        
        return None
    
    def _load_learning_data(self):
        """저장된 학습 데이터 로드"""
        try:
            patterns_file = os.path.join(self.data_dir, "liquidity_patterns.json")
            
            if os.path.exists(patterns_file):
                with open(patterns_file, 'r', encoding='utf-8') as f:
                    self.liquidity_patterns = json.load(f)
                    self.logger.log_info(f"✅ 호가창 패턴 학습 데이터 로드 완료: {len(self.liquidity_patterns)}개")
        
        except Exception as e:
            self.logger.log_error("ORDERBOOK_LOAD", "학습 데이터 로드 실패", e)
    
    def save_learning_data(self):
        """학습 데이터 저장"""
        try:
            patterns_file = os.path.join(self.data_dir, "liquidity_patterns.json")
            
            with open(patterns_file, 'w', encoding='utf-8') as f:
                json.dump(self.liquidity_patterns, f, ensure_ascii=False, indent=2)
            
            self.logger.log_info(f"✅ 호가창 학습 데이터 저장 완료: {len(self.liquidity_patterns)}개")
        
        except Exception as e:
            self.logger.log_error("ORDERBOOK_SAVE", "학습 데이터 저장 실패", e)
    
    def get_statistics(self) -> Dict:
        """통계 정보 조회"""
        return {
            'monitored_tickers': len(self.orderbook_history),
            'total_patterns': sum(sum(p.values()) for p in self.liquidity_patterns.values()),
            'cache_size': len(self.cache),
            'history_size': sum(len(h) for h in self.orderbook_history.values())
        }
