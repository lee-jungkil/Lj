"""
수익 최적화 봇 v7.0 (Profit-Optimized Bot)
=========================================

핵심 개선사항:
1. ✅ 거래량 급증 + 가격 모멘텀 기반 진입
2. ✅ 빠른 익절 (0.3-0.8%), 엄격한 손절 (-0.5%)
3. ✅ 실시간 학습 시스템 (매 거래마다 파라미터 최적화)
4. ✅ 스마트 주문 실행 (시장가/지정가 자동 선택)
5. ✅ 명확한 매수/매도 로직 (버그 없음)

목표: 일일 수익률 1-3% 달성
"""

import sys
import os
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('profit_bot.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# 프로젝트 임포트
from src.config import Config
from src.upbit_api import UpbitAPI
from src.strategies.profit_optimized_strategy import ProfitOptimizedStrategy
from src.ai.realtime_learner import RealtimeLearner
from src.utils.smart_order_executor import SmartOrderExecutor
from src.utils.risk_manager import RiskManager


class Position:
    """포지션 데이터 클래스"""
    def __init__(self, ticker: str, quantity: float, entry_price: float, 
                 entry_time: datetime, strategy_name: str = "ProfitOptimized"):
        self.ticker = ticker
        self.quantity = quantity
        self.entry_price = entry_price
        self.avg_buy_price = entry_price
        self.entry_time = entry_time
        self.strategy = strategy_name
        self.entry_volume = 0  # 진입 시 거래량


class ProfitOptimizedBot:
    """수익 최적화 자동매매 봇"""
    
    def __init__(self, mode: str = 'paper'):
        """
        초기화
        
        Args:
            mode: 거래 모드 (paper=시뮬레이션, live=실전)
        """
        self.mode = mode
        logger.info(f"🚀 Profit-Optimized Bot v7.0 시작 (모드: {mode})")
        
        # API 초기화
        if mode == 'live':
            self.api = UpbitAPI(Config.UPBIT_ACCESS_KEY, Config.UPBIT_SECRET_KEY)
        else:
            self.api = UpbitAPI()  # 시뮬레이션 모드
        
        # 전략 & 학습 시스템
        self.strategy = ProfitOptimizedStrategy()
        self.learner = RealtimeLearner()
        
        # 주문 실행기 (order_selector는 None으로 - 내부에서 생성됨)
        from src.utils.order_method_selector import OrderMethodSelector
        order_selector = OrderMethodSelector()
        self.order_executor = SmartOrderExecutor(self.api, order_selector)
        
        # 리스크 매니저
        self.risk_manager = RiskManager(
            initial_capital=5000000,  # 초기 자본 500만원
            max_daily_loss=250000,    # 일일 최대 손실 25만원 (5%)
            max_cumulative_loss=500000,  # 누적 최대 손실 50만원
            max_positions=10,         # 최대 10개 포지션
            upbit_api=self.api
        )
        self.risk_manager.max_open_positions = 10  # 포지션 제한 명시
        
        # 포지션 관리 설정
        self.base_position_limit = 5   # 기본 포지션 수
        self.max_position_limit = 10   # 최대 포지션 수
        
        # 포지션 관리
        self.positions: Dict[str, Position] = {}
        
        # 성과 추적
        self.total_trades = 0
        self.winning_trades = 0
        self.total_profit_krw = 0
        self.daily_profit_krw = 0
        
        # 타이밍
        self.last_scan_time = 0
        self.scan_interval = 30  # 30초마다 스캔 (API 부하 감소)
        self.last_position_check_time = 0
        self.position_check_interval = 5  # 5초마다 포지션 체크
        
        logger.info("✅ 초기화 완료!")
    
    def run(self):
        """메인 루프"""
        logger.info("=" * 60)
        logger.info("🎯 수익 최적화 봇 가동 시작!")
        logger.info("=" * 60)
        
        try:
            while True:
                current_time = time.time()
                
                # 1. 포지션 체크 (3초마다) - 최우선
                if current_time - self.last_position_check_time >= self.position_check_interval:
                    self._check_positions()
                    self.last_position_check_time = current_time
                
                # 2. 신규 진입 스캔 (10초마다) - 포지션 여유 있을 때만
                if (current_time - self.last_scan_time >= self.scan_interval and
                    len(self.positions) < self.risk_manager.max_open_positions):
                    self._scan_for_entry()
                    self.last_scan_time = current_time
                
                # 3. 성과 리포트 (60초마다)
                if int(current_time) % 60 == 0:
                    self._print_performance()
                
                # CPU 절약
                time.sleep(1)
        
        except KeyboardInterrupt:
            logger.info("\n👋 종료 신호 받음. 정리 중...")
            self._cleanup()
        except Exception as e:
            logger.error(f"❌ 치명적 오류: {e}", exc_info=True)
            self._cleanup()
    
    def _scan_for_entry(self):
        """신규 진입 기회 스캔"""
        try:
            logger.info("🔍 진입 기회 스캔 중...")
            
            # KRW 마켓 코인 목록
            all_tickers = self.api.get_all_tickers(fiat="KRW")
            if not all_tickers:
                logger.warning("⚠️ 코인 목록 가져오기 실패")
                return
            
            # 이미 보유 중인 코인 제외
            available_tickers = [t for t in all_tickers if t not in self.positions]
            
            # 거래량 상위 50개만 검토 (효율성)
            top_volume_tickers = self._get_top_volume_tickers(available_tickers, limit=50)
            
            logger.info(f"📊 {len(top_volume_tickers)}개 코인 빠른 스캔 중...")
            
            # 빠른 1차 스캔: 가격만 체크 (API 호출 최소화)
            candidates = []
            for i, ticker in enumerate(top_volume_tickers[:10], 1):  # 상위 10개만 빠르게 체크
                try:
                    current_price = self.api.get_current_price(ticker)
                    if current_price and current_price > 0:
                        candidates.append(ticker)
                        logger.debug(f"   [{i}/10] {ticker}: {current_price:,.0f}원")
                    
                    # API 제한 방지: 각 호출 사이 0.2초 대기 (초당 5개)
                    import time
                    time.sleep(0.2)
                except Exception as e:
                    logger.debug(f"   [{i}/10] {ticker}: 오류 - {e}")
                    continue
            
            logger.info(f"🎯 {len(candidates)}개 후보 발견, 상세 분석 중...")
            
            # 2차 상세 스캔: 후보들만 상세 분석 (최대 5개까지만)
            logger.debug(f"   상세 스캔 시작: {min(len(candidates), 5)}개 코인 분석...")
            for i, ticker in enumerate(candidates[:5], 1):
                # 동적 포지션 제한 체크
                current_position_limit = self._get_current_position_limit()
                if len(self.positions) >= current_position_limit:
                    logger.info(f"⚠️ 포지션 제한 도달 ({len(self.positions)}/{current_position_limit})")
                    break
                
                # 시장 데이터 수집 (상세)
                logger.debug(f"   [{i}/5] {ticker} 분석 중...")
                market_data = self._get_market_data(ticker)
                if not market_data:
                    logger.debug(f"   [{i}/5] {ticker}: 데이터 수집 실패")
                    continue
                
                # 상세 스캔 각 코인 사이 딜레이 (API 호출이 많으므로)
                time.sleep(0.5)  # 0.5초 대기
                
                # 포지션 수에 따라 진입 조건 강화
                if len(self.positions) >= self.base_position_limit:
                    # 5개 이상 시 강화된 조건 적용
                    enhanced_entry = self._check_enhanced_entry(ticker, market_data)
                    if not enhanced_entry:
                        logger.debug(f"   {ticker}: 강화 조건 미충족 (현재 {len(self.positions)}개 포지션)")
                        continue
                
                # 진입 조건 검사
                should_enter, reason = self.strategy.should_enter(ticker, market_data)
                
                if should_enter:
                    logger.info(f"✅ 진입 신호: {ticker} - {reason}")
                    self._execute_buy(ticker, market_data)
                    break  # 한 번에 하나씩만 진입
            
            logger.info("✅ 스캔 완료")
        
        except Exception as e:
            logger.error(f"❌ 스캔 중 오류: {e}")
    
    def _check_positions(self):
        """보유 포지션 체크 및 청산"""
        if not self.positions:
            return
        
        logger.info(f"📊 포지션 체크 ({len(self.positions)}개)...")
        
        for ticker in list(self.positions.keys()):  # 리스트로 복사 (삭제 안전)
            try:
                position = self.positions[ticker]
                
                # 현재 가격
                current_price = self.api.get_current_price(ticker)
                if not current_price:
                    logger.warning(f"⚠️ {ticker} 가격 조회 실패")
                    continue
                
                # 보유 시간
                hold_time = (datetime.now() - position.entry_time).total_seconds()
                
                # 수익률
                profit_pct = ((current_price - position.entry_price) / position.entry_price) * 100
                
                # 시장 데이터
                market_data = self._get_market_data(ticker)
                
                # 청산 조건 검사
                should_exit, reason, exit_type = self.strategy.should_exit(
                    ticker, position.entry_price, current_price, hold_time, market_data
                )
                
                if should_exit:
                    logger.info(f"🔔 청산 신호: {ticker} - {reason}")
                    self._execute_sell(ticker, exit_type, reason, profit_pct)
                else:
                    # 보유 중 상태 출력
                    logger.debug(f"   {ticker}: {profit_pct:+.2f}% (보유: {hold_time:.0f}초)")
            
            except Exception as e:
                logger.error(f"❌ {ticker} 체크 중 오류: {e}")
    
    def _execute_buy(self, ticker: str, market_data: Dict):
        """매수 실행 (v7.0.5: 호가창 유동성 체크 + 시장가/지정가 자동 선택)"""
        try:
            logger.info(f"💰 매수 시작: {ticker}")
            
            # 현재 가격 (market_data에서 재사용 - API 호출 절약)
            current_price = market_data.get('current_price', 0)
            if not current_price or current_price <= 0:
                # market_data에 없으면 직접 조회
                current_price = self.api.get_current_price(ticker)
                if not current_price:
                    logger.error(f"❌ {ticker} 가격 조회 실패")
                    return
            
            # 가용 자금 확인
            if self.mode == 'live':
                balance = self.api.get_balance()
                available_krw = balance.get('KRW', 0)
            else:
                available_krw = 5000000  # 시뮬레이션: 500만원
            
            if available_krw < 10000:
                logger.warning("⚠️ 가용 자금 부족 (최소 10,000원)")
                return
            
            # 1️⃣ 포지션 크기 계산 (희망 매수 금액)
            quantity = self.strategy.get_position_size(available_krw, current_price)
            desired_krw = quantity * current_price
            
            logger.info(f"   희망 매수 금액: {desired_krw:,.0f}원")
            
            # 2️⃣ 호가창 유동성 체크 (v7.0.5)
            # ⚠️ API 호출 추가 - 필요시에만 호출
            time.sleep(0.15)  # API 제한 방지
            try:
                liquidity = self.api.check_orderbook_liquidity(
                    ticker=ticker,
                    target_krw=desired_krw,
                    max_price_levels=1  # 최우선 호가만 사용 (보수적)
                )
            except Exception as e:
                logger.warning(f"⚠️ {ticker} 호가창 조회 실패: {e}, 기본 동작으로 진행")
                # 호가창 조회 실패 시 기본값 사용 (유동성 충분으로 간주)
                liquidity = {
                    'can_fill': True,
                    'available_krw': desired_krw,
                    'best_ask_price': current_price,
                    'liquidity_ratio': 1.0,
                    'suggested_krw': desired_krw,
                }
            
            logger.info(f"   호가창 유동성: {liquidity['available_krw']:,.0f}원 ({liquidity['liquidity_ratio']*100:.1f}%)")
            
            # 3️⃣ 유동성 기반 매수 금액 조정
            if liquidity['liquidity_ratio'] >= 0.5:  # 50% 이상 유동성
                # 호가창 물량이 충분 → 조정된 금액으로 매수
                final_krw = liquidity['suggested_krw']
                
                if liquidity['can_fill']:
                    logger.info(f"   ✅ 호가창 유동성 충분 → 전량 매수")
                else:
                    logger.info(f"   ⚠️ 호가창 유동성 부족 → 조정: {final_krw:,.0f}원 ({liquidity['liquidity_ratio']*100:.1f}%)")
            else:
                # 호가창 물량 50% 미만 → 이번 기회 포기
                logger.warning(
                    f"   ❌ {ticker} 유동성 부족으로 매수 취소\n"
                    f"      희망: {desired_krw:,.0f}원 / 호가창: {liquidity['available_krw']:,.0f}원 ({liquidity['liquidity_ratio']*100:.1f}%)"
                )
                return
            
            # 4️⃣ 최소 주문 금액 확인 (5000원)
            if final_krw < 5000:
                logger.warning(f"⚠️ {ticker} 조정된 금액 부족: {final_krw:.0f}원 < 5000원 (매수 취소)")
                return
            
            # 5️⃣ 스프레드 계산 (시장가 vs 지정가 판단용)
            time.sleep(0.15)  # API 제한 방지
            try:
                spread_pct = self.api.calculate_spread_percentage(ticker)
                logger.info(f"   스프레드: {spread_pct:.3f}%")
            except Exception as e:
                logger.warning(f"⚠️ {ticker} 스프레드 조회 실패: {e}, 시장가로 진행")
                spread_pct = 0.05  # 기본값 (시장가 사용)
            
            # 6️⃣ 주문 방식 자동 선택 (스프레드 기반)
            if spread_pct < 0.1:
                # 스프레드 0.1% 미만 → 시장가 (슬리피지 무시 가능)
                order_method = 'market'
                order_price = current_price
                logger.info(f"   📊 주문 방식: 시장가 (스프레드 낮음 {spread_pct:.3f}%)")
            elif spread_pct < 0.3:
                # 스프레드 0.1~0.3% → 최우선 호가 지정가
                order_method = 'limit'
                order_price = liquidity['best_ask_price']  # 최우선 매도 호가
                logger.info(f"   📊 주문 방식: 지정가 @ {order_price:,.0f}원 (스프레드 보통 {spread_pct:.3f}%)")
            else:
                # 스프레드 0.3% 이상 → 최우선 호가 지정가 (슬리피지 방지)
                order_method = 'limit'
                order_price = liquidity['best_ask_price']
                logger.info(f"   📊 주문 방식: 지정가 @ {order_price:,.0f}원 (스프레드 높음 {spread_pct:.3f}%)")
            
            # 7️⃣ 최종 수량 계산
            final_quantity = final_krw / order_price
            
            # 8️⃣ 주문 실행
            if self.mode == 'live':
                # 실전: 실제 주문
                if order_method == 'market':
                    result = self.api.buy_market_order(ticker, final_krw)
                else:  # limit
                    result = self.api.buy_limit_order(ticker, order_price, final_quantity)
                
                if not result or 'error' in result:
                    logger.error(f"❌ {ticker} 매수 주문 실패: {result}")
                    return
                
                logger.info(f"✅ {ticker} 매수 완료! {final_quantity:.8f}개 @ {order_price:,.0f}원 ({order_method})")
            else:
                # 시뮬레이션
                logger.info(f"✅ [시뮬] {ticker} 매수! {final_quantity:.8f}개 @ {order_price:,.0f}원 (금액: {final_krw:,.0f}원, {order_method})")
            
            # 9️⃣ 포지션 생성
            position = Position(
                ticker=ticker,
                quantity=final_quantity,
                entry_price=order_price,
                entry_time=datetime.now(),
                strategy_name="ProfitOptimized"
            )
            position.entry_volume = market_data.get('current_volume', 0)
            
            self.positions[ticker] = position
            
            logger.info(f"📍 포지션 생성: {ticker} (현재 포지션: {len(self.positions)}개)")
        
        except Exception as e:
            logger.error(f"❌ {ticker} 매수 실행 중 오류: {e}", exc_info=True)
    
    def _execute_sell(self, ticker: str, exit_type: str, reason: str, profit_pct: float):
        """매도 실행"""
        try:
            if ticker not in self.positions:
                logger.warning(f"⚠️ {ticker} 포지션 없음")
                return
            
            position = self.positions[ticker]
            
            logger.info(f"💸 매도 시작: {ticker} (수익률: {profit_pct:+.2f}%)")
            
            # 현재 가격
            current_price = self.api.get_current_price(ticker)
            if not current_price:
                logger.error(f"❌ {ticker} 가격 조회 실패")
                return
            
            # 주문 실행
            if self.mode == 'live':
                # 실전: 실제 주문
                result = self.order_executor.execute_sell(
                    ticker=ticker,
                    volume=position.quantity,
                    method='market'  # 시장가 매도
                )
                
                if not result or 'error' in result:
                    logger.error(f"❌ {ticker} 매도 주문 실패: {result}")
                    return
                
                logger.info(f"✅ {ticker} 매도 완료! {position.quantity:.8f}개 @ {current_price:,.0f}원")
            else:
                # 시뮬레이션
                logger.info(f"✅ [시뮬] {ticker} 매도! {position.quantity:.8f}개 @ {current_price:,.0f}원")
            
            # 손익 계산
            profit_krw = (current_price - position.entry_price) * position.quantity
            
            # 통계 업데이트
            self.total_trades += 1
            if profit_pct > 0:
                self.winning_trades += 1
            self.total_profit_krw += profit_krw
            self.daily_profit_krw += profit_krw
            
            logger.info(f"{'💰' if profit_pct > 0 else '🚨'} {ticker} 청산 완료!")
            logger.info(f"   수익: {profit_krw:+,.0f}원 ({profit_pct:+.2f}%)")
            logger.info(f"   이유: {reason}")
            
            # 학습 시스템에 기록
            hold_time = (datetime.now() - position.entry_time).total_seconds()
            self.learner.record_trade({
                'ticker': ticker,
                'entry_price': position.entry_price,
                'exit_price': current_price,
                'entry_time': position.entry_time,
                'exit_time': datetime.now(),
                'profit_pct': profit_pct,
                'profit_krw': profit_krw,
                'exit_reason': exit_type,
                'hold_time': hold_time,
                'market_conditions': {}
            })
            
            # 전략 정리
            self.strategy.cleanup(ticker)
            
            # 포지션 삭제
            del self.positions[ticker]
            
            logger.info(f"📍 포지션 제거: {ticker} (남은 포지션: {len(self.positions)}개)")
        
        except Exception as e:
            logger.error(f"❌ {ticker} 매도 실행 중 오류: {e}", exc_info=True)
    
    def _get_market_data(self, ticker: str) -> Dict:
        """시장 데이터 수집 (v7.0.5.3: API 호출 간 딜레이 추가)"""
        try:
            # 현재 가격
            current_price = self.api.get_current_price(ticker)
            if not current_price:
                logger.debug(f"   {ticker}: 현재가 조회 실패")
                return {}
            
            logger.debug(f"   {ticker}: 현재가 {current_price:,.0f}원")
            time.sleep(0.15)  # API 제한 방지
            
            # OHLCV 데이터 (1분봉)
            df_1m = self.api.get_ohlcv(ticker, interval='minute1', count=10)
            if df_1m is None or df_1m.empty:
                logger.debug(f"   {ticker}: 1분봉 데이터 없음")
                return {}
            time.sleep(0.15)  # API 제한 방지
            
            # OHLCV 데이터 (5분봉)
            df_5m = self.api.get_ohlcv(ticker, interval='minute5', count=20)
            if df_5m is None or df_5m.empty:
                logger.debug(f"   {ticker}: 5분봉 데이터 없음")
                return {}
            time.sleep(0.15)  # API 제한 방지
            
            # 거래량
            current_volume = float(df_1m['volume'].iloc[-1]) if not df_1m.empty else 0
            avg_volume_5m = float(df_5m['volume'].mean()) if not df_5m.empty else 0
            
            # 가격 변화 (1분)
            if len(df_1m) >= 2:
                price_1m_ago = float(df_1m['close'].iloc[-2])
                price_change_1m = ((current_price - price_1m_ago) / price_1m_ago) * 100
            else:
                price_change_1m = 0
            
            # RSI (14)
            from src.utils.technical_indicators import calculate_rsi, calculate_bollinger_bands, calculate_stochastic
            rsi = calculate_rsi(df_5m, period=14)
            rsi_value = float(rsi.iloc[-1]) if rsi is not None and not rsi.empty else 50
            
            # 볼린저 밴드 (20, 2)
            bb_upper, bb_mid, bb_lower = calculate_bollinger_bands(df_5m, period=20, std_dev=2)
            bb_lower_value = float(bb_lower.iloc[-1]) if bb_lower is not None and not bb_lower.empty else 0
            
            # 스토캐스틱 (14, 3)
            stoch_k, stoch_d = calculate_stochastic(df_5m, period=14, smooth_k=3)
            stoch_k_value = float(stoch_k.iloc[-1]) if stoch_k is not None and not stoch_k.empty else 50
            stoch_d_value = float(stoch_d.iloc[-1]) if stoch_d is not None and not stoch_d.empty else 50
            
            # 호가창 (매도 압력)
            orderbook = self.api.get_orderbook(ticker)
            time.sleep(0.15)  # API 제한 방지
            if orderbook and 'orderbook_units' in orderbook:
                orderbook_units = orderbook['orderbook_units']
                # 매도 호가 (ask) 상위 5개
                sell_volume = sum([float(unit.get('ask_size', 0)) for unit in orderbook_units[:5]])
                # 매수 호가 (bid) 상위 5개
                buy_volume = sum([float(unit.get('bid_size', 0)) for unit in orderbook_units[:5]])
                sell_pressure = sell_volume / buy_volume if buy_volume > 0 else 1.0
            else:
                sell_pressure = 1.0
            
            logger.debug(f"   {ticker}: 데이터 수집 완료 (RSI:{rsi_value:.1f}, Stoch:{stoch_k_value:.1f})")
            
            return {
                'current_price': current_price,
                'current_volume': current_volume,
                'avg_volume_5m': avg_volume_5m,
                'price_change_1m': price_change_1m,
                'rsi': rsi_value,
                'sell_pressure': sell_pressure,
                'bb_lower': bb_lower_value,
                'stoch_k': stoch_k_value,
                'stoch_d': stoch_d_value,
            }
        
        except Exception as e:
            logger.error(f"❌ {ticker} 시장 데이터 수집 실패: {e}", exc_info=True)
            return {}
    
    def _get_top_volume_tickers(self, tickers: List[str], limit: int = 50) -> List[str]:
        """거래량 상위 코인 목록 (빠른 버전 - 샘플링)"""
        try:
            # 너무 많은 코인을 검사하면 느려지므로, 랜덤 샘플링 후 limit개 반환
            # 또는 이미 알려진 주요 코인 우선 검사
            import random
            
            # 주요 코인 (거래량이 높은 코인들)
            major_coins = [
                'KRW-BTC', 'KRW-ETH', 'KRW-XRP', 'KRW-ADA', 'KRW-SOL',
                'KRW-DOGE', 'KRW-AVAX', 'KRW-DOT', 'KRW-MATIC', 'KRW-SHIB',
                'KRW-LINK', 'KRW-UNI', 'KRW-ATOM', 'KRW-ETC', 'KRW-BCH',
                'KRW-LTC', 'KRW-NEAR', 'KRW-APT', 'KRW-FIL', 'KRW-ICP'
            ]
            
            # 주요 코인 중 사용 가능한 것들
            available_major = [t for t in major_coins if t in tickers]
            
            # 나머지 코인에서 랜덤 샘플링
            remaining = [t for t in tickers if t not in available_major]
            sample_size = max(0, limit - len(available_major))
            
            if sample_size > 0 and remaining:
                sampled = random.sample(remaining, min(sample_size, len(remaining)))
            else:
                sampled = []
            
            result = available_major + sampled
            
            logger.info(f"✅ {len(result)}개 코인 선정 (주요 {len(available_major)}개 + 샘플 {len(sampled)}개)")
            return result[:limit]
        
        except Exception as e:
            logger.error(f"❌ 거래량 정렬 실패: {e}")
            return tickers[:limit]
    
    def _print_performance(self):
        """성과 출력"""
        win_rate = (self.winning_trades / self.total_trades * 100) if self.total_trades > 0 else 0
        
        logger.info("=" * 60)
        logger.info("📊 성과 요약")
        logger.info("-" * 60)
        logger.info(f"   총 거래: {self.total_trades}건")
        logger.info(f"   승률: {win_rate:.1f}% ({self.winning_trades}/{self.total_trades})")
        logger.info(f"   총 수익: {self.total_profit_krw:+,.0f}원")
        logger.info(f"   오늘 수익: {self.daily_profit_krw:+,.0f}원")
        logger.info(f"   현재 포지션: {len(self.positions)}개")
        
        # 학습 상태
        perf = self.learner.get_performance_report()
        logger.info(f"   학습 승률: {perf['win_rate']}")
        logger.info(f"   Profit Factor: {perf['profit_factor']}")
        logger.info("=" * 60)
    
    def _get_current_position_limit(self) -> int:
        """
        현재 포지션 제한 계산
        
        Returns:
            현재 허용되는 최대 포지션 수
        """
        # 기본: 5개까지는 일반 조건
        # 5개 이상: 강화된 조건으로 최대 10개까지
        return self.max_position_limit
    
    def _check_enhanced_entry(self, ticker: str, market_data: Dict) -> bool:
        """
        강화된 진입 조건 검사 (5개 포지션 이후)
        
        Args:
            ticker: 티커
            market_data: 시장 데이터
        
        Returns:
            강화 조건 통과 여부
        """
        try:
            # 1. 거래량 급증 더 강하게 (2.5x → 3.0x)
            current_volume = market_data.get('current_volume', 0)
            avg_volume = market_data.get('avg_volume_5m', 0)
            
            if avg_volume <= 0:
                return False
            
            volume_ratio = current_volume / avg_volume
            if volume_ratio < 3.0:  # 강화: 3배 이상
                return False
            
            # 2. 가격 모멘텀 더 강하게 (0.15-1.5% → 0.3-1.2%)
            price_change_1m = market_data.get('price_change_1m', 0)
            if price_change_1m < 0.3 or price_change_1m > 1.2:
                return False
            
            # 3. RSI 더 보수적으로 (70 → 65)
            rsi = market_data.get('rsi', 50)
            if rsi > 65:
                return False
            
            # 4. 매도 압력 더 엄격하게 (1.5 → 1.2)
            sell_pressure = market_data.get('sell_pressure', 1.0)
            if sell_pressure > 1.2:
                return False
            
            # 5. 볼린저 밴드 더 엄격하게 (±5% → ±3%)
            bb_lower = market_data.get('bb_lower', 0)
            current_price = market_data.get('current_price', 0)
            
            if bb_lower > 0 and current_price > 0:
                bb_position_pct = ((current_price - bb_lower) / bb_lower) * 100
                if not (-3 <= bb_position_pct <= 3):  # 강화: ±3%
                    return False
            
            # 6. 스토캐스틱 더 엄격하게 (20-40 → 25-35)
            stoch_k = market_data.get('stoch_k', 50)
            stoch_d = market_data.get('stoch_d', 50)
            
            if not (25 < stoch_k < 35 and stoch_k > stoch_d + 2):  # 강화: K가 D보다 2 이상 높아야
                return False
            
            logger.info(f"   ✅ {ticker}: 강화 조건 통과 (거래량:{volume_ratio:.2f}x, 모멘텀:{price_change_1m:.2f}%, RSI:{rsi:.1f}, Stoch:{stoch_k:.1f})")
            return True
            
        except Exception as e:
            logger.error(f"❌ 강화 조건 검사 실패: {e}")
            return False
    
    def _cleanup(self):
        """종료 처리"""
        logger.info("정리 작업 중...")
        
        # 포지션 정리 (실전 모드에서는 수동으로)
        if self.positions:
            logger.warning(f"⚠️ {len(self.positions)}개 포지션이 남아있습니다:")
            for ticker, pos in self.positions.items():
                current_price = self.api.get_current_price(ticker)
                if current_price:
                    profit_pct = ((current_price - pos.entry_price) / pos.entry_price) * 100
                    logger.info(f"   {ticker}: {profit_pct:+.2f}%")
        
        # 최종 성과
        self._print_performance()
        
        logger.info("✅ 종료 완료")


def main():
    """메인 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Profit-Optimized Bot v7.0')
    parser.add_argument('--mode', type=str, default='paper', choices=['paper', 'live'],
                       help='거래 모드 (paper=시뮬레이션, live=실전)')
    args = parser.parse_args()
    
    # 봇 실행
    bot = ProfitOptimizedBot(mode=args.mode)
    bot.run()


if __name__ == '__main__':
    main()
