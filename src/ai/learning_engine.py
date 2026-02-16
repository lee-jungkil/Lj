"""
AI 학습 엔진
매매 경험을 축적하고 패턴을 분석하여 전략을 자동 최적화
"""

import json
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, asdict, field
from collections import defaultdict, deque


@dataclass
class TradeExperience:
    """거래 경험 데이터 (⭐ v6.29 확장: order_method, exit_reason, surge_score)"""
    # 거래 기본 정보
    timestamp: str
    ticker: str
    strategy: str
    action: str  # BUY, SELL
    
    # 진입 정보
    entry_price: float
    entry_amount: float
    
    # 청산 정보 (매도 시)
    exit_price: Optional[float] = None
    profit_loss: Optional[float] = None
    profit_loss_ratio: Optional[float] = None
    holding_duration: Optional[float] = None  # 초
    
    # ⭐ v6.29 신규 필드
    order_method: Optional[str] = None  # 주문 방식 (market, limit, best, etc.)
    exit_reason: Optional[str] = None  # 청산 사유 (stop_loss, take_profit, trailing_stop, etc.)
    surge_score: Optional[float] = None  # 급등 점수 (추격매수 시)
    confidence: Optional[float] = None  # 신뢰도
    slippage_pct: Optional[float] = None  # 슬리피지 (%)
    spread_pct: Optional[float] = None  # 스프레드 (%)
    
    # ⭐ v6.29.5 추가: 보유 중 차트 신호 및 청산 조건
    holding_chart_signals: List[Dict] = field(default_factory=list)  # 보유 중 차트 신호 이력
    exit_chart_condition: Dict = field(default_factory=dict)  # 청산 시 차트 조건
    liquidity_at_entry: Optional[str] = None  # 진입 시 유동성 (low/medium/high)
    liquidity_at_exit: Optional[str] = None  # 청산 시 유동성
    risk_score_at_check: Optional[float] = None  # 포지션 체크 시 리스크 점수
    
    # 시장 상황 (진입 시점)
    market_condition: Dict = None
    
    # 결과
    success: Optional[bool] = None  # 수익 여부
    
    def to_dict(self) -> Dict:
        """딕셔너리 변환"""
        return asdict(self)


@dataclass
class MarketSnapshot:
    """시장 상황 스냅샷"""
    # 가격 정보
    price: float
    price_change_1m: float
    price_change_5m: float
    price_change_15m: float
    
    # 기술적 지표
    rsi: float
    macd: float
    macd_signal: float
    bb_position: float  # 볼린저 밴드 내 위치 (0~1)
    
    # 거래량
    volume_ratio: float  # 평균 대비 거래량
    volume_spike: bool  # 거래량 급증 여부
    
    # 추세
    trend: str  # 'up', 'down', 'sideways'
    trend_strength: float  # 0~1
    
    # 변동성
    volatility: float  # 변동성 지표
    
    # 시장 상태
    market_phase: str  # 'bullish', 'bearish', 'neutral'
    
    def to_dict(self) -> Dict:
        """딕셔너리 변환"""
        return asdict(self)


class LearningEngine:
    """AI 학습 엔진 클래스"""
    
    def __init__(self, data_dir: str = "trading_logs/learning"):
        """
        초기화
        
        Args:
            data_dir: 학습 데이터 저장 디렉토리
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # 경험 데이터베이스
        self.experiences: List[TradeExperience] = []
        self.max_experiences = 10000  # 최대 저장 경험 수
        
        # 전략별 성과 통계
        self.strategy_stats: Dict[str, Dict] = defaultdict(lambda: {
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'total_profit_loss': 0.0,
            'avg_profit_ratio': 0.0,
            'avg_holding_duration': 0.0,
            'success_rate': 0.0,
            'best_market_conditions': [],
            'worst_market_conditions': [],
        })
        
        # 패턴 분석 결과
        self.learned_patterns: Dict[str, List[Dict]] = defaultdict(list)
        
        # 최적 파라미터 (전략별)
        self.optimized_params: Dict[str, Dict] = {}
        
        # 최근 성과 트래킹 (30일)
        self.recent_performance: Dict[str, deque] = defaultdict(lambda: deque(maxlen=30))
        
        # 학습 설정
        self.min_experiences_for_learning = 20  # 학습 최소 경험 수
        self.learning_rate = 0.1  # 파라미터 조정 비율
        
        # 데이터 로드
        self.load_experiences()
        self.load_strategy_stats()
        self.load_optimized_params()
        
        print(f"🧠 AI 학습 엔진 초기화")
        print(f"   저장된 경험: {len(self.experiences)}개")
        print(f"   학습된 전략: {len(self.strategy_stats)}개")
    
    def analyze_market_decision(self, 
                                ticker: str,
                                df,
                                strategy: str,
                                current_indicators: Dict) -> Tuple[str, float, str]:
        """
        매수/매도 판단 분석 (AI 의사결정)
        
        Args:
            ticker: 코인 티커
            df: OHLCV 데이터프레임
            strategy: 전략 이름
            current_indicators: 현재 기술 지표
        
        Returns:
            (결정, 신뢰도, 사유)
        """
        # 현재 시장 상황 분석
        market_snapshot = self._create_market_snapshot(df, current_indicators)
        
        # 과거 유사 상황에서의 성과 조회
        similar_experiences = self._find_similar_situations(
            strategy, 
            market_snapshot
        )
        
        if len(similar_experiences) < 5:
            # 경험 부족 → 기본 전략 따름
            return 'NEUTRAL', 0.5, "경험 부족, 기본 전략 사용"
        
        # 유사 상황 성과 분석
        success_count = sum(1 for exp in similar_experiences if exp.success)
        success_rate = success_count / len(similar_experiences)
        
        avg_profit = np.mean([
            exp.profit_loss_ratio 
            for exp in similar_experiences 
            if exp.profit_loss_ratio is not None
        ])
        
        # 의사결정 (⭐ v6.31.6: 승률 임계값 10% 상향)
        if success_rate >= 0.715:  # 71.5% 이상 승률 (65% → 71.5%)
            if avg_profit > 0:
                confidence = min(success_rate, 0.95)
                reason = f"유사 상황 성공률 {success_rate*100:.1f}% (평균 수익 {avg_profit:+.2f}%)"
                return 'STRONG_BUY', confidence, reason
            else:
                confidence = success_rate * 0.8
                reason = f"유사 상황 성공률 {success_rate*100:.1f}% (수익 제한적)"
                return 'BUY', confidence, reason
        
        elif success_rate <= 0.35:  # 35% 이하 승률
            confidence = min(1 - success_rate, 0.95)
            reason = f"유사 상황 실패율 {(1-success_rate)*100:.1f}% (평균 손실 {avg_profit:+.2f}%)"
            return 'AVOID', confidence, reason
        
        else:
            # 중립 구간
            confidence = 0.5
            reason = f"유사 상황 성공률 {success_rate*100:.1f}% (불확실)"
            return 'NEUTRAL', confidence, reason
    
    def should_exit_position(self,
                            ticker: str,
                            strategy: str,
                            entry_price: float,
                            current_price: float,
                            holding_duration: float,
                            market_snapshot: MarketSnapshot) -> Tuple[bool, str, float]:
        """
        청산 판단 분석 (AI 의사결정)
        
        Args:
            ticker: 코인 티커
            strategy: 전략 이름
            entry_price: 진입 가격
            current_price: 현재 가격
            holding_duration: 보유 시간 (초)
            market_snapshot: 현재 시장 상황
        
        Returns:
            (청산 여부, 사유, 신뢰도)
        """
        profit_loss_ratio = ((current_price - entry_price) / entry_price) * 100
        
        # 과거 유사 포지션의 결과 분석
        similar_exits = self._find_similar_exit_situations(
            strategy,
            profit_loss_ratio,
            holding_duration,
            market_snapshot
        )
        
        if len(similar_exits) < 5:
            # 경험 부족
            return False, "경험 부족, 기본 규칙 사용", 0.5
        
        # 이 시점에서 청산했을 때 vs 더 보유했을 때 비교
        early_exits = [exp for exp in similar_exits if exp.holding_duration <= holding_duration * 1.2]
        late_exits = [exp for exp in similar_exits if exp.holding_duration > holding_duration * 1.2]
        
        if len(early_exits) >= 3:
            avg_early_profit = np.mean([exp.profit_loss_ratio for exp in early_exits])
            
            if avg_early_profit < profit_loss_ratio * 0.7:
                # 더 보유하는 것이 역사적으로 더 나음
                return False, f"과거 데이터: 더 보유 시 평균 {avg_early_profit:.2f}% 수익", 0.7
        
        if len(late_exits) >= 3:
            avg_late_profit = np.mean([exp.profit_loss_ratio for exp in late_exits])
            
            if profit_loss_ratio > 0 and avg_late_profit < profit_loss_ratio * 0.8:
                # 지금 청산하는 것이 역사적으로 더 나음
                return True, f"과거 데이터: 더 보유 시 수익 감소 경향 ({avg_late_profit:.2f}%)", 0.75
        
        # 추세 반전 감지
        if market_snapshot.trend == 'down' and profit_loss_ratio > 0:
            # 수익 중이지만 하락 추세 시작
            similar_trend_reversals = [
                exp for exp in similar_exits 
                if exp.market_condition and exp.market_condition.get('trend') == 'down'
            ]
            
            if len(similar_trend_reversals) >= 3:
                avg_reversal_profit = np.mean([exp.profit_loss_ratio for exp in similar_trend_reversals])
                if avg_reversal_profit < profit_loss_ratio * 0.9:
                    return True, f"추세 반전 감지, 과거 평균 {avg_reversal_profit:.2f}% → 현재 청산 유리", 0.8
        
        return False, "학습 결과: 보유 유지", 0.6
    
    def record_trade_entry(self,
                          ticker: str,
                          strategy: str,
                          entry_price: float,
                          entry_amount: float,
                          market_condition: Dict,
                          order_method: str = None,
                          surge_score: float = None,
                          confidence: float = None,
                          slippage_pct: float = None,
                          spread_pct: float = None) -> str:
        """
        매수 경험 기록 (⭐ v6.29 확장: 메타데이터 추가)
        
        Args:
            ticker: 코인 티커
            strategy: 전략 이름
            entry_price: 진입 가격
            entry_amount: 매수 수량
            market_condition: 시장 상황
            order_method: 주문 방식 (market, limit, best, etc.)
            surge_score: 급등 점수 (추격매수 시)
            confidence: 신뢰도
            slippage_pct: 슬리피지 (%)
            spread_pct: 스프레드 (%)
        
        Returns:
            경험 ID
        """
        experience = TradeExperience(
            timestamp=datetime.now().isoformat(),
            ticker=ticker,
            strategy=strategy,
            action='BUY',
            entry_price=entry_price,
            entry_amount=entry_amount,
            market_condition=market_condition,
            order_method=order_method,
            surge_score=surge_score,
            confidence=confidence,
            slippage_pct=slippage_pct,
            spread_pct=spread_pct
        )
        
        self.experiences.append(experience)
        
        # 저장 용량 관리
        if len(self.experiences) > self.max_experiences:
            self.experiences = self.experiences[-self.max_experiences:]
        
        # 주기적 저장
        if len(self.experiences) % 10 == 0:
            self.save_experiences()
        
        return experience.timestamp
    
    def record_trade_exit(self,
                         ticker: str,
                         strategy: str,
                         exit_price: float,
                         entry_time: str,
                         market_condition: Dict,
                         exit_reason: str = None):
        """
        매도 경험 기록 및 학습 (⭐ v6.29 확장: exit_reason 추가)
        
        Args:
            ticker: 코인 티커
            strategy: 전략 이름
            exit_price: 청산 가격
            entry_time: 진입 시간
            market_condition: 시장 상황
            exit_reason: 청산 사유 (stop_loss, take_profit, trailing_stop, etc.)
        """
        # 해당 진입 경험 찾기
        for exp in reversed(self.experiences):
            if (exp.ticker == ticker and 
                exp.strategy == strategy and 
                exp.timestamp == entry_time and
                exp.exit_price is None):
                
                # 청산 정보 업데이트
                exp.exit_price = exit_price
                
                # ⭐ v6.31.5: Include trading fees in profit calculation
                # Buy fee: 0.05%, Sell fee: 0.05% = Total 0.1%
                buy_cost = exp.entry_price * exp.entry_amount
                buy_fee = buy_cost * 0.0005  # 0.05%
                sell_revenue = exit_price * exp.entry_amount
                sell_fee = sell_revenue * 0.0005  # 0.05%
                
                # Net profit = sell revenue - sell fee - buy cost - buy fee
                exp.profit_loss = sell_revenue - sell_fee - buy_cost - buy_fee
                exp.profit_loss_ratio = (exp.profit_loss / buy_cost) * 100
                exp.exit_reason = exit_reason  # ⭐ 새로 추가
                
                # 타임스탬프 처리
                if isinstance(exp.timestamp, str):
                    entry_dt = datetime.fromisoformat(exp.timestamp)
                elif isinstance(exp.timestamp, datetime):
                    entry_dt = exp.timestamp
                else:
                    entry_dt = datetime.now()
                
                exp.holding_duration = (datetime.now() - entry_dt).total_seconds()
                
                exp.success = exp.profit_loss > 0
                
                # 전략 통계 업데이트
                self._update_strategy_stats(strategy, exp)
                
                # 학습 실행
                self._learn_from_experience(exp)
                
                # 저장
                self.save_experiences()
                self.save_strategy_stats()
                
                print(f"\n📚 학습 완료: {strategy} | {ticker}")
                print(f"   수익: {exp.profit_loss_ratio:+.2f}% | 보유: {exp.holding_duration:.0f}초")
                
                break
    
    def get_optimized_params(self, strategy: str) -> Optional[Dict]:
        """
        학습된 최적 파라미터 조회
        
        Args:
            strategy: 전략 이름
        
        Returns:
            최적 파라미터 딕셔너리 (없으면 None)
        """
        if strategy not in self.optimized_params:
            return None
        
        params = self.optimized_params[strategy]
        
        # 신뢰도 확인
        if params.get('confidence', 0) < 0.6:
            return None
        
        return params.get('params', {})
    
    def _create_market_snapshot(self, df, indicators: Dict) -> MarketSnapshot:
        """시장 상황 스냅샷 생성"""
        # 가격 변화율 계산
        price = df['close'].iloc[-1]
        price_1m = df['close'].iloc[-2] if len(df) >= 2 else price
        price_5m = df['close'].iloc[-6] if len(df) >= 6 else price
        price_15m = df['close'].iloc[-16] if len(df) >= 16 else price
        
        price_change_1m = ((price - price_1m) / price_1m * 100) if price_1m > 0 else 0
        price_change_5m = ((price - price_5m) / price_5m * 100) if price_5m > 0 else 0
        price_change_15m = ((price - price_15m) / price_15m * 100) if price_15m > 0 else 0
        
        # 추세 판단
        if price_change_5m > 1:
            trend = 'up'
            trend_strength = min(abs(price_change_5m) / 5, 1.0)
        elif price_change_5m < -1:
            trend = 'down'
            trend_strength = min(abs(price_change_5m) / 5, 1.0)
        else:
            trend = 'sideways'
            trend_strength = 0.3
        
        # 변동성 계산
        volatility = df['close'].pct_change().std() * 100
        
        # 시장 상태
        rsi = indicators.get('rsi', 50)
        if rsi > 60 and trend == 'up':
            market_phase = 'bullish'
        elif rsi < 40 and trend == 'down':
            market_phase = 'bearish'
        else:
            market_phase = 'neutral'
        
        return MarketSnapshot(
            price=price,
            price_change_1m=price_change_1m,
            price_change_5m=price_change_5m,
            price_change_15m=price_change_15m,
            rsi=indicators.get('rsi', 50),
            macd=indicators.get('macd', 0),
            macd_signal=indicators.get('macd_signal', 0),
            bb_position=indicators.get('bb_position', 0.5),
            volume_ratio=indicators.get('volume_ratio', 1.0),
            volume_spike=indicators.get('volume_ratio', 1.0) > 2.0,
            trend=trend,
            trend_strength=trend_strength,
            volatility=volatility,
            market_phase=market_phase
        )
    
    def _find_similar_situations(self, 
                                 strategy: str, 
                                 current_market: MarketSnapshot,
                                 max_results: int = 20) -> List[TradeExperience]:
        """유사한 시장 상황 찾기"""
        similar = []
        
        for exp in self.experiences:
            if exp.strategy != strategy or not exp.market_condition:
                continue
            
            if exp.exit_price is None:  # 아직 청산되지 않은 경험
                continue
            
            mc = exp.market_condition
            
            # 유사도 계산
            similarity_score = 0
            
            # RSI 유사도 (±10 범위)
            rsi_diff = abs(mc.get('rsi', 50) - current_market.rsi)
            if rsi_diff <= 10:
                similarity_score += (10 - rsi_diff) / 10 * 0.3
            
            # 추세 유사도
            if mc.get('trend') == current_market.trend:
                similarity_score += 0.25
            
            # 변동성 유사도
            vol_diff = abs(mc.get('volatility', 1) - current_market.volatility)
            if vol_diff <= 2:
                similarity_score += (2 - vol_diff) / 2 * 0.2
            
            # 거래량 유사도
            vol_ratio_diff = abs(mc.get('volume_ratio', 1) - current_market.volume_ratio)
            if vol_ratio_diff <= 1:
                similarity_score += (1 - vol_ratio_diff) * 0.15
            
            # 시장 상태 유사도
            if mc.get('market_phase') == current_market.market_phase:
                similarity_score += 0.1
            
            # 유사도 임계값
            if similarity_score >= 0.6:
                similar.append(exp)
        
        # 유사도 높은 순으로 정렬
        similar.sort(key=lambda x: self._calculate_similarity(x.market_condition, current_market), reverse=True)
        
        return similar[:max_results]
    
    def _find_similar_exit_situations(self,
                                      strategy: str,
                                      current_profit_ratio: float,
                                      current_holding_duration: float,
                                      current_market: MarketSnapshot,
                                      max_results: int = 15) -> List[TradeExperience]:
        """유사한 청산 상황 찾기"""
        similar = []
        
        for exp in self.experiences:
            if (exp.strategy != strategy or 
                exp.exit_price is None or 
                exp.profit_loss_ratio is None):
                continue
            
            # 수익률 범위 (±2%)
            profit_diff = abs(exp.profit_loss_ratio - current_profit_ratio)
            if profit_diff > 2.0:
                continue
            
            # 보유 시간 범위 (±50%)
            duration_diff = abs(exp.holding_duration - current_holding_duration) / current_holding_duration
            if duration_diff > 0.5:
                continue
            
            similar.append(exp)
        
        return similar[:max_results]
    
    def _calculate_similarity(self, market_cond: Dict, current_market: MarketSnapshot) -> float:
        """시장 상황 유사도 계산"""
        score = 0
        
        rsi_diff = abs(market_cond.get('rsi', 50) - current_market.rsi)
        score += max(0, 1 - rsi_diff / 50) * 0.3
        
        if market_cond.get('trend') == current_market.trend:
            score += 0.3
        
        vol_diff = abs(market_cond.get('volatility', 1) - current_market.volatility)
        score += max(0, 1 - vol_diff / 5) * 0.2
        
        if market_cond.get('market_phase') == current_market.market_phase:
            score += 0.2
        
        return score
    
    def _update_strategy_stats(self, strategy: str, experience: TradeExperience):
        """전략 통계 업데이트"""
        stats = self.strategy_stats[strategy]
        
        stats['total_trades'] += 1
        
        if experience.success:
            stats['winning_trades'] += 1
        else:
            stats['losing_trades'] += 1
        
        stats['total_profit_loss'] += experience.profit_loss or 0
        
        # 평균 계산
        total_trades = stats['total_trades']
        stats['avg_profit_ratio'] = (
            (stats['avg_profit_ratio'] * (total_trades - 1) + (experience.profit_loss_ratio or 0)) / total_trades
        )
        stats['avg_holding_duration'] = (
            (stats['avg_holding_duration'] * (total_trades - 1) + (experience.holding_duration or 0)) / total_trades
        )
        stats['success_rate'] = (stats['winning_trades'] / total_trades) * 100
        
        # 최근 성과 추가
        self.recent_performance[strategy].append({
            'timestamp': experience.timestamp,
            'profit_loss_ratio': experience.profit_loss_ratio,
            'success': experience.success
        })
    
    def _learn_from_experience(self, experience: TradeExperience):
        """경험으로부터 학습"""
        strategy = experience.strategy
        
        # 충분한 경험이 쌓였는지 확인
        strategy_experiences = [
            exp for exp in self.experiences 
            if exp.strategy == strategy and exp.exit_price is not None
        ]
        
        if len(strategy_experiences) < self.min_experiences_for_learning:
            return
        
        # 최적 파라미터 찾기
        self._optimize_strategy_params(strategy, strategy_experiences)
    
    def _optimize_strategy_params(self, strategy: str, experiences: List[TradeExperience]):
        """전략 파라미터 최적화"""
        if len(experiences) < self.min_experiences_for_learning:
            return
        
        # 성공/실패 패턴 분석
        successful = [exp for exp in experiences if exp.success]
        failed = [exp for exp in experiences if not exp.success]
        
        if len(successful) < 5:
            return
        
        # 성공한 거래의 평균 보유 시간
        avg_success_duration = np.mean([exp.holding_duration for exp in successful])
        
        # 성공한 거래의 평균 수익률
        avg_success_profit = np.mean([exp.profit_loss_ratio for exp in successful])
        
        # 실패한 거래의 평균 손실률
        avg_failed_loss = np.mean([exp.profit_loss_ratio for exp in failed]) if failed else 0
        
        # 최적 손절/익절 비율 계산
        optimal_stop_loss = abs(avg_failed_loss) * 0.8  # 평균 손실의 80%에서 손절
        optimal_take_profit = avg_success_profit * 1.1  # 평균 수익의 110%에서 익절
        
        # 최적 RSI 범위
        successful_rsi = [
            exp.market_condition.get('rsi', 50) 
            for exp in successful 
            if exp.market_condition
        ]
        
        if len(successful_rsi) >= 5:
            optimal_rsi_low = np.percentile(successful_rsi, 25)
            optimal_rsi_high = np.percentile(successful_rsi, 75)
        else:
            optimal_rsi_low = 40
            optimal_rsi_high = 60
        
        # 신뢰도 계산
        success_rate = len(successful) / len(experiences)
        confidence = min(success_rate * 1.2, 0.95)
        
        # 최적 파라미터 저장
        self.optimized_params[strategy] = {
            'params': {
                'stop_loss': max(0.005, min(optimal_stop_loss / 100, 0.05)),  # 0.5% ~ 5%
                'take_profit': max(0.01, min(optimal_take_profit / 100, 0.10)),  # 1% ~ 10%
                'rsi_low': max(20, min(optimal_rsi_low, 40)),
                'rsi_high': max(60, min(optimal_rsi_high, 80)),
                'avg_holding_duration': avg_success_duration,
            },
            'confidence': confidence,
            'based_on_trades': len(experiences),
            'success_rate': success_rate * 100,
            'last_updated': datetime.now().isoformat()
        }
        
        self.save_optimized_params()
        
        print(f"\n🎓 전략 최적화 완료: {strategy}")
        print(f"   기반 거래: {len(experiences)}개 (성공: {len(successful)}, 실패: {len(failed)})")
        print(f"   신뢰도: {confidence*100:.1f}%")
        print(f"   최적 손절: {optimal_stop_loss:.2f}%")
        print(f"   최적 익절: {optimal_take_profit:.2f}%")
    
    def get_strategy_performance_report(self, strategy: str) -> Dict:
        """전략 성과 리포트"""
        if strategy not in self.strategy_stats:
            return {}
        
        stats = self.strategy_stats[strategy]
        recent = self.recent_performance.get(strategy, [])
        
        # 최근 30일 성과
        recent_success_rate = (
            sum(1 for p in recent if p.get('success')) / len(recent) * 100
            if recent else 0
        )
        
        recent_avg_profit = (
            np.mean([p.get('profit_loss_ratio', 0) for p in recent])
            if recent else 0
        )
        
        return {
            'strategy': strategy,
            'total_trades': stats['total_trades'],
            'success_rate': stats['success_rate'],
            'avg_profit_ratio': stats['avg_profit_ratio'],
            'total_profit_loss': stats['total_profit_loss'],
            'avg_holding_duration': stats['avg_holding_duration'],
            'recent_30d_success_rate': recent_success_rate,
            'recent_30d_avg_profit': recent_avg_profit,
            'has_optimized_params': strategy in self.optimized_params,
        }
    
    # === 데이터 저장/로드 ===
    
    def save_experiences(self):
        """경험 데이터 저장"""
        file_path = self.data_dir / "experiences.json"
        
        experiences_dict = [exp.to_dict() for exp in self.experiences]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(experiences_dict, f, ensure_ascii=False, indent=2)
    
    def load_experiences(self):
        """경험 데이터 로드"""
        file_path = self.data_dir / "experiences.json"
        
        if not file_path.exists():
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                experiences_dict = json.load(f)
            
            self.experiences = [
                TradeExperience(**exp) 
                for exp in experiences_dict
            ]
        except Exception as e:
            print(f"⚠️  경험 데이터 로드 실패: {e}")
    
    def save_strategy_stats(self):
        """전략 통계 저장"""
        file_path = self.data_dir / "strategy_stats.json"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(dict(self.strategy_stats), f, ensure_ascii=False, indent=2)
    
    def load_strategy_stats(self):
        """전략 통계 로드"""
        file_path = self.data_dir / "strategy_stats.json"
        
        if not file_path.exists():
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                stats_dict = json.load(f)
            
            self.strategy_stats = defaultdict(lambda: {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'total_profit_loss': 0.0,
                'avg_profit_ratio': 0.0,
                'avg_holding_duration': 0.0,
                'success_rate': 0.0,
            }, stats_dict)
        except Exception as e:
            print(f"⚠️  전략 통계 로드 실패: {e}")
    
    def save_optimized_params(self):
        """최적 파라미터 저장"""
        file_path = self.data_dir / "optimized_params.json"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.optimized_params, f, ensure_ascii=False, indent=2)
    
    def load_optimized_params(self):
        """최적 파라미터 로드"""
        file_path = self.data_dir / "optimized_params.json"
        
        if not file_path.exists():
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.optimized_params = json.load(f)
        except Exception as e:
            print(f"⚠️  최적 파라미터 로드 실패: {e}")
    
    def get_stats(self) -> Dict:
        """
        AI 학습 통계 조회 (화면 표시용)
        
        Returns:
            Dict: 통계 정보
                - total_trades: 총 거래 수
                - profit_trades: 수익 거래 수
                - loss_trades: 손실 거래 수
                - win_rate: 승률 (%)
        """
        # 모든 전략의 통계 합산
        total_trades = 0
        profit_trades = 0
        loss_trades = 0
        
        for strategy_name, stats in self.strategy_stats.items():
            total_trades += stats.get('total_trades', 0)
            profit_trades += stats.get('winning_trades', 0)
            loss_trades += stats.get('losing_trades', 0)
        
        # 승률 계산
        win_rate = (profit_trades / total_trades * 100) if total_trades > 0 else 0.0
        
        return {
            'total_trades': total_trades,
            'profit_trades': profit_trades,
            'loss_trades': loss_trades,
            'win_rate': win_rate
        }
    
    def record_holding_chart_signal(self, ticker: str, strategy: str, 
                                    chart_signal: Dict, market_snapshot: Dict):
        """
        보유 중 차트 신호 기록
        
        Args:
            ticker: 코인 티커
            strategy: 전략 이름
            chart_signal: 차트 신호 (RSI, MACD 등)
            market_snapshot: 시장 스냅샷
        """
        # 해당 진입 경험 찾기
        for exp in reversed(self.experiences):
            if (exp.ticker == ticker and 
                exp.strategy == strategy and 
                exp.exit_price is None):  # 아직 청산되지 않은 포지션
                
                # 차트 신호 추가
                signal_record = {
                    'timestamp': datetime.now().isoformat(),
                    'rsi': chart_signal.get('rsi'),
                    'macd_direction': chart_signal.get('macd_direction'),
                    'volume_ratio': chart_signal.get('volume_ratio'),
                    'price': market_snapshot.get('price'),
                    'profit_ratio': market_snapshot.get('profit_ratio')
                }
                
                exp.holding_chart_signals.append(signal_record)
                break
    
    def record_exit_chart_condition(self, ticker: str, strategy: str, 
                                    chart_condition: Dict):
        """
        청산 시 차트 조건 기록
        
        Args:
            ticker: 코인 티커
            strategy: 전략 이름
            chart_condition: 청산 시 차트 조건
        """
        # 해당 진입 경험 찾기
        for exp in reversed(self.experiences):
            if (exp.ticker == ticker and 
                exp.strategy == strategy and 
                exp.exit_price is None):  # 아직 청산되지 않은 포지션
                
                exp.exit_chart_condition = chart_condition
                break
    
    def get_optimal_order_method(self, ticker: str, strategy: str, 
                                 market_condition: Dict) -> Optional[str]:
        """
        과거 학습 데이터 기반 최적 주문 방식 추천
        
        Args:
            ticker: 코인 티커
            strategy: 전략 이름
            market_condition: 시장 조건
        
        Returns:
            가장 성공률 높은 order_method (None if not enough data)
        """
        # Filter experiences for similar conditions
        similar = [
            exp for exp in self.experiences[-100:]  # Recent 100
            if exp.ticker == ticker 
            and exp.strategy == strategy
            and exp.exit_price is not None  # Completed trades only
            and hasattr(exp, 'order_method') and exp.order_method
        ]
        
        if len(similar) < 3:
            return None  # Not enough data
        
        # Calculate success rate by order_method
        method_stats = {}
        for exp in similar:
            method = exp.order_method
            if method not in method_stats:
                method_stats[method] = {'wins': 0, 'total': 0, 'total_profit': 0.0}
            
            method_stats[method]['total'] += 1
            if exp.profit_loss > 0:
                method_stats[method]['wins'] += 1
                method_stats[method]['total_profit'] += exp.profit_loss
        
        # Find best method
        best_method = None
        best_score = 0.0
        for method, stats in method_stats.items():
            if stats['total'] >= 2:  # Minimum sample
                win_rate = stats['wins'] / stats['total']
                avg_profit = stats['total_profit'] / stats['total']
                # Weighted score: 70% win rate + 30% average profit
                score = (win_rate * 0.7) + (min(avg_profit / 10000, 1.0) * 0.3)
                
                if score > best_score:
                    best_score = score
                    best_method = method
        
        return best_method

    def get_optimal_exit_timing(self, ticker: str, strategy: str) -> Dict:
        """
        최적 청산 타이밍 분석
        
        Args:
            ticker: 코인 티커
            strategy: 전략 이름
        
        Returns:
            {
                'avg_hold_time': seconds,
                'best_exit_reason': str,
                'avg_profit': float,
                'sample_size': int
            }
        """
        # Filter similar completed trades
        similar = [exp for exp in self.experiences[-100:] 
                   if exp.ticker == ticker 
                   and exp.strategy == strategy 
                   and exp.holding_duration is not None
                   and exp.exit_price is not None]
        
        if not similar:
            return {}
        
        # Calculate averages for profitable trades
        profitable = [exp for exp in similar if exp.profit_loss > 0]
        
        if profitable:
            avg_hold_time = sum(exp.holding_duration for exp in profitable) / len(profitable)
            avg_profit = sum(exp.profit_loss for exp in profitable) / len(profitable)
            
            # Most common successful exit reason
            exit_reasons = [exp.exit_reason for exp in profitable if hasattr(exp, 'exit_reason') and exp.exit_reason]
            best_exit = max(set(exit_reasons), key=exit_reasons.count) if exit_reasons else None
            
            return {
                'avg_hold_time': avg_hold_time,
                'best_exit_reason': best_exit,
                'avg_profit': avg_profit,
                'sample_size': len(profitable)
            }
        
        return {}
    
    def get_average_slippage(self, ticker: str, order_method: str) -> float:
        """
        특정 티커 + 주문방식의 평균 슬리피지 조회
        
        Args:
            ticker: 코인 티커
            order_method: 주문 방식
        
        Returns:
            평균 슬리피지 (%)
        """
        similar = [
            exp for exp in self.experiences[-50:]
            if exp.ticker == ticker
            and hasattr(exp, 'order_method') and exp.order_method == order_method
            and hasattr(exp, 'slippage_pct') and exp.slippage_pct is not None
        ]
        
        if not similar:
            return 0.3  # 기본값
        
        return sum(exp.slippage_pct for exp in similar) / len(similar)
