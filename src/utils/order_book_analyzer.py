"""
호가창 분석 시스템
실시간 호가창 데이터를 분석하여 최적의 주문 방식 결정
"""

from typing import Dict, List, Tuple, Optional
import time
from datetime import datetime


class OrderBookAnalyzer:
    """호가창 실시간 분석기"""
    
    def __init__(self, api_client):
        """
        Args:
            api_client: Upbit API 클라이언트
        """
        self.api = api_client
        self.analysis_cache = {}  # 티커별 분석 결과 캐시
        self.cache_duration = 3  # 캐시 유효 시간 (초)
        
    def analyze_order_book(self, ticker: str) -> Dict:
        """
        호가창 종합 분석
        
        Returns:
            {
                'liquidity_score': 0~100,  # 유동성 점수
                'bid_ask_spread': float,    # 호가 스프레드
                'imbalance_ratio': float,   # 매수/매도 불균형 비율
                'depth_score': 0~100,       # 호가 깊이 점수
                'slippage_risk': 'LOW'|'MEDIUM'|'HIGH',  # 슬리피지 위험
                'recommended_order_type': 'MARKET'|'LIMIT',
                'limit_price': float,       # 지정가 추천 가격
                'timestamp': datetime
            }
        """
        # 캐시 확인
        if ticker in self.analysis_cache:
            cached = self.analysis_cache[ticker]
            if time.time() - cached['timestamp'].timestamp() < self.cache_duration:
                return cached
        
        try:
            # 호가창 데이터 조회
            orderbook = self.api.get_orderbook(ticker)
            if not orderbook:
                return self._default_analysis()
            
            # 매수/매도 호가 추출
            bids = orderbook[0]['orderbook_units']  # 매수 호가
            asks = orderbook[0]['orderbook_units']  # 매도 호가
            
            # 1. 유동성 분석
            liquidity_score = self._calculate_liquidity(bids, asks)
            
            # 2. 스프레드 계산
            best_bid = bids[0]['bid_price']
            best_ask = asks[0]['ask_price']
            spread = (best_ask - best_bid) / best_bid * 100
            
            # 3. 매수/매도 불균형
            total_bid_size = sum(b['bid_size'] for b in bids)
            total_ask_size = sum(a['ask_size'] for a in asks)
            imbalance = total_bid_size / (total_ask_size + 1e-10)
            
            # 4. 호가 깊이
            depth_score = self._calculate_depth_score(bids, asks)
            
            # 5. 슬리피지 위험 평가
            slippage_risk = self._assess_slippage_risk(spread, liquidity_score)
            
            # 6. 주문 방식 추천
            order_type, limit_price = self._recommend_order_type(
                best_bid, best_ask, spread, slippage_risk
            )
            
            analysis = {
                'liquidity_score': liquidity_score,
                'bid_ask_spread': spread,
                'imbalance_ratio': imbalance,
                'depth_score': depth_score,
                'slippage_risk': slippage_risk,
                'recommended_order_type': order_type,
                'limit_price': limit_price,
                'best_bid': best_bid,
                'best_ask': best_ask,
                'timestamp': datetime.now()
            }
            
            # 캐시 저장
            self.analysis_cache[ticker] = analysis
            
            return analysis
            
        except Exception as e:
            print(f"❌ 호가창 분석 오류 ({ticker}): {e}")
            return self._default_analysis()
    
    def _calculate_liquidity(self, bids: List[Dict], asks: List[Dict]) -> float:
        """
        유동성 점수 계산 (0~100)
        
        높은 점수 = 높은 유동성 = 거래하기 좋음
        """
        try:
            # 상위 5단계 호가의 총 거래량
            bid_volume = sum(b['bid_size'] * b['bid_price'] for b in bids[:5])
            ask_volume = sum(a['ask_size'] * a['ask_price'] for a in asks[:5])
            total_volume = bid_volume + ask_volume
            
            # 100만원 기준 정규화
            liquidity_score = min(100, (total_volume / 1_000_000) * 100)
            
            return round(liquidity_score, 2)
        except:
            return 50.0
    
    def _calculate_depth_score(self, bids: List[Dict], asks: List[Dict]) -> float:
        """
        호가 깊이 점수 (0~100)
        
        높은 점수 = 깊은 호가창 = 대량 거래 가능
        """
        try:
            # 전체 10단계 호가 분석
            bid_depth = sum(b['bid_size'] for b in bids)
            ask_depth = sum(a['ask_size'] for a in asks)
            total_depth = bid_depth + ask_depth
            
            # 평균 대비 깊이 평가 (임의 기준: 10 BTC = 100점)
            depth_score = min(100, (total_depth / 10) * 100)
            
            return round(depth_score, 2)
        except:
            return 50.0
    
    def _assess_slippage_risk(self, spread: float, liquidity_score: float) -> str:
        """
        슬리피지 위험도 평가
        
        Args:
            spread: 호가 스프레드 (%)
            liquidity_score: 유동성 점수
        
        Returns:
            'LOW', 'MEDIUM', 'HIGH'
        """
        # 스프레드가 크거나 유동성이 낮으면 위험
        if spread > 0.5 or liquidity_score < 30:
            return 'HIGH'
        elif spread > 0.2 or liquidity_score < 60:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _recommend_order_type(
        self, 
        best_bid: float, 
        best_ask: float, 
        spread: float, 
        slippage_risk: str
    ) -> Tuple[str, float]:
        """
        최적 주문 방식 추천
        
        Returns:
            (주문 타입, 지정가 가격)
        """
        # 1. 슬리피지 위험 높음 → 지정가 추천
        if slippage_risk == 'HIGH':
            # 매수: 최우선 매수호가보다 약간 높게
            # 매도: 최우선 매도호가보다 약간 낮게
            limit_price = (best_bid + best_ask) / 2
            return 'LIMIT', limit_price
        
        # 2. 스프레드 0.3% 이상 → 지정가 유리
        if spread > 0.3:
            limit_price = (best_bid + best_ask) / 2
            return 'LIMIT', limit_price
        
        # 3. 낮은 위험 + 좁은 스프레드 → 시장가 가능
        return 'MARKET', best_ask
    
    def _default_analysis(self) -> Dict:
        """기본 분석 결과 (오류 시)"""
        return {
            'liquidity_score': 50.0,
            'bid_ask_spread': 0.5,
            'imbalance_ratio': 1.0,
            'depth_score': 50.0,
            'slippage_risk': 'MEDIUM',
            'recommended_order_type': 'MARKET',
            'limit_price': 0.0,
            'best_bid': 0.0,
            'best_ask': 0.0,
            'timestamp': datetime.now()
        }
    
    def should_execute_order(self, ticker: str, amount: float, action: str = "BUY") -> Dict:
        """
        주문 실행 여부 및 방식 결정
        
        Args:
            ticker: 티커 심볼
            amount: 주문 수량 (원화)
            action: 'BUY' 또는 'SELL'
        
        Returns:
            {
                'should_execute': bool,
                'order_type': 'MARKET'|'LIMIT'|'SKIP',
                'price': float,
                'reason': str
            }
        """
        analysis = self.analyze_order_book(ticker)
        
        # 슬리피지 위험 평가
        if analysis['slippage_risk'] == 'HIGH' and amount > 100_000:
            # 10만원 이상 + 고위험 → SKIP
            return {
                'should_execute': False,
                'order_type': 'SKIP',
                'price': 0.0,
                'reason': f'슬리피지 위험 높음 (스프레드: {analysis["bid_ask_spread"]:.3f}%)'
            }
        
        # 주문 방식 결정
        if analysis['recommended_order_type'] == 'LIMIT':
            return {
                'should_execute': True,
                'order_type': 'LIMIT',
                'price': analysis['limit_price'],
                'reason': f'지정가 주문 추천 (스프레드: {analysis["bid_ask_spread"]:.3f}%)'
            }
        else:
            return {
                'should_execute': True,
                'order_type': 'MARKET',
                'price': analysis['best_ask'] if action == "BUY" else analysis['best_bid'],
                'reason': f'시장가 주문 안전 (유동성: {analysis["liquidity_score"]:.1f}점)'
            }
    
    def get_optimal_entry_price(self, ticker: str, action: str = "BUY") -> Optional[float]:
        """
        최적 진입 가격 계산
        
        매수: 최우선 매도호가 ~ 중간가
        매도: 최우선 매수호가 ~ 중간가
        """
        analysis = self.analyze_order_book(ticker)
        
        if action == "BUY":
            # 시장가보다 유리한 가격 제시
            return analysis['best_ask'] * 0.999  # 0.1% 낮게
        else:
            return analysis['best_bid'] * 1.001  # 0.1% 높게
