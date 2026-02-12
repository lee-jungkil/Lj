"""
급등 감지 시스템 (Surge Detector)
- 1분/5분/15분 상승률 및 거래량 분석
- 급등 점수 계산 및 추격매수 신호 생성
"""

import time
from typing import Dict, Optional, List, Tuple
from datetime import datetime
import pandas as pd


class SurgeDetector:
    """급등 감지 및 점수 계산"""
    
    def __init__(self):
        """초기화"""
        self.surge_history = {}  # {ticker: [timestamps]}
        self.failed_chase_history = {}  # {ticker: [(timestamp, reason)]}
        self.max_history = 100
        
        # 임계값 설정
        self.threshold_1m = 1.5  # 1분 상승률 ≥ 1.5%
        self.threshold_5m = 3.0  # 5분 상승률 ≥ 3.0%
        self.threshold_15m = 5.0  # 15분 상승률 ≥ 5.0%
        self.volume_ratio_threshold = 2.0  # 거래량 비율 ≥ 2.0
        self.min_surge_score = 50  # 최소 급등 점수
    
    def detect_surge(self, ticker: str, api) -> Optional[Dict]:
        """
        급등 감지 및 분석
        
        Args:
            ticker: 코인 티커
            api: UpbitAPI 인스턴스
        
        Returns:
            급등 정보 딕셔너리 or None
        """
        try:
            # 1분 OHLCV 데이터
            df_1m = api.get_ohlcv(ticker, interval="minute1", count=20)
            if df_1m is None or len(df_1m) < 2:
                return None
            
            # 5분 OHLCV 데이터
            df_5m = api.get_ohlcv(ticker, interval="minute5", count=20)
            if df_5m is None or len(df_5m) < 2:
                return None
            
            # 15분 OHLCV 데이터
            df_15m = api.get_ohlcv(ticker, interval="minute15", count=20)
            if df_15m is None or len(df_15m) < 2:
                return None
            
            # 1분 상승률
            current_1m = df_1m['close'].iloc[-1]
            prev_1m = df_1m['close'].iloc[-2]
            change_1m = ((current_1m - prev_1m) / prev_1m) * 100
            
            # 5분 상승률
            current_5m = df_5m['close'].iloc[-1]
            prev_5m = df_5m['close'].iloc[-6] if len(df_5m) >= 6 else df_5m['close'].iloc[0]
            change_5m = ((current_5m - prev_5m) / prev_5m) * 100
            
            # 15분 상승률
            current_15m = df_15m['close'].iloc[-1]
            prev_15m = df_15m['close'].iloc[-4] if len(df_15m) >= 4 else df_15m['close'].iloc[0]
            change_15m = ((current_15m - prev_15m) / prev_15m) * 100
            
            # 거래량 비율 (최근 5분 vs 평균)
            volume_current = df_1m['volume'].iloc[-5:].mean()
            volume_avg = df_1m['volume'].iloc[-20:-5].mean()
            volume_ratio = volume_current / volume_avg if volume_avg > 0 else 1.0
            
            # 급등 점수 계산
            surge_score = self.calculate_surge_score(
                change_1m, change_5m, change_15m, volume_ratio
            )
            
            # 급등 감지 조건
            is_surge = (
                change_1m >= self.threshold_1m and
                volume_ratio >= self.volume_ratio_threshold and
                surge_score >= self.min_surge_score
            )
            
            if not is_surge:
                return None
            
            # 급등 정보 반환
            return {
                'ticker': ticker,
                'change_1m': change_1m,
                'change_5m': change_5m,
                'change_15m': change_15m,
                'volume_ratio': volume_ratio,
                'surge_score': surge_score,
                'current_price': current_1m,
                'timestamp': datetime.now(),
                'confidence': self.calculate_confidence(surge_score, volume_ratio)
            }
        
        except Exception as e:
            print(f"❌ {ticker} 급등 감지 실패: {e}")
            return None
    
    def calculate_surge_score(self, change_1m: float, change_5m: float, 
                             change_15m: float, volume_ratio: float) -> float:
        """
        급등 점수 계산
        
        Formula:
            surge_score = 
                (1분 상승률 ≥ 1.5%) × 10 +
                (5분 상승률 ≥ 3.0%) × 5 +
                (15분 상승률 ≥ 5.0%) × 2 +
                (거래량 비율 ≥ 2.0) × 20
        
        Args:
            change_1m: 1분 상승률
            change_5m: 5분 상승률
            change_15m: 15분 상승률
            volume_ratio: 거래량 비율
        
        Returns:
            급등 점수 (0~100)
        """
        score = 0.0
        
        # 1분 상승률 점수
        if change_1m >= self.threshold_1m:
            score += 10 * (change_1m / self.threshold_1m)
        
        # 5분 상승률 점수
        if change_5m >= self.threshold_5m:
            score += 5 * (change_5m / self.threshold_5m)
        
        # 15분 상승률 점수
        if change_15m >= self.threshold_15m:
            score += 2 * (change_15m / self.threshold_15m)
        
        # 거래량 점수
        if volume_ratio >= self.volume_ratio_threshold:
            score += 20 * (volume_ratio / self.volume_ratio_threshold)
        
        return min(score, 100.0)  # 최대 100점
    
    def calculate_confidence(self, surge_score: float, volume_ratio: float) -> float:
        """
        신뢰도 계산 (0.0 ~ 1.0)
        
        Args:
            surge_score: 급등 점수
            volume_ratio: 거래량 비율
        
        Returns:
            신뢰도
        """
        # 점수 기반 신뢰도 (0.5 ~ 1.0)
        score_confidence = 0.5 + (surge_score / 200)
        
        # 거래량 기반 신뢰도 (0.5 ~ 1.0)
        volume_confidence = 0.5 + min(volume_ratio / 6.0, 0.5)
        
        # 평균
        confidence = (score_confidence + volume_confidence) / 2
        
        return min(max(confidence, 0.0), 1.0)
    
    def can_chase_buy(self, ticker: str, surge_info: Dict) -> Tuple[bool, str]:
        """
        추격매수 가능 여부 판단
        
        Checks:
        1. 급등 점수 ≥ 50
        2. 거래량 비율 ≥ 2.0
        3. 신뢰도 ≥ 0.7
        4. 1분 모멘텀 ≥ 1.5%
        5. 24시간 내 3회 미만 실패
        
        Args:
            ticker: 코인 티커
            surge_info: 급등 정보
        
        Returns:
            (가능 여부, 사유)
        """
        # 1. 급등 점수 체크
        if surge_info['surge_score'] < self.min_surge_score:
            return False, f"급등 점수 부족 ({surge_info['surge_score']:.1f} < {self.min_surge_score})"
        
        # 2. 거래량 비율 체크
        if surge_info['volume_ratio'] < self.volume_ratio_threshold:
            return False, f"거래량 부족 ({surge_info['volume_ratio']:.1f}x < {self.volume_ratio_threshold}x)"
        
        # 3. 신뢰도 체크
        if surge_info['confidence'] < 0.7:
            return False, f"신뢰도 부족 ({surge_info['confidence']:.2f} < 0.70)"
        
        # 4. 1분 모멘텀 체크
        if surge_info['change_1m'] < self.threshold_1m:
            return False, f"1분 상승률 부족 ({surge_info['change_1m']:.2f}% < {self.threshold_1m}%)"
        
        # 5. 24시간 내 실패 횟수 체크
        failed_count = self.get_failed_count_24h(ticker)
        if failed_count >= 3:
            return False, f"24시간 내 실패 {failed_count}회 (최대 3회)"
        
        return True, "추격매수 조건 충족"
    
    def get_failed_count_24h(self, ticker: str) -> int:
        """
        24시간 내 추격매수 실패 횟수 조회
        
        Args:
            ticker: 코인 티커
        
        Returns:
            실패 횟수
        """
        if ticker not in self.failed_chase_history:
            return 0
        
        now = time.time()
        day_ago = now - 86400  # 24시간
        
        # 24시간 내 실패 횟수 계산
        count = sum(1 for ts, _ in self.failed_chase_history[ticker] if ts > day_ago)
        return count
    
    def record_failed_chase(self, ticker: str, reason: str):
        """
        추격매수 실패 기록
        
        Args:
            ticker: 코인 티커
            reason: 실패 사유
        """
        if ticker not in self.failed_chase_history:
            self.failed_chase_history[ticker] = []
        
        self.failed_chase_history[ticker].append((time.time(), reason))
        
        # 최대 100개 유지
        if len(self.failed_chase_history[ticker]) > self.max_history:
            self.failed_chase_history[ticker].pop(0)
    
    def get_chase_investment_multiplier(self, surge_score: float, confidence: float) -> float:
        """
        추격매수 투자 배율 계산
        
        Formula:
            multiplier = 1.5 + (surge_score / 200) + (confidence * 0.5)
        
        Args:
            surge_score: 급등 점수
            confidence: 신뢰도
        
        Returns:
            투자 배율 (1.5 ~ 2.0)
        """
        multiplier = 1.5 + (surge_score / 200) + (confidence * 0.5)
        return min(max(multiplier, 1.5), 2.0)
    
    def scan_market_batch(self, tickers: List[str], prices_dict: Dict[str, float]) -> List[Dict]:
        """
        여러 코인의 급등/급락을 배치로 스캔
        
        Args:
            tickers: 코인 티커 리스트
            prices_dict: {ticker: price} 딕셔너리
        
        Returns:
            급등 감지된 코인 정보 리스트
        """
        detected = []
        
        # 간단한 구현: detect_surge를 순회 호출
        # 실제로는 이 부분도 배치 최적화 가능
        for ticker in tickers:
            if ticker not in prices_dict:
                continue
            
            # 이 부분은 실제로 api를 필요로 하므로
            # main.py에서 호출할 때 api를 전달받아야 함
            # 현재는 빈 리스트 반환 (호환성 유지)
            pass
        
        return detected


# 전역 인스턴스
surge_detector = SurgeDetector()
