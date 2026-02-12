"""
Conditional Sell System (조건부 매도 시스템)
- 여러 기술적 지표 조건을 복합 평가
- 최소 N개 조건 충족 시 매도
- 신뢰도 기반 의사결정
- 거짓 신호 필터링

⭐ v6.30 Integration Phase 2B

Evaluation Criteria:
1. 수익률 임계값 (Profit Threshold)
2. RSI 과매수 (RSI Overbought)
3. 거래량 감소 (Volume Drop)
4. MACD 하락 전환 (MACD Bearish)
5. 저항선 근접 (Near Resistance)
6. 추세 전환 (Trend Reversal)
"""

from typing import Dict, Optional, List, Tuple
from dataclasses import dataclass
import os


@dataclass
class ConditionResult:
    """조건 평가 결과"""
    name: str
    met: bool
    value: float
    threshold: float
    description: str


class ConditionalSellManager:
    """조건부 매도 관리 시스템"""
    
    def __init__(self, config, market_analyzer):
        """
        초기화
        
        Args:
            config: Config 객체
            market_analyzer: 시장 분석기
        """
        self.config = config
        self.analyzer = market_analyzer
        self.enabled = os.getenv('ENABLE_CONDITIONAL_SELL', 'true').lower() == 'true'
        
        # 최소 충족 조건 개수
        self.min_conditions = int(os.getenv('CONDITIONAL_SELL_MIN_CONDITIONS', '2'))
        
        # 조건별 가중치 (중요도)
        self.condition_weights = {
            'profit_threshold': 1.5,
            'rsi_overbought': 1.0,
            'volume_drop': 1.2,
            'macd_bearish': 1.3,
            'near_resistance': 0.8,
            'trend_reversal': 1.4
        }
    
    def evaluate_sell_conditions(self, ticker: str, position, 
                                 current_price: float) -> Dict:
        """
        매도 조건 종합 평가
        
        Args:
            ticker: 코인 티커
            position: 포지션 객체
            current_price: 현재 가격
        
        Returns:
            {
                'should_sell': bool,
                'confidence': float (0.0 ~ 1.0),
                'met_conditions': int,
                'total_conditions': int,
                'conditions': List[ConditionResult],
                'weighted_score': float,
                'reasons': List[str]
            }
        """
        if not self.enabled:
            return {'should_sell': False, 'confidence': 0.0}
        
        # 수익률 계산
        profit_ratio = ((current_price - position.avg_buy_price) / 
                       position.avg_buy_price * 100)
        
        # 각 조건 평가
        conditions = []
        
        # 1. 수익률 임계값
        profit_cond = self._check_profit_threshold(profit_ratio, position.strategy)
        conditions.append(profit_cond)
        
        # 2. RSI 과매수
        rsi_cond = self._check_rsi_overbought(ticker)
        conditions.append(rsi_cond)
        
        # 3. 거래량 감소
        volume_cond = self._check_volume_drop(ticker)
        conditions.append(volume_cond)
        
        # 4. MACD 하락 전환
        macd_cond = self._check_macd_bearish(ticker)
        conditions.append(macd_cond)
        
        # 5. 저항선 근접
        resistance_cond = self._check_near_resistance(ticker, current_price)
        conditions.append(resistance_cond)
        
        # 6. 추세 전환
        trend_cond = self._check_trend_reversal(ticker)
        conditions.append(trend_cond)
        
        # 충족된 조건 수 계산
        met_conditions = [c for c in conditions if c.met]
        met_count = len(met_conditions)
        total_count = len(conditions)
        
        # 가중치 점수 계산
        weighted_score = sum(
            self.condition_weights.get(c.name, 1.0) 
            for c in met_conditions
        )
        max_score = sum(self.condition_weights.values())
        
        # 신뢰도 계산 (가중치 기반)
        confidence = weighted_score / max_score if max_score > 0 else 0.0
        
        # 매도 결정
        should_sell = met_count >= self.min_conditions
        
        # 사유 생성
        reasons = [c.description for c in met_conditions]
        
        return {
            'should_sell': should_sell,
            'confidence': confidence,
            'met_conditions': met_count,
            'total_conditions': total_count,
            'conditions': conditions,
            'weighted_score': weighted_score,
            'max_score': max_score,
            'reasons': reasons
        }
    
    def _check_profit_threshold(self, profit_ratio: float, 
                               strategy: str) -> ConditionResult:
        """수익률 임계값 체크"""
        # 전략별 최소 수익 기준
        min_profit = {
            'ULTRA_SCALPING': 0.5,
            'AGGRESSIVE_SCALPING': 1.0,
            'CONSERVATIVE_SCALPING': 0.8,
            'MEAN_REVERSION': 1.5,
            'GRID_TRADING': 1.0
        }.get(strategy.upper(), 1.0)
        
        met = profit_ratio >= min_profit
        
        return ConditionResult(
            name='profit_threshold',
            met=met,
            value=profit_ratio,
            threshold=min_profit,
            description=f"수익 {profit_ratio:.2f}% {'≥' if met else '<'} {min_profit}%"
        )
    
    def _check_rsi_overbought(self, ticker: str) -> ConditionResult:
        """RSI 과매수 체크"""
        try:
            rsi = self.analyzer.calculate_rsi(ticker, period=14)
            threshold = 70.0
            met = rsi is not None and rsi > threshold
            
            return ConditionResult(
                name='rsi_overbought',
                met=met,
                value=rsi if rsi else 50.0,
                threshold=threshold,
                description=f"RSI {rsi:.1f if rsi else 'N/A'} {'과매수' if met else '정상'}"
            )
        except:
            return ConditionResult('rsi_overbought', False, 50.0, 70.0, "RSI 계산 불가")
    
    def _check_volume_drop(self, ticker: str) -> ConditionResult:
        """거래량 감소 체크"""
        try:
            volume_ratio = self.analyzer.get_volume_ratio(ticker)
            threshold = 0.7  # 평균 대비 70% 미만
            met = volume_ratio < threshold
            
            return ConditionResult(
                name='volume_drop',
                met=met,
                value=volume_ratio,
                threshold=threshold,
                description=f"거래량 {volume_ratio*100:.0f}% {'감소' if met else '정상'}"
            )
        except:
            return ConditionResult('volume_drop', False, 1.0, 0.7, "거래량 계산 불가")
    
    def _check_macd_bearish(self, ticker: str) -> ConditionResult:
        """MACD 하락 전환 체크"""
        try:
            macd_signal = self.analyzer.get_macd_signal(ticker)
            met = macd_signal == 'bearish'
            
            return ConditionResult(
                name='macd_bearish',
                met=met,
                value=1.0 if met else 0.0,
                threshold=1.0,
                description=f"MACD {'하락' if met else '상승/중립'} 전환"
            )
        except:
            return ConditionResult('macd_bearish', False, 0.0, 1.0, "MACD 계산 불가")
    
    def _check_near_resistance(self, ticker: str, 
                               current_price: float) -> ConditionResult:
        """저항선 근접 체크"""
        try:
            resistance = self.analyzer.get_resistance_level(ticker)
            
            if resistance is None:
                return ConditionResult('near_resistance', False, 0.0, 0.98, "저항선 없음")
            
            ratio = current_price / resistance
            threshold = 0.98  # 저항선의 98% 이상
            met = ratio >= threshold
            
            return ConditionResult(
                name='near_resistance',
                met=met,
                value=ratio,
                threshold=threshold,
                description=f"저항선 {ratio*100:.1f}% {'근접' if met else '여유'}"
            )
        except:
            return ConditionResult('near_resistance', False, 0.0, 0.98, "저항선 계산 불가")
    
    def _check_trend_reversal(self, ticker: str) -> ConditionResult:
        """추세 전환 체크"""
        try:
            trend = self.analyzer.get_trend(ticker)
            met = trend == 'down'
            
            return ConditionResult(
                name='trend_reversal',
                met=met,
                value=1.0 if met else 0.0,
                threshold=1.0,
                description=f"추세 {trend if trend else '불명'} ({'하락' if met else '상승/횡보'})"
            )
        except:
            return ConditionResult('trend_reversal', False, 0.0, 1.0, "추세 계산 불가")
    
    def get_config_summary(self) -> str:
        """
        설정 요약 정보
        
        Returns:
            설정 요약 문자열
        """
        if not self.enabled:
            return "조건부 매도: 비활성화"
        
        return (f"조건부 매도: 최소 {self.min_conditions}개 조건 충족 "
                f"(총 {len(self.condition_weights)}개 조건)")
    
    def format_evaluation_result(self, eval_result: Dict) -> str:
        """
        평가 결과 포맷팅 (로그용)
        
        Args:
            eval_result: evaluate_sell_conditions() 결과
        
        Returns:
            포맷된 문자열
        """
        if not eval_result.get('should_sell'):
            return (f"❌ 조건부 매도 불충족 "
                   f"({eval_result['met_conditions']}/{eval_result['total_conditions']} 조건, "
                   f"신뢰도 {eval_result['confidence']*100:.1f}%)")
        
        reasons_str = ", ".join(eval_result['reasons'])
        
        return (f"✅ 조건부 매도 충족 "
               f"({eval_result['met_conditions']}/{eval_result['total_conditions']} 조건, "
               f"신뢰도 {eval_result['confidence']*100:.1f}%)\n"
               f"   사유: {reasons_str}")
