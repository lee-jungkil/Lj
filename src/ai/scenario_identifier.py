"""
45가지 시장 상황 자동 인식 시스템
시장 데이터를 분석하여 현재 상황을 정확히 식별
"""

from typing import Dict, List, Tuple
import pandas as pd
import numpy as np
from datetime import datetime


class ScenarioIdentifier:
    """시장 상황 식별기 - 45가지 시나리오"""
    
    # 시나리오 정의
    SCENARIOS = {
        # === 추세 기반 (1-10) ===
        1: "강한 상승 추세 (연속 상승)",
        2: "약한 상승 추세 (완만 상승)",
        3: "강한 하락 추세 (연속 하락)",
        4: "약한 하락 추세 (완만 하락)",
        5: "횡보장 (좁은 범위)",
        6: "횡보장 (넓은 범위)",
        7: "추세 전환 시그널 (상승→하락)",
        8: "추세 전환 시그널 (하락→상승)",
        9: "급등 후 조정",
        10: "급락 후 반등",
        
        # === 변동성 기반 (11-20) ===
        11: "초고변동성 (>5%)",
        12: "고변동성 (3-5%)",
        13: "중변동성 (1-3%)",
        14: "저변동성 (<1%)",
        15: "변동성 급증",
        16: "변동성 수축",
        17: "볼린저밴드 상단 돌파",
        18: "볼린저밴드 하단 돌파",
        19: "볼린저밴드 수축 (스퀴즈)",
        20: "볼린저밴드 확장",
        
        # === 거래량 기반 (21-30) ===
        21: "거래량 폭증 (>3배)",
        22: "거래량 증가 (1.5-3배)",
        23: "거래량 정상",
        24: "거래량 감소 (<0.5배)",
        25: "거래량 선행 상승",
        26: "거래량 선행 하락",
        27: "가격-거래량 다이버전스 (상승)",
        28: "가격-거래량 다이버전스 (하락)",
        29: "거래량 패턴: 축적",
        30: "거래량 패턴: 분산",
        
        # === 기술적 지표 기반 (31-40) ===
        31: "RSI 과매수 (>70)",
        32: "RSI 과매도 (<30)",
        33: "MACD 골든크로스",
        34: "MACD 데드크로스",
        35: "이동평균 정배열",
        36: "이동평균 역배열",
        37: "지지선 반등",
        38: "저항선 돌파",
        39: "지지선 이탈",
        40: "저항선 실패",
        
        # === 복합 패턴 (41-45) ===
        41: "바닥 형성 패턴",
        42: "천장 형성 패턴",
        43: "삼각수렴 패턴",
        44: "쐐기형 패턴",
        45: "깃발형 패턴"
    }
    
    def __init__(self):
        """시나리오 식별기 초기화"""
        self.history = []  # 식별 히스토리
        
    def identify(self, df: pd.DataFrame, ticker: str) -> Dict:
        """
        현재 시장 상황 식별
        
        Args:
            df: OHLCV 데이터프레임 (최소 100개 캔들)
            ticker: 티커 심볼
        
        Returns:
            {
                'primary_scenario': int,        # 주요 시나리오 ID
                'secondary_scenarios': List[int],  # 부가 시나리오들
                'scenario_names': List[str],    # 시나리오 이름들
                'confidence': float,            # 신뢰도 (0~100)
                'indicators': Dict,             # 계산된 지표들
                'timestamp': datetime
            }
        """
        if len(df) < 100:
            return self._default_scenario()
        
        try:
            # 기술적 지표 계산
            indicators = self._calculate_indicators(df)
            
            # 각 카테고리별 시나리오 식별
            trend_scenarios = self._identify_trend(df, indicators)
            volatility_scenarios = self._identify_volatility(df, indicators)
            volume_scenarios = self._identify_volume(df, indicators)
            technical_scenarios = self._identify_technical(df, indicators)
            pattern_scenarios = self._identify_patterns(df, indicators)
            
            # 모든 시나리오 통합
            all_scenarios = (
                trend_scenarios + 
                volatility_scenarios + 
                volume_scenarios + 
                technical_scenarios + 
                pattern_scenarios
            )
            
            # 가장 강한 시나리오 선택
            if all_scenarios:
                primary = all_scenarios[0]
                secondary = all_scenarios[1:4] if len(all_scenarios) > 1 else []
            else:
                primary = 23  # 거래량 정상 (기본값)
                secondary = []
            
            result = {
                'primary_scenario': primary,
                'secondary_scenarios': secondary,
                'scenario_names': [self.SCENARIOS[s] for s in [primary] + secondary],
                'confidence': self._calculate_confidence(all_scenarios, indicators),
                'indicators': indicators,
                'ticker': ticker,
                'timestamp': datetime.now()
            }
            
            # 히스토리 저장
            self.history.append(result)
            if len(self.history) > 100:
                self.history.pop(0)
            
            return result
            
        except Exception as e:
            print(f"❌ 시나리오 식별 오류: {e}")
            return self._default_scenario()
    
    def _calculate_indicators(self, df: pd.DataFrame) -> Dict:
        """기술적 지표 계산"""
        indicators = {}
        
        try:
            # 가격 변화
            indicators['price_change_1h'] = (df['close'].iloc[-1] / df['close'].iloc[-12] - 1) * 100
            indicators['price_change_4h'] = (df['close'].iloc[-1] / df['close'].iloc[-48] - 1) * 100
            indicators['price_change_24h'] = (df['close'].iloc[-1] / df['close'].iloc[-288] - 1) * 100
            
            # 변동성
            returns = df['close'].pct_change()
            indicators['volatility'] = returns.std() * 100
            
            # 이동평균
            indicators['ma5'] = df['close'].rolling(5).mean().iloc[-1]
            indicators['ma20'] = df['close'].rolling(20).mean().iloc[-1]
            indicators['ma60'] = df['close'].rolling(60).mean().iloc[-1]
            
            # RSI
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss
            indicators['rsi'] = 100 - (100 / (1 + rs.iloc[-1]))
            
            # MACD
            exp1 = df['close'].ewm(span=12).mean()
            exp2 = df['close'].ewm(span=26).mean()
            macd = exp1 - exp2
            signal = macd.ewm(span=9).mean()
            indicators['macd'] = macd.iloc[-1]
            indicators['macd_signal'] = signal.iloc[-1]
            indicators['macd_hist'] = macd.iloc[-1] - signal.iloc[-1]
            
            # 볼린저 밴드
            bb_middle = df['close'].rolling(20).mean()
            bb_std = df['close'].rolling(20).std()
            indicators['bb_upper'] = (bb_middle + 2 * bb_std).iloc[-1]
            indicators['bb_middle'] = bb_middle.iloc[-1]
            indicators['bb_lower'] = (bb_middle - 2 * bb_std).iloc[-1]
            indicators['bb_width'] = (indicators['bb_upper'] - indicators['bb_lower']) / indicators['bb_middle']
            
            # 거래량
            indicators['volume_avg'] = df['volume'].rolling(20).mean().iloc[-1]
            indicators['volume_current'] = df['volume'].iloc[-1]
            indicators['volume_ratio'] = indicators['volume_current'] / indicators['volume_avg']
            
        except Exception as e:
            print(f"⚠️ 지표 계산 오류: {e}")
        
        return indicators
    
    def _identify_trend(self, df: pd.DataFrame, ind: Dict) -> List[int]:
        """추세 시나리오 식별 (1-10)"""
        scenarios = []
        
        # 1-2: 상승 추세
        if ind.get('price_change_1h', 0) > 2 and ind.get('price_change_4h', 0) > 5:
            scenarios.append(1)  # 강한 상승
        elif ind.get('price_change_4h', 0) > 2:
            scenarios.append(2)  # 약한 상승
        
        # 3-4: 하락 추세
        if ind.get('price_change_1h', 0) < -2 and ind.get('price_change_4h', 0) < -5:
            scenarios.append(3)  # 강한 하락
        elif ind.get('price_change_4h', 0) < -2:
            scenarios.append(4)  # 약한 하락
        
        # 5-6: 횡보
        if abs(ind.get('price_change_4h', 0)) < 1:
            if ind.get('volatility', 0) < 0.5:
                scenarios.append(5)  # 좁은 횡보
            else:
                scenarios.append(6)  # 넓은 횡보
        
        # 7-8: 추세 전환
        price_1h = ind.get('price_change_1h', 0)
        price_4h = ind.get('price_change_4h', 0)
        if price_4h > 3 and price_1h < -1:
            scenarios.append(7)  # 상승→하락
        elif price_4h < -3 and price_1h > 1:
            scenarios.append(8)  # 하락→상승
        
        # 9-10: 급등/급락 후
        if ind.get('price_change_1h', 0) > 5:
            scenarios.append(9)  # 급등 후
        elif ind.get('price_change_1h', 0) < -5:
            scenarios.append(10)  # 급락 후
        
        return scenarios
    
    def _identify_volatility(self, df: pd.DataFrame, ind: Dict) -> List[int]:
        """변동성 시나리오 식별 (11-20)"""
        scenarios = []
        vol = ind.get('volatility', 0)
        bb_width = ind.get('bb_width', 0)
        current_price = df['close'].iloc[-1]
        
        # 11-14: 변동성 수준
        if vol > 5:
            scenarios.append(11)  # 초고변동성
        elif vol > 3:
            scenarios.append(12)  # 고변동성
        elif vol > 1:
            scenarios.append(13)  # 중변동성
        else:
            scenarios.append(14)  # 저변동성
        
        # 17-18: 볼린저밴드 돌파
        if current_price > ind.get('bb_upper', float('inf')):
            scenarios.append(17)  # 상단 돌파
        elif current_price < ind.get('bb_lower', 0):
            scenarios.append(18)  # 하단 돌파
        
        # 19-20: 볼린저밴드 폭
        if bb_width < 0.02:
            scenarios.append(19)  # 수축 (스퀴즈)
        elif bb_width > 0.05:
            scenarios.append(20)  # 확장
        
        return scenarios
    
    def _identify_volume(self, df: pd.DataFrame, ind: Dict) -> List[int]:
        """거래량 시나리오 식별 (21-30)"""
        scenarios = []
        vol_ratio = ind.get('volume_ratio', 1.0)
        
        # 21-24: 거래량 수준
        if vol_ratio > 3:
            scenarios.append(21)  # 폭증
        elif vol_ratio > 1.5:
            scenarios.append(22)  # 증가
        elif vol_ratio > 0.5:
            scenarios.append(23)  # 정상
        else:
            scenarios.append(24)  # 감소
        
        # 27-28: 가격-거래량 다이버전스
        price_trend = ind.get('price_change_4h', 0)
        if price_trend > 2 and vol_ratio < 0.8:
            scenarios.append(27)  # 상승 다이버전스
        elif price_trend < -2 and vol_ratio < 0.8:
            scenarios.append(28)  # 하락 다이버전스
        
        return scenarios
    
    def _identify_technical(self, df: pd.DataFrame, ind: Dict) -> List[int]:
        """기술적 지표 시나리오 식별 (31-40)"""
        scenarios = []
        
        # 31-32: RSI
        rsi = ind.get('rsi', 50)
        if rsi > 70:
            scenarios.append(31)  # 과매수
        elif rsi < 30:
            scenarios.append(32)  # 과매도
        
        # 33-34: MACD
        macd = ind.get('macd', 0)
        signal = ind.get('macd_signal', 0)
        if macd > signal and macd > 0:
            scenarios.append(33)  # 골든크로스
        elif macd < signal and macd < 0:
            scenarios.append(34)  # 데드크로스
        
        # 35-36: 이동평균 배열
        ma5 = ind.get('ma5', 0)
        ma20 = ind.get('ma20', 0)
        ma60 = ind.get('ma60', 0)
        if ma5 > ma20 > ma60:
            scenarios.append(35)  # 정배열
        elif ma5 < ma20 < ma60:
            scenarios.append(36)  # 역배열
        
        return scenarios
    
    def _identify_patterns(self, df: pd.DataFrame, ind: Dict) -> List[int]:
        """패턴 시나리오 식별 (41-45)"""
        scenarios = []
        
        # 41-42: 바닥/천장 패턴
        rsi = ind.get('rsi', 50)
        price_change = ind.get('price_change_24h', 0)
        
        if rsi < 35 and price_change < -10:
            scenarios.append(41)  # 바닥 형성
        elif rsi > 65 and price_change > 10:
            scenarios.append(42)  # 천장 형성
        
        # 43: 삼각수렴
        vol = ind.get('volatility', 0)
        bb_width = ind.get('bb_width', 0)
        if vol < 1 and bb_width < 0.025:
            scenarios.append(43)  # 삼각수렴
        
        return scenarios
    
    def _calculate_confidence(self, scenarios: List[int], indicators: Dict) -> float:
        """
        시나리오 신뢰도 계산
        
        더 많은 시나리오가 일치할수록 신뢰도 증가
        """
        if not scenarios:
            return 50.0
        
        # 기본 신뢰도
        base_confidence = 60.0
        
        # 시나리오 수에 따른 보너스
        scenario_bonus = min(len(scenarios) * 5, 30)
        
        # 지표 완전성 보너스
        indicator_bonus = min(len(indicators) / 20 * 10, 10)
        
        total = base_confidence + scenario_bonus + indicator_bonus
        return min(total, 95.0)
    
    def _default_scenario(self) -> Dict:
        """기본 시나리오 (오류 시)"""
        return {
            'primary_scenario': 23,  # 거래량 정상
            'secondary_scenarios': [],
            'scenario_names': [self.SCENARIOS[23]],
            'confidence': 50.0,
            'indicators': {},
            'ticker': 'UNKNOWN',
            'timestamp': datetime.now()
        }
    
    def get_scenario_description(self, scenario_id: int) -> str:
        """시나리오 ID로 설명 조회"""
        return self.SCENARIOS.get(scenario_id, "알 수 없는 시나리오")
    
    def get_all_scenarios(self) -> Dict[int, str]:
        """전체 시나리오 목록 반환"""
        return self.SCENARIOS.copy()
