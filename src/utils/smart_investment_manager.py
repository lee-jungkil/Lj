"""
스마트 투자 금액 관리 시스템 (Smart Investment Manager)
- 전략별 10단계 점수 기반 매수 금액 결정
- 호가창 유동성 검증 및 슬리피지 방지
- 실시간 잔고 기반 동적 금액 조정
"""

from typing import Dict, Optional, Tuple
import logging


class SmartInvestmentManager:
    """스마트 투자 금액 관리자"""
    
    # 10단계 매수 금액 테이블 (원)
    INVESTMENT_LEVELS = {
        1: 100000,   # 10만원 (최소)
        2: 150000,   # 15만원
        3: 200000,   # 20만원
        4: 300000,   # 30만원
        5: 500000,   # 50만원
        6: 700000,   # 70만원
        7: 1000000,  # 100만원
        8: 1500000,  # 150만원
        9: 2000000,  # 200만원
        10: 3000000  # 300만원 (최대)
    }
    
    def __init__(self, logger=None):
        """초기화"""
        self.logger = logger or logging.getLogger(__name__)
        
        # 전략별 기본 점수 (1~10)
        self.strategy_scores = {
            'aggressive_scalping': 4,    # 30만원
            'conservative_scalping': 5,  # 50만원
            'mean_reversion': 6,         # 70만원
            'grid_trading': 5,           # 50만원
            'ultra_scalping': 3,         # 20만원 (빠른 진입/퇴출)
        }
        
        self.logger.info("✅ SmartInvestmentManager 초기화 완료")
        self.logger.info(f"📊 투자 단계: {len(self.INVESTMENT_LEVELS)}단계 (10만원 ~ 300만원)")
    
    def get_strategy_score(self, strategy_name: str) -> int:
        """
        전략별 점수 조회
        
        Args:
            strategy_name: 전략 이름
        
        Returns:
            점수 (1~10)
        """
        # 전략 이름 정규화
        strategy_key = strategy_name.lower()
        
        # 별칭 처리
        if 'aggressive' in strategy_key or '공격' in strategy_key:
            strategy_key = 'aggressive_scalping'
        elif 'conservative' in strategy_key or '보수' in strategy_key:
            strategy_key = 'conservative_scalping'
        elif 'mean' in strategy_key or 'reversion' in strategy_key:
            strategy_key = 'mean_reversion'
        elif 'grid' in strategy_key or '그리드' in strategy_key:
            strategy_key = 'grid_trading'
        elif 'ultra' in strategy_key or '초단타' in strategy_key:
            strategy_key = 'ultra_scalping'
        
        # 점수 반환 (기본값: 5)
        return self.strategy_scores.get(strategy_key, 5)
    
    def get_investment_amount(self, strategy_name: str, score: Optional[int] = None) -> int:
        """
        전략에 따른 기본 투자 금액 계산
        
        Args:
            strategy_name: 전략 이름
            score: 직접 지정한 점수 (None이면 전략별 기본 점수 사용)
        
        Returns:
            투자 금액 (원)
        """
        if score is None:
            score = self.get_strategy_score(strategy_name)
        
        # 점수 범위 제한 (1~10)
        score = max(1, min(10, score))
        
        return self.INVESTMENT_LEVELS[score]
    
    def calculate_orderbook_liquidity(self, orderbook: Dict, target_amount: int) -> Tuple[int, float, str]:
        """
        호가창 유동성 분석 및 실제 매수 가능 금액 계산
        
        Args:
            orderbook: 호가창 데이터 {'bids': [...], 'asks': [...]}
            target_amount: 목표 투자 금액 (원)
        
        Returns:
            (실제_매수_금액, 슬리피지_예상%, 위험도)
        """
        if not orderbook or 'asks' not in orderbook:
            # 호가창 없으면 목표 금액의 50%만 허용
            return int(target_amount * 0.5), 0.0, 'HIGH'
        
        asks = orderbook.get('asks', [])
        if not asks:
            return int(target_amount * 0.5), 0.0, 'HIGH'
        
        # 매도호가(asks) 분석
        total_liquidity = 0  # 누적 유동성 (원)
        best_ask_price = asks[0]['price'] if asks else 0
        
        for level in asks[:10]:  # 상위 10호가까지 분석
            price = level['price']
            size = level['size']
            liquidity = price * size
            total_liquidity += liquidity
        
        # 실제 매수 가능 금액 계산
        available_amount = min(int(total_liquidity * 0.3), target_amount)  # 유동성의 30%까지만
        
        # 슬리피지 예상 계산
        if best_ask_price > 0 and len(asks) > 5:
            avg_price = sum(a['price'] for a in asks[:5]) / 5
            slippage = ((avg_price - best_ask_price) / best_ask_price) * 100
        else:
            slippage = 0.0
        
        # 위험도 판단
        if available_amount >= target_amount:
            risk = 'LOW'
        elif available_amount >= target_amount * 0.7:
            risk = 'MEDIUM'
        else:
            risk = 'HIGH'
        
        return available_amount, slippage, risk
    
    def get_safe_investment_amount(
        self, 
        strategy_name: str, 
        orderbook: Optional[Dict] = None,
        current_balance: float = 0,
        score: Optional[int] = None
    ) -> Tuple[int, Dict]:
        """
        호가창 검증 후 안전한 투자 금액 결정
        
        Args:
            strategy_name: 전략 이름
            orderbook: 호가창 데이터 (선택)
            current_balance: 현재 잔고 (원)
            score: 직접 지정한 점수 (선택)
        
        Returns:
            (최종_투자_금액, 분석_정보)
        """
        # 1단계: 전략별 기본 금액
        target_amount = self.get_investment_amount(strategy_name, score)
        
        # 2단계: 잔고 확인
        if current_balance > 0:
            max_by_balance = int(current_balance * 0.3)  # 잔고의 30%까지
            if target_amount > max_by_balance:
                target_amount = max_by_balance
                self.logger.info(
                    f"⚠️ [{strategy_name}] 잔고 부족으로 금액 조정: {target_amount:,}원"
                )
        
        # 3단계: 호가창 검증
        if orderbook:
            safe_amount, slippage, risk = self.calculate_orderbook_liquidity(
                orderbook, target_amount
            )
            
            analysis = {
                'target_amount': target_amount,
                'safe_amount': safe_amount,
                'slippage': slippage,
                'risk': risk,
                'adjustment': safe_amount - target_amount,
                'adjustment_pct': ((safe_amount - target_amount) / target_amount * 100) if target_amount > 0 else 0
            }
            
            # 로그 출력
            if safe_amount < target_amount:
                self.logger.warning(
                    f"⚠️ [{strategy_name}] 호가창 유동성 부족: "
                    f"{target_amount:,}원 → {safe_amount:,}원 "
                    f"(슬리피지: {slippage:.2f}%, 위험도: {risk})"
                )
            else:
                self.logger.info(
                    f"✅ [{strategy_name}] 호가창 유동성 충분: {safe_amount:,}원 "
                    f"(슬리피지: {slippage:.2f}%, 위험도: {risk})"
                )
            
            return safe_amount, analysis
        else:
            # 호가창 없으면 목표 금액 그대로
            analysis = {
                'target_amount': target_amount,
                'safe_amount': target_amount,
                'slippage': 0.0,
                'risk': 'UNKNOWN',
                'adjustment': 0,
                'adjustment_pct': 0.0
            }
            
            return target_amount, analysis
    
    def update_strategy_score(self, strategy_name: str, new_score: int) -> bool:
        """
        전략 점수 업데이트
        
        Args:
            strategy_name: 전략 이름
            new_score: 새 점수 (1~10)
        
        Returns:
            성공 여부
        """
        strategy_key = strategy_name.lower()
        
        # 점수 범위 검증
        if not 1 <= new_score <= 10:
            self.logger.error(f"❌ 잘못된 점수: {new_score} (1~10 범위)")
            return False
        
        # 점수 업데이트
        old_score = self.strategy_scores.get(strategy_key, 5)
        self.strategy_scores[strategy_key] = new_score
        
        old_amount = self.INVESTMENT_LEVELS[old_score]
        new_amount = self.INVESTMENT_LEVELS[new_score]
        
        self.logger.info(
            f"✅ [{strategy_name}] 점수 업데이트: "
            f"{old_score} → {new_score} "
            f"({old_amount:,}원 → {new_amount:,}원)"
        )
        
        return True
    
    def get_all_strategy_info(self) -> Dict:
        """
        모든 전략 정보 조회
        
        Returns:
            전략별 점수 및 금액 정보
        """
        info = {}
        
        for strategy, score in self.strategy_scores.items():
            amount = self.INVESTMENT_LEVELS[score]
            info[strategy] = {
                'score': score,
                'amount': amount,
                'amount_formatted': f"{amount:,}원"
            }
        
        return info
    
    def print_investment_table(self):
        """투자 금액 테이블 출력"""
        print("\n" + "=" * 70)
        print("📊 스마트 투자 금액 시스템 (10단계)")
        print("=" * 70)
        
        print("\n[전략별 설정]")
        print("-" * 70)
        for strategy, score in sorted(self.strategy_scores.items()):
            amount = self.INVESTMENT_LEVELS[score]
            print(f"  {strategy:25s} | 점수: {score:2d} | 금액: {amount:>10,}원")
        
        print("\n[점수별 금액 테이블]")
        print("-" * 70)
        for level, amount in self.INVESTMENT_LEVELS.items():
            print(f"  점수 {level:2d} → {amount:>10,}원")
        
        print("\n" + "=" * 70)
