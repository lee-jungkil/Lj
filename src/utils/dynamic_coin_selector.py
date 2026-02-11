"""
동적 코인 선정 시스템
5분마다 거래량/RSI/변동성 기준으로 최적 코인 자동 선정
"""
import pyupbit
import pandas as pd
from typing import List, Dict, Tuple
from datetime import datetime, timedelta
import time
from colorlog import ColoredFormatter
import logging


class DynamicCoinSelector:
    """동적 코인 선정 시스템"""
    
    def __init__(self, coin_count: int = 35):
        """
        Args:
            coin_count: 고정 코인 개수 (기본 35개)
        """
        self.coin_count = coin_count
        self.last_update = 0
        self.update_interval = 180  # 3분 = 180초
        self.current_coins = []
        self.logger = self._setup_logger()
        
    def _setup_logger(self):
        """로거 설정"""
        logger = logging.getLogger("DynamicCoinSelector")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = ColoredFormatter(
                "%(log_color)s[%(asctime)s] [COIN] %(message)s",
                datefmt="%H:%M:%S",
                log_colors={
                    'DEBUG': 'cyan',
                    'INFO': 'blue',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'red,bg_white',
                }
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    
    def should_update(self) -> bool:
        """업데이트 필요 여부 확인 (3분마다)"""
        current_time = time.time()
        if current_time - self.last_update >= self.update_interval:
            return True
        return False
    
    def get_all_krw_tickers(self) -> List[str]:
        """모든 KRW 마켓 티커 조회"""
        try:
            all_tickers = pyupbit.get_tickers(fiat="KRW")
            self.logger.info(f"📊 전체 KRW 마켓: {len(all_tickers)}개")
            return all_tickers
        except Exception as e:
            self.logger.error(f"❌ 티커 조회 실패: {e}")
            return []
    
    def get_volume_ranking(self, tickers: List[str], top_n: int = 50) -> List[Tuple[str, float]]:
        """거래량 순위 Top N"""
        try:
            # 24시간 거래대금 조회
            volumes = {}
            
            # 배치로 현재가 조회 (100개씩)
            for i in range(0, len(tickers), 100):
                batch = tickers[i:i+100]
                try:
                    prices_data = pyupbit.get_current_price(batch)
                    if isinstance(prices_data, dict):
                        for ticker, price in prices_data.items():
                            if price is not None:
                                # OHLCV에서 거래대금 확인
                                try:
                                    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=24)
                                    if df is not None and not df.empty:
                                        volume_krw = (df['close'] * df['volume']).sum()
                                        volumes[ticker] = volume_krw
                                except:
                                    pass
                    time.sleep(0.1)  # API 한도 방지
                except Exception as e:
                    self.logger.debug(f"배치 조회 실패: {e}")
                    continue
            
            # 거래량 정렬
            sorted_volumes = sorted(volumes.items(), key=lambda x: x[1], reverse=True)
            
            self.logger.info(f"📈 거래량 Top {top_n} 추출 완료")
            return sorted_volumes[:top_n]
            
        except Exception as e:
            self.logger.error(f"❌ 거래량 순위 조회 실패: {e}")
            return []
    
    def calculate_rsi(self, df: pd.DataFrame, period: int = 14) -> float:
        """RSI 계산"""
        try:
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            return rsi.iloc[-1] if not rsi.empty else 50.0
        except:
            return 50.0
    
    def calculate_volatility(self, df: pd.DataFrame) -> float:
        """변동성 계산 (표준편차)"""
        try:
            returns = df['close'].pct_change()
            volatility = returns.std() * 100
            return volatility
        except:
            return 0.0
    
    def get_rsi_ranking(self, tickers: List[str]) -> List[Tuple[str, float]]:
        """RSI 기준 순위 (과매도/과매수 구간)"""
        rsi_scores = {}
        
        for ticker in tickers:
            try:
                df = pyupbit.get_ohlcv(ticker, interval="minute5", count=100)
                if df is not None and not df.empty:
                    rsi = self.calculate_rsi(df)
                    
                    # RSI 스코어 계산 (30 이하 또는 70 이상이 높은 점수)
                    if rsi <= 30:
                        score = 100 - rsi  # 과매도 → 매수 기회
                    elif rsi >= 70:
                        score = rsi  # 과매수 → 단타 기회
                    else:
                        score = 50  # 중립
                    
                    rsi_scores[ticker] = score
                
                time.sleep(0.05)  # API 한도 방지
            except:
                continue
        
        # RSI 스코어 정렬
        sorted_rsi = sorted(rsi_scores.items(), key=lambda x: x[1], reverse=True)
        
        self.logger.info(f"📊 RSI 분석 완료: {len(sorted_rsi)}개")
        return sorted_rsi
    
    def get_volatility_ranking(self, tickers: List[str]) -> List[Tuple[str, float]]:
        """변동성 기준 순위"""
        volatility_scores = {}
        
        for ticker in tickers:
            try:
                df = pyupbit.get_ohlcv(ticker, interval="minute5", count=100)
                if df is not None and not df.empty:
                    volatility = self.calculate_volatility(df)
                    volatility_scores[ticker] = volatility
                
                time.sleep(0.05)
            except:
                continue
        
        # 변동성 정렬
        sorted_volatility = sorted(volatility_scores.items(), key=lambda x: x[1], reverse=True)
        
        self.logger.info(f"🔥 변동성 분석 완료: {len(sorted_volatility)}개")
        return sorted_volatility
    
    def select_coins_multi_criteria(self) -> List[str]:
        """복합 기준 코인 선정"""
        self.logger.info(f"🎯 동적 코인 선정 시작 (목표: {self.coin_count}개)")
        
        # 1단계: 모든 KRW 티커 조회
        all_tickers = self.get_all_krw_tickers()
        if not all_tickers:
            return self._get_fallback_coins()
        
        # 2단계: 거래량 Top 50 추출
        volume_ranking = self.get_volume_ranking(all_tickers, top_n=50)
        if not volume_ranking:
            return self._get_fallback_coins()
        
        top_50_tickers = [ticker for ticker, _ in volume_ranking]
        
        # 3단계: Top 50에서 RSI 분석
        rsi_ranking = self.get_rsi_ranking(top_50_tickers)
        
        # 4단계: Top 50에서 변동성 분석
        volatility_ranking = self.get_volatility_ranking(top_50_tickers)
        
        # 5단계: 복합 점수 계산
        scores = {}
        
        # 거래량 점수 (50점 만점)
        for i, (ticker, _) in enumerate(volume_ranking):
            scores[ticker] = scores.get(ticker, 0) + (50 - i)
        
        # RSI 점수 (30점 만점)
        for i, (ticker, _) in enumerate(rsi_ranking[:30]):
            scores[ticker] = scores.get(ticker, 0) + (30 - i)
        
        # 변동성 점수 (20점 만점)
        for i, (ticker, _) in enumerate(volatility_ranking[:20]):
            scores[ticker] = scores.get(ticker, 0) + (20 - i)
        
        # 최종 순위
        final_ranking = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # 상위 N개 선택
        selected_coins = [ticker for ticker, _ in final_ranking[:self.coin_count]]
        
        self.logger.info(f"✅ 최종 선정: {len(selected_coins)}개")
        self.logger.info(f"📋 선정 코인: {', '.join(selected_coins[:10])}...")
        
        self.current_coins = selected_coins
        self.last_update = time.time()
        
        return selected_coins
    
    def select_coins_volume_only(self) -> List[str]:
        """거래량 기준 단순 선정 (빠름)"""
        self.logger.info(f"🎯 거래량 기준 코인 선정 (목표: {self.coin_count}개)")
        
        all_tickers = self.get_all_krw_tickers()
        if not all_tickers:
            return self._get_fallback_coins()
        
        volume_ranking = self.get_volume_ranking(all_tickers, top_n=self.coin_count)
        
        selected_coins = [ticker for ticker, _ in volume_ranking]
        
        self.logger.info(f"✅ 거래량 Top {len(selected_coins)}개 선정 완료")
        self.logger.info(f"📋 선정 코인: {', '.join(selected_coins[:10])}...")
        
        self.current_coins = selected_coins
        self.last_update = time.time()
        
        return selected_coins
    
    def select_coins_rsi_focus(self) -> List[str]:
        """RSI 중심 선정 (초단타 전략용)"""
        self.logger.info(f"🎯 RSI 중심 코인 선정 (목표: {self.coin_count}개)")
        
        all_tickers = self.get_all_krw_tickers()
        if not all_tickers:
            return self._get_fallback_coins()
        
        # 거래량 Top 100에서 RSI 분석
        volume_ranking = self.get_volume_ranking(all_tickers, top_n=100)
        top_100_tickers = [ticker for ticker, _ in volume_ranking]
        
        rsi_ranking = self.get_rsi_ranking(top_100_tickers)
        
        selected_coins = [ticker for ticker, _ in rsi_ranking[:self.coin_count]]
        
        self.logger.info(f"✅ RSI 기준 {len(selected_coins)}개 선정 완료")
        self.logger.info(f"📋 선정 코인: {', '.join(selected_coins[:10])}...")
        
        self.current_coins = selected_coins
        self.last_update = time.time()
        
        return selected_coins
    
    def get_coins(self, method: str = "multi") -> List[str]:
        """
        코인 목록 반환 (5분마다 자동 갱신)
        
        Args:
            method: "multi" (복합), "volume" (거래량), "rsi" (RSI 중심)
        """
        # 5분마다 업데이트
        if self.should_update() or not self.current_coins:
            if method == "volume":
                self.select_coins_volume_only()
            elif method == "rsi":
                self.select_coins_rsi_focus()
            else:
                self.select_coins_multi_criteria()
        
        return self.current_coins
    
    def _get_fallback_coins(self) -> List[str]:
        """폴백: 기본 메이저 코인"""
        fallback = [
            "KRW-BTC", "KRW-ETH", "KRW-XRP", "KRW-ADA", "KRW-SOL",
            "KRW-DOGE", "KRW-DOT", "KRW-AVAX", "KRW-LINK", "KRW-ATOM",
            "KRW-UNI", "KRW-NEAR", "KRW-ALGO", "KRW-VET", "KRW-FTM",
            "KRW-HBAR", "KRW-ICP", "KRW-APT", "KRW-OP", "KRW-ARB"
        ]
        return fallback[:self.coin_count]
    
    def get_status(self) -> Dict:
        """현재 상태 반환"""
        time_since_update = time.time() - self.last_update
        next_update_in = max(0, self.update_interval - time_since_update)
        
        return {
            "coin_count": self.coin_count,
            "current_coins": self.current_coins,
            "last_update": datetime.fromtimestamp(self.last_update).strftime("%H:%M:%S") if self.last_update > 0 else "미실행",
            "next_update_in": f"{int(next_update_in)}초",
            "update_interval": f"{self.update_interval}초"
        }


if __name__ == "__main__":
    # 테스트
    print("=" * 60)
    print("동적 코인 선정 시스템 테스트")
    print("=" * 60)
    
    # 35개 코인 선정
    selector = DynamicCoinSelector(coin_count=35)
    
    print("\n[방법 1] 거래량 기준")
    coins_volume = selector.select_coins_volume_only()
    print(f"선정: {len(coins_volume)}개")
    
    print("\n[방법 2] RSI 기준")
    selector2 = DynamicCoinSelector(coin_count=35)
    coins_rsi = selector2.select_coins_rsi_focus()
    print(f"선정: {len(coins_rsi)}개")
    
    print("\n[방법 3] 복합 기준")
    selector3 = DynamicCoinSelector(coin_count=35)
    coins_multi = selector3.select_coins_multi_criteria()
    print(f"선정: {len(coins_multi)}개")
    
    print("\n✅ 테스트 완료")
