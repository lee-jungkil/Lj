"""
주문 방법 자동 선택 시스템 (Order Method Selector)
- 시장 조건, 전략, 청산 사유 기반 최적 주문 방식 자동 선택
"""

from typing import Dict, Optional, Literal
from enum import Enum


class OrderMethod(Enum):
    """주문 방법 열거형"""
    MARKET = "market"  # 시장가
    LIMIT = "limit"  # 지정가
    BEST = "best"  # 최유리 (IOC)
    IOC = "ioc"  # Immediate Or Cancel
    FOK = "fok"  # Fill Or Kill (미지원 - market fallback)
    POST_ONLY = "post_only"  # Post Only (maker 수수료)


class ExitReason(Enum):
    """청산 사유"""
    STOP_LOSS = "stop_loss"  # 손절
    TAKE_PROFIT = "take_profit"  # 익절
    TRAILING_STOP = "trailing_stop"  # 트레일링 스탑
    CHART_SIGNAL = "chart_signal"  # 차트 신호
    TIME_EXCEEDED = "time_exceeded"  # 시간 초과
    SUDDEN_DROP = "sudden_drop"  # 급락 감지
    VOLUME_DROP = "volume_drop"  # 거래량 급감
    EMERGENCY = "emergency"  # 긴급 청산


class OrderMethodSelector:
    """주문 방법 자동 선택 엔진"""
    
    def __init__(self):
        """초기화"""
        self.spread_threshold_low = 0.1  # 스프레드 낮음 (%)
        self.spread_threshold_high = 0.5  # 스프레드 높음 (%)
    
    def select_buy_method(self, ticker: str, strategy: str, market_condition: Dict,
                         spread_pct: float, is_chase: bool = False) -> tuple[OrderMethod, str]:
        """
        매수 주문 방법 자동 선택
        
        Decision Tree:
        1. 추격매수 → market (즉시 진입 필수)
        2. Ultra Scalping + 스프레드 < 0.1% → best (슬리피지 최소화)
        3. Aggressive + 고변동성 → market (빠른 진입)
        4. Aggressive + 정상 → limit -0.1% (대기 후 진입)
        5. Conservative → best + IOC (균형)
        6. Mean Reversion → limit -0.5% (지지선 매수)
        7. Grid Trading → post_only (메이커 수수료)
        
        Args:
            ticker: 코인 티커
            strategy: 전략 이름
            market_condition: 시장 조건 {'volatility', 'trend', 'market_phase'}
            spread_pct: 스프레드 비율 (%)
            is_chase: 추격매수 여부
        
        Returns:
            (주문 방법, 사유)
        """
        # 1. 추격매수 → 무조건 시장가
        if is_chase:
            return OrderMethod.MARKET, "추격매수 - 즉시 진입 필수"
        
        # 2. Ultra Scalping + 스프레드 < 0.1% → 최유리
        if "ULTRA" in strategy.upper() or "초단타" in strategy:
            if spread_pct < self.spread_threshold_low:
                return OrderMethod.BEST, "초단타 + 낮은 스프레드 → 최유리"
            else:
                return OrderMethod.MARKET, "초단타 + 높은 스프레드 → 시장가"
        
        # 3. Aggressive Scalping
        if "AGGRESSIVE" in strategy.upper() or "공격적" in strategy:
            volatility = market_condition.get('volatility', 'medium')
            if volatility == 'high':
                return OrderMethod.MARKET, "공격적 전략 + 고변동성 → 시장가"
            else:
                return OrderMethod.LIMIT, "공격적 전략 + 정상 변동 → 지정가 -0.1%"
        
        # 4. Conservative Scalping
        if "CONSERVATIVE" in strategy.upper() or "보수적" in strategy:
            if spread_pct < self.spread_threshold_low:
                return OrderMethod.BEST, "보수적 전략 + 낮은 스프레드 → 최유리"
            else:
                return OrderMethod.IOC, "보수적 전략 + 높은 스프레드 → IOC"
        
        # 5. Mean Reversion
        if "MEAN" in strategy.upper() or "평균회귀" in strategy:
            return OrderMethod.LIMIT, "평균회귀 전략 → 지지선 지정가 -0.5%"
        
        # 6. Grid Trading
        if "GRID" in strategy.upper() or "그리드" in strategy:
            return OrderMethod.POST_ONLY, "그리드 전략 → Post Only (메이커 수수료)"
        
        # 7. 기본 (변동성 기반)
        volatility = market_condition.get('volatility', 'medium')
        if volatility == 'high':
            return OrderMethod.MARKET, "고변동성 → 시장가"
        elif volatility == 'low':
            return OrderMethod.LIMIT, "저변동성 → 지정가"
        else:
            return OrderMethod.BEST, "보통 변동성 → 최유리"
    
    def select_sell_method(self, ticker: str, strategy: str, exit_reason: ExitReason,
                          spread_pct: float, profit_ratio: float, 
                          market_condition: Dict) -> tuple[OrderMethod, str]:
        """
        매도 주문 방법 자동 선택
        
        Decision Tree:
        1. 손절 (STOP_LOSS) → market (즉시 청산)
        2. 긴급 (EMERGENCY) → market (급락 탈출)
        3. 익절 (TAKE_PROFIT) + 추격/초단타 → market (수익 확보 우선)
        4. 익절 + 스프레드 < 0.1% → best (슬리피지 최소화)
        5. 익절 + 일반 → limit +0.1% (대기 후 실현)
        6. 트레일링 스탑 → market (수익 보호)
        7. 시간 초과 + 수익 중 → best (빠른 실현)
        8. 시간 초과 + 손실 중 → market (즉시 청산)
        9. 차트 신호 + 수익 ≥ 1% → best (수익 보호)
        10. 차트 신호 + 낮은 수익 → limit +0.3% (대기)
        11. 거래량 급감 + 수익 > 0.5% → market (즉시 보호)
        
        Args:
            ticker: 코인 티커
            strategy: 전략 이름
            exit_reason: 청산 사유
            spread_pct: 스프레드 비율 (%)
            profit_ratio: 수익률 (%)
            market_condition: 시장 조건
        
        Returns:
            (주문 방법, 사유)
        """
        # 1. 손절 → 무조건 시장가
        if exit_reason == ExitReason.STOP_LOSS:
            return OrderMethod.MARKET, "손절 → 즉시 청산"
        
        # 2. 긴급 청산 → 무조건 시장가
        if exit_reason == ExitReason.EMERGENCY or exit_reason == ExitReason.SUDDEN_DROP:
            return OrderMethod.MARKET, "긴급 청산 → 즉시 탈출"
        
        # 3. 익절
        if exit_reason == ExitReason.TAKE_PROFIT:
            # 추격매수 or 초단타 → 시장가
            if "CHASE" in strategy.upper() or "ULTRA" in strategy.upper():
                return OrderMethod.MARKET, "익절 (추격/초단타) → 즉시 청산"
            
            # 스프레드 낮음 → 최유리
            if spread_pct < self.spread_threshold_low:
                return OrderMethod.BEST, "익절 + 낮은 스프레드 → 최유리"
            
            # 일반 → 지정가 +0.1%
            return OrderMethod.LIMIT, "익절 → 지정가 +0.1%"
        
        # 4. 트레일링 스탑 → 시장가
        if exit_reason == ExitReason.TRAILING_STOP:
            return OrderMethod.MARKET, "트레일링 스탑 → 수익 보호"
        
        # 5. 시간 초과
        if exit_reason == ExitReason.TIME_EXCEEDED:
            if profit_ratio > 0:
                return OrderMethod.BEST, "시간 초과 + 수익 중 → 빠른 실현"
            else:
                return OrderMethod.MARKET, "시간 초과 + 손실 중 → 즉시 청산"
        
        # 6. 차트 신호
        if exit_reason == ExitReason.CHART_SIGNAL:
            if profit_ratio >= 1.0:
                return OrderMethod.BEST, "차트 신호 + 수익 ≥ 1% → 수익 보호"
            else:
                return OrderMethod.LIMIT, "차트 신호 + 낮은 수익 → 지정가 +0.3%"
        
        # 7. 거래량 급감
        if exit_reason == ExitReason.VOLUME_DROP:
            if profit_ratio > 0.5:
                return OrderMethod.MARKET, "거래량 급감 + 수익 > 0.5% → 즉시 보호"
            else:
                return OrderMethod.BEST, "거래량 급감 + 낮은 수익 → 최유리"
        
        # 8. 기본 (수익률 기반)
        if profit_ratio > 2.0:
            return OrderMethod.MARKET, "고수익 → 즉시 청산"
        elif profit_ratio > 0:
            return OrderMethod.BEST, "수익 중 → 최유리"
        else:
            return OrderMethod.MARKET, "손실 중 → 즉시 청산"
    
    def get_limit_price_offset(self, method: OrderMethod, is_buy: bool, 
                              current_price: float, strategy: str) -> float:
        """
        지정가 주문 시 가격 오프셋 계산
        
        Args:
            method: 주문 방법
            is_buy: 매수 여부
            current_price: 현재가
            strategy: 전략 이름
        
        Returns:
            오프셋 가격 (양수/음수)
        """
        if method != OrderMethod.LIMIT:
            return 0.0
        
        # 매수: 현재가보다 낮게
        if is_buy:
            if "MEAN" in strategy.upper():
                return -current_price * 0.005  # -0.5%
            elif "AGGRESSIVE" in strategy.upper():
                return -current_price * 0.001  # -0.1%
            else:
                return -current_price * 0.002  # -0.2%
        
        # 매도: 현재가보다 높게
        else:
            if "CHART" in strategy or "차트" in strategy:
                return current_price * 0.003  # +0.3%
            else:
                return current_price * 0.001  # +0.1%
    
    def should_use_fallback(self, method: OrderMethod, wait_time: int, 
                           max_wait: int = 5) -> bool:
        """
        Fallback 시장가로 전환 여부
        
        Args:
            method: 주문 방법
            wait_time: 대기 시간 (초)
            max_wait: 최대 대기 시간 (초)
        
        Returns:
            Fallback 필요 여부
        """
        # 지정가 주문이 max_wait 초과 시 시장가로 전환
        if method == OrderMethod.LIMIT and wait_time > max_wait:
            return True
        
        # IOC는 즉시 완료되므로 fallback 불필요
        if method == OrderMethod.IOC:
            return False
        
        return False


# 전역 인스턴스
order_method_selector = OrderMethodSelector()
