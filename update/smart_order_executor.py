"""
스마트 주문 실행기 (Smart Order Executor)
- 재시도 로직 (최대 3회)
- Fallback 지원 (지정가 → 시장가)
- 호가 단위 자동 조정
- 주문 상태 모니터링
"""

import time
from typing import Dict, Optional, Tuple
from datetime import datetime


class SmartOrderExecutor:
    """스마트 주문 실행기"""
    
    def __init__(self, api, order_selector):
        """
        초기화
        
        Args:
            api: UpbitAPI 인스턴스
            order_selector: OrderMethodSelector 인스턴스
        """
        self.api = api
        self.order_selector = order_selector
        
        # 설정
        self.max_retries = 3  # 최대 재시도 횟수
        self.retry_delay = 1.0  # 재시도 대기 시간 (초)
        self.limit_order_timeout = 5  # 지정가 주문 타임아웃 (초)
        self.enable_fallback = True  # Fallback 활성화
    
    def execute_buy(self, ticker: str, investment: float, strategy: str,
                   market_condition: Dict, is_chase: bool = False) -> Optional[Dict]:
        """
        스마트 매수 실행
        
        Process:
        1. 주문 방법 자동 선택
        2. 호가창 조회 (스프레드 계산)
        3. 주문 실행 (재시도 포함)
        4. 지정가 → 시장가 Fallback (필요 시)
        
        Args:
            ticker: 코인 티커
            investment: 투자 금액 (KRW)
            strategy: 전략 이름
            market_condition: 시장 조건
            is_chase: 추격매수 여부
        
        Returns:
            주문 결과 딕셔너리
        """
        try:
            # 1. 스프레드 계산
            spread_pct = self.api.calculate_spread_percentage(ticker)
            
            # 2. 주문 방법 선택
            from src.utils.order_method_selector import OrderMethod
            method, reason = self.order_selector.select_buy_method(
                ticker=ticker,
                strategy=strategy,
                market_condition=market_condition,
                spread_pct=spread_pct,
                is_chase=is_chase
            )
            
            print(f"💰 매수 준비: {ticker}")
            print(f"   주문 방법: {method.value}")
            print(f"   사유: {reason}")
            print(f"   투자금: {investment:,.0f}원")
            print(f"   스프레드: {spread_pct:.2f}%")
            
            # 3. 주문 실행 (재시도 포함)
            order_result = None
            current_price = self.api.get_current_price(ticker)
            
            if method == OrderMethod.MARKET:
                order_result = self._execute_market_buy(ticker, investment)
            
            elif method == OrderMethod.BEST:
                order_result = self._execute_best_buy(ticker, investment)
            
            elif method == OrderMethod.LIMIT:
                # 지정가 오프셋 계산
                offset = self.order_selector.get_limit_price_offset(
                    method, True, current_price, strategy
                )
                limit_price = current_price + offset
                limit_price = self.api.adjust_price_to_tick(ticker, limit_price)
                
                order_result = self._execute_limit_buy_with_fallback(
                    ticker, limit_price, investment
                )
            
            elif method == OrderMethod.IOC:
                limit_price = self.api.adjust_price_to_tick(ticker, current_price)
                order_result = self._execute_ioc_buy(ticker, limit_price, investment)
            
            else:
                # 기본: 시장가
                order_result = self._execute_market_buy(ticker, investment)
            
            # 4. 결과 메타데이터 추가
            if order_result:
                order_result['order_method'] = method.value
                order_result['order_reason'] = reason
                order_result['spread_pct'] = spread_pct
                order_result['is_chase'] = is_chase
                
                print(f"✅ 매수 성공: {ticker}")
                print(f"   UUID: {order_result.get('uuid', 'N/A')}")
            else:
                print(f"❌ 매수 실패: {ticker}")
            
            return order_result
        
        except Exception as e:
            print(f"❌ 매수 실행 오류: {ticker}, {e}")
            return None
    
    def execute_sell(self, ticker: str, volume: float, strategy: str,
                    exit_reason_enum, profit_ratio: float,
                    market_condition: Dict) -> Optional[Dict]:
        """
        스마트 매도 실행
        
        Args:
            ticker: 코인 티커
            volume: 매도 수량
            strategy: 전략 이름
            exit_reason_enum: 청산 사유 (ExitReason enum)
            profit_ratio: 수익률 (%)
            market_condition: 시장 조건
        
        Returns:
            주문 결과 딕셔너리
        """
        try:
            # 1. 스프레드 계산
            spread_pct = self.api.calculate_spread_percentage(ticker)
            
            # 2. 주문 방법 선택
            from src.utils.order_method_selector import OrderMethod
            method, reason = self.order_selector.select_sell_method(
                ticker=ticker,
                strategy=strategy,
                exit_reason=exit_reason_enum,
                spread_pct=spread_pct,
                profit_ratio=profit_ratio,
                market_condition=market_condition
            )
            
            print(f"📊 매도 준비: {ticker}")
            print(f"   주문 방법: {method.value}")
            print(f"   사유: {reason}")
            print(f"   청산 이유: {exit_reason_enum.value}")
            print(f"   수익률: {profit_ratio:+.2f}%")
            print(f"   스프레드: {spread_pct:.2f}%")
            
            # 3. 주문 실행
            order_result = None
            current_price = self.api.get_current_price(ticker)
            
            if method == OrderMethod.MARKET:
                order_result = self._execute_market_sell(ticker, volume)
            
            elif method == OrderMethod.BEST:
                order_result = self._execute_best_sell(ticker, volume)
            
            elif method == OrderMethod.LIMIT:
                offset = self.order_selector.get_limit_price_offset(
                    method, False, current_price, strategy
                )
                limit_price = current_price + offset
                limit_price = self.api.adjust_price_to_tick(ticker, limit_price)
                
                order_result = self._execute_limit_sell_with_fallback(
                    ticker, limit_price, volume
                )
            
            else:
                # 기본: 시장가
                order_result = self._execute_market_sell(ticker, volume)
            
            # 4. 결과 메타데이터 추가
            if order_result:
                order_result['order_method'] = method.value
                order_result['order_reason'] = reason
                order_result['exit_reason'] = exit_reason_enum.value
                order_result['spread_pct'] = spread_pct
                order_result['profit_ratio'] = profit_ratio
                
                print(f"✅ 매도 성공: {ticker}")
                print(f"   UUID: {order_result.get('uuid', 'N/A')}")
            else:
                print(f"❌ 매도 실패: {ticker}")
            
            return order_result
        
        except Exception as e:
            print(f"❌ 매도 실행 오류: {ticker}, {e}")
            return None
    
    # ==================== Private Methods ====================
    
    def _execute_market_buy(self, ticker: str, investment: float) -> Optional[Dict]:
        """시장가 매수 (재시도 포함)"""
        for attempt in range(self.max_retries):
            try:
                result = self.api.buy_market_order(ticker, investment)
                if result:
                    return result
                
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
            except Exception as e:
                print(f"⚠️ 시장가 매수 재시도 {attempt + 1}/{self.max_retries}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
        
        return None
    
    def _execute_best_buy(self, ticker: str, investment: float) -> Optional[Dict]:
        """최유리 매수 (재시도 포함)"""
        for attempt in range(self.max_retries):
            try:
                result = self.api.buy_best_order(ticker, investment)
                if result:
                    return result
                
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
            except Exception as e:
                print(f"⚠️ 최유리 매수 재시도 {attempt + 1}/{self.max_retries}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
        
        # Fallback to market
        if self.enable_fallback:
            print("⚡ Fallback: 최유리 → 시장가")
            return self._execute_market_buy(ticker, investment)
        
        return None
    
    def _execute_limit_buy_with_fallback(self, ticker: str, limit_price: float,
                                        investment: float) -> Optional[Dict]:
        """
        지정가 매수 + Fallback
        
        Process:
        1. 지정가 주문 실행
        2. timeout 초 대기
        3. 미체결 시 취소 → 시장가 전환
        """
        try:
            volume = investment / limit_price
            result = self.api.buy_limit_order(ticker, limit_price, volume)
            
            if not result:
                if self.enable_fallback:
                    print("⚡ Fallback: 지정가 주문 실패 → 시장가")
                    return self._execute_market_buy(ticker, investment)
                return None
            
            uuid = result.get('uuid')
            if not uuid:
                return result
            
            # timeout 대기
            print(f"⏳ 지정가 주문 대기 ({self.limit_order_timeout}초)...")
            time.sleep(self.limit_order_timeout)
            
            # 주문 상태 확인
            order = self.api.get_order(uuid)
            if not order:
                return result
            
            state = order.get('state')
            
            # 완료된 경우
            if state == 'done':
                print("✅ 지정가 주문 체결 완료")
                return result
            
            # 미체결 → Fallback
            if state == 'wait' and self.enable_fallback:
                print("⚡ Fallback: 지정가 미체결 → 주문 취소 후 시장가")
                self.api.cancel_order(uuid)
                time.sleep(0.5)
                return self._execute_market_buy(ticker, investment)
            
            return result
        
        except Exception as e:
            print(f"❌ 지정가 매수 오류: {e}")
            if self.enable_fallback:
                print("⚡ Fallback: 오류 발생 → 시장가")
                return self._execute_market_buy(ticker, investment)
            return None
    
    def _execute_ioc_buy(self, ticker: str, limit_price: float,
                        investment: float) -> Optional[Dict]:
        """IOC 매수"""
        try:
            volume = investment / limit_price
            return self.api.buy_limit_ioc(ticker, limit_price, volume)
        except Exception as e:
            print(f"❌ IOC 매수 오류: {e}")
            if self.enable_fallback:
                return self._execute_market_buy(ticker, investment)
            return None
    
    def _execute_market_sell(self, ticker: str, volume: float) -> Optional[Dict]:
        """시장가 매도 (재시도 포함)"""
        for attempt in range(self.max_retries):
            try:
                result = self.api.sell_market_order(ticker, volume)
                if result:
                    return result
                
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
            except Exception as e:
                print(f"⚠️ 시장가 매도 재시도 {attempt + 1}/{self.max_retries}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
        
        return None
    
    def _execute_best_sell(self, ticker: str, volume: float) -> Optional[Dict]:
        """최유리 매도 (재시도 포함)"""
        for attempt in range(self.max_retries):
            try:
                result = self.api.sell_best_order(ticker, volume)
                if result:
                    return result
                
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
            except Exception as e:
                print(f"⚠️ 최유리 매도 재시도 {attempt + 1}/{self.max_retries}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
        
        # Fallback to market
        if self.enable_fallback:
            print("⚡ Fallback: 최유리 → 시장가")
            return self._execute_market_sell(ticker, volume)
        
        return None
    
    def _execute_limit_sell_with_fallback(self, ticker: str, limit_price: float,
                                         volume: float) -> Optional[Dict]:
        """지정가 매도 + Fallback"""
        try:
            result = self.api.sell_limit_order(ticker, limit_price, volume)
            
            if not result:
                if self.enable_fallback:
                    print("⚡ Fallback: 지정가 주문 실패 → 시장가")
                    return self._execute_market_sell(ticker, volume)
                return None
            
            uuid = result.get('uuid')
            if not uuid:
                return result
            
            # timeout 대기
            print(f"⏳ 지정가 주문 대기 ({self.limit_order_timeout}초)...")
            time.sleep(self.limit_order_timeout)
            
            # 주문 상태 확인
            order = self.api.get_order(uuid)
            if not order:
                return result
            
            state = order.get('state')
            
            if state == 'done':
                print("✅ 지정가 주문 체결 완료")
                return result
            
            if state == 'wait' and self.enable_fallback:
                print("⚡ Fallback: 지정가 미체결 → 주문 취소 후 시장가")
                self.api.cancel_order(uuid)
                time.sleep(0.5)
                return self._execute_market_sell(ticker, volume)
            
            return result
        
        except Exception as e:
            print(f"❌ 지정가 매도 오류: {e}")
            if self.enable_fallback:
                print("⚡ Fallback: 오류 발생 → 시장가")
                return self._execute_market_sell(ticker, volume)
            return None
