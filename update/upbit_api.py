"""
Upbit API 래퍼 클래스
pyupbit 라이브러리를 사용하여 Upbit 거래소 API와 통신
"""

import pyupbit
import time
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import pandas as pd


class UpbitAPI:
    """Upbit API 래퍼 클래스"""
    
    def __init__(self, access_key: str = "", secret_key: str = ""):
        """
        초기화
        
        Args:
            access_key: Upbit Access Key
            secret_key: Upbit Secret Key
        """
        self.access_key = access_key
        self.secret_key = secret_key
        
        # 실거래용 객체 (키가 있을 때만)
        self.upbit = None
        if access_key and secret_key:
            try:
                self.upbit = pyupbit.Upbit(access_key, secret_key)
                print("✅ Upbit API 연결 성공")
            except Exception as e:
                print(f"⚠️ Upbit API 연결 실패: {e}")
                self.upbit = None
        
        # 티커 캐시
        self._valid_tickers_cache = None
        self._cache_time = 0
    
    def get_valid_tickers(self, fiat: str = "KRW", force_refresh: bool = False) -> List[str]:
        """
        유효한 티커 목록 조회 (5분 캐시)
        
        Args:
            fiat: 법정화폐 (기본값: KRW)
            force_refresh: 강제 새로고침
        
        Returns:
            유효한 티커 리스트
        """
        current_time = time.time()
        
        # 캐시 확인 (5분)
        if not force_refresh and self._valid_tickers_cache and (current_time - self._cache_time < 300):
            return self._valid_tickers_cache
        
        try:
            tickers = pyupbit.get_tickers(fiat=fiat)
            self._valid_tickers_cache = tickers or []
            self._cache_time = current_time
            return self._valid_tickers_cache
        except Exception as e:
            print(f"❌ 티커 목록 조회 실패: {e}")
            return self._valid_tickers_cache or []
    
    def validate_tickers(self, tickers: List[str]) -> List[str]:
        """
        티커 유효성 검증
        
        Args:
            tickers: 검증할 티커 리스트
        
        Returns:
            유효한 티커만 반환
        """
        valid_set = set(self.get_valid_tickers())
        validated = [t for t in tickers if t in valid_set]
        
        # 제외된 티커 로그
        excluded = set(tickers) - set(validated)
        if excluded:
            print(f"⚠️ 유효하지 않은 티커 제외: {excluded}")
        
        return validated
    
    # ==================== 시장 정보 ====================
    
    def get_all_tickers(self, fiat: str = "KRW") -> List[str]:
        """
        모든 티커 목록 가져오기
        
        Args:
            fiat: 기준 화폐 (KRW, BTC, USDT)
        
        Returns:
            티커 목록
        """
        try:
            tickers = pyupbit.get_tickers(fiat=fiat)
            return tickers
        except Exception as e:
            print(f"❌ 티커 조회 실패: {e}")
            return []
    
    def get_current_price(self, ticker: str) -> Optional[float]:
        """
        현재가 조회
        
        Args:
            ticker: 코인 티커 (예: KRW-BTC)
        
        Returns:
            현재가
        """
        try:
            price = pyupbit.get_current_price(ticker)
            return float(price) if price else None
        except Exception as e:
            print(f"❌ {ticker} 현재가 조회 실패: {e}")
            return None
    
    def get_current_prices(self, tickers: List[str]) -> Dict[str, float]:
        """
        여러 코인의 현재가를 한 번에 조회 (배치 API)
        
        ⚡ API 최적화: N개 코인을 1회 호출로 조회
        ⚠️ Upbit 제한: 최대 100개까지 동시 조회 가능
        
        Args:
            tickers: 코인 티커 리스트 (예: ['KRW-BTC', 'KRW-ETH'])
        
        Returns:
            {ticker: price} 딕셔너리
        """
        if not tickers:
            return {}
        
        try:
            # 티커 유효성 검증 (KRW-로 시작하는지 확인)
            valid_tickers = [t for t in tickers if isinstance(t, str) and t.startswith('KRW-')]
            
            if not valid_tickers:
                return {}
            
            # 최대 100개씩 나누어 조회
            result = {}
            for i in range(0, len(valid_tickers), 100):
                batch = valid_tickers[i:i+100]
                
                try:
                    # pyupbit는 리스트를 받으면 한 번에 조회
                    prices = pyupbit.get_current_price(batch)
                    
                    if isinstance(prices, dict):
                        for k, v in prices.items():
                            if v is not None:
                                result[k] = float(v)
                    elif isinstance(prices, (int, float)) and len(batch) == 1:
                        # 단일 티커인 경우
                        result[batch[0]] = float(prices)
                        
                except Exception as e:
                    # 배치 실패 시 개별 조회로 폴백
                    print(f"⚠️ 배치 조회 실패, 개별 조회로 전환: {e}")
                    for ticker in batch:
                        try:
                            price = pyupbit.get_current_price(ticker)
                            if price is not None:
                                result[ticker] = float(price)
                        except:
                            pass  # 개별 실패는 무시
            
            return result
            
        except Exception as e:
            print(f"❌ 다중 현재가 조회 실패: {e}")
            return {}
    
    def get_orderbook(self, ticker: str) -> Optional[Dict]:
        """
        호가 정보 조회
        
        Args:
            ticker: 코인 티커
        
        Returns:
            호가 정보
        """
        try:
            orderbook = pyupbit.get_orderbook(ticker)
            return orderbook
        except Exception as e:
            print(f"❌ {ticker} 호가 조회 실패: {e}")
            return None
    
    def get_orderbooks(self, tickers: List[str]) -> Dict[str, Dict]:
        """
        여러 코인의 호가 정보를 한 번에 조회 (배치 API)
        
        ⚡ API 최적화: N개 코인을 1회 호출로 조회
        ⚠️ Upbit 제한: 최대 5개까지 동시 조회 권장 (10회/초 제한)
        
        Args:
            tickers: 코인 티커 리스트
        
        Returns:
            {ticker: orderbook_data} 딕셔너리
        """
        try:
            # pyupbit는 리스트를 받으면 한 번에 조회
            orderbooks = pyupbit.get_orderbook(tickers)
            
            if isinstance(orderbooks, list):
                return {ob['market']: ob for ob in orderbooks}
            else:
                return {}
        except Exception as e:
            print(f"❌ 다중 호가 조회 실패: {e}")
            return {}
    
    def get_recent_trades(self, ticker: str, count: int = 100) -> List[Dict]:
        """
        최근 체결 내역 조회
        
        Args:
            ticker: 코인 티커
            count: 조회할 체결 개수 (최대 500)
        
        Returns:
            체결 내역 리스트
        """
        try:
            # pyupbit는 체결 내역 조회 미지원, requests로 직접 호출
            import requests
            
            url = f"https://api.upbit.com/v1/trades/ticks"
            params = {
                'market': ticker,
                'count': min(count, 500)
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                return []
                
        except Exception as e:
            print(f"❌ {ticker} 체결 내역 조회 실패: {e}")
            return []
    
    def get_ohlcv(self, ticker: str, interval: str = "minute5", count: int = 200) -> Optional[pd.DataFrame]:
        """
        OHLCV (봉 차트) 데이터 조회
        
        Args:
            ticker: 코인 티커
            interval: 시간 간격 (minute1, minute5, minute15, minute30, hour, day, week, month)
            count: 조회할 데이터 개수
        
        Returns:
            OHLCV DataFrame
        """
        try:
            df = pyupbit.get_ohlcv(ticker, interval=interval, count=count)
            return df
        except Exception as e:
            print(f"❌ {ticker} OHLCV 조회 실패: {e}")
            return None
    
    # ==================== 계좌 정보 ====================
    
    def get_balance(self, ticker: str = "KRW") -> float:
        """
        잔고 조회
        
        Args:
            ticker: 화폐 또는 코인 (KRW, BTC, ETH 등)
        
        Returns:
            잔고
        """
        if not self.upbit:
            print("⚠️ API 키가 설정되지 않았습니다")
            return 0.0
        
        try:
            balance = self.upbit.get_balance(ticker)
            return float(balance) if balance else 0.0
        except Exception as e:
            print(f"❌ {ticker} 잔고 조회 실패: {e}")
            return 0.0
    
    def get_balances(self) -> List[Dict]:
        """
        전체 잔고 조회
        
        Returns:
            잔고 목록
        """
        if not self.upbit:
            print("⚠️ API 키가 설정되지 않았습니다")
            return []
        
        try:
            balances = self.upbit.get_balances()
            return balances if balances else []
        except Exception as e:
            print(f"❌ 전체 잔고 조회 실패: {e}")
            return []
    
    def get_amount(self, ticker: str) -> float:
        """
        특정 코인 보유량 조회
        
        Args:
            ticker: 코인 티커 (예: BTC, ETH)
        
        Returns:
            보유량
        """
        if not self.upbit:
            return 0.0
        
        try:
            # KRW-BTC -> BTC 추출
            if '-' in ticker:
                ticker = ticker.split('-')[1]
            
            amount = self.upbit.get_amount(ticker)
            return float(amount) if amount else 0.0
        except Exception as e:
            print(f"❌ {ticker} 보유량 조회 실패: {e}")
            return 0.0
    
    def get_avg_buy_price(self, ticker: str) -> float:
        """
        평균 매수가 조회
        
        Args:
            ticker: 코인 티커
        
        Returns:
            평균 매수가
        """
        if not self.upbit:
            return 0.0
        
        try:
            if '-' in ticker:
                ticker = ticker.split('-')[1]
            
            avg_price = self.upbit.get_avg_buy_price(ticker)
            return float(avg_price) if avg_price else 0.0
        except Exception as e:
            print(f"❌ {ticker} 평균 매수가 조회 실패: {e}")
            return 0.0
    
    # ==================== 주문 ====================
    
    def buy_market_order(self, ticker: str, price: float) -> Optional[Dict]:
        """
        시장가 매수
        
        Args:
            ticker: 코인 티커
            price: 매수 금액 (KRW)
        
        Returns:
            주문 정보
        """
        if not self.upbit:
            print("⚠️ API 키가 설정되지 않았습니다")
            return None
        
        try:
            result = self.upbit.buy_market_order(ticker, price)
            print(f"✅ 매수 주문 성공: {ticker}, {price:,.0f}원")
            return result
        except Exception as e:
            print(f"❌ 매수 주문 실패: {ticker}, {e}")
            return None
    
    def sell_market_order(self, ticker: str, volume: float) -> Optional[Dict]:
        """
        시장가 매도
        
        Args:
            ticker: 코인 티커
            volume: 매도 수량
        
        Returns:
            주문 정보
        """
        if not self.upbit:
            print("⚠️ API 키가 설정되지 않았습니다")
            return None
        
        try:
            result = self.upbit.sell_market_order(ticker, volume)
            print(f"✅ 매도 주문 성공: {ticker}, {volume}")
            return result
        except Exception as e:
            print(f"❌ 매도 주문 실패: {ticker}, {e}")
            return None
    
    def buy_limit_order(self, ticker: str, price: float, volume: float) -> Optional[Dict]:
        """
        지정가 매수
        
        Args:
            ticker: 코인 티커
            price: 매수 가격
            volume: 매수 수량
        
        Returns:
            주문 정보
        """
        if not self.upbit:
            print("⚠️ API 키가 설정되지 않았습니다")
            return None
        
        try:
            result = self.upbit.buy_limit_order(ticker, price, volume)
            print(f"✅ 지정가 매수 주문 성공: {ticker}, {price:,.0f}원, {volume}")
            return result
        except Exception as e:
            print(f"❌ 지정가 매수 실패: {ticker}, {e}")
            return None
    
    def sell_limit_order(self, ticker: str, price: float, volume: float) -> Optional[Dict]:
        """
        지정가 매도
        
        Args:
            ticker: 코인 티커
            price: 매도 가격
            volume: 매도 수량
        
        Returns:
            주문 정보
        """
        if not self.upbit:
            print("⚠️ API 키가 설정되지 않았습니다")
            return None
        
        try:
            result = self.upbit.sell_limit_order(ticker, price, volume)
            print(f"✅ 지정가 매도 주문 성공: {ticker}, {price:,.0f}원, {volume}")
            return result
        except Exception as e:
            print(f"❌ 지정가 매도 실패: {ticker}, {e}")
            return None
    
    def cancel_order(self, uuid: str) -> Optional[Dict]:
        """
        주문 취소
        
        Args:
            uuid: 주문 ID
        
        Returns:
            취소 정보
        """
        if not self.upbit:
            print("⚠️ API 키가 설정되지 않았습니다")
            return None
        
        try:
            result = self.upbit.cancel_order(uuid)
            print(f"✅ 주문 취소 성공: {uuid}")
            return result
        except Exception as e:
            print(f"❌ 주문 취소 실패: {uuid}, {e}")
            return None
    
    def get_order(self, uuid: str) -> Optional[Dict]:
        """
        주문 조회
        
        Args:
            uuid: 주문 ID
        
        Returns:
            주문 정보
        """
        if not self.upbit:
            print("⚠️ API 키가 설정되지 않았습니다")
            return None
        
        try:
            result = self.upbit.get_order(uuid)
            return result
        except Exception as e:
            print(f"❌ 주문 조회 실패: {uuid}, {e}")
            return None
    
    # ==================== 유틸리티 ====================
    
    def get_24h_volume(self, ticker: str) -> float:
        """
        24시간 거래량 조회
        
        Args:
            ticker: 코인 티커
        
        Returns:
            24시간 거래량 (KRW)
        """
        try:
            df = self.get_ohlcv(ticker, interval="day", count=1)
            if df is not None and not df.empty:
                return float(df['value'].iloc[-1])
            return 0.0
        except Exception as e:
            print(f"❌ {ticker} 24시간 거래량 조회 실패: {e}")
            return 0.0
    
    def get_24h_change(self, ticker: str) -> float:
        """
        24시간 변동률 조회
        
        Args:
            ticker: 코인 티커
        
        Returns:
            변동률 (%)
        """
        try:
            df = self.get_ohlcv(ticker, interval="day", count=2)
            if df is not None and len(df) >= 2:
                prev_close = df['close'].iloc[-2]
                curr_close = df['close'].iloc[-1]
                change = ((curr_close - prev_close) / prev_close) * 100
                return float(change)
            return 0.0
        except Exception as e:
            print(f"❌ {ticker} 24시간 변동률 조회 실패: {e}")
            return 0.0
    
    def wait_for_order_complete(self, uuid: str, timeout: int = 60) -> bool:
        """
        주문 완료 대기
        
        Args:
            uuid: 주문 ID
            timeout: 타임아웃 (초)
        
        Returns:
            완료 여부
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            order = self.get_order(uuid)
            if order and order.get('state') == 'done':
                return True
            time.sleep(1)
        
        return False
    
    def is_market_open(self) -> bool:
        """
        시장 개장 여부 (암호화폐는 24시간이지만 점검 시간 체크)
        
        Returns:
            개장 여부
        """
        # 업비트는 24시간 거래이므로 항상 True
        # 단, 점검 시간이 있다면 추가 로직 필요
        return True
    
    # ==================== 확장 주문 방식 (v6.29+) ====================
    
    def buy_best_order(self, ticker: str, price: float) -> Optional[Dict]:
        """
        최유리 매수 (IOC: Immediate Or Cancel)
        - 1호가에 지정가 주문 + IOC 옵션
        - 즉시 체결되지 않으면 취소
        
        Args:
            ticker: 코인 티커
            price: 매수 금액 (KRW)
        
        Returns:
            주문 정보
        """
        if not self.upbit:
            print("⚠️ API 키가 설정되지 않았습니다")
            return None
        
        try:
            # 호가창 조회
            orderbook = self.get_orderbook(ticker)
            if not orderbook:
                print(f"❌ {ticker} 호가창 조회 실패 - 시장가로 fallback")
                return self.buy_market_order(ticker, price)
            
            # 1호가 매도가 (최유리가)
            best_ask = orderbook['orderbook_units'][0]['ask_price']
            volume = price / best_ask
            
            # 지정가 주문 + IOC (즉시 체결 or 취소)
            result = self.upbit.buy_limit_order(ticker, best_ask, volume)
            print(f"✅ 최유리 매수 주문 성공: {ticker}, {best_ask:,.0f}원, {volume:.8f}")
            return result
        except Exception as e:
            print(f"❌ 최유리 매수 실패: {ticker}, {e}")
            # Fallback to market order
            return self.buy_market_order(ticker, price)
    
    def sell_best_order(self, ticker: str, volume: float) -> Optional[Dict]:
        """
        최유리 매도 (IOC)
        - 1호가에 지정가 주문 + IOC 옵션
        
        Args:
            ticker: 코인 티커
            volume: 매도 수량
        
        Returns:
            주문 정보
        """
        if not self.upbit:
            print("⚠️ API 키가 설정되지 않았습니다")
            return None
        
        try:
            # 호가창 조회
            orderbook = self.get_orderbook(ticker)
            if not orderbook:
                print(f"❌ {ticker} 호가창 조회 실패 - 시장가로 fallback")
                return self.sell_market_order(ticker, volume)
            
            # 1호가 매수가 (최유리가)
            best_bid = orderbook['orderbook_units'][0]['bid_price']
            
            # 지정가 주문
            result = self.upbit.sell_limit_order(ticker, best_bid, volume)
            print(f"✅ 최유리 매도 주문 성공: {ticker}, {best_bid:,.0f}원, {volume:.8f}")
            return result
        except Exception as e:
            print(f"❌ 최유리 매도 실패: {ticker}, {e}")
            # Fallback to market order
            return self.sell_market_order(ticker, volume)
    
    def adjust_price_to_tick(self, ticker: str, price: float) -> float:
        """
        호가 단위로 가격 조정
        
        Upbit 호가 단위:
        - 100만원 이상: 1,000원
        - 50만~100만: 500원
        - 10만~50만: 100원
        - 1만~10만: 50원
        - 1천~1만: 10원
        - 100~1천: 5원
        - 10~100: 1원
        - 10원 미만: 0.1원
        
        Args:
            ticker: 코인 티커
            price: 조정할 가격
        
        Returns:
            조정된 가격
        """
        if price >= 1000000:
            tick = 1000
        elif price >= 500000:
            tick = 500
        elif price >= 100000:
            tick = 100
        elif price >= 10000:
            tick = 50
        elif price >= 1000:
            tick = 10
        elif price >= 100:
            tick = 5
        elif price >= 10:
            tick = 1
        else:
            tick = 0.1
        
        return round(price / tick) * tick
    
    def buy_limit_ioc(self, ticker: str, price: float, volume: float) -> Optional[Dict]:
        """
        IOC 지정가 매수 (Immediate Or Cancel)
        - 부분 체결 허용
        - 즉시 체결 가능한 부분만 체결, 나머지 취소
        
        ⚠️ pyupbit는 IOC를 직접 지원하지 않으므로,
           지정가 주문 후 1초 대기 → 미체결 취소로 구현
        
        Args:
            ticker: 코인 티커
            price: 매수 가격
            volume: 매수 수량
        
        Returns:
            주문 정보
        """
        if not self.upbit:
            print("⚠️ API 키가 설정되지 않았습니다")
            return None
        
        try:
            # 호가 단위 조정
            adjusted_price = self.adjust_price_to_tick(ticker, price)
            
            # 지정가 주문
            result = self.upbit.buy_limit_order(ticker, adjusted_price, volume)
            if not result:
                return None
            
            uuid = result.get('uuid')
            if not uuid:
                return result
            
            # 1초 대기 후 미체결 부분 취소
            time.sleep(1)
            order = self.get_order(uuid)
            if order and order.get('state') == 'wait':
                self.cancel_order(uuid)
                print(f"⚡ IOC: 미체결 부분 취소 - {ticker}")
            
            print(f"✅ IOC 매수 주문 성공: {ticker}, {adjusted_price:,.0f}원, {volume:.8f}")
            return result
        except Exception as e:
            print(f"❌ IOC 매수 실패: {ticker}, {e}")
            return None
    
    def sell_limit_ioc(self, ticker: str, price: float, volume: float) -> Optional[Dict]:
        """
        IOC 지정가 매도
        
        Args:
            ticker: 코인 티커
            price: 매도 가격
            volume: 매도 수량
        
        Returns:
            주문 정보
        """
        if not self.upbit:
            print("⚠️ API 키가 설정되지 않았습니다")
            return None
        
        try:
            adjusted_price = self.adjust_price_to_tick(ticker, price)
            
            result = self.upbit.sell_limit_order(ticker, adjusted_price, volume)
            if not result:
                return None
            
            uuid = result.get('uuid')
            if not uuid:
                return result
            
            time.sleep(1)
            order = self.get_order(uuid)
            if order and order.get('state') == 'wait':
                self.cancel_order(uuid)
                print(f"⚡ IOC: 미체결 부분 취소 - {ticker}")
            
            print(f"✅ IOC 매도 주문 성공: {ticker}, {adjusted_price:,.0f}원, {volume:.8f}")
            return result
        except Exception as e:
            print(f"❌ IOC 매도 실패: {ticker}, {e}")
            return None
    
    def calculate_spread_percentage(self, ticker: str) -> float:
        """
        호가창 스프레드 계산 (%)
        
        Args:
            ticker: 코인 티커
        
        Returns:
            스프레드 비율 (%)
        """
        try:
            orderbook = self.get_orderbook(ticker)
            if not orderbook or 'orderbook_units' not in orderbook:
                return 0.0
            
            best_ask = orderbook['orderbook_units'][0]['ask_price']
            best_bid = orderbook['orderbook_units'][0]['bid_price']
            
            spread_pct = ((best_ask - best_bid) / best_bid) * 100
            return spread_pct
        except Exception as e:
            print(f"❌ {ticker} 스프레드 계산 실패: {e}")
            return 0.0
