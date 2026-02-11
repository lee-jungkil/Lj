"""
시장 조건 분석기 - 진입 조건 완화/강화 결정
"""

from typing import Dict, Tuple
import pandas as pd


class MarketConditionAnalyzer:
    """시장 조건 분석 및 진입 조건 자동 조정"""
    
    def __init__(self):
        """초기화"""
        self.condition_history = []
        self.max_history = 100
    
    def analyze_market(self, df: pd.DataFrame) -> Tuple[str, str, str]:
        """
        시장 조건 분석
        
        Args:
            df: OHLCV 데이터프레임
        
        Returns:
            (시장 국면, 진입 조건, 한 줄 요약)
        """
        if df is None or df.empty or len(df) < 20:
            return "분석 중", "기본", "시장 데이터 수집 중..."
        
        try:
            # 가격 변동
            current_price = df['close'].iloc[-1]
            price_1h_ago = df['close'].iloc[-12] if len(df) >= 12 else df['close'].iloc[0]
            price_change_1h = ((current_price - price_1h_ago) / price_1h_ago) * 100
            
            # 거래량 변화
            volume_current = df['volume'].iloc[-5:].mean()
            volume_prev = df['volume'].iloc[-20:-5].mean()
            volume_ratio = volume_current / volume_prev if volume_prev > 0 else 1.0
            
            # 변동성
            volatility = df['close'].pct_change().std() * 100
            
            # RSI 계산
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            current_rsi = rsi.iloc[-1]
            
            # 시장 국면 판단
            if price_change_1h > 2.0:
                market_phase = "강세장"
            elif price_change_1h < -2.0:
                market_phase = "약세장"
            else:
                market_phase = "횡보장"
            
            # 진입 조건 결정
            # 강세장 + 거래량 증가 → 완화
            if market_phase == "강세장" and volume_ratio > 1.5:
                entry_condition = "완화"
            # 약세장 + 거래량 감소 → 강화
            elif market_phase == "약세장" and volume_ratio < 0.8:
                entry_condition = "강화"
            # 횡보장 + 변동성 낮음 → 강화
            elif market_phase == "횡보장" and volatility < 1.0:
                entry_condition = "강화"
            # 횡보장 + 변동성 높음 → 완화
            elif market_phase == "횡보장" and volatility > 3.0:
                entry_condition = "완화"
            else:
                entry_condition = "기본"
            
            # 한 줄 요약
            summary = (
                f"{market_phase} | "
                f"가격 {price_change_1h:+.2f}% | "
                f"거래량 {volume_ratio:.1f}x | "
                f"변동성 {volatility:.2f}% | "
                f"RSI {current_rsi:.0f}"
            )
            
            # 이력 기록
            self.condition_history.append({
                'phase': market_phase,
                'entry_condition': entry_condition,
                'price_change': price_change_1h,
                'volume_ratio': volume_ratio,
                'volatility': volatility,
                'rsi': current_rsi
            })
            
            if len(self.condition_history) > self.max_history:
                self.condition_history.pop(0)
            
            return market_phase, entry_condition, summary
        
        except Exception as e:
            return "분석 중", "기본", f"분석 오류: {str(e)[:30]}"
    
    def get_adjusted_thresholds(self, base_thresholds: Dict, entry_condition: str) -> Dict:
        """
        진입 조건에 따라 임계값 조정
        
        Args:
            base_thresholds: 기본 임계값
            entry_condition: 진입 조건 (완화/기본/강화)
        
        Returns:
            조정된 임계값
        """
        adjusted = base_thresholds.copy()
        
        if entry_condition == "완화":
            # RSI 범위 확대
            adjusted['rsi_oversold'] = adjusted.get('rsi_oversold', 30) + 5  # 30 → 35
            adjusted['rsi_overbought'] = adjusted.get('rsi_overbought', 70) - 5  # 70 → 65
            
            # 거래량 임계값 낮춤
            adjusted['volume_threshold'] = adjusted.get('volume_threshold', 1.5) * 0.8
            
            # 가격 변화 임계값 낮춤
            adjusted['min_price_change'] = adjusted.get('min_price_change', 0.01) * 0.7
            
        elif entry_condition == "강화":
            # RSI 범위 축소
            adjusted['rsi_oversold'] = adjusted.get('rsi_oversold', 30) - 5  # 30 → 25
            adjusted['rsi_overbought'] = adjusted.get('rsi_overbought', 70) + 5  # 70 → 75
            
            # 거래량 임계값 높임
            adjusted['volume_threshold'] = adjusted.get('volume_threshold', 1.5) * 1.2
            
            # 가격 변화 임계값 높임
            adjusted['min_price_change'] = adjusted.get('min_price_change', 0.01) * 1.3
        
        return adjusted
    
    def get_statistics(self) -> Dict:
        """
        조건 변경 통계
        
        Returns:
            통계 딕셔너리
        """
        if not self.condition_history:
            return {}
        
        total = len(self.condition_history)
        relaxed = sum(1 for h in self.condition_history if h['entry_condition'] == '완화')
        strengthened = sum(1 for h in self.condition_history if h['entry_condition'] == '강화')
        
        return {
            'total_samples': total,
            'relaxed_count': relaxed,
            'strengthened_count': strengthened,
            'relaxed_ratio': relaxed / total if total > 0 else 0,
            'strengthened_ratio': strengthened / total if total > 0 else 0
        }


# 전역 인스턴스
market_condition_analyzer = MarketConditionAnalyzer()
