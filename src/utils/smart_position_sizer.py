"""
Smart Position Sizing System
- Dynamic position sizing based on signal strength (100k-500k KRW)
- Orderbook depth analysis for slippage prevention
- Score-based position size determination
"""

from typing import Dict, Optional, Tuple
import logging


class SmartPositionSizer:
    """스마트 포지션 사이징 시스템"""
    
    def __init__(self):
        """초기화"""
        self.min_position_krw = 100000  # 최소 10만원
        self.max_position_krw = 500000  # 최대 50만원
        self.min_orderbook_depth_krw = 300000  # 호가창 최소 깊이 30만원
        
    def calculate_signal_score(self, 
                               surge_score: float = 0,
                               ai_confidence: float = 0,
                               volume_ratio: float = 1.0,
                               price_momentum: float = 0,
                               strategy: str = "") -> float:
        """
        신호 점수 계산 (0-100점)
        
        Args:
            surge_score: 급등 점수 (0-100)
            ai_confidence: AI 신뢰도 (0-100)
            volume_ratio: 거래량 비율 (1.0 = 평균)
            price_momentum: 가격 모멘텀 (%)
            strategy: 전략 이름
        
        Returns:
            종합 점수 (0-100)
        """
        score = 0.0
        
        # 1. 급등 점수 (40% 가중치)
        score += surge_score * 0.4
        
        # 2. AI 신뢰도 (30% 가중치)
        score += ai_confidence * 0.3
        
        # 3. 거래량 점수 (20% 가중치)
        volume_score = min((volume_ratio / 2.0) * 100, 100)  # 2.0배 = 100점
        score += volume_score * 0.2
        
        # 4. 가격 모멘텀 점수 (10% 가중치)
        momentum_score = min((price_momentum / 5.0) * 100, 100)  # 5% = 100점
        score += momentum_score * 0.1
        
        # 5. 전략별 보너스/페널티
        strategy_upper = strategy.upper() if strategy else ""
        if "ULTRA" in strategy_upper or "CHASE" in strategy_upper:
            score *= 1.1  # 초단타/추격 전략: +10%
        elif "CONSERVATIVE" in strategy_upper:
            score *= 0.9  # 보수 전략: -10%
        
        return min(score, 100.0)
    
    def calculate_position_size(self, 
                               total_score: float,
                               current_balance: float,
                               orderbook_depth: Optional[Dict] = None) -> int:
        """
        점수 기반 포지션 크기 계산
        
        Args:
            total_score: 종합 신호 점수 (0-100)
            current_balance: 현재 잔고 (KRW)
            orderbook_depth: 호가창 깊이 정보
        
        Returns:
            투자 금액 (KRW)
        """
        # 1. 기본 점수 기반 계산
        score_ratio = total_score / 100.0
        
        # 2. 선형 매핑: 0점=10만원, 100점=50만원
        base_position = self.min_position_krw + (
            (self.max_position_krw - self.min_position_krw) * score_ratio
        )
        
        # 3. 호가창 깊이 확인 및 조정
        if orderbook_depth:
            available_depth = orderbook_depth.get('total_ask_amount_krw', 0)
            
            # 호가창 깊이가 부족하면 포지션 크기 줄이기
            if available_depth < self.min_orderbook_depth_krw:
                # 호가창의 60%만 사용 (슬리피지 최소화)
                max_safe_position = available_depth * 0.6
                base_position = min(base_position, max_safe_position)
                
                logging.warning(
                    f"⚠️ 호가창 깊이 부족: {available_depth:,.0f}원 "
                    f"→ 포지션 축소: {base_position:,.0f}원"
                )
        
        # 4. 잔고 제한 (최대 30%)
        max_by_balance = current_balance * 0.3
        final_position = min(base_position, max_by_balance)
        
        # 5. 최소/최대 제한 적용
        final_position = max(self.min_position_krw, 
                            min(final_position, self.max_position_krw))
        
        # 6. 1만원 단위로 반올림
        final_position = round(final_position / 10000) * 10000
        
        return int(final_position)
    
    def analyze_orderbook_depth(self, orderbook: Dict, target_amount_krw: int = 500000) -> Dict:
        """
        호가창 깊이 분석
        
        Args:
            orderbook: 호가창 데이터 {'asks': [...], 'bids': [...]}
            target_amount_krw: 목표 매수 금액 (KRW)
        
        Returns:
            깊이 분석 결과
        """
        if not orderbook or 'asks' not in orderbook:
            return {
                'total_ask_amount_krw': 0,
                'average_price': 0,
                'slippage_percent': 0,
                'sufficient_depth': False
            }
        
        asks = orderbook.get('asks', [])
        if not asks:
            return {
                'total_ask_amount_krw': 0,
                'average_price': 0,
                'slippage_percent': 0,
                'sufficient_depth': False
            }
        
        # 누적 매수 시뮬레이션
        accumulated_krw = 0
        accumulated_volume = 0
        best_ask_price = asks[0]['price'] if asks else 0
        
        for ask in asks:
            price = ask['price']
            size = ask['size']
            order_krw = price * size
            
            if accumulated_krw + order_krw <= target_amount_krw:
                accumulated_krw += order_krw
                accumulated_volume += size
            else:
                # 목표 금액 도달
                remaining_krw = target_amount_krw - accumulated_krw
                partial_size = remaining_krw / price
                accumulated_krw += remaining_krw
                accumulated_volume += partial_size
                break
        
        # 평균 체결가 계산
        if accumulated_volume > 0:
            average_price = accumulated_krw / accumulated_volume
            slippage = ((average_price - best_ask_price) / best_ask_price) * 100
        else:
            average_price = 0
            slippage = 0
        
        # 전체 호가창 깊이
        total_depth = sum(ask['price'] * ask['size'] for ask in asks)
        
        return {
            'total_ask_amount_krw': total_depth,
            'average_price': average_price,
            'best_ask_price': best_ask_price,
            'slippage_percent': slippage,
            'sufficient_depth': accumulated_krw >= target_amount_krw * 0.8,
            'available_amount_krw': accumulated_krw
        }
    
    def get_recommended_position(self,
                                ticker: str,
                                api,
                                surge_info: Optional[Dict] = None,
                                ai_decision: Optional[Dict] = None,
                                current_balance: float = 0) -> Tuple[int, Dict]:
        """
        추천 포지션 크기 계산 (통합 인터페이스)
        
        Args:
            ticker: 코인 티커
            api: UpbitAPI 인스턴스
            surge_info: 급등 정보
            ai_decision: AI 의사결정 정보
            current_balance: 현재 잔고
        
        Returns:
            (포지션 크기, 상세 정보)
        """
        # 1. 호가창 조회
        orderbook = api.get_orderbook(ticker)
        
        # 2. 신호 점수 계산
        surge_score = surge_info.get('surge_score', 0) if surge_info else 0
        ai_confidence = ai_decision.get('confidence', 0) * 100 if ai_decision else 0
        volume_ratio = surge_info.get('volume_ratio', 1.0) if surge_info else 1.0
        price_momentum = surge_info.get('change_1m', 0) if surge_info else 0
        strategy = surge_info.get('strategy', '') if surge_info else ''
        
        total_score = self.calculate_signal_score(
            surge_score=surge_score,
            ai_confidence=ai_confidence,
            volume_ratio=volume_ratio,
            price_momentum=price_momentum,
            strategy=strategy
        )
        
        # 3. 호가창 깊이 분석
        depth_analysis = self.analyze_orderbook_depth(orderbook, target_amount_krw=500000)
        
        # 4. 최종 포지션 크기 결정
        position_size = self.calculate_position_size(
            total_score=total_score,
            current_balance=current_balance,
            orderbook_depth=depth_analysis
        )
        
        # 5. 상세 정보 반환
        detail = {
            'total_score': total_score,
            'surge_score': surge_score,
            'ai_confidence': ai_confidence,
            'volume_ratio': volume_ratio,
            'price_momentum': price_momentum,
            'orderbook_depth': depth_analysis,
            'position_size': position_size,
            'slippage_estimate': depth_analysis['slippage_percent']
        }
        
        return position_size, detail
