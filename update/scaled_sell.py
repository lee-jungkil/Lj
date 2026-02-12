"""
Scaled Sell System (분할 매도 시스템)
- 여러 가격 레벨에서 순차적 매도
- 수익 극대화 및 리스크 분산
- 레벨별 매도 비율 설정
- 실시간 매도 진행 상황 추적

⭐ v6.30 Integration Phase 2B

Example:
    SCALED_SELL_LEVELS="2.0:30,4.0:40,6.0:30"
    → 수익 +2% 도달 시 30% 매도
    → 수익 +4% 도달 시 40% 매도
    → 수익 +6% 도달 시 30% 매도
"""

from typing import Dict, Optional, List
from dataclasses import dataclass
import os


@dataclass
class SellLevel:
    """매도 레벨 정의"""
    profit_threshold: float  # 수익 임계값 (%)
    sell_percentage: float   # 매도 비율 (0.0 ~ 1.0)
    is_executed: bool = False  # 실행 여부


class ScaledSellManager:
    """분할 매도 관리 시스템"""
    
    def __init__(self, config):
        """
        초기화
        
        Args:
            config: Config 객체
        """
        self.config = config
        self.enabled = os.getenv('ENABLE_SCALED_SELL', 'true').lower() == 'true'
        
        # 매도 레벨 파싱
        self.levels = self._parse_levels()
        
        # 포지션별 매도 진행 상황
        self.position_progress = {}  # {ticker: [executed_level_indices]}
    
    def _parse_levels(self) -> List[SellLevel]:
        """
        환경변수에서 매도 레벨 파싱
        
        Example:
            SCALED_SELL_LEVELS="2.0:30,4.0:40,6.0:30"
            → [
                SellLevel(2.0, 0.30),
                SellLevel(4.0, 0.40),
                SellLevel(6.0, 0.30)
              ]
        
        Returns:
            매도 레벨 리스트
        """
        levels_str = os.getenv('SCALED_SELL_LEVELS', '2.0:30,4.0:40,6.0:30')
        levels = []
        
        try:
            for level in levels_str.split(','):
                profit_pct, sell_pct = level.split(':')
                levels.append(SellLevel(
                    profit_threshold=float(profit_pct),
                    sell_percentage=float(sell_pct) / 100
                ))
            
            # 수익 임계값 기준 정렬
            levels.sort(key=lambda x: x.profit_threshold)
            
            # 검증: 총 매도 비율이 100%인지 확인
            total_pct = sum(level.sell_percentage for level in levels)
            if abs(total_pct - 1.0) > 0.01:
                print(f"⚠️ 분할 매도 비율 합계 오류: {total_pct*100:.1f}% (100%여야 함)")
                print(f"   → 비율 자동 조정")
                # 정규화
                for level in levels:
                    level.sell_percentage /= total_pct
            
            return levels
        
        except Exception as e:
            print(f"❌ 분할 매도 레벨 파싱 오류: {e}")
            print(f"   → 기본값 사용: 2%@30%, 4%@40%, 6%@30%")
            return [
                SellLevel(2.0, 0.30),
                SellLevel(4.0, 0.40),
                SellLevel(6.0, 0.30)
            ]
    
    def should_sell_partial(self, ticker: str, current_price: float, 
                           entry_price: float, remaining_amount: float) -> Optional[Dict]:
        """
        분할 매도 실행 여부 확인
        
        Args:
            ticker: 코인 티커
            current_price: 현재 가격
            entry_price: 진입 가격
            remaining_amount: 남은 수량
        
        Returns:
            {
                'level_index': int,
                'sell_percentage': float,
                'sell_amount': float,
                'profit_threshold': float,
                'reason': str
            } 또는 None
        """
        if not self.enabled:
            return None
        
        # 수익률 계산
        profit_ratio = ((current_price - entry_price) / entry_price) * 100
        
        # 포지션 진행 상황 가져오기
        if ticker not in self.position_progress:
            self.position_progress[ticker] = []
        
        executed_levels = self.position_progress[ticker]
        
        # 각 레벨 체크
        for i, level in enumerate(self.levels):
            # 이미 실행된 레벨은 스킵
            if i in executed_levels:
                continue
            
            # 수익 임계값 도달 체크
            if profit_ratio >= level.profit_threshold:
                # 매도 수량 계산
                sell_amount = remaining_amount * level.sell_percentage
                
                return {
                    'level_index': i,
                    'sell_percentage': level.sell_percentage,
                    'sell_amount': sell_amount,
                    'profit_threshold': level.profit_threshold,
                    'reason': f"분할매도 Level {i+1}: +{level.profit_threshold}% ({level.sell_percentage*100:.0f}% 매도)"
                }
        
        return None
    
    def mark_level_executed(self, ticker: str, level_index: int):
        """
        레벨 실행 완료 표시
        
        Args:
            ticker: 코인 티커
            level_index: 레벨 인덱스
        """
        if ticker not in self.position_progress:
            self.position_progress[ticker] = []
        
        if level_index not in self.position_progress[ticker]:
            self.position_progress[ticker].append(level_index)
    
    def reset_position(self, ticker: str):
        """
        포지션 진행 상황 초기화 (완전 청산 시)
        
        Args:
            ticker: 코인 티커
        """
        if ticker in self.position_progress:
            del self.position_progress[ticker]
    
    def get_progress(self, ticker: str) -> Dict:
        """
        매도 진행 상황 조회
        
        Args:
            ticker: 코인 티커
        
        Returns:
            {
                'total_levels': int,
                'executed_levels': int,
                'remaining_levels': int,
                'next_threshold': float or None,
                'total_sold_percentage': float
            }
        """
        if ticker not in self.position_progress:
            return {
                'total_levels': len(self.levels),
                'executed_levels': 0,
                'remaining_levels': len(self.levels),
                'next_threshold': self.levels[0].profit_threshold if self.levels else None,
                'total_sold_percentage': 0.0
            }
        
        executed_levels = self.position_progress[ticker]
        executed_count = len(executed_levels)
        
        # 총 매도 비율 계산
        total_sold_pct = sum(
            self.levels[i].sell_percentage 
            for i in executed_levels
        )
        
        # 다음 레벨 찾기
        next_threshold = None
        for i, level in enumerate(self.levels):
            if i not in executed_levels:
                next_threshold = level.profit_threshold
                break
        
        return {
            'total_levels': len(self.levels),
            'executed_levels': executed_count,
            'remaining_levels': len(self.levels) - executed_count,
            'next_threshold': next_threshold,
            'total_sold_percentage': total_sold_pct
        }
    
    def is_fully_executed(self, ticker: str) -> bool:
        """
        모든 레벨 실행 완료 여부
        
        Args:
            ticker: 코인 티커
        
        Returns:
            완료 여부
        """
        if ticker not in self.position_progress:
            return False
        
        executed_count = len(self.position_progress[ticker])
        return executed_count >= len(self.levels)
    
    def get_remaining_percentage(self, ticker: str) -> float:
        """
        남은 수량 비율 계산
        
        Args:
            ticker: 코인 티커
        
        Returns:
            남은 비율 (0.0 ~ 1.0)
        """
        progress = self.get_progress(ticker)
        return 1.0 - progress['total_sold_percentage']
    
    def calculate_average_exit_price(self, ticker: str, 
                                     executed_prices: List[float]) -> float:
        """
        평균 청산 가격 계산
        
        Args:
            ticker: 코인 티커
            executed_prices: 레벨별 실행 가격 리스트
        
        Returns:
            가중 평균 청산 가격
        """
        if ticker not in self.position_progress:
            return 0.0
        
        executed_levels = self.position_progress[ticker]
        
        if len(executed_prices) != len(executed_levels):
            print("⚠️ 실행 가격 데이터 불일치")
            return sum(executed_prices) / len(executed_prices) if executed_prices else 0.0
        
        # 가중 평균 계산
        total_weighted_price = 0.0
        total_weight = 0.0
        
        for i, level_idx in enumerate(executed_levels):
            level = self.levels[level_idx]
            weight = level.sell_percentage
            price = executed_prices[i]
            
            total_weighted_price += price * weight
            total_weight += weight
        
        return total_weighted_price / total_weight if total_weight > 0 else 0.0
    
    def get_status_message(self, ticker: str) -> str:
        """
        상태 메시지 생성
        
        Args:
            ticker: 코인 티커
        
        Returns:
            상태 메시지
        """
        progress = self.get_progress(ticker)
        
        if progress['executed_levels'] == 0:
            return f"분할매도 대기 (첫 레벨: +{progress['next_threshold']}%)"
        elif progress['executed_levels'] == progress['total_levels']:
            return f"분할매도 완료 ({progress['total_sold_percentage']*100:.0f}%)"
        else:
            return (f"분할매도 진행 중 "
                   f"({progress['executed_levels']}/{progress['total_levels']} 레벨, "
                   f"다음: +{progress['next_threshold']}%)")
    
    def get_config_summary(self) -> str:
        """
        설정 요약 정보
        
        Returns:
            설정 요약 문자열
        """
        if not self.enabled:
            return "분할 매도: 비활성화"
        
        level_strs = [
            f"+{level.profit_threshold}%@{level.sell_percentage*100:.0f}%"
            for level in self.levels
        ]
        
        return f"분할 매도: {' → '.join(level_strs)}"
