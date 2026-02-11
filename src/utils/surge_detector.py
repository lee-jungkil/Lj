"""
급등/급락 감지 엔진
실시간으로 코인 가격 변동을 모니터링하여 초단타 기회 포착

감지 조건:
- 1~3분 내 2% 이상 가격 변동
- 거래량 3배 이상 증가
- RSI 극단값
"""

import time
from typing import Dict, List, Optional
from datetime import datetime
import pandas as pd


class SurgeDetector:
    """급등/급락 감지기"""
    
    def __init__(self, upbit_api, logger):
        """
        초기화
        
        Args:
            upbit_api: UpbitAPI 인스턴스
            logger: TradingLogger 인스턴스
        """
        self.api = upbit_api
        self.logger = logger
        
        # 감지 설정 (완화)
        self.min_surge_ratio = 0.015  # 1.5% 이상 변동 (완화)
        self.min_volume_spike = 2.0  # 거래량 2배 이상 (완화)
        self.scan_interval = 30  # 30초마다 스캔
        
        # 감지 기록 (중복 방지)
        self.recent_detections = {}  # {ticker: timestamp}
        self.detection_cooldown = 180  # 3분 쿨다운 (완화)
    
    def scan_market(self, tickers: List[str]) -> List[Dict]:
        """
        시장 전체 스캔하여 급등/급락 코인 탐지
        
        Args:
            tickers: 스캔할 코인 목록
        
        Returns:
            감지된 코인 목록 [{ticker, type, price_change, volume_ratio, ...}]
        """
        detected_coins = []
        
        for ticker in tickers:
            try:
                # 쿨다운 확인
                if self._is_in_cooldown(ticker):
                    continue
                
                # 급등/급락 확인
                surge_info = self._check_surge(ticker)
                
                if surge_info:
                    detected_coins.append(surge_info)
                    self.recent_detections[ticker] = time.time()
                    
                    self.logger.log_info(
                        f"🔥 급등/급락 감지: {surge_info['ticker']} "
                        f"({surge_info['type']}) "
                        f"가격변동: {surge_info['price_change']:+.2f}%, "
                        f"거래량: {surge_info['volume_ratio']:.1f}x"
                    )
                
                time.sleep(0.5)  # API 호출 제한 고려
                
            except Exception as e:
                self.logger.log_error("SURGE_DETECTION", f"{ticker} 감지 실패", e)
        
        return detected_coins
    
    def scan_market_batch(self, tickers: List[str], prices_dict: Dict[str, float]) -> List[Dict]:
        """
        ⚡ 배치 API 최적화: 이미 조회된 가격으로 급등/급락 탐지
        
        Args:
            tickers: 스캔할 코인 목록
            prices_dict: {ticker: price} 딕셔너리 (이미 배치 조회됨)
        
        Returns:
            감지된 코인 목록 [{ticker, type, price_change, volume_ratio, ...}]
        """
        detected_coins = []
        
        for ticker in tickers:
            try:
                # 쿨다운 확인
                if self._is_in_cooldown(ticker):
                    continue
                
                # 현재가가 없으면 스킵
                if ticker not in prices_dict or prices_dict[ticker] is None:
                    continue
                
                # 급등/급락 확인 (현재가 전달)
                surge_info = self._check_surge_with_price(ticker, prices_dict[ticker])
                
                if surge_info:
                    detected_coins.append(surge_info)
                    self.recent_detections[ticker] = time.time()
                    
                    self.logger.log_info(
                        f"🔥 급등/급락 감지: {surge_info['ticker']} "
                        f"({surge_info['type']}) "
                        f"가격변동: {surge_info['price_change']:+.2f}%, "
                        f"거래량: {surge_info['volume_ratio']:.1f}x"
                    )
                
                time.sleep(0.1)  # 배치 모드이므로 대기 시간 단축
                
            except Exception as e:
                self.logger.log_error("SURGE_DETECTION", f"{ticker} 감지 실패", e)
        
        return detected_coins
    
    def _check_surge_with_price(self, ticker: str, current_price: float) -> Optional[Dict]:
        """
        개별 코인의 급등/급락 확인 (현재가 사용)
        
        Args:
            ticker: 코인 티커
            current_price: 이미 조회된 현재가
        
        Returns:
            급등/급락 정보 또는 None
        """
        # 1분봉 데이터 조회 (최근 10개)
        df = self.api.get_ohlcv(ticker, interval="minute1", count=10)
        if df is None or len(df) < 3:
            return None
        
        # 1분 가격 변동 (배치 조회된 현재가 사용)
        price_1min = current_price
        price_1min_ago = df['close'].iloc[-2]
        change_1min = (price_1min - price_1min_ago) / price_1min_ago
        
        # 3분 가격 변동
        price_3min_ago = df['close'].iloc[-4] if len(df) >= 4 else price_1min_ago
        change_3min = (price_1min - price_3min_ago) / price_3min_ago
        
        # 거래량 급증 확인 (최근 1분 vs 평균)
        volume_recent = df['volume'].iloc[-1]
        volume_avg = df['volume'].iloc[:-1].mean()
        volume_ratio = volume_recent / volume_avg if volume_avg > 0 else 0
        
        # RSI 계산 (짧은 기간)
        rsi = self._calculate_quick_rsi(df['close'], period=6)
        
        # 감지 조건 확인
        is_surge = False
        surge_type = None
        
        # 급등 감지
        if change_1min >= self.min_surge_ratio and volume_ratio >= self.min_volume_spike:
            is_surge = True
            surge_type = "급등"
        
        # 급락 감지
        elif change_1min <= -self.min_surge_ratio and volume_ratio >= self.min_volume_spike:
            is_surge = True
            surge_type = "급락"
        
        # 3분 급등 (완만한 상승)
        elif change_3min >= self.min_surge_ratio * 1.5 and volume_ratio >= self.min_volume_spike * 0.7:
            is_surge = True
            surge_type = "완만급등"
        
        if is_surge:
            return {
                'ticker': ticker,
                'type': surge_type,
                'price_change': change_1min * 100,
                'price_change_3min': change_3min * 100,
                'volume_ratio': volume_ratio,
                'rsi': rsi,
                'current_price': price_1min,
                'timestamp': datetime.now()
            }
        
        return None
    
    def _check_surge(self, ticker: str) -> Optional[Dict]:
        """
        개별 코인의 급등/급락 확인
        
        Args:
            ticker: 코인 티커
        
        Returns:
            급등/급락 정보 또는 None
        """
        # 1분봉 데이터 조회 (최근 10개)
        df = self.api.get_ohlcv(ticker, interval="minute1", count=10)
        if df is None or len(df) < 3:
            return None
        
        # 1분 가격 변동
        price_1min = df['close'].iloc[-1]
        price_1min_ago = df['close'].iloc[-2]
        change_1min = (price_1min - price_1min_ago) / price_1min_ago
        
        # 3분 가격 변동
        price_3min_ago = df['close'].iloc[-4] if len(df) >= 4 else price_1min_ago
        change_3min = (price_1min - price_3min_ago) / price_3min_ago
        
        # 거래량 급증 확인 (최근 1분 vs 평균)
        volume_recent = df['volume'].iloc[-1]
        volume_avg = df['volume'].iloc[:-1].mean()
        volume_ratio = volume_recent / volume_avg if volume_avg > 0 else 0
        
        # RSI 계산 (짧은 기간)
        rsi = self._calculate_quick_rsi(df['close'], period=6)
        
        # 감지 조건 확인
        is_surge = False
        surge_type = None
        
        # 급등 감지
        if change_1min >= self.min_surge_ratio and volume_ratio >= self.min_volume_spike:
            is_surge = True
            surge_type = "급등"
        
        # 급락 감지
        elif change_1min <= -self.min_surge_ratio and volume_ratio >= self.min_volume_spike:
            is_surge = True
            surge_type = "급락"
        
        # 3분 급등 (완만한 상승)
        elif change_3min >= self.min_surge_ratio * 1.5 and volume_ratio >= self.min_volume_spike * 0.7:
            is_surge = True
            surge_type = "완만급등"
        
        if is_surge:
            return {
                'ticker': ticker,
                'type': surge_type,
                'price_change': change_1min * 100,
                'price_change_3min': change_3min * 100,
                'volume_ratio': volume_ratio,
                'rsi': rsi,
                'current_price': price_1min,
                'timestamp': datetime.now()
            }
        
        return None
    
    def _is_in_cooldown(self, ticker: str) -> bool:
        """쿨다운 확인"""
        if ticker not in self.recent_detections:
            return False
        
        elapsed = time.time() - self.recent_detections[ticker]
        return elapsed < self.detection_cooldown
    
    def _calculate_quick_rsi(self, prices: pd.Series, period: int = 6) -> float:
        """빠른 RSI 계산"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi.iloc[-1] if not rsi.empty else 50.0
