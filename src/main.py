"""
AutoProfit Bot - 메인 봇 엔진 (Phase 1 + Phase 2 완전 통합)
24시간 자동매매 봇

버전: 5.1 (실시간 호가창/체결 모니터링 추가)
개선사항:
- ✅ Phase 1: 텔레그램/Gmail 손익 알림 시스템
- ✅ Phase 2: 20가지 분할 전략 + 45가지 시나리오 + 호가창 분석
- ✅ AI 학습: 보유 시간 최적화 + 전략 선택 + 동적 청산
- ✅ 실시간 호가창 모니터링 + 학습 시스템
- ✅ 실시간 체결 데이터 수집 + 매수/매도 강도 분석
- 3분 주기: 전체 코인 스캔 + 신규 진입
- 5초 주기: 포지션 빠른 체크
- 10초 주기: 급등/급락 감지 (최적화)
"""

# ⭐ CRITICAL: print() 출력 억제 (화면 스크롤 방지)
import sys
import os

# NULL 디바이스로 리다이렉션
class SuppressPrint:
    """print() 출력을 완전히 억제하는 컨텍스트 관리자"""
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

# 전역 print 비활성화 (고정 화면 디스플레이를 위해 필수)
_original_print = print
def _suppressed_print(*args, **kwargs):
    """print() 호출 시 아무것도 출력하지 않음"""
    pass

# ⭐ DEBUG 모드 환경 변수 확인
import os
DEBUG_MODE = os.getenv('DEBUG_MODE', '0') == '1' or os.getenv('ENABLE_DEBUG_LOGS', '1') == '1'

# print 함수를 덮어씀 (단, DEBUG 모드에서는 원본 print 사용)
import builtins
if not DEBUG_MODE:
    builtins.print = _suppressed_print
else:
    # DEBUG 모드에서는 print() 출력 허용
    builtins.print = _original_print

import time
import argparse
from datetime import datetime
from typing import Dict, List
import random

from src.config import Config
from src.upbit_api import UpbitAPI
from src.utils.logger import TradingLogger
from src.utils.risk_manager import RiskManager
from src.utils.sentiment_analyzer import SentimentAnalyzer
from src.utils.strategy_optimizer import StrategyOptimizer, MarketCondition
from src.utils.market_analyzer import analyze_market_condition, get_market_description
from src.utils.holding_protector import HoldingProtector
from src.utils.surge_detector import SurgeDetector
from src.utils.dynamic_coin_selector import DynamicCoinSelector
from src.utils.fixed_screen_display import FixedScreenDisplay
from src.utils.market_condition_analyzer import market_condition_analyzer
# Phase 1: 알림 시스템
from src.utils.telegram_notifier import TelegramNotifier
from src.utils.email_reporter import EmailReporter
from src.utils.notification_scheduler import NotificationScheduler
# Phase 2: 호가창 + 스마트 주문 + 동적 청산
from src.utils.order_book_analyzer import OrderBookAnalyzer
from src.utils.smart_order_executor import SmartOrderExecutor
from src.utils.orderbook_monitor import OrderbookMonitor
from src.utils.trade_monitor import TradeMonitor
# Phase 3 (v6.29): Advanced Order System
from src.utils.surge_detector import surge_detector
from src.utils.order_method_selector import order_method_selector, ExitReason
from src.utils.smart_order_executor import SmartOrderExecutor
from src.utils.smart_position_sizer import SmartPositionSizer  # ⭐ v6.31.7: 스마트 포지션 사이징
# Phase 2: AI 시스템
from src.ai.learning_engine import LearningEngine
from src.ai.scenario_identifier import ScenarioIdentifier
from src.ai.strategy_selector import StrategySelector
from src.ai.holding_time_optimizer import HoldingTimeOptimizer
from src.ai.adaptive_learner import AdaptiveLearner
from src.ai.auto_optimizer import AutoOptimizer  # ⭐ v6.30.17: 자동 최적화
from src.ai.loss_analyzer import LossAnalyzer  # ⭐ v6.30.17: 손실 분석
# 전략
from src.strategies.aggressive_scalping import AggressiveScalping
from src.strategies.conservative_scalping import ConservativeScalping
from src.strategies.mean_reversion import MeanReversion
from src.strategies.grid_trading import GridTrading
from src.strategies.ultra_scalping import UltraScalping
from src.strategies.split_strategies import SplitStrategies
from src.strategies.dynamic_exit_manager import DynamicExitManager
# ⭐ v6.31.9: 5가지 고급 매수 전략 추가
from src.strategies.breakout_strategy import BreakoutStrategy
from src.strategies.pullback_strategy import PullbackStrategy
from src.strategies.golden_cross_strategy import GoldenCrossStrategy
from src.strategies.volatility_breakout_strategy import VolatilityBreakoutStrategy
from src.strategies.double_bottom_strategy import DoubleBottomStrategy


class AutoProfitBot:
    """자동매매 봇 (Phase 1 + Phase 2 완전 통합)"""
    
    def __init__(self, mode: str = 'backtest'):
        """
        초기화
        
        Args:
            mode: 거래 모드 (backtest, paper, live)
        """
        self.mode = mode
        
        # 설정 로드
        Config.TRADING_MODE = mode
        Config.validate()
        
        # 로거 초기화
        self.logger = TradingLogger()
        self.logger.log_info(f"🚀 AutoProfit Bot v5.0 시작 (Phase 1+2 통합)")
        self.logger.log_info(f"   모드: {mode}")
        
        # API 초기화
        if mode == 'live':
            self.api = UpbitAPI(Config.UPBIT_ACCESS_KEY, Config.UPBIT_SECRET_KEY)
        else:
            self.api = UpbitAPI()
        
        # === Phase 1: 알림 시스템 초기화 ===
        self.telegram = TelegramNotifier(
            Config.TELEGRAM_BOT_TOKEN,
            Config.TELEGRAM_CHAT_ID
        )
        self.email_reporter = EmailReporter(
            Config.GMAIL_SENDER,
            Config.GMAIL_PASSWORD,
            Config.GMAIL_RECEIVER
        )
        
        # === Phase 2: AI 시스템 초기화 ===
        # 기존 학습 엔진
        self.learning_engine = LearningEngine()
        
        # Phase 2 AI 컴포넌트
        if Config.ENABLE_ADVANCED_AI:
            self.scenario_identifier = ScenarioIdentifier()
            self.strategy_selector = StrategySelector()
            self.holding_optimizer = HoldingTimeOptimizer()
            
            # ⭐ v6.30.17: 손실 분석 시스템
            self.loss_analyzer = LossAnalyzer(
                learning_engine=self.learning_engine,
                scenario_identifier=self.scenario_identifier,
                strategy_selector=self.strategy_selector
            )
            self.logger.log_info("📉 손실 분석 시스템 활성화")
            
            # ⭐ v6.30.17: 자동 최적화 시스템
            self.auto_optimizer = AutoOptimizer(
                risk_manager=None,  # 나중에 설정
                learning_engine=self.learning_engine,
                loss_analyzer=self.loss_analyzer,
                strategy_selector=self.strategy_selector
            )
            self.logger.log_info("🔧 자동 최적화 시스템 활성화")
            
            # 통합 학습 시스템
            self.adaptive_learner = AdaptiveLearner(
                learning_engine=self.learning_engine,
                scenario_identifier=self.scenario_identifier,
                strategy_selector=self.strategy_selector,
                holding_time_optimizer=self.holding_optimizer
            )
            self.logger.log_info("🧠 Phase 2 AI 시스템 활성화")
        else:
            self.adaptive_learner = None
            self.loss_analyzer = None
            self.auto_optimizer = None
            self.logger.log_info("⚠️ Phase 2 AI 시스템 비활성화")
        
        # 호가창 분석기
        if Config.ENABLE_ORDERBOOK_ANALYSIS:
            self.orderbook_analyzer = OrderBookAnalyzer(self.api)
            self.logger.log_info("📊 호가창 분석 활성화")
        else:
            self.orderbook_analyzer = None
        
        # 분할 전략
        self.split_strategies = SplitStrategies()
        
        # ⭐ v6.29 스마트 주문 실행기 (Advanced Order System)
        self.smart_order_executor = SmartOrderExecutor(
            api=self.api,
            order_selector=order_method_selector
        )
        self.logger.log_info("⚡ v6.29 스마트 주문 실행기 활성화 (9가지 주문 방식)")
        
        # 기존 호환성 지원 (필요 시)
        self.order_executor = self.smart_order_executor  # Alias
        
        # 동적 청산 관리자
        if Config.ENABLE_DYNAMIC_EXIT:
            self.exit_manager = DynamicExitManager(mode=Config.EXIT_MODE)
            self.logger.log_info(f"🎯 동적 청산 활성화 (모드: {Config.EXIT_MODE})")
        else:
            self.exit_manager = None
        
        # 실시간 호가창 모니터링 시스템
        if Config.ENABLE_ORDERBOOK_ANALYSIS and self.orderbook_analyzer:
            self.orderbook_monitor = OrderbookMonitor(
                upbit_api=self.api,
                logger=self.logger,
                order_book_analyzer=self.orderbook_analyzer
            )
            self.logger.log_info("📈 실시간 호가창 모니터링 활성화")
        else:
            self.orderbook_monitor = None
        
        # 실시간 체결 모니터링 시스템
        self.trade_monitor = TradeMonitor(
            upbit_api=self.api,
            logger=self.logger
        )
        self.logger.log_info("📊 실시간 체결 모니터링 활성화")
        
        # ⭐ 고정 화면 디스플레이 (v5.4)
        self.display = FixedScreenDisplay(max_positions=5)
        self.logger.log_info("🖥️ 고정 화면 디스플레이 활성화")
        
        # ⭐ v6.31.7: 스마트 포지션 사이징 시스템
        self.position_sizer = SmartPositionSizer()
        self.logger.log_info("💰 스마트 포지션 사이징 활성화 (10만~50만원 동적 조절)")
        
        # 리스크 관리자
        self.risk_manager = RiskManager(
            initial_capital=Config.INITIAL_CAPITAL,
            max_daily_loss=Config.MAX_DAILY_LOSS,
            max_cumulative_loss=Config.MAX_CUMULATIVE_LOSS,
            max_positions=Config.MAX_POSITIONS,
            max_position_ratio=Config.MAX_POSITION_RATIO,
            upbit_api=self.api if mode == 'live' else None
        )
        
        # ⭐ v6.30.17: AutoOptimizer에 risk_manager 연결
        if Config.ENABLE_ADVANCED_AI and self.auto_optimizer:
            self.auto_optimizer.risk_manager = self.risk_manager
            self.logger.log_info("🔗 AutoOptimizer <-> RiskManager 연결 완료")
        
        # 감정 분석기
        self.sentiment_analyzer = None
        if Config.ENABLE_SENTIMENT:
            self.sentiment_analyzer = SentimentAnalyzer(Config.NEWS_API_KEY)
        
        # 전략 초기화
        self.strategies = {
            'aggressive_scalping': AggressiveScalping(
                Config.get_strategy_config('aggressive_scalping'),
                learning_engine=self.learning_engine
            ),
            'conservative_scalping': ConservativeScalping(
                Config.get_strategy_config('conservative_scalping'),
                learning_engine=self.learning_engine
            ),
            'mean_reversion': MeanReversion(Config.get_strategy_config('mean_reversion')),
            'grid_trading': GridTrading(Config.get_strategy_config('grid_trading')),
            'ultra_scalping': UltraScalping(Config.get_strategy_config('ultra_scalping')),
            # ⭐ v6.31.9: 5가지 고급 매수 전략 추가
            'breakout': BreakoutStrategy(Config.get_strategy_config('breakout')),
            'pullback': PullbackStrategy(Config.get_strategy_config('pullback')),
            'golden_cross': GoldenCrossStrategy(Config.get_strategy_config('golden_cross')),
            'volatility_breakout': VolatilityBreakoutStrategy(Config.get_strategy_config('volatility_breakout')),
            'double_bottom': DoubleBottomStrategy(Config.get_strategy_config('double_bottom'))
        }
        
        # 전략 최적화 엔진
        self.optimizer = StrategyOptimizer()
        
        # 기존 보유 보호
        self.holding_protector = HoldingProtector()
        
        # 급등/급락 감지기
        self.surge_detector = SurgeDetector()
        
        # ⭐ 고정 화면 표시 시스템
        self.display = FixedScreenDisplay(max_positions=7)
        # clear_screen()은 render()에서 자동으로 첫 실행만 수행
        
        # ⭐ 시장 조건 분석기
        self.market_analyzer = market_condition_analyzer
        
        # ⭐ v6.30.1 Phase 2B: Advanced Trading Features
        # 1. Dynamic Stop Loss
        if Config.ENABLE_DYNAMIC_STOP_LOSS:
            from src.strategies.dynamic_stop_loss import DynamicStopLoss
            self.dynamic_stop_loss = DynamicStopLoss(self.learning_engine, Config)
            self.logger.log_info("🎯 동적 손절 시스템 활성화 (AI 학습 기반)")
        else:
            self.dynamic_stop_loss = None
        
        # 2. Scaled Sell Manager
        if os.getenv('ENABLE_SCALED_SELL', 'false').lower() == 'true':
            from src.strategies.scaled_sell import ScaledSellManager
            self.scaled_sell = ScaledSellManager(Config)
            self.logger.log_info(f"📊 분할 매도 활성화: {self.scaled_sell.get_config_summary()}")
        else:
            self.scaled_sell = None
        
        # 3. Conditional Sell Manager
        if os.getenv('ENABLE_CONDITIONAL_SELL', 'false').lower() == 'true':
            from src.strategies.conditional_sell import ConditionalSellManager
            self.conditional_sell = ConditionalSellManager(Config, self.market_analyzer)
            self.logger.log_info(f"🔍 조건부 매도 활성화: {self.conditional_sell.get_config_summary()}")
        else:
            self.conditional_sell = None
        
        # ⭐ 동적 코인 선정 시스템
        self.dynamic_coin_selector = None
        if Config.ENABLE_DYNAMIC_COIN_SELECTION:
            print("🔄 동적 코인 선정 시스템 활성화")
            self.dynamic_coin_selector = DynamicCoinSelector(coin_count=Config.FIXED_COIN_COUNT)
            print(f"📈 코인 개수: {Config.FIXED_COIN_COUNT}개 (고정)")
            print(f"⏱️ 선정 간격: {Config.COIN_SELECTION_INTERVAL}초 ({Config.COIN_SELECTION_INTERVAL//60}분)")
            print(f"🎯 선정 방법: {Config.COIN_SELECTION_METHOD}")
            
            # 초기 코인 선정
            self.tickers = self.dynamic_coin_selector.get_coins(method=Config.COIN_SELECTION_METHOD)
            print(f"✅ 초기 선정 완료: {len(self.tickers)}개 코인")
        else:
            # 기존 화이트리스트 방식
            print("🔍 코인 목록 검증 중...")
            all_tickers = Config.WHITELIST_COINS
            self.tickers = self.api.validate_tickers(all_tickers)
            
            if len(self.tickers) < len(all_tickers):
                print(f"⚠️ {len(all_tickers) - len(self.tickers)}개 코인이 제외되었습니다")
            
            print(f"✅ 거래 대상: {len(self.tickers)}개 코인")
        
        if not self.tickers:
            raise ValueError("거래 가능한 코인이 없습니다!")
        
        # ⭐ 실시간 잔고 감지 (Upbit 실제 KRW 사용)
        self.use_real_balance = Config.USE_REAL_BALANCE and mode == 'live'
        if self.use_real_balance:
            print("💰 실시간 잔고 감지 활성화: Upbit 실제 KRW 사용")
            self._update_real_balance()
        
        # ⭐ 기존 보유 코인 제외 (투자금으로 미사용)
        self.existing_holdings = {}
        if mode == 'live':
            self._load_existing_holdings()
            print(f"📦 기존 보유 코인: {len(self.existing_holdings)}개 (투자금 제외)")
        
        # 타이밍 설정 (v5.5 업데이트)
        self.last_trade_time = {}
        self.min_trade_interval = 60
        self.full_scan_interval = 60   # ⭐ v6.30.9: 20초 → 60초 (전체 스캔, 동적 갱신 충돌 방지)
        self.position_check_interval = 3  # ⭐ v6.30.9: 7초 → 3초 (빠른 청산 속도)
        self.surge_scan_interval = 5   # ⭐ 유지: 5초 (초단타 급등/급락 감지)
        self.coin_update_interval = 180  # 3분 (동적 코인 갱신)
        self.last_full_scan_time = 0
        self.last_position_check_time = 0
        self.last_surge_scan_time = 0
        self.last_coin_update_time = 0
        self.last_screen_clear_time = 0  # ⭐ v6.30.69: 10분마다 화면 클리어
        
        # 화면 갱신 주기
        self.display_update_interval = 3  # 3초마다 화면 갱신
        self.last_display_update_time = 0
        self.screen_clear_interval = 600  # ⭐ v6.30.69: 10분 = 600초
        
        # 초단타 포지션 (v5.4: 기본 3개, 최대 5개)
        self.ultra_positions = {}
        self.default_ultra_positions = Config.ULTRA_SCALPING_CONFIG.get('default_positions', 3)
        self.max_ultra_positions = Config.ULTRA_SCALPING_CONFIG.get('max_positions', 5)
        self.high_confidence_threshold = Config.ULTRA_SCALPING_CONFIG.get('high_confidence_threshold', 0.8)
        
        # === 알림 스케줄러 시작 ===
        self.notification_scheduler = NotificationScheduler(
            telegram_notifier=self.telegram,
            email_reporter=self.email_reporter,
            get_summary_callback=self.get_summary_data
        )
        if mode == 'live':
            self.notification_scheduler.start()
            self.logger.log_info("📢 알림 스케줄러 시작")
        
        # ⭐ 매도 실패 추적 시스템 (v6.30.13)
        self.failed_sell_tracker = {}  # {ticker: {'count': int, 'last_attempt': datetime}}
        
        # 실행 플래그
        self.running = False
        
        self.logger.log_info("✅ 모든 시스템 초기화 완료")
    
    def get_current_strategy_weights(self) -> Dict[str, float]:
        """현재 시간대의 전략 가중치 가져오기 (학습 기반 최적화)"""
        current_hour = datetime.now().hour
        base_weights = Config.get_time_weights(current_hour)
        
        # 감정 점수 가져오기
        sentiment_score = 0.5
        if self.sentiment_analyzer:
            sentiment = self.sentiment_analyzer.get_market_sentiment()
            sentiment_score = sentiment['score']
            
            self.logger.log_info(
                f"📊 시장 감정: {sentiment['label']} ({sentiment['score']:.2f})"
            )
        
        # 시장 상황 분석 (대표 코인 기준)
        try:
            df = self.api.get_ohlcv('KRW-BTC', interval="minute5", count=200)
            if df is not None and not df.empty:
                volatility, trend, volume, sentiment_label = analyze_market_condition(df, sentiment_score)
                
                market_condition = MarketCondition(
                    volatility=volatility,
                    trend=trend,
                    volume=volume,
                    sentiment=sentiment_label
                )
                
                # 시장 상황 로그
                market_desc = get_market_description(volatility, trend, volume, sentiment_label)
                self.logger.log_info(f"📈 시장 상황: {market_desc}")
                
                # 학습 기반 최적화된 가중치 계산
                optimized_weights = self.optimizer.get_optimized_weights(
                    market_condition, 
                    base_weights
                )
                
                # 최적 전략 추천
                best_strategy = self.optimizer.get_best_strategy(market_condition)
                self.logger.log_info(f"🎯 추천 전략: {best_strategy}")
                
                return optimized_weights
        except Exception as e:
            self.logger.log_error("MARKET_ANALYSIS", "시장 분석 실패", e)
        
        # 실패 시 기본 가중치
        return base_weights
    
    def select_strategy(self, weights: Dict[str, float]) -> str:
        """가중치 기반 전략 선택"""
        strategies = list(weights.keys())
        probabilities = list(weights.values())
        
        selected = random.choices(strategies, weights=probabilities, k=1)[0]
        return selected
    
    def analyze_ticker(self, ticker: str, strategy_name: str):
        """
        티커 분석 및 거래 신호 생성 (AI 학습 통합)
        
        Args:
            ticker: 코인 티커
            strategy_name: 사용할 전략 이름
        """
        try:
            # 최소 거래 간격 확인
            last_time = self.last_trade_time.get(ticker, 0)
            if time.time() - last_time < self.min_trade_interval:
                return
            
            # 🆕 1. 실시간 호가창 모니터링
            orderbook_signal = None
            if self.orderbook_monitor:
                try:
                    orderbook_analysis = self.orderbook_monitor.get_cached_orderbook(ticker)
                    if orderbook_analysis:
                        # 호가창 기반 진입 판단
                        should_use_limit = self.orderbook_monitor.should_use_limit_order(ticker, 100000)
                        orderbook_signal = {
                            'use_limit': should_use_limit,
                            'liquidity_score': orderbook_analysis.get('liquidity_score', 50),
                            'slippage_risk': orderbook_analysis.get('slippage_risk', 'MEDIUM')
                        }
                except Exception as e:
                    self.logger.log_error("ORDERBOOK_ERROR", f"{ticker} 호가창 분석 실패", e)
            
            # 🆕 2. 실시간 체결 데이터 분석
            trade_signal = None
            if self.trade_monitor:
                try:
                    trade_analysis = self.trade_monitor.monitor_trades(ticker, count=100)
                    if trade_analysis:
                        # 매수/매도 강도 기반 진입 판단
                        entry_decision = self.trade_monitor.should_enter_trade(ticker)
                        trade_signal = {
                            'buy_strength': trade_analysis.get('buy_strength', 50),
                            'sell_strength': trade_analysis.get('sell_strength', 50),
                            'signal': trade_analysis.get('strength_signal', 'NEUTRAL'),
                            'should_enter': entry_decision.get('should_enter', False),
                            'confidence': entry_decision.get('confidence', 0)
                        }
                except Exception as e:
                    self.logger.log_error("TRADE_MONITOR_ERROR", f"{ticker} 체결 분석 실패", e)
            
            # OHLCV 데이터 가져오기
            df = self.api.get_ohlcv(ticker, interval="minute5", count=200)
            if df is None or df.empty:
                return
            
            # 전략 선택
            strategy = self.strategies.get(strategy_name)
            if not strategy or not strategy.enabled:
                return
            
            # 신호 생성
            signal, reason, indicators = strategy.generate_signal(df, ticker)
            
            # 🔥 AI 학습 기반 신호 보정 (⭐ v6.31.6: 신뢰도 임계값 10% 상향)
            if trade_signal and trade_signal.get('should_enter') and trade_signal.get('confidence') >= 66:  # 60 → 66
                # 체결 데이터가 강한 매수 신호를 주면 신호 강화
                if signal == 'HOLD' and trade_signal['signal'] in ['BUY', 'STRONG_BUY']:
                    signal = 'BUY'
                    reason += f" + 체결 신호: {trade_signal['signal']} (신뢰도 {trade_signal['confidence']}%)"
            
            # 신호 로그는 BUY/SELL만 (HOLD는 제외)
            # if signal != 'HOLD':
            #     self.logger.log_signal(ticker, signal, strategy_name, indicators)
            
            # 매수 신호 처리
            if signal == 'BUY':
                # 호가창/체결 신호 전달
                self.execute_buy(
                    ticker, strategy_name, reason, indicators,
                    orderbook_signal=orderbook_signal,
                    trade_signal=trade_signal
                )
            
            # 매도 신호 처리 (포지션 보유 중일 때)
            elif signal == 'SELL' and ticker in self.risk_manager.positions:
                self.execute_sell(ticker, reason)
            
            # 기존 포지션 손익 체크
            self.check_positions(ticker, strategy)
            
        except Exception as e:
            self.logger.log_error("ANALYZE_ERROR", f"{ticker} 분석 실패", e)
    
    def execute_buy(self, ticker: str, strategy: str, reason: str, indicators: Dict,
                    orderbook_signal: Dict = None, trade_signal: Dict = None, is_chase: bool = False, surge_info: Dict = None):
        """
        매수 실행 (v6.29: Advanced Order System 통합)
        
        Args:
            ticker: 코인 티커
            strategy: 전략 이름
            reason: 매수 사유
            indicators: 지표 데이터
            orderbook_signal: 호가창 신호 (선택)
            trade_signal: 체결 신호 (선택)
            is_chase: 추격매수 여부 (v6.29)
            surge_info: 급등 정보 (v6.29)
        """
        try:
            # 포지션 개설 가능 여부 확인
            can_open, msg = self.risk_manager.can_open_position(ticker)
            if not can_open:
                self.logger.log_warning(f"매수 불가: {ticker} - {msg}")
                return
            
            # 현재가 조회
            current_price = self.api.get_current_price(ticker)
            if not current_price:
                return
            
            # ⭐ v6.31.7: 스마트 포지션 사이징 (점수 기반 10만~50만원)
            position_size, sizing_detail = self.position_sizer.get_recommended_position(
                ticker=ticker,
                api=self.api,
                surge_info=surge_info,
                ai_decision={'confidence': trade_signal.get('confidence', 0) / 100 if trade_signal else 0},
                current_balance=self.risk_manager.current_balance
            )
            
            investment = position_size
            
            # 로그 출력
            _original_print(f"\n💰 [SMART-SIZING] {ticker}")
            _original_print(f"   종합 점수: {sizing_detail['total_score']:.1f}/100")
            _original_print(f"   - 급등: {sizing_detail['surge_score']:.0f}, AI: {sizing_detail['ai_confidence']:.0f}")
            _original_print(f"   - 거래량: {sizing_detail['volume_ratio']:.1f}x, 모멘텀: {sizing_detail['price_momentum']:+.2f}%")
            _original_print(f"   호가창 깊이: {sizing_detail['orderbook_depth']['total_ask_amount_krw']:,.0f}원")
            _original_print(f"   예상 슬리피지: {sizing_detail['slippage_estimate']:.3f}%")
            _original_print(f"   → 결정: {investment:,.0f}원 매수\n")
            
            if investment < 5000:
                self.logger.log_warning(f"투자 금액 부족: {ticker} - {investment:,.0f}원")
                return
            
            # 수량 계산
            amount = investment / current_price
            
            # ⭐ v6.29: SmartOrderExecutor 사용
            market_condition = {
                'volatility': indicators.get('volatility', 'medium'),
                'trend': indicators.get('trend', 'neutral'),
                'market_phase': indicators.get('market_phase', 'neutral')
            }
            
            # 실거래 모드에서만 실제 주문
            order_result = None
            if self.mode == 'live' and self.api.upbit:
                order_result = self.smart_order_executor.execute_buy(
                    ticker=ticker,
                    investment=investment,
                    strategy=strategy,
                    market_condition=market_condition,
                    is_chase=is_chase
                )
                if not order_result:
                    return
            else:
                self.logger.log_info(f"[모의거래] 매수: {ticker}, {investment:,.0f}원")
            
            # 포지션 추가
            success = self.risk_manager.add_position(
                ticker=ticker,
                amount=amount,
                price=current_price,
                strategy=strategy
            )
            
            
            if success:
                # 기존 보유 보호 시스템에도 봇 포지션 추가
                self.holding_protector.add_bot_position(
                    ticker=ticker,
                    amount=amount,
                    price=current_price,
                    strategy=strategy
                )
                
                # 🎓 AI 학습: 매수 경험 기록
                try:
                    market_condition = indicators.copy()
                    market_condition['trend'] = 'up' if indicators.get('price_change', 0) > 0 else 'down'
                    market_condition['market_phase'] = 'bullish' if indicators.get('rsi', 50) < 40 else 'neutral'
                    
                    entry_time_id = self.learning_engine.record_trade_entry(
                        ticker=ticker,
                        strategy=strategy,
                        entry_price=current_price,
                        entry_amount=amount,
                        market_condition=market_condition,
                        order_method=order_result.get('order_method') if order_result else None,
                        surge_score=surge_info.get('surge_score') if surge_info else None,
                        confidence=surge_info.get('confidence') if surge_info else None,
                        slippage_pct=order_result.get('slippage_pct') if order_result else None,
                        spread_pct=order_result.get('spread_pct') if order_result else None
                    )
                    
                    # 포지션에 entry_time_id 저장 (청산 시 사용)
                    if ticker in self.risk_manager.positions:
                        self.risk_manager.positions[ticker].entry_time_id = entry_time_id
                        
                        # ⭐ v6.30.1: Dynamic Stop Loss 적용
                        if self.dynamic_stop_loss:
                            stop_loss_price = self.dynamic_stop_loss.calculate_optimal_stop_loss(
                                ticker, strategy, current_price, market_condition
                            )
                            self.risk_manager.positions[ticker].stop_loss_price = stop_loss_price
                            self.logger.log_info(
                                f"🎯 동적 손절가 설정: {ticker} → {stop_loss_price:,.0f}원 "
                                f"({((stop_loss_price/current_price-1)*100):+.2f}%)"
                            )
                        
                except Exception as e:
                    self.logger.log_warning(f"⚠️  AI 학습 기록 실패: {e}")
                
                # 거래 로그
                self.logger.log_trade(
                    action='BUY',
                    ticker=ticker,
                    price=current_price,
                    amount=amount,
                    strategy=strategy,
                    reason=reason,
                    profit_loss=0.0,
                    balance=self.risk_manager.current_balance,
                    metadata=indicators
                )
                
                # ⭐ 매수 즉시 화면에 포지션 표시
                slot = self.display.get_available_slot()
                if slot:
                    position = self.risk_manager.positions[ticker]
                    self.display.update_position(
                        slot=slot,
                        ticker=ticker,
                        entry_price=current_price,
                        current_price=current_price,
                        amount=amount,
                        strategy=strategy,
                        entry_time=position.entry_time
                    )
                    self.display.render()  # 즉시 화면 갱신
                    
                    # 작업 상태에 매수 완료 표시
                    coin_short = ticker.split('-')[1]
                    self.display.update_monitoring(
                        f"✅ {coin_short} 매수 완료",
                        f"슬롯 {slot} | {investment:,.0f}원",
                        f"전략: {strategy}"
                    )
                    self.display.render()
                    time.sleep(1)  # 1초간 표시
                
                self.last_trade_time[ticker] = time.time()
            
        except Exception as e:
            self.logger.log_error("BUY_ERROR", f"{ticker} 매수 실패", e)
    
    def execute_sell(self, ticker: str, reason: str):
        """
        매도 실행 (⭐ v6.29 확장: SmartOrderExecutor + ExitReason 연동)
        
        Args:
            ticker: 코인 티커
            reason: 매도 사유
        """
        _original_print(f"[EXECUTE-SELL] execute_sell() 호출됨 - ticker: {ticker}, reason: {reason}")
        try:
            if ticker not in self.risk_manager.positions:
                _original_print(f"[EXECUTE-SELL] ❌ 포지션 없음! ticker={ticker}")
                _original_print(f"[EXECUTE-SELL] 현재 보유 포지션 목록: {list(self.risk_manager.positions.keys())}")
                return
            
            position = self.risk_manager.positions[ticker]
            _original_print(f"[EXECUTE-SELL] ✅ 포지션 찾음: {ticker}, amount={position.amount}, avg_price={position.avg_buy_price}")
            
            # 현재가 조회 (⭐ v6.30.13: 재시도 로직 추가)
            _original_print(f"[EXECUTE-SELL] 현재가 조회 시작...")
            current_price = None
            for attempt in range(3):  # 최대 3회 재시도
                _original_print(f"[EXECUTE-SELL] 가격 조회 시도 {attempt+1}/3...")
                try:
                    current_price = self.api.get_current_price(ticker)
                    _original_print(f"[EXECUTE-SELL] 가격 조회 결과: {current_price}")
                    if current_price:
                        break
                except Exception as e:
                    _original_print(f"[EXECUTE-SELL] 가격 조회 예외: {e}")
                if attempt < 2:
                    time.sleep(0.5)  # 0.5초 대기 후 재시도
            
            if not current_price:
                self.logger.log_error("PRICE_FETCH_FAILED", f"{ticker} 가격 조회 3회 실패", None)
                _original_print(f"[EXECUTE-SELL] ❌ 가격 조회 실패 - 평균 매수가로 대체")
                current_price = position.avg_buy_price  # ⭐ v6.30.67: 가격 실패 시에도 청산 진행
            
            # 손익률 계산
            _original_print(f"[EXECUTE-SELL] 손익률 계산 중...")
            profit_ratio = ((current_price - position.avg_buy_price) / position.avg_buy_price) * 100
            _original_print(f"[EXECUTE-SELL] 손익률: {profit_ratio:+.2f}%")
            
            # ⭐ ExitReason 파싱 (매도 사유 분석)
            _original_print(f"[EXECUTE-SELL] ExitReason 파싱 중...")
            from src.utils.order_method_selector import ExitReason
            
            exit_reason = ExitReason.TAKE_PROFIT  # 기본값
            if "손절" in reason or "stop" in reason.lower():
                exit_reason = ExitReason.STOP_LOSS
            elif "트레일링" in reason or "trailing" in reason.lower():
                exit_reason = ExitReason.TRAILING_STOP
            elif "차트" in reason or "MACD" in reason or "RSI" in reason:
                exit_reason = ExitReason.CHART_SIGNAL
            elif "시간초과" in reason or "time" in reason.lower():
                exit_reason = ExitReason.TIME_EXCEEDED
            elif "급락" in reason or "drop" in reason.lower():
                exit_reason = ExitReason.SUDDEN_DROP
            elif "거래량" in reason or "volume" in reason.lower():
                exit_reason = ExitReason.VOLUME_DROP
            
            _original_print(f"[EXECUTE-SELL] ExitReason: {exit_reason}")
            
            # ⭐ 스프레드 분석
            _original_print(f"[EXECUTE-SELL] 스프레드 분석 중...")
            try:
                spread_pct = self.api.calculate_spread_percentage(ticker)
                _original_print(f"[EXECUTE-SELL] 스프레드: {spread_pct:.2f}%")
            except Exception as e:
                _original_print(f"[EXECUTE-SELL] 스프레드 계산 실패: {e}, 기본값 0.1 사용")
                spread_pct = 0.1
            
            # ⭐ 시장 조건 분석
            _original_print(f"[EXECUTE-SELL] 시장 조건 분석 중...")
            market_condition = {}
            try:
                df = self.api.get_ohlcv(ticker, interval="minute5", count=50)
                if df is not None and not df.empty:
                    # 변동성
                    returns = df['close'].pct_change().dropna()
                    volatility = returns.std() * 100
                    
                    # 추세
                    price_change = ((df['close'].iloc[-1] - df['close'].iloc[0]) / df['close'].iloc[0]) * 100
                    
                    market_condition = {
                        'volatility': 'high' if volatility > 2.0 else 'medium' if volatility > 1.0 else 'low',
                        'trend': 'bullish' if price_change > 1.0 else 'bearish' if price_change < -1.0 else 'neutral'
                    }
                    _original_print(f"[EXECUTE-SELL] 시장 조건: {market_condition}")
            except Exception as e:
                _original_print(f"[EXECUTE-SELL] 시장 조건 분석 실패: {e}, 기본값 사용")
                market_condition = {'volatility': 'medium', 'trend': 'neutral'}
            
            # ⭐ SmartOrderExecutor로 주문 방법 자동 선택
            _original_print(f"[EXECUTE-SELL] 주문 방법 선택 중...")
            try:
                order_method, method_reason = self.order_method_selector.select_sell_method(
                    ticker=ticker,
                    strategy=position.strategy,
                    exit_reason=exit_reason,
                    market_condition=market_condition,
                    spread_pct=spread_pct,
                    profit_ratio=profit_ratio
                )
                _original_print(f"[EXECUTE-SELL] 주문 방법: {order_method}, 이유: {method_reason}")
            except Exception as e:
                _original_print(f"[EXECUTE-SELL] 주문 방법 선택 실패: {e}, 시장가 주문 사용")
                order_method = "market"
                method_reason = "fallback"
            
            # 기존 보유 보호: 매도 가능 수량 확인 (v5.7: 투자금 + 이익분만)
            # ⭐ v6.30.65: 모의거래 모드에서는 holding_protector 체크 우회
            sell_amount = position.amount
            
            if self.mode == 'live':
                # 실거래 모드에서만 보유 보호 체크
                sellable_amount, sell_msg = self.holding_protector.calculate_sellable_amount(
                    ticker,
                    current_price=current_price,
                    upbit_api=self.api.upbit
                )
                
                # 기존 보유가 있으면 봇 투자분만 매도
                if self.holding_protector.is_existing_holding(ticker):
                    if sellable_amount <= 0:
                        self.logger.log_warning(
                            f"🛡️  {ticker} 매도 불가: 기존 보유 보호 중 ({sell_msg})"
                        )
                        _original_print(f"[EXECUTE-SELL] ❌ 실거래 모드: 기존 보유 보호로 매도 차단")
                        return
                    
                    sell_amount = min(sell_amount, sellable_amount)
                    self.logger.log_info(
                        f"🛡️  {ticker} 부분 매도: {sell_amount:.8f} (기존 보유 보호)"
                    )
            else:
                # 모의거래 모드: 포지션 전체 매도
                _original_print(f"[EXECUTE-SELL] 모의거래 모드: 포지션 전체 매도 허용 (holding_protector 우회)")
            
            # ⭐ SmartOrderExecutor로 매도 주문 실행 (⭐ v6.30.13: 재시도 + 추적)
            # ⭐ v6.30.64: 모의거래 모드에서도 포지션 청산 진행하도록 수정
            order_result = None
            order_success = False
            
            if self.mode == 'live' and self.api.upbit:
                _original_print(f"[EXECUTE-SELL] 실거래 모드: 실제 매도 주문 실행")
                # 최대 3회 재시도
                max_attempts = 3
                for attempt in range(max_attempts):
                    _original_print(f"[EXECUTE-SELL] 매도 시도 {attempt+1}/{max_attempts}...")
                    order_result = self.smart_order_executor.execute_sell(
                        ticker=ticker,
                        volume=sell_amount,
                        strategy=position.strategy,
                        exit_reason_enum=exit_reason,
                        profit_ratio=profit_ratio,
                        market_condition=market_condition
                    )
                    
                    if order_result and order_result.get('success'):
                        # 성공 시 실패 추적 리셋
                        if ticker in self.failed_sell_tracker:
                            del self.failed_sell_tracker[ticker]
                        order_success = True
                        _original_print(f"[EXECUTE-SELL] ✅ 실거래 매도 주문 성공")
                        break
                    
                    self.logger.log_warning(f"{ticker} 매도 시도 {attempt+1}/{max_attempts} 실패")
                    _original_print(f"[EXECUTE-SELL] ⚠️ 매도 시도 {attempt+1}/{max_attempts} 실패")
                    
                    if attempt < max_attempts - 1:
                        time.sleep(1)  # 1초 대기 후 재시도
                
                # 최종 실패 시 추적 및 알림 (하지만 포지션 청산은 계속 진행)
                if not order_success:
                    # 실패 횟수 기록
                    if ticker not in self.failed_sell_tracker:
                        self.failed_sell_tracker[ticker] = {'count': 0, 'last_attempt': datetime.now()}
                    
                    self.failed_sell_tracker[ticker]['count'] += 1
                    self.failed_sell_tracker[ticker]['last_attempt'] = datetime.now()
                    failure_count = self.failed_sell_tracker[ticker]['count']
                    
                    # 5회 연속 실패 시 긴급 알림
                    if failure_count >= 5:
                        self.logger.log_critical(
                            f"🚨 {ticker} 긴급: {failure_count}회 연속 매도 실패! "
                            f"현재 손익: {profit_ratio:+.2f}% - 수동 매도 필요!"
                        )
                    
                    self.logger.log_error("SELL_ORDER_FAILED", f"{ticker} 매도 주문 {max_attempts}회 실패", None)
                    _original_print(f"[EXECUTE-SELL] ❌ 실거래 매도 주문 실패 - 하지만 포지션 청산은 계속 진행")
                    # ⭐ 중요: return 하지 않고 포지션 청산 계속 진행
            else:
                _original_print(f"[EXECUTE-SELL] 모의거래 모드: 매도 주문 시뮬레이션")
                self.logger.log_info(f"[모의거래] 매도: {ticker}, {sell_amount:.8f}")
                _original_print(f"[EXECUTE-SELL] 모의거래 매도 완료: {ticker}, amount={sell_amount:.8f}")
                order_success = True
            
            # 기존 보유 보호 시스템에서 봇 포지션 청산
            _original_print(f"[EXECUTE-SELL] ========== 포지션 청산 시작 ==========")
            _original_print(f"[EXECUTE-SELL] holding_protector.close_bot_position() 호출...")
            bot_profit_loss = None
            try:
                bot_profit_loss = self.holding_protector.close_bot_position(
                    ticker, sell_amount, current_price
                )
                _original_print(f"[EXECUTE-SELL] ✅ holding_protector 청산 완료, P/L: {bot_profit_loss}")
            except Exception as e:
                _original_print(f"[EXECUTE-SELL] ❌ holding_protector 청산 실패: {e}")
                import traceback
                _original_print(f"[EXECUTE-SELL] 스택 트레이스:\n{traceback.format_exc()}")
            
            # 리스크 관리자에서도 포지션 청산
            _original_print(f"[EXECUTE-SELL] risk_manager.close_position() 호출...")
            profit_loss = None
            try:
                profit_loss = self.risk_manager.close_position(ticker, current_price)
                _original_print(f"[EXECUTE-SELL] ✅ risk_manager 청산 완료, P/L: {profit_loss}")
                _original_print(f"[EXECUTE-SELL] 포지션 제거 후 남은 포지션: {list(self.risk_manager.positions.keys())}")
            except Exception as e:
                _original_print(f"[EXECUTE-SELL] ❌ risk_manager 청산 실패: {e}")
                import traceback
                _original_print(f"[EXECUTE-SELL] 스택 트레이스:\n{traceback.format_exc()}")
            
            # ⭐ 화면에서 포지션 제거
            _original_print(f"[EXECUTE-SELL] ========== 화면 업데이트 시작 ==========")
            _original_print(f"[EXECUTE-SELL] 화면에서 포지션 제거 시작...")
            try:
                slot = self.display.get_slot_by_ticker(ticker)
                _original_print(f"[EXECUTE-SELL] 화면 슬롯: {slot}")
                if slot:
                    # ⭐ 수정: avg_buy_price 사용
                    if profit_loss is not None:
                        profit_ratio = (profit_loss / (position.avg_buy_price * position.amount)) * 100 if position.amount > 0 else 0
                    else:
                        profit_ratio = 0
                    
                    _original_print(f"[EXECUTE-SELL] display.remove_position() 호출...")
                    self.display.remove_position(slot, current_price, profit_loss if profit_loss else 0, profit_ratio)
                    _original_print(f"[EXECUTE-SELL] ✅ 화면에서 포지션 제거 완료")
                    
                    # 작업 상태에 로그 기록 완료 표시
                    result = "수익" if (profit_loss and profit_loss > 0) else "손실"
                    coin_short = ticker.split('-')[1]
                    self.display.update_monitoring(
                        f"✅ {coin_short} 매도 완료",
                        f"{result}: {profit_loss if profit_loss else 0:+,.0f}원 ({profit_ratio:+.2f}%)",
                        f"로그 기록 완료"
                    )
                    self.display.render()
                    _original_print(f"[EXECUTE-SELL] ✅ 화면 렌더링 완료")
                    time.sleep(1)  # 1초간 표시
                else:
                    _original_print(f"[EXECUTE-SELL] ⚠️ 화면 슬롯을 찾을 수 없음: {ticker}")
            except Exception as e:
                _original_print(f"[EXECUTE-SELL] ❌ 화면 업데이트 실패: {e}")
                import traceback
                _original_print(f"[EXECUTE-SELL] 스택 트레이스:\n{traceback.format_exc()}")
            
            if profit_loss is not None:
                # 거래 로그
                self.logger.log_trade(
                    action='SELL',
                    ticker=ticker,
                    price=current_price,
                    amount=position.amount,
                    strategy=position.strategy,
                    reason=reason,
                    profit_loss=profit_loss,
                    balance=self.risk_manager.current_balance
                )
                
                # 전략 학습 기록
                try:
                    # 시장 상황 분석
                    df = self.api.get_ohlcv(ticker, interval="minute5", count=200)
                    if df is not None and not df.empty:
                        sentiment_score = 0.5
                        if self.sentiment_analyzer:
                            sentiment_score = self.sentiment_analyzer.get_market_sentiment()['score']
                        
                        volatility, trend, volume, sentiment_label = analyze_market_condition(df, sentiment_score)
                        market_condition = MarketCondition(
                            volatility=volatility,
                            trend=trend,
                            volume=volume,
                            sentiment=sentiment_label
                        )
                        
                        # 보유 시간 계산
                        hold_time = (datetime.now() - position.entry_time).total_seconds()
                        
                        # 기존 학습 기록 (전략 최적화용)
                        self.optimizer.record_trade(
                            strategy=position.strategy,
                            profit_loss=profit_loss,
                            market_condition=market_condition,
                            entry_price=position.avg_buy_price,
                            exit_price=current_price,
                            hold_time=hold_time
                        )
                        
                        # 🎓 AI 학습: 매도 경험 기록
                        try:
                            # 시장 스냅샷 생성
                            market_snapshot_dict = {
                                'rsi': indicators.get('rsi', 50) if 'rsi' in locals() else 50,
                                'volatility': volatility,
                                'trend': trend,
                                'volume_ratio': volume,
                                'market_phase': sentiment_label,
                                'price': current_price
                            }
                            
                            # entry_time_id 가져오기
                            entry_time_id = getattr(position, 'entry_time_id', position.entry_time.isoformat())
                            
                            # ⭐ v6.29: exit_reason 추가
                            self.learning_engine.record_trade_exit(
                                ticker=ticker,
                                strategy=position.strategy,
                                exit_price=current_price,
                                entry_time=entry_time_id,
                                market_condition=market_snapshot_dict,
                                exit_reason=exit_reason.value if hasattr(exit_reason, 'value') else str(exit_reason)
                            )
                            
                            # ⭐ 매도 직후 학습 통계 즉시 화면 업데이트
                            stats = self.learning_engine.get_stats()
                            total_trades = 0
                            profit_trades = 0
                            loss_trades = 0
                            
                            for strat_name, strat_stat in self.learning_engine.strategy_stats.items():
                                total_trades += strat_stat.get('total_trades', 0)
                                profit_trades += strat_stat.get('winning_trades', 0)
                                loss_trades += strat_stat.get('losing_trades', 0)
                            
                            # ⭐ v6.30.17: 손실 발생 시 LossAnalyzer 자동 분석
                            if profit_loss < 0 and self.loss_analyzer:
                                loss_analysis = self.loss_analyzer.analyze_loss(
                                    ticker=ticker,
                                    entry_price=position.avg_buy_price,
                                    exit_price=current_price,
                                    entry_scenario=getattr(position, 'entry_scenario', 'UNKNOWN'),
                                    selected_strategy=position.strategy,
                                    hold_time=hold_time,
                                    profit_loss=profit_loss,
                                    market_data=df
                                )
                                
                                # 손실 분석 결과 로그
                                if loss_analysis:
                                    self.logger.log_warning(
                                        f"📉 손실 분석: {ticker} | "
                                        f"원인: {loss_analysis.get('loss_category', 'UNKNOWN')} | "
                                        f"대안: {loss_analysis.get('alternative_strategy', 'N/A')}"
                                    )
                            
                            self.display.update_ai_learning(
                                total_trades=total_trades,
                                profit_trades=profit_trades,
                                loss_trades=loss_trades
                            )
                            self.display.render()  # 즉시 화면 갱신
                            
                        except Exception as e:
                            self.logger.log_warning(f"⚠️  AI 학습 기록 실패: {e}")
                        
                        # 성과 로그
                        result = "수익" if profit_loss > 0 else "손실"
                        self.logger.log_info(
                            f"📚 학습 기록: {position.strategy} - {result} {profit_loss:+,.0f}원 "
                            f"(시장: {get_market_description(volatility, trend, volume, sentiment_label)})"
                        )
                except Exception as e:
                    self.logger.log_error("LEARNING_ERROR", "학습 기록 실패", e)
                
                self.last_trade_time[ticker] = time.time()
            
        except Exception as e:
            self.logger.log_error("SELL_ERROR", f"{ticker} 매도 중 예외 발생 - 포지션 강제 청산 진행", e)
            _original_print(f"[EXECUTE-SELL] ⚠️ 예외 발생: {e}")
            import traceback
            _original_print(f"[EXECUTE-SELL] 스택 트레이스:\n{traceback.format_exc()}")
            
            # ⭐ v6.30.66: 예외 발생 시에도 포지션 강제 청산
            _original_print(f"[EXECUTE-SELL] ========== 예외 발생 - 포지션 강제 청산 시작 ==========")
            try:
                if ticker in self.risk_manager.positions:
                    position = self.risk_manager.positions[ticker]
                    current_price = self.api.get_current_price(ticker)
                    
                    if not current_price:
                        # 가격 조회 실패 시 평균 매수가로 청산
                        current_price = position.avg_buy_price
                        _original_print(f"[EXECUTE-SELL] ⚠️ 가격 조회 실패, 평균 매수가로 청산: {current_price}")
                    
                    # holding_protector 청산
                    _original_print(f"[EXECUTE-SELL] holding_protector.close_bot_position() 호출...")
                    try:
                        bot_profit_loss = self.holding_protector.close_bot_position(
                            ticker, position.amount, current_price
                        )
                        _original_print(f"[EXECUTE-SELL] ✅ holding_protector 청산 완료, P/L: {bot_profit_loss}")
                    except Exception as e2:
                        _original_print(f"[EXECUTE-SELL] ❌ holding_protector 청산 실패: {e2}")
                    
                    # risk_manager 청산
                    _original_print(f"[EXECUTE-SELL] risk_manager.close_position() 호출...")
                    try:
                        profit_loss = self.risk_manager.close_position(ticker, current_price)
                        _original_print(f"[EXECUTE-SELL] ✅ risk_manager 청산 완료, P/L: {profit_loss}")
                        _original_print(f"[EXECUTE-SELL] 포지션 제거 후 남은 포지션: {list(self.risk_manager.positions.keys())}")
                    except Exception as e3:
                        _original_print(f"[EXECUTE-SELL] ❌ risk_manager 청산 실패: {e3}")
                    
                    # UI 업데이트
                    _original_print(f"[EXECUTE-SELL] display.remove_position() 호출...")
                    try:
                        slot = self.display.get_slot_by_ticker(ticker)
                        if slot:
                            self.display.remove_position(slot, current_price, 0, 0)
                            _original_print(f"[EXECUTE-SELL] ✅ UI에서 포지션 제거 완료")
                    except Exception as e4:
                        _original_print(f"[EXECUTE-SELL] ❌ UI 업데이트 실패: {e4}")
                    
                    _original_print(f"[EXECUTE-SELL] ✅ 예외 발생했지만 포지션 강제 청산 완료")
                else:
                    _original_print(f"[EXECUTE-SELL] ⚠️ 포지션이 이미 없음: {ticker}")
            except Exception as cleanup_error:
                _original_print(f"[EXECUTE-SELL] ❌ 강제 청산 중 오류: {cleanup_error}")
                import traceback
                _original_print(f"[EXECUTE-SELL] 청산 오류 스택:\n{traceback.format_exc()}")
    
    def check_positions(self, ticker: str, strategy, position=None):
        """
        포지션 손익 체크 및 자동 청산 (⭐ v6.30.50: 동시성 문제 해결)
        
        10가지 청산 조건:
        0. 리스크 평가 (통합 위험도 분석) ⭐ NEW
        1. 시간 초과 (전략별 max_hold_time)
        2. 트레일링 스탑 (Trailing Stop)
        3. 차트 신호 (RSI, MACD, 거래량)
        4. 급락 감지 (1분 내 -1.5% 이상)
        5. 거래량 급감 (평균 대비 0.5배 이하)
        6. 기본 손익률 (익절/손절)
        7. 분할 매도 (Scaled Sell)
        8. 조건부 매도 (Conditional Sell)
        9. 동적 손절 (Dynamic Stop Loss)
        
        Args:
            ticker: 코인 티커
            strategy: 전략 객체
            position: 포지션 객체 (optional, 동시성 문제 방지용)
        """
        # ⭐ v6.30.48: check_positions 진입 로그 (콘솔)
        
        # ⭐ v6.30.18: check_positions 진입 로그
        
        # ⭐ v6.30.50: 포지션이 전달되지 않은 경우에만 조회
        if position is None:
            if ticker not in self.risk_manager.positions:
                self.logger.log_warning(f"⚠️ {ticker} 포지션 없음 (이미 청산됨?)")
                return
            position = self.risk_manager.positions[ticker]
        else:
            # 포지션이 여전히 존재하는지 재확인
            if ticker not in self.risk_manager.positions:
                return
        current_price = self.api.get_current_price(ticker)
        
        if not current_price:
            self.logger.log_warning(f"⚠️ {ticker} 현재가 조회 실패")
            return
        
        # 손익률 계산
        profit_ratio = ((current_price - position.avg_buy_price) / position.avg_buy_price) * 100
        self.logger.log_info(
            f"💰 {ticker} 현재 상태: "
            f"진입가 {position.avg_buy_price:,.0f}원 → "
            f"현재가 {current_price:,.0f}원 | "
            f"손익률 {profit_ratio:+.2f}%"
        )
        
        # ⭐ 조건 0: 통합 리스크 평가 (새로 추가)
        try:
            # 시장 상황 분석
            market_condition = {'volatility': 'medium', 'trend': 'neutral'}
            
            # 최근 가격 데이터로 변동성 추정
            ohlcv = self.api.get_ohlcv(ticker, interval='minute1', count=10)
            if ohlcv is not None and len(ohlcv) >= 2:
                recent_changes = []
                # DataFrame인 경우 .iloc 사용
                for i in range(1, len(ohlcv)):
                    if isinstance(ohlcv, list):
                        pct_change = ((ohlcv[i]['close'] - ohlcv[i-1]['close']) / ohlcv[i-1]['close']) * 100
                    else:
                        # DataFrame일 때
                        pct_change = ((ohlcv.iloc[i]['close'] - ohlcv.iloc[i-1]['close']) / ohlcv.iloc[i-1]['close']) * 100
                    recent_changes.append(abs(pct_change))
                
                avg_volatility = sum(recent_changes) / len(recent_changes) if recent_changes else 0
                
                if avg_volatility > 2.0:
                    market_condition['volatility'] = 'high'
                elif avg_volatility > 1.0:
                    market_condition['volatility'] = 'medium'
                else:
                    market_condition['volatility'] = 'low'
                
                # 트렌드 판단
                if isinstance(ohlcv, list):
                    price_change_5min = ((current_price - ohlcv[0]['close']) / ohlcv[0]['close']) * 100
                else:
                    price_change_5min = ((current_price - ohlcv.iloc[0]['close']) / ohlcv.iloc[0]['close']) * 100
                if price_change_5min > 1.0:
                    market_condition['trend'] = 'bullish'
                elif price_change_5min < -1.0:
                    market_condition['trend'] = 'bearish'
            
            # 리스크 평가 실행
            risk_eval = self.risk_manager.evaluate_holding_risk(ticker, market_condition)
            
            # 로그 출력
            if risk_eval['risk_level'] in ['HIGH', 'CRITICAL']:
                reasons_str = ', '.join(risk_eval['reasons'])
                self.logger.log_warning(
                    f"⚠️ {ticker} 리스크 평가: {risk_eval['risk_level']} "
                    f"(점수: {risk_eval['risk_score']}/100) - {reasons_str}"
                )
            
            # CRITICAL 리스크 시 즉시 청산
            if risk_eval['risk_level'] == 'CRITICAL':
                _original_print(f"[FORCE-SELL] 🚨 CRITICAL 리스크 강제 매도 시작!")
                try:
                    self.execute_sell(ticker, f"위험도 CRITICAL 청산 ({risk_eval['recommended_action']})")
                    _original_print(f"[FORCE-SELL] ✅ CRITICAL 리스크 매도 완료!")
                except Exception as e:
                    _original_print(f"[FORCE-SELL] ❌ 매도 실패: {e}")
                    import traceback
                    _original_print(f"[FORCE-SELL] ❌ 스택 트레이스:\n{traceback.format_exc()}")
                return
            
            # HIGH 리스크 + 손실 중이면 청산
            if risk_eval['risk_level'] == 'HIGH' and position.profit_loss_ratio < -2.0:
                _original_print(f"[FORCE-SELL] 🚨 HIGH 리스크 강제 매도 시작!")
                try:
                    self.execute_sell(ticker, f"고위험 + 손실 청산 ({risk_eval['recommended_action']})")
                    _original_print(f"[FORCE-SELL] ✅ HIGH 리스크 매도 완료!")
                except Exception as e:
                    _original_print(f"[FORCE-SELL] ❌ 매도 실패: {e}")
                    import traceback
                    _original_print(f"[FORCE-SELL] ❌ 스택 트레이스:\n{traceback.format_exc()}")
                return
            
                
        except Exception as e:
            import traceback
            self.logger.log_warning(f"{ticker} 리스크 평가 실패: {e}")
        
        # 보유 시간 계산
        import time
        hold_time = time.time() - position.entry_time.timestamp()
        
        # 환경 변수 설정 (기본값) - ⭐ v6.30.47: 단축형 설정
        from src.config import Config
        
        # ⭐ v6.31.5: Minimum hold time enforcement (CRITICAL FIX)
        # Prevent premature exits that lock in small losses
        MIN_HOLD_TIME = getattr(Config, 'MIN_HOLD_TIME', 300)  # Default 5 minutes
        
        if hold_time < MIN_HOLD_TIME:
            # Skip ALL exit checks if holding time is less than minimum
            # Exception: Allow CRITICAL risk exits (already handled above)
            return
        max_hold_times = {
            'CHASE_BUY': getattr(Config, 'MAX_HOLD_TIME_CHASE', 300),  # 5분
            'ULTRA_SCALPING': getattr(Config, 'MAX_HOLD_TIME_ULTRA', 600),  # 10분
            'AGGRESSIVE': getattr(Config, 'MAX_HOLD_TIME_AGGRESSIVE', 300),  # 5분 (30분 → 5분)
            'CONSERVATIVE': getattr(Config, 'MAX_HOLD_TIME_CONSERVATIVE', 600),  # 10분 (1시간 → 10분)
            'MEAN_REVERSION': getattr(Config, 'MAX_HOLD_TIME_MEAN_REVERSION', 1800),  # 30분 (2시간 → 30분)
            'GRID': getattr(Config, 'MAX_HOLD_TIME_GRID', 3600)  # 1시간 (24시간 → 1시간)
        }
        
        # 현재 전략의 최대 보유 시간
        max_hold_time = max_hold_times.get(position.strategy, 600)  # 기본 10분 (1시간 → 10분)
        
        # ⭐ v6.30.52: 전략명 정규화 (대소문자 무시)
        strategy_upper = position.strategy.upper() if position.strategy else ''
        if 'AGGRESSIVE' in strategy_upper:
            max_hold_time = 300  # 5분
        elif 'CONSERVATIVE' in strategy_upper:
            max_hold_time = 600  # 10분
        elif 'MEAN' in strategy_upper or 'REVERSION' in strategy_upper:
            max_hold_time = 1800  # 30분
        elif 'GRID' in strategy_upper:
            max_hold_time = 3600  # 1시간
        
        
        # ⭐ v6.30.52: 강제 매도 로직 - 시간 초과 조건 완화
        # 보유 시간이 최대의 80%만 넘어도 매도 (예: 10분 기준 8분 이상)
        force_sell_threshold = max_hold_time * 0.8
        
        
        # ⭐ 조건 1: 시간 초과 청산 (⭐ v6.31.8: 수익 조건 추가)
        if hold_time > force_sell_threshold:
            profit_ratio = ((current_price - position.avg_buy_price) / position.avg_buy_price) * 100
            
            # v6.31.8: 수익/손실 조건 체크
            min_profit = getattr(Config, 'TIME_FORCE_SELL_MIN_PROFIT', 0.3)
            max_loss = getattr(Config, 'TIME_FORCE_SELL_MAX_LOSS', -0.5)
            
            # 조건: +0.3% 이상 OR -0.5% 이하만 매도
            should_force_sell = (profit_ratio >= min_profit) or (profit_ratio <= max_loss)
            
            if should_force_sell:
                _original_print(f"[FORCE-SELL] 🚨 강제 매도 실행 시작!")
                try:
                    self.execute_sell(ticker, f"시간초과청산 (보유:{hold_time/60:.0f}분, 손익:{profit_ratio:+.2f}%)")
                    _original_print(f"[FORCE-SELL] ✅ 매도 주문 완료!")
                except Exception as e:
                    _original_print(f"[FORCE-SELL] ❌ 매도 실패: {e}")
                    import traceback
                    _original_print(f"[FORCE-SELL] ❌ 스택 트레이스:\n{traceback.format_exc()}")
                return
            else:
                # 수익/손실이 기준 범위 내면 계속 보유
                _original_print(f"[HOLD] {ticker} 시간 도달했지만 보유 지속 (손익:{profit_ratio:+.2f}%)")
                # 다른 청산 조건 체크는 계속 진행
        else:
            # ⭐ 조건 2-6: 차트 지표 및 급락/거래량 분석
            try:
                df = self.api.get_ohlcv(ticker, interval="minute5", count=200)
                df_1m = self.api.get_ohlcv(ticker, interval="minute1", count=5)  # 급락 감지용
                
                if df is not None and not df.empty:
                    # RSI 계산
                    delta = df['close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rs = gain / loss
                    rsi = 100 - (100 / (1 + rs))
                    current_rsi = rsi.iloc[-1] if not rsi.empty else 50
                    
                    # MACD 계산
                    exp1 = df['close'].ewm(span=12).mean()
                    exp2 = df['close'].ewm(span=26).mean()
                    macd = exp1 - exp2
                    signal = macd.ewm(span=9).mean()
                    macd_val = macd.iloc[-1]
                    signal_val = signal.iloc[-1]
                    macd_direction = "상승" if macd_val > signal_val else "하락"
                    
                    # 거래량 변화 분석
                    avg_volume = df['volume'].mean()
                    current_volume = df['volume'].iloc[-1]
                    volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1.0
                    
                    # ⭐ 조건 5: 급락 감지 (1분 내 -1.5% 이상)
                    if df_1m is not None and not df_1m.empty and len(df_1m) >= 2:
                        price_1m_ago = df_1m['close'].iloc[-2]
                        price_change_1m = ((current_price - price_1m_ago) / price_1m_ago) * 100
                        sudden_drop_threshold = getattr(Config, 'SUDDEN_DROP_THRESHOLD', -2.5)
                        
                        if price_change_1m <= sudden_drop_threshold:
                            _original_print(f"[FORCE-SELL] 🚨 급락 감지 강제 매도 시작!")
                            try:
                                self.execute_sell(ticker, f"급락감지 (1분:{price_change_1m:.2f}%)")
                                _original_print(f"[FORCE-SELL] ✅ 급락 감지 매도 완료!")
                            except Exception as e:
                                _original_print(f"[FORCE-SELL] ❌ 매도 실패: {e}")
                                import traceback
                                _original_print(f"[FORCE-SELL] ❌ 스택 트레이스:\n{traceback.format_exc()}")
                            return
                    
                    # ⭐ 조건 6: 거래량 급감 (⭐ v6.31.8: 가격 하락 조건 추가)
                    volume_drop_threshold = getattr(Config, 'VOLUME_DROP_THRESHOLD', 0.2)  # 0.5 → 0.2
                    price_drop_threshold = getattr(Config, 'VOLUME_DROP_PRICE_CHECK', -0.5)  # -0.5%
                    
                    # 거래량이 극도로 낮고 + 가격이 하락 중일 때만 매도
                    if volume_ratio < volume_drop_threshold:
                        # 가격 변화율 계산
                        if df_1m is not None and not df_1m.empty and len(df_1m) >= 2:
                            price_1m_ago = df_1m['close'].iloc[-2]
                            price_change_1m = ((current_price - price_1m_ago) / price_1m_ago) * 100
                            
                            # 최소 3분 경과 + 거래량 급감 + 가격 하락
                            if hold_time >= 180 and price_change_1m <= price_drop_threshold:
                                _original_print(f"[FORCE-SELL] 🚨 거래량 급감 + 가격 하락 매도 시작!")
                                try:
                                    self.execute_sell(ticker, f"거래량급감+가격하락 (거래량:{volume_ratio:.2f}배, 가격:{price_change_1m:+.2f}%)")
                                    _original_print(f"[FORCE-SELL] ✅ 거래량 급감 매도 완료!")
                                except Exception as e:
                                    _original_print(f"[FORCE-SELL] ❌ 매도 실패: {e}")
                                    import traceback
                                    _original_print(f"[FORCE-SELL] ❌ 스택 트레이스:\n{traceback.format_exc()}")
                                return
                    
                    # ⭐ 조건 3: 차트 신호 청산
                    chart_exit = False
                    chart_reason = ""
                    
                    # 과매수 + MACD 하락
                    if current_rsi > 70 and macd_direction == "하락":
                        chart_exit = True
                        chart_reason = f"과매수+MACD하락 (RSI:{current_rsi:.0f})"
                    
                    # 과매도 + MACD 하락 + 거래량 감소
                    elif current_rsi < 30 and macd_direction == "하락" and volume_ratio < 0.8:
                        chart_exit = True
                        chart_reason = f"과매도+MACD하락+거래량감소 (RSI:{current_rsi:.0f})"
                    
                    if chart_exit:
                        self.execute_sell(ticker, chart_reason)
                        return
                    
                    # ⭐ 조건 2: 트레일링 스탑 (Trailing Stop)
                    enable_trailing = getattr(Config, 'ENABLE_TRAILING_STOP', True)
                    if enable_trailing:
                        # 포지션에 최고가 기록 (없으면 현재가로 초기화)
                        if not hasattr(position, 'highest_price'):
                            position.highest_price = current_price
                        else:
                            position.highest_price = max(position.highest_price, current_price)
                        
                        # 최고가 대비 하락률 계산
                        drop_from_peak = ((current_price - position.highest_price) / position.highest_price) * 100
                        trailing_offset = getattr(Config, 'TRAILING_STOP_OFFSET', 1.0)  # 기본 1%
                        trailing_min_profit = getattr(Config, 'TRAILING_STOP_MIN_PROFIT', 1.0)  # 최소 1% 수익
                        
                        current_profit = ((current_price - position.avg_buy_price) / position.avg_buy_price) * 100
                        
                        # 최소 수익 조건 만족 + 최고가 대비 하락 시 트레일링 스탑
                        if current_profit >= trailing_min_profit and drop_from_peak <= -trailing_offset:
                            self.execute_sell(
                                ticker, 
                                f"트레일링스탑 (최고가 대비 {drop_from_peak:.2f}%, 수익:{current_profit:+.2f}%)"
                            )
                            return
                        
            except Exception as e:
                self.logger.log_warning(f"{ticker} 고급 청산 조건 분석 실패: {e}")
        
        # ⭐ v6.30.1 Phase 2B: 고급 청산 기능 통합
        
        # 조건 7: 분할 매도 체크 (Scaled Sell)
        if self.scaled_sell:
            try:
                remaining_amount = position.amount
                partial_sell = self.scaled_sell.should_sell_partial(
                    ticker, current_price, position.avg_buy_price, remaining_amount
                )
                
                if partial_sell:
                    # 분할 매도 실행
                    sell_amount = partial_sell['sell_amount']
                    level_reason = partial_sell['reason']
                    
                    self.logger.log_info(
                        f"📊 {ticker} {level_reason} "
                        f"(매도: {sell_amount:.6f}, 남음: {remaining_amount - sell_amount:.6f})"
                    )
                    
                    # 일부만 매도 (실제 구현 시 partial sell 로직 필요)
                    # 여기서는 로그만 남기고, 실제 매도는 execute_sell 수정 필요
                    
                    # 레벨 실행 완료 표시
                    self.scaled_sell.mark_level_executed(ticker, partial_sell['level_index'])
                    
                    # 모든 레벨 완료 시 포지션 초기화
                    if self.scaled_sell.is_fully_executed(ticker):
                        self.scaled_sell.reset_position(ticker)
                        self.execute_sell(ticker, "분할매도 완료 (모든 레벨)")
                        return
            except Exception as e:
                self.logger.log_warning(f"{ticker} 분할 매도 체크 실패: {e}")
        
        # 조건 8: 조건부 매도 체크 (Conditional Sell)
        if self.conditional_sell:
            try:
                eval_result = self.conditional_sell.evaluate_sell_conditions(
                    ticker, position, current_price
                )
                
                if eval_result['should_sell']:
                    formatted_msg = self.conditional_sell.format_evaluation_result(eval_result)
                    self.logger.log_info(f"{ticker} {formatted_msg}")
                    
                    reasons_str = ', '.join(eval_result['reasons'])
                    self.execute_sell(ticker, f"조건부매도 ({reasons_str})")
                    return
            except Exception as e:
                self.logger.log_warning(f"{ticker} 조건부 매도 체크 실패: {e}")
        
        # 조건 9: 동적 손절 체크 (Dynamic Stop Loss)
        if self.dynamic_stop_loss and hasattr(position, 'stop_loss_price'):
            try:
                profit_ratio = ((current_price - position.avg_buy_price) / position.avg_buy_price) * 100
                
                # 손절가 도달 체크
                if self.dynamic_stop_loss.should_trigger_stop_loss(current_price, position.stop_loss_price):
                    reason = self.dynamic_stop_loss.get_stop_loss_reason(
                        current_price, position.avg_buy_price, position.stop_loss_price, profit_ratio
                    )
                    self.execute_sell(ticker, reason)
                    return
                
                # 트레일링 스탑 업데이트 (수익 중일 때만)
                if profit_ratio > 1.0:
                    new_stop = self.dynamic_stop_loss.update_stop_loss_trailing(
                        current_price, position.avg_buy_price, position.stop_loss_price,
                        position.strategy, profit_ratio
                    )
                    
                    if new_stop > position.stop_loss_price:
                        old_stop = position.stop_loss_price
                        position.stop_loss_price = new_stop
                        self.logger.log_info(
                            f"📈 {ticker} 트레일링 스탑 상향: "
                            f"{old_stop:,.0f} → {new_stop:,.0f} "
                            f"(+{((new_stop-old_stop)/old_stop*100):.2f}%)"
                        )
            except Exception as e:
                self.logger.log_warning(f"{ticker} 동적 손절 체크 실패: {e}")
        
        # ⭐ 조건 6: 기본 손익률 기준 청산 (전략별) - v6.30.28: hold_time 계산 수정
        
        # 보유 시간 계산 (v6.30.28: timestamp() 추가)
        if hasattr(position, 'entry_time'):
            hold_time = time.time() - position.entry_time.timestamp()
        else:
            hold_time = 0
        
        # 손익률 계산 및 로그
        profit_ratio = ((current_price - position.avg_buy_price) / position.avg_buy_price) * 100
        self.logger.log_info(
            f"📊 {ticker} 손익률: {profit_ratio:+.2f}% "
            f"(진입: {position.avg_buy_price:,.0f}원 → 현재: {current_price:,.0f}원, "
            f"보유: {hold_time:.0f}초)"
        )
        
        # 시장 스냅샷 (간단 버전)
        market_snapshot = {
            'current_price': current_price,
            'entry_price': position.avg_buy_price,
            'profit_ratio': profit_ratio
        }
        
        # 전략별 청산 판단 (v6.30.21: 4개 인자 전달)
        should_exit, exit_reason = strategy.should_exit(
            position.avg_buy_price, 
            current_price,
            hold_time,
            market_snapshot
        )
        
        # ⭐ v6.30.28: 매도 판단 결과를 화면에 표시 + 익절/손절 기준 명시
        if should_exit:
            # 익절/손절 타입 판별
            sell_type = "💸 익절" if profit_ratio > 0 else "🚨 손절"
            
            # ⭐ v6.30.45: 콘솔에 익절/손절 실행 메시지 출력
            _original_print(f"   ✅ {sell_type} 조건 충족! ({profit_ratio:+.2f}% {'≥ +1.5%' if profit_ratio > 0 else '≤ -1.0%'})")
            _original_print(f"   💰 {sell_type} 매도 주문 실행 중...")
            
            # ⭐ v6.30.53: 강제 매도 로그 추가
            _original_print(f"[FORCE-SELL] 🚨 {sell_type} 강제 매도 실행 시작!")
            
            self.display.update_monitoring(
                f"{sell_type} 트리거 발생!",
                f"{ticker}: {exit_reason} | 손익: {profit_ratio:+.2f}%",
                datetime.now().strftime('%H:%M:%S')
            )
            self.logger.log_info(f"{sell_type} {ticker} 매도 트리거! 사유: {exit_reason} | 손익률: {profit_ratio:+.2f}%")
            
            # ⭐ v6.30.53: 강제 매도 실행 (예외 캡처)
            try:
                self.execute_sell(ticker, exit_reason)
                _original_print(f"[FORCE-SELL] ✅ {sell_type} 매도 주문 완료!")
            except Exception as e:
                _original_print(f"[FORCE-SELL] ❌ {sell_type} 매도 실패: {e}")
                import traceback
                _original_print(f"[FORCE-SELL] ❌ 스택 트레이스:\n{traceback.format_exc()}")
            
            return
        else:
            # ⭐ v6.30.28: 보유 판단 + 익절/손절 기준 표시
            take_profit_pct = strategy.take_profit * 100 if hasattr(strategy, 'take_profit') else 1.5
            stop_loss_pct = strategy.stop_loss * 100 if hasattr(strategy, 'stop_loss') else 1.0
            
            self.display.update_monitoring(
                f"✅ {ticker} 보유 유지",
                f"손익: {profit_ratio:+.2f}% | 익절목표: +{take_profit_pct:.1f}% | 손절: -{stop_loss_pct:.1f}%",
                datetime.now().strftime('%H:%M:%S')
            )
            self.logger.log_info(
                f"✅ {ticker} 청산 조건 미충족 - 보유 유지\n"
                f"   현재 손익률: {profit_ratio:+.2f}%\n"
                f"   익절 기준: +{take_profit_pct:.1f}% | 손절 기준: -{stop_loss_pct:.1f}%\n"
                f"   보유 시간: {hold_time/60:.1f}분"
            )
    
    def update_all_positions(self):
        """모든 포지션 가격 업데이트"""
        try:
            if not self.risk_manager.positions:
                return
            
            prices = {}
            for ticker in self.risk_manager.positions.keys():
                try:
                    price = self.api.get_current_price(ticker)
                    if price:
                        prices[ticker] = price
                except Exception as e:
                    self.logger.log_warning(f"{ticker} 가격 조회 실패: {e}")
                    continue
            
            if prices:
                self.risk_manager.update_positions(prices)
        
        except Exception as e:
            self.logger.log_error("UPDATE_POSITIONS_ERROR", "포지션 업데이트 실패", e)
    
    def quick_check_positions(self):
        """
        빠른 포지션 체크 (1분마다 실행)
        모든 포지션에 대해 청산 조건을 체크합니다.
        """
        try:
            # ⭐ v6.30.45: 포지션 상태 캐싱 (멀티스레딩 경쟁 조건 방지)
            has_positions = bool(self.risk_manager.positions)
            position_count = len(self.risk_manager.positions) if has_positions else 0
            
            
            if not has_positions or position_count == 0:
                return
            
            # ⭐ v6.30.46: 청산 체크 헤더를 먼저 출력 (display.update_monitoring 전에)
            from datetime import datetime
            check_time = datetime.now().strftime('%H:%M:%S')
            
            # ⭐ v6.30.26: 화면 업데이트 (예외 발생 시에도 계속 진행)
            try:
                self.display.update_monitoring(
                    "🔍 매도 조건 체크",
                    f"{position_count}개 포지션 검사 중",
                    datetime.now().strftime('%H:%M:%S')
                )
            except Exception as e:
                self.logger.log_warning(f"포지션 카운트 업데이트 실패: {e}")
            
            # ⭐ v6.30.18: 디버그 로그 추가
            
            # 포지션 목록 복사 (iteration 중 변경 방지)
            positions_to_check = list(self.risk_manager.positions.items())
            
            for idx, (ticker, position) in enumerate(positions_to_check, 1):
                try:
                    # ⭐ v6.30.26: 진행 상황 표시
                    self.display.update_monitoring(
                        f"🔍 매도 체크 [{idx}/{position_count}]",
                        f"{ticker}: 손익률 체크 중",
                        datetime.now().strftime('%H:%M:%S')
                    )
                    
                    # ⭐ v6.30.18: 포지션별 체크 시작 로그
                    
                    # 현재 가격 조회
                    current_price = self.api.get_current_price(ticker)
                    if not current_price:
                        self.logger.log_warning(f"⚠️ {ticker} 가격 조회 실패")
                        continue
                    
                    # 포지션 가격 업데이트
                    self.risk_manager.update_positions({ticker: current_price})
                    
                    # 손익률 계산
                    profit_ratio = ((current_price - position.avg_buy_price) / position.avg_buy_price) * 100
                    
                    # ⭐ v6.30.45: 콘솔에 손익률 출력 (사용자가 볼 수 있도록)
                    profit_str = f"+{profit_ratio:.2f}%" if profit_ratio > 0 else f"{profit_ratio:.2f}%"
                    hold_seconds = int(time.time() - position.entry_time.timestamp())
                    hold_time_str = f"{hold_seconds//60}분 {hold_seconds%60}초" if hold_seconds >= 60 else f"{hold_seconds}초"
                    
                    _original_print(f"📊 {ticker} 손익률: {profit_str} (보유 {hold_time_str})")
                    _original_print(f"   익절 목표: +1.5% | 손절 목표: -1.0%")
                    
                    # ⭐ v6.30.26: 손익률 화면 표시
                    self.display.update_monitoring(
                        f"📊 {ticker}",
                        f"손익: {profit_str}",
                        datetime.now().strftime('%H:%M:%S')
                    )
                    
                    # 전략 객체 가져오기
                    strategy_name = position.strategy
                    
                    try:
                        strategy = self._get_strategy_by_name(strategy_name)
                    except Exception as e:
                        import traceback
                        strategy = None
                    
                    if strategy:
                        # check_positions 호출 (10가지 청산 조건 체크)
                        # ⭐ v6.30.50: 포지션 객체를 직접 전달 (동시성 문제 방지)
                        self.check_positions(ticker, strategy, position=position)  # ← 포지션 직접 전달!
                    else:
                        self.logger.log_warning(f"⚠️ {ticker} 전략 객체 없음: {strategy_name}")
                
                except Exception as e:
                    self.logger.log_warning(f"{ticker} 빠른 체크 실패: {e}")
                    continue
        
        except Exception as e:
            self.logger.log_error("QUICK_CHECK_ERROR", "빠른 포지션 체크 실패", e)
    
    def _get_strategy_by_name(self, strategy_name: str):
        """
        전략 이름으로 전략 객체 가져오기
        ⭐ v6.30.49: 대소문자 및 다양한 형식 지원 강화
        ⭐ v6.30.54: self.strategies 딕셔너리 사용 (AttributeError 수정)
        """
        
        # ⭐ v6.30.54: self.strategies 딕셔너리에서 직접 가져오기
        strategy_map = {
            # Aggressive Scalping (공격적 단타)
            'AGGRESSIVE': self.strategies.get('aggressive_scalping'),
            'aggressive': self.strategies.get('aggressive_scalping'),
            'AGGRESSIVE_SCALPING': self.strategies.get('aggressive_scalping'),
            'aggressive_scalping': self.strategies.get('aggressive_scalping'),
            'AGGRESSIVE-SCALPING': self.strategies.get('aggressive_scalping'),
            'aggressive-scalping': self.strategies.get('aggressive_scalping'),
            # ⭐ TYPO FIX: aggressive_scaling (without 'p') - 오타 처리
            'AGGRESSIVE_SCALING': self.strategies.get('aggressive_scalping'),
            'aggressive_scaling': self.strategies.get('aggressive_scalping'),
            'AGGRESSIVE-SCALING': self.strategies.get('aggressive_scalping'),
            'aggressive-scaling': self.strategies.get('aggressive_scalping'),
            '공격적': self.strategies.get('aggressive_scalping'),
            
            # Conservative Scalping (보수적 단타)
            'CONSERVATIVE': self.strategies.get('conservative_scalping'),
            'conservative': self.strategies.get('conservative_scalping'),
            'CONSERVATIVE_SCALPING': self.strategies.get('conservative_scalping'),
            'conservative_scalping': self.strategies.get('conservative_scalping'),
            'CONSERVATIVE-SCALPING': self.strategies.get('conservative_scalping'),
            'conservative-scalping': self.strategies.get('conservative_scalping'),
            # ⭐ TYPO FIX: conservative_scaling (without 'p') - 오타 처리
            'CONSERVATIVE_SCALING': self.strategies.get('conservative_scalping'),
            'conservative_scaling': self.strategies.get('conservative_scalping'),
            'CONSERVATIVE-SCALING': self.strategies.get('conservative_scalping'),
            'conservative-scaling': self.strategies.get('conservative_scalping'),
            '보수적': self.strategies.get('conservative_scalping'),
            
            # Mean Reversion (평균 회귀)
            'MEAN_REVERSION': self.strategies.get('mean_reversion'),
            'mean_reversion': self.strategies.get('mean_reversion'),
            'MEAN-REVERSION': self.strategies.get('mean_reversion'),
            'mean-reversion': self.strategies.get('mean_reversion'),
            '평균회귀': self.strategies.get('mean_reversion'),
            
            # Grid Trading (그리드)
            'GRID': self.strategies.get('grid_trading'),
            'grid': self.strategies.get('grid_trading'),
            'GRID_TRADING': self.strategies.get('grid_trading'),
            'grid_trading': self.strategies.get('grid_trading'),
            'GRID-TRADING': self.strategies.get('grid_trading'),
            'grid-trading': self.strategies.get('grid_trading'),
            '그리드': self.strategies.get('grid_trading'),
            
            # Ultra Scalping (초단타)
            'ULTRA_SCALPING': self.strategies.get('ultra_scalping'),
            'ultra_scalping': self.strategies.get('ultra_scalping'),
            'ULTRA-SCALPING': self.strategies.get('ultra_scalping'),
            'ultra-scalping': self.strategies.get('ultra_scalping'),
            'ULTRA': self.strategies.get('ultra_scalping'),
            'ultra': self.strategies.get('ultra_scalping'),
            '초단타': self.strategies.get('ultra_scalping'),
            'CHASE_BUY': self.strategies.get('ultra_scalping'),
            'chase_buy': self.strategies.get('ultra_scalping'),
        }
        
        
        # 먼저 정확히 매칭되는지 확인
        if strategy_name in strategy_map and strategy_map[strategy_name]:
            result = strategy_map[strategy_name]
            return result
        
        # 매칭 실패 시 대소문자 무시하고 재시도
        strategy_name_upper = strategy_name.upper()
        for key, value in strategy_map.items():
            if value and key.upper() == strategy_name_upper:
                return value
        
        # 그래도 실패 시 기본값 (aggressive_scalping)
        result = self.strategies.get('aggressive_scalping')
        return result
    
    def check_profit_withdrawal(self):
        """수익 출금 확인 및 처리"""
        should_withdraw, amount = self.risk_manager.should_withdraw_profit()
        
        if should_withdraw:
            self.logger.log_info(
                f"💰 월간 수익 출금: {amount:,.0f}원 (50% 자동 출금)"
            )
            self.logger.log_warning(
                "⚠️ 실제 출금은 Upbit에서 수동으로 진행하세요!"
            )
            
            # 리스크 관리자에 출금 처리
            self.risk_manager.process_profit_withdrawal(amount)
    
    def get_summary_data(self, period: str = 'daily') -> Dict:
        """
        손익 요약 데이터 생성 (알림용)
        
        Args:
            period: 'daily', 'weekly', 'monthly'
        
        Returns:
            요약 데이터 딕셔너리
        """
        risk_status = self.risk_manager.get_risk_status()
        positions_summary = self.risk_manager.get_positions_summary()
        
        # 기본 데이터
        summary = {
            'period': period,
            'start_balance': Config.INITIAL_CAPITAL,
            'current_balance': risk_status['current_balance'],
            'total_equity': risk_status['total_equity'],
            'daily_profit': risk_status['daily_profit_loss'],
            'daily_profit_ratio': risk_status['daily_profit_loss_ratio'],
            'weekly_profit': 0,  # TODO: 주간 데이터 추적 필요
            'monthly_profit': risk_status.get('monthly_profit', 0),
            'total_trades': risk_status['total_trades'],
            'win_rate': risk_status['win_rate'],
            'positions': positions_summary,
            'max_positions': Config.MAX_POSITIONS,
            'ai_confidence': 0,
            'best_trade': None,
            'worst_trade': None
        }
        
        # AI 신뢰도 (Phase 2)
        if self.adaptive_learner:
            try:
                comprehensive_report = self.adaptive_learner.get_comprehensive_report()
                summary['ai_confidence'] = comprehensive_report.get('adaptive_stats', {}).get('overall_win_rate', 0)
            except:
                pass
        
        # 최고/최저 거래 (학습 엔진에서)
        try:
            recent_perf = self.learning_engine.get_recent_performance(days=1 if period == 'daily' else 30)
            if recent_perf.get('trades'):
                trades = recent_perf['trades']
                trades_sorted = sorted(trades, key=lambda x: x.get('profit_ratio', 0), reverse=True)
                if trades_sorted:
                    summary['best_trade'] = trades_sorted[0]
                    summary['worst_trade'] = trades_sorted[-1]
        except:
            pass
        
        # 주간 리포트용 추가 데이터
        if period in ['weekly', 'monthly']:
            summary['end_balance'] = risk_status['current_balance']
            summary['total_profit'] = risk_status['cumulative_profit_loss']
            summary['profit_ratio'] = (summary['total_profit'] / Config.INITIAL_CAPITAL) * 100
            summary['daily_avg_profit'] = summary['total_profit'] / (7 if period == 'weekly' else 30)
            summary['wins'] = int(risk_status['total_trades'] * risk_status['win_rate'] / 100)
            summary['losses'] = risk_status['total_trades'] - summary['wins']
            summary['strategy_performance'] = {}
            summary['fees'] = 0  # TODO: 수수료 추적
            summary['daily_profits'] = {}  # TODO: 일별 데이터
        
        return summary
    
    def print_status(self):
        """현재 상태 출력"""
        risk_status = self.risk_manager.get_risk_status()
        positions = self.risk_manager.get_positions_summary()
        
        self.logger.log_info("=" * 60)
        self.logger.log_info(f"💼 잔고: {risk_status['current_balance']:,.0f}원")
        self.logger.log_info(f"💎 총 자산: {risk_status['total_equity']:,.0f}원")
        self.logger.log_info(f"📈 총 수익률: {risk_status['total_profit_loss_ratio']:+.2f}%")
        self.logger.log_info(f"📊 일일 손익: {risk_status['daily_profit_loss']:+,.0f}원")
        self.logger.log_info(f"🎯 승률: {risk_status['win_rate']:.1f}%")
        self.logger.log_info(f"🔢 총 거래: {risk_status['total_trades']}회")
        
        if positions:
            self.logger.log_info(f"📦 보유 포지션: {len(positions)}개")
            for pos in positions:
                self.logger.log_info(
                    f"  - {pos['ticker']}: "
                    f"{pos['amount']:.8f} "
                    f"(평균가: {pos['avg_buy_price']:,.0f}, "
                    f"손익: {pos['profit_loss_ratio']:+.2f}%)"
                )
        
        # 전략 성과 요약 (10회 주기마다)
        if risk_status['total_trades'] > 0 and risk_status['total_trades'] % 10 == 0:
            self.logger.log_info("\n📊 전략별 성과 순위:")
            rankings = self.optimizer.get_strategy_rankings()
            for i, (strategy, score, info) in enumerate(rankings[:3], 1):  # 상위 3개
                self.logger.log_info(
                    f"  {i}. {strategy}: {score:.1f}점 "
                    f"(승률 {info['win_rate']:.1f}%, "
                    f"PF {info['profit_factor']:.2f})"
                )
        
        self.logger.log_info("=" * 60)
    
    def scan_for_surges(self):
        """
        급등/급락 스캔 및 초단타 진입 (30초 주기)
        
        ⚡ API 최적화: 배치 API로 다중 코인 현재가 한 번에 조회
        
        조건:
        - 최대 2개까지만 초단타 포지션
        - 급등/급락 감지 시 즉시 진입
        - 빠른 익절/손절 (0.5%~1%)
        """
        # 초단타 포지션 수 확인
        if len(self.ultra_positions) >= self.max_ultra_positions:
            return
        
        self.logger.log_info(f"🔍 급등/급락 스캔 중... (초단타 {len(self.ultra_positions)}/{self.max_ultra_positions})")
        
        # 🔥 개선 1: 스냅샷 사용 (중간 갱신 방지)
        tickers_snapshot = self.tickers.copy()
        
        # 🔥 배치 API: 한 번에 모든 티커 현재가 조회 (N회 → 1회)
        prices_dict = self.api.get_current_prices(tickers_snapshot)
        if not prices_dict:
            return
        
        # 급등/급락 코인 탐지 (각 티커별로 검사)
        detected_coins = []
        for ticker in tickers_snapshot:
            if ticker not in prices_dict:
                continue
            
            # 급등 감지
            try:
                surge_info = self.surge_detector.detect_surge(ticker, self.api)
                if surge_info and surge_info.get('surge_score', 0) >= self.surge_detector.min_surge_score:
                    detected_coins.append({
                        'ticker': ticker,
                        **surge_info
                    })
            except Exception as e:
                # 개별 코인 에러는 무시하고 계속 진행
                pass
        
        if not detected_coins:
            return
        
        # 감지된 코인 중 진입 가능한 것 선택
        for coin_info in detected_coins:
            if len(self.ultra_positions) >= self.max_ultra_positions:
                break
            
            ticker = coin_info['ticker']
            
            # 이미 포지션 있으면 스킵
            if ticker in self.ultra_positions or ticker in self.risk_manager.positions:
                continue
            
            # 기존 보유 코인이면 스킵
            if self.holding_protector.is_existing_holding(ticker):
                continue
            
            # ⭐ v6.30: 추격매수 가능 여부 검증
            surge_info = {k: v for k, v in coin_info.items() if k != 'ticker'}
            can_chase, reason = self.surge_detector.can_chase_buy(ticker, surge_info)
            
            if not can_chase:
                self.logger.log_info(f"❌ [{ticker}] 추격매수 불가: {reason}")
                continue
            
            # 일일 추격매수 한도 체크
            chase_count = len([p for p in self.risk_manager.positions.values() 
                              if p.strategy == 'ULTRA_SCALPING'])
            if chase_count >= Config.CHASE_DAILY_LIMIT:
                self.logger.log_info(
                    f"❌ 일일 추격매수 한도 초과 ({chase_count}/{Config.CHASE_DAILY_LIMIT}회)"
                )
                break
            
            self.logger.log_info(
                f"✅ [{ticker}] 추격매수 조건 충족: {reason} "
                f"(점수: {surge_info.get('surge_score', 0):.1f}, "
                f"신뢰도: {surge_info.get('confidence', 0):.2f})"
            )
            
            # 초단타 진입
            self.execute_ultra_buy(ticker, coin_info)
    
    def execute_ultra_buy(self, ticker: str, surge_info: Dict):
        """
        초단타 매수 실행
        
        Args:
            ticker: 코인 티커
            surge_info: 급등/급락 정보
        """
        try:
            # 거래 정지 확인
            if self.risk_manager.is_trading_stopped:
                return
            
            # 현재가 조회
            current_price = self.api.get_current_price(ticker)
            if not current_price:
                return
            
            # 초단타 전용 투자 금액 (일반보다 작게)
            max_ratio = Config.ULTRA_SCALPING_CONFIG.get('max_investment_ratio', 0.15)
            max_amount = Config.ULTRA_SCALPING_CONFIG.get('max_investment_amount', 100000)
            
            investment = self.risk_manager.current_balance * max_ratio
            investment = min(investment, max_amount)
            
            if investment < 5000:
                return
            
            # 수량 계산
            amount = investment / current_price
            
            # 실거래 모드에서만 실제 주문
            if self.mode == 'live' and self.api.upbit:
                order = self.api.buy_market_order(ticker, investment)
                if not order:
                    return
            else:
                self.logger.log_info(f"[모의거래] 초단타 매수: {ticker}, {investment:,.0f}원")
            
            # 초단타 포지션 등록 (⭐ 가격 이력 추가)
            self.ultra_positions[ticker] = {
                'entry_time': datetime.now(),
                'entry_price': current_price,
                'amount': amount,
                'investment': investment,
                'surge_type': surge_info['type'],
                'price_change': surge_info['price_change'],
                'price_history': [current_price],  # ⭐ 가격 이력 시작
                'max_price': current_price,  # 최고가 추적
                'last_update': time.time()  # 마지막 업데이트 시간
            }
            
            # 거래 로그
            self.logger.log_trade(
                action='BUY',
                ticker=ticker,
                price=current_price,
                amount=amount,
                strategy='ultra_scalping',
                reason=f"초단타 진입: {surge_info['type']} ({surge_info['price_change']:+.2f}%)",
                profit_loss=0.0,
                balance=self.risk_manager.current_balance,
                metadata=surge_info
            )
            
            # ⭐ AI 학습: 초단타 매수 진입 기록
            try:
                entry_time_id = self.learning_engine.record_trade_entry(
                    ticker=ticker,
                    strategy='ultra_scalping',
                    entry_price=current_price,
                    entry_amount=amount,
                    market_condition={
                        'rsi': 50,
                        'volatility': 'high',
                        'trend': surge_info['type'],
                        'volume_ratio': 1.5,
                        'market_phase': 'surge',
                        'price': current_price,
                        'price_change': surge_info['price_change']
                    }
                )
                # entry_time_id를 포지션에 저장
                self.ultra_positions[ticker]['entry_time_id'] = entry_time_id
            except Exception as e:
                self.logger.log_warning(f"⚠️  초단타 학습 진입 기록 실패: {e}")
            
            self.logger.log_info(
                f"🔥 초단타 매수: {ticker} "
                f"({surge_info['type']}, {investment:,.0f}원, "
                f"가격변동: {surge_info['price_change']:+.2f}%)"
            )
            
            # ⭐ 초단타 매수 즉시 화면에 포지션 표시
            slot = self.display.get_available_slot()
            if slot:
                self.display.update_position(
                    slot=slot,
                    ticker=ticker,
                    entry_price=current_price,
                    current_price=current_price,
                    amount=amount,
                    strategy='⚡초단타',
                    entry_time=self.ultra_positions[ticker]['entry_time']
                )
                self.display.render()  # 즉시 화면 갱신
                
                # 작업 상태에 초단타 매수 완료 표시
                coin_short = ticker.split('-')[1]
                self.display.update_monitoring(
                    f"⚡ {coin_short} 초단타 매수",
                    f"슬롯 {slot} | {surge_info['type']} {surge_info['price_change']:+.1f}%",
                    f"{investment:,.0f}원"
                )
                self.display.render()
                time.sleep(1)  # 1초간 표시
            
        except Exception as e:
            self.logger.log_error("ULTRA_BUY_ERROR", f"{ticker} 초단타 매수 실패", e)
    
    def check_ultra_positions(self):
        """
        초단타 포지션 체크 (⭐ 1초마다 - 스마트 버전)
        
        특징:
        - 빠른 익절: 1%
        - 빠른 손절: 0.5%
        - 시간 제한: 5분
        - ⭐ 스마트 매도: 수익 시 추세 재확인
        """
        if not self.ultra_positions:
            return
        
        ultra_strategy = self.strategies.get('ultra_scalping')
        if not ultra_strategy:
            return
        
        current_time = time.time()
        
        for ticker in list(self.ultra_positions.keys()):
            try:
                position = self.ultra_positions[ticker]
                
                # 현재가 조회
                current_price = self.api.get_current_price(ticker)
                if not current_price:
                    continue
                
                # ⭐ 가격 이력 업데이트 (1초마다)
                position['price_history'].append(current_price)
                
                # 최고가 갱신
                if current_price > position['max_price']:
                    position['max_price'] = current_price
                
                # 이력은 최근 30개만 유지 (30초)
                if len(position['price_history']) > 30:
                    position['price_history'] = position['price_history'][-30:]
                
                position['last_update'] = current_time
                
                # 보유 시간 계산
                hold_time = (datetime.now() - position['entry_time']).total_seconds()
                
                # ⭐ 청산 조건 확인 (가격 이력 포함)
                should_exit, exit_reason = ultra_strategy.should_exit(
                    position['entry_price'], 
                    current_price,
                    hold_time,
                    price_history=position['price_history']  # ⭐ 가격 이력 전달
                )
                
                if should_exit:
                    self.execute_ultra_sell(ticker, current_price, exit_reason)
                else:
                    # 손익 로그 (0.3% 이상만, 3초마다만 출력)
                    profit_ratio = (current_price - position['entry_price']) / position['entry_price']
                    if abs(profit_ratio) > 0.003 and int(hold_time) % 3 == 0:
                        max_gain = (position['max_price'] - position['entry_price']) / position['entry_price']
                        self.logger.log_info(
                            f"  ⚡ {ticker}: {profit_ratio*100:+.2f}% "
                            f"(최고 {max_gain*100:+.2f}%, 보유: {hold_time:.0f}초)"
                        )
                
            except Exception as e:
                self.logger.log_error("ULTRA_CHECK", f"{ticker} 초단타 체크 실패", e)
    
    def execute_ultra_sell(self, ticker: str, current_price: float, reason: str):
        """
        초단타 매도 실행
        
        Args:
            ticker: 코인 티커
            current_price: 현재 가격
            reason: 매도 사유
        """
        try:
            if ticker not in self.ultra_positions:
                return
            
            position = self.ultra_positions[ticker]
            
            # 실거래 모드에서만 실제 주문
            if self.mode == 'live' and self.api.upbit:
                order = self.api.sell_market_order(ticker, position['amount'])
                if not order:
                    return
            else:
                self.logger.log_info(f"[모의거래] 초단타 매도: {ticker}")
            
            # 손익 계산
            sell_value = current_price * position['amount']
            profit_loss = sell_value - position['investment']
            profit_ratio = (current_price - position['entry_price']) / position['entry_price']
            hold_time = (datetime.now() - position['entry_time']).total_seconds()
            
            # 거래 로그
            self.logger.log_trade(
                action='SELL',
                ticker=ticker,
                price=current_price,
                amount=position['amount'],
                strategy='ultra_scalping',
                reason=reason,
                profit_loss=profit_loss,
                balance=self.risk_manager.current_balance
            )
            
            # ⭐ AI 학습: 초단타 매도 경험 기록
            try:
                df = self.api.get_ohlcv(ticker, interval="minute1", count=50)
                if df is not None and not df.empty:
                    # 시장 스냅샷 생성
                    market_snapshot_dict = {
                        'rsi': 50,  # 초단타는 간단한 지표
                        'volatility': 'high',
                        'trend': 'volatile',
                        'volume_ratio': 1.0,
                        'market_phase': 'surge',
                        'price': current_price
                    }
                    
                    # entry_time_id 가져오기 (포지션에 저장된 값 사용)
                    entry_time_id = position.get('entry_time_id', position['entry_time'].isoformat())
                    
                    self.learning_engine.record_trade_exit(
                        ticker=ticker,
                        strategy='ultra_scalping',
                        exit_price=current_price,
                        entry_time=entry_time_id,
                        market_condition=market_snapshot_dict
                    )
                    
                    # ⭐ 매도 직후 학습 통계 즉시 화면 업데이트
                    stats = self.learning_engine.get_stats()
                    total_trades = 0
                    profit_trades = 0
                    loss_trades = 0
                    
                    for strat_name, strat_stat in self.learning_engine.strategy_stats.items():
                        total_trades += strat_stat.get('total_trades', 0)
                        profit_trades += strat_stat.get('winning_trades', 0)
                        loss_trades += strat_stat.get('losing_trades', 0)
                    
                    self.display.update_ai_learning(
                        total_trades=total_trades,
                        profit_trades=profit_trades,
                        loss_trades=loss_trades
                    )
                    self.display.render()  # 즉시 화면 갱신
                    
            except Exception as e:
                self.logger.log_warning(f"⚠️  초단타 학습 기록 실패: {e}")
            
            # 결과 로그
            result_emoji = "💰" if profit_loss > 0 else "📉"
            self.logger.log_info(
                f"{result_emoji} 초단타 매도: {ticker} "
                f"- {reason} "
                f"(손익: {profit_loss:+,.0f}원, {profit_ratio*100:+.2f}%, "
                f"보유: {hold_time:.0f}초)"
            )
            
            # 포지션 제거
            del self.ultra_positions[ticker]
            
        except Exception as e:
            self.logger.log_error("ULTRA_SELL_ERROR", f"{ticker} 초단타 매도 실패", e)
    
    def run(self):
        """
        봇 실행 (하이브리드 + 초단타 - AI 학습 통합)
        
        실행 주기 (v6.30.9 최적화):
        - 60초: 전체 코인 스캔 + 신규 진입
        - 3초: 일반 포지션 체크 (10가지 청산 조건)
        - 5초: 급등/급락 감지 + 초단타 진입
        - 3분: 동적 코인 갱신
        - 3초: 화면 자동 갱신
        """
        self.running = True
        
        # ⭐ 고정 화면 초기화 (첫 실행만)
        # clear_screen()은 FixedScreenDisplay의 render()에서 자동 처리됨
        self.display.update_bot_status("시작 중...")
        self.display.update_scan_status(f"코인 {len(self.tickers)}개 모니터링 준비")
        
        # 초기 로그는 파일에만 기록
        # self.logger.log_info("🤖 봇 가동 시작! (AI 학습 통합 모드)")
        # self.logger.log_info(f"   📅 전체 스캔: {self.full_scan_interval}초 ({self.full_scan_interval//60}분)")
        # self.logger.log_info(f"   🔥 급등 감지: {self.surge_scan_interval}초 (초단타 최대 {self.max_ultra_positions}개)")
        # self.logger.log_info(f"   🔄 화면 갱신: {self.display_update_interval}초\n")
        
        cycle = 0
        monitor_count = 0  # ⭐ 모니터링 카운터 초기화
        
        try:
            while self.running:
                current_time = time.time()
                monitor_count += 1  # ⭐ 모니터링 카운터 증가
                
                # 🔍 DEBUG: 루프 시작 확인
                
                # 화면 갱신 (3초마다)
                if current_time - self.last_display_update_time >= self.display_update_interval:
                    self._update_display()
                    self.last_display_update_time = current_time
                
                # 일일 통계 리셋
                self.risk_manager.reset_daily_stats()
                
                # 거래 정지 확인
                if self.risk_manager.is_trading_stopped:
                    self.display.update_scan_status(f"⛔ 거래 정지: {self.risk_manager.stop_reason}")
                    time.sleep(self.full_scan_interval)
                    continue
                
                # 🆕 실시간 모니터링 (30초마다)
                if monitor_count % 30 == 0 and self.risk_manager.positions:
                    active_tickers = list(self.risk_manager.positions.keys())
                    
                    # 호가창 모니터링 (로그 없이)
                    if self.orderbook_monitor:
                        self.orderbook_monitor.monitor_orderbook(active_tickers)
                    
                    # 체결 모니터링 (선택적, 로그 없이)
                    if self.trade_monitor and len(active_tickers) <= 3:
                        for ticker in active_tickers:
                            self.trade_monitor.monitor_trades(ticker, count=100)
                
                # ⭐ PHASE 0: 동적 코인 선정 갱신 (5분마다 또는 설정 주기)
                if self.dynamic_coin_selector and self.dynamic_coin_selector.should_update():
                    self.display.update_scan_status("코인 목록 갱신 중...")
                    
                    old_count = len(self.tickers)
                    new_tickers = self.dynamic_coin_selector.get_coins(method=Config.COIN_SELECTION_METHOD)
                    
                    # 🔥 개선 2: 급등 추적 중인 코인 보존 (점수 70+ 유지)
                    tracking_tickers = []
                    if hasattr(self, 'surge_detector') and self.surge_detector:
                        try:
                            for ticker in self.tickers:
                                # 급등 점수가 70 이상인 코인은 목록에서 제외하지 않음
                                surge_info = self.surge_detector.detect_surge(ticker, self.api)
                                if surge_info and surge_info.get('surge_score', 0) >= 70:
                                    tracking_tickers.append(ticker)
                        except Exception as e:
                            pass
                    
                    # 새 코인 목록 + 급등 추적 중인 코인 병합 (중복 제거, 최대 40개)
                    self.tickers = list(set(new_tickers + tracking_tickers))[:40]
                    
                    if tracking_tickers:
                        self.display.update_scan_status(
                            f"코인 갱신 완료: {old_count}개 → {len(self.tickers)}개 "
                            f"(급등 추적: {len(tracking_tickers)}개 보존)"
                        )
                    else:
                        self.display.update_scan_status(f"코인 갱신 완료: {old_count}개 → {len(self.tickers)}개")
                
                # ⭐ v6.30.69: 10분마다 화면 클리어 (가독성 향상)
                if current_time - self.last_screen_clear_time >= self.screen_clear_interval:
                    import os
                    os.system('cls' if os.name == 'nt' else 'clear')
                    self.display.render()
                    self.last_screen_clear_time = current_time
                
                # ⭐ PHASE 1: 전체 스캔 (60초)
                if current_time - self.last_full_scan_time >= self.full_scan_interval:
                    cycle += 1
                    
                    # ⭐ 스캔 시간 기록
                    scan_time = datetime.now()
                    self.display.update_scan_times(full_scan_time=scan_time)
                    
                    # 화면 상태만 업데이트 (로그 출력 최소화)
                    self.display.update_scan_status(f"전체 스캔 #{cycle} 시작...")
                    
                    weights = self.get_current_strategy_weights()
                    self.check_profit_withdrawal()
                    
                    # 🆕 전체 코인 호가창 스냅샷 (배치)
                    if self.orderbook_monitor and cycle % 5 == 0:  # 15분마다
                        self.orderbook_monitor.monitor_orderbook(self.tickers[:20])  # 상위 20개
                    
                    # 🔥 개선 1: 스캔 시 스냅샷 사용 (중간 갱신 방지)
                    tickers_snapshot = self.tickers.copy()  # 코인 목록 고정
                    
                    # ⭐ 병렬 분석 (5개씩 배치 처리)
                    batch_size = 5
                    total_tickers = len(tickers_snapshot)
                    
                    for batch_start in range(0, total_tickers, batch_size):
                        batch_end = min(batch_start + batch_size, total_tickers)
                        batch_tickers = tickers_snapshot[batch_start:batch_end]  # 스냅샷 사용
                        
                        # 배치 진행률 표시
                        batch_num = (batch_start // batch_size) + 1
                        total_batches = (total_tickers + batch_size - 1) // batch_size
                        
                        # 배치 모니터링 업데이트
                        coin_names = ", ".join([t.split('-')[1] for t in batch_tickers])
                        self.display.update_monitoring(
                            f"배치 #{batch_num}/{total_batches}: {coin_names}",
                            f"진행: {batch_end}/{total_tickers} ({int(batch_end/total_tickers*100)}%)",
                            f"동시 분석 중..."
                        )
                        self.display.render()
                        
                        # 배치 내 코인들 순차 분석 (빠른 속도)
                        for ticker in batch_tickers:
                            strategy_name = self.select_strategy(weights)
                            self.analyze_ticker(ticker, strategy_name)
                            time.sleep(0.2)  # 1초 → 0.2초로 단축
                        
                        # 배치 완료 표시
                        self.display.update_monitoring(
                            f"✅ 배치 #{batch_num} 완료",
                            f"진행: {batch_end}/{total_tickers}",
                            ""
                        )
                        self.display.render()
                        time.sleep(0.5)  # 배치 간 짧은 대기
                    
                    self.update_all_positions()
                    
                    if cycle % 10 == 0:
                        # 상태는 화면에만 표시 (로그 파일에만 기록)
                        risk_status = self.risk_manager.get_risk_status()
                        # 로그 파일에만 기록
                        self.logger.log_performance(
                            total_profit=risk_status['cumulative_profit_loss'],
                            win_rate=risk_status['win_rate'],
                            total_trades=risk_status['total_trades'],
                            current_balance=risk_status['current_balance'],
                            daily_profit=risk_status['daily_profit_loss']
                        )
                    
                    self.display.update_scan_status(f"전체 스캔 #{cycle} 완료")
                    self.last_full_scan_time = current_time
                    quick_check_count = 0
                    surge_scan_count = 0
                
                # ⭐ PHASE 2: 급등/급락 감지 (5초)
                if current_time - self.last_surge_scan_time >= self.surge_scan_interval:
                    surge_scan_count += 1
                    
                    # ⭐ 스캔 시간 기록
                    surge_time = datetime.now()
                    self.display.update_scan_times(surge_scan_time=surge_time)
                    
                    # ⭐ 모니터링 정보 업데이트 (간단하게)
                    self.display.update_monitoring(
                        f"급등/급락 감지 #{surge_scan_count}",
                        f"초단타: {len(self.ultra_positions)}/{self.max_ultra_positions}",
                        ""
                    )
                    
                    # 초단타 포지션 체크 (빠름)
                    self.check_ultra_positions()
                    
                    # 급등/급락 스캔 (신규 진입)
                    if len(self.ultra_positions) < self.max_ultra_positions:
                        self.scan_for_surges()
                    
                    self.last_surge_scan_time = current_time
                
                # ⭐ PHASE 3: 일반 포지션 체크 (3초) - v6.30.29: 시간 간격 체크 추가!
                # 🔍 DEBUG: 항상 로그 출력
                positions_count = len(self.risk_manager.positions)
                positions_list = list(self.risk_manager.positions.keys())
                positions_bool = bool(self.risk_manager.positions)
                
                
                if current_time - self.last_position_check_time >= self.position_check_interval:
                    
                    # ⭐ 포지션 체크 (positions를 변수에 고정)
                    has_positions = bool(self.risk_manager.positions)
                    positions_count = len(self.risk_manager.positions)
                    
                    
                    if has_positions:
                        quick_check_count += 1
                        
                        # ⭐ 스캔 시간 기록
                        position_time = datetime.now()
                        self.display.update_scan_times(position_check_time=position_time)
                        
                        # ⭐ v6.30.26: 화면에도 매도 체크 상태 표시
                        check_status = f"⚡ 청산 체크 #{quick_check_count}"
                        self.display.update_monitoring(
                            check_status,
                            f"포지션 {len(self.risk_manager.positions)}개 체크 중",
                            datetime.now().strftime('%H:%M:%S')
                        )
                        
                        # ⭐ v6.30.19: UI 업데이트 제거, 바로 청산 조건 체크
                        
                        # 실제 포지션 청산 조건 체크 (10가지 조건)
                        if hasattr(self, 'quick_check_positions'):
                            self.quick_check_positions()
                        else:
                            self.update_all_positions()
                        
                        # ⭐ v6.30.29: 마지막 체크 시간 업데이트 (중요!)
                        self.last_position_check_time = current_time
                    else:
                        pass  # 시간 조건 미충족
                
                # ⭐ 대기 중일 때 (간단하게)
                else:
                    wait_seconds = int(self.full_scan_interval - (time.time() - self.last_full_scan_time))
                    self.display.update_monitoring(
                        "대기 중",
                        f"다음 스캔: {wait_seconds}초",
                        ""
                    )
                
                # 대기 시간 최적화 (v6.30.14 개선: 포지션 체크 주기 고려)
                if self.ultra_positions or self.risk_manager.positions:
                    # 포지션 있으면 더 자주 체크 (3초와 5초 중 작은 값)
                    wait_time = min(self.position_check_interval, self.surge_scan_interval)  # 3초
                    next_action = "포지션체크 OR 급등감지"
                else:
                    time_until_next_scan = self.full_scan_interval - (time.time() - self.last_full_scan_time)
                    wait_time = max(self.surge_scan_interval, min(self.position_check_interval, time_until_next_scan))
                    next_action = "전체 스캔"
                
                # 🔍 DEBUG: 대기 시간 확인
                
                self.logger.log_info(f"⏳ {wait_time:.0f}초 대기 (다음: {next_action})")
                time.sleep(wait_time)
                
        
        except KeyboardInterrupt:
            self.logger.log_info("\n⏹️ 사용자에 의해 중지됨")
        except Exception as e:
            # 상세한 에러 로깅
            import traceback
            error_details = traceback.format_exc()
            self.logger.log_error("RUNTIME_ERROR", f"봇 실행 중 치명적 오류: {str(e)}", e)
            self.logger.log_error("TRACEBACK", "상세 스택 트레이스", error_details)
            # 화면에 에러 표시
            if hasattr(self, 'display'):
                self.display.update_bot_status(f"❌ 오류 발생: {str(e)[:50]}")
                self.display.render()
        finally:
            self.stop()
    
    def stop(self):
        """봇 중지 (학습 데이터 자동 저장)"""
        self.running = False
        self.logger.log_info("🛑 봇 종료 중...")
        
        # 초단타 포지션 강제 청산
        if self.ultra_positions:
            self.logger.log_warning(f"⚠️ 초단타 포지션 {len(self.ultra_positions)}개 강제 청산 중...")
            for ticker in list(self.ultra_positions.keys()):
                current_price = self.api.get_current_price(ticker)
                if current_price:
                    self.execute_ultra_sell(ticker, current_price, "봇 종료")
        
        # 🆕 학습 데이터 저장
        try:
            self.logger.log_info("💾 학습 데이터 저장 중...")
            
            # ⭐ AI 학습 엔진 데이터 저장 (가장 중요!)
            if self.learning_engine:
                self.learning_engine.save_experiences()
                self.learning_engine.save_strategy_stats()
                self.learning_engine.save_optimized_params()
                self.logger.log_info(f"   ✅ AI 학습 데이터 저장: {len(self.learning_engine.experiences)}개 경험")
            
            # 호가창 학습 데이터 저장
            if self.orderbook_monitor:
                self.orderbook_monitor.save_learning_data()
            
            # 체결 학습 데이터 저장
            if self.trade_monitor:
                self.trade_monitor.save_learning_data()
            
            # 알림 스케줄러 중지
            if hasattr(self, 'notification_scheduler'):
                self.notification_scheduler.stop()
            
            self.logger.log_info("✅ 학습 데이터 저장 완료")
        
        except Exception as e:
            self.logger.log_error("SAVE_ERROR", "학습 데이터 저장 실패", e)
        
        # ⭐ 화면 표시 정리 (커서 다시 표시)
        if hasattr(self, 'display'):
            self.display.cleanup()
        
        # 최종 상태 출력
        self.print_status()
    
    def _update_display(self):
        """화면 표시 전체 업데이트 (3초마다)"""
        try:
            # 1. AI 학습 상태 업데이트 (실시간 동기화)
            if self.learning_engine:
                # learning_engine에서 최신 통계 가져오기
                stats = self.learning_engine.get_stats()
                
                # 전략 통계 재계산 (동기화)
                total_trades = 0
                profit_trades = 0
                loss_trades = 0
                
                for strategy_name, strategy_stat in self.learning_engine.strategy_stats.items():
                    total_trades += strategy_stat.get('total_trades', 0)
                    profit_trades += strategy_stat.get('winning_trades', 0)
                    loss_trades += strategy_stat.get('losing_trades', 0)
                
                # ⭐ 디버그: AI 학습 데이터 확인 (로그 파일에만 기록)
                if total_trades > 0:
                    # print 대신 로거 사용 (v6.19 print 억제 대응)
                    pass
                
                # 화면 업데이트
                self.display.update_ai_learning(
                    total_trades=total_trades,
                    profit_trades=profit_trades,
                    loss_trades=loss_trades
                )
            
            # 2. ⭐ 자본금, 포지션, 총 자산 상태 업데이트 (실시간 동기화)
            risk_status = self.risk_manager.get_risk_status()
            position_value = self.risk_manager.get_total_position_value()  # ⭐ 추가
            total_equity = self.risk_manager.get_total_equity()  # ⭐ 추가
            
            # ⭐ 실시간 손익 계산 (총자산 - 초기자본)
            real_time_profit = total_equity - Config.INITIAL_CAPITAL
            
            self.display.update_capital_status(
                initial=Config.INITIAL_CAPITAL,
                current=risk_status['current_balance'],
                profit=real_time_profit,  # ⭐ 수정: 실시간 손익 사용
                position_value=position_value,  # ⭐ 추가: 포지션 가치
                total_equity=total_equity  # ⭐ 추가: 총 자산
            )
            
            # 3. ⭐ 시장 조건 분석 (BTC 기준 + 상세 지표)
            try:
                df = self.api.get_ohlcv('KRW-BTC', interval="minute5", count=200)
                if df is not None and not df.empty:
                    # 기본 분석
                    market_phase, entry_condition, _ = self.market_analyzer.analyze_market(df)
                    
                    # ⭐ 상세 지표 계산
                    latest = df.iloc[-1]
                    prev = df.iloc[-2]
                    
                    # BTC 변화율
                    btc_change = ((latest['close'] - prev['close']) / prev['close']) * 100
                    
                    # 거래량 변화율
                    volume_change = ((latest['volume'] - df['volume'].mean()) / df['volume'].mean()) * 100
                    
                    # 변동성 (표준편차)
                    volatility = df['close'].pct_change().std() * 100
                    
                    # RSI 계산
                    delta = df['close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rs = gain / loss
                    rsi = 100 - (100 / (1 + rs))
                    current_rsi = rsi.iloc[-1] if not rsi.empty else 50
                    
                    # ⭐ 시장 조건 이유 생성
                    reason_parts = []
                    reason_parts.append(f"BTC {btc_change:+.1f}%")
                    
                    if abs(volume_change) > 20:
                        reason_parts.append(f"거래량 {'↑' if volume_change > 0 else '↓'}{abs(volume_change):.0f}%")
                    
                    reason_parts.append(f"변동성 {volatility:.2f}%")
                    reason_parts.append(f"RSI {current_rsi:.0f}")
                    
                    # MACD 추가
                    try:
                        exp1 = df['close'].ewm(span=12).mean()
                        exp2 = df['close'].ewm(span=26).mean()
                        macd = exp1 - exp2
                        signal = macd.ewm(span=9).mean()
                        macd_val = macd.iloc[-1]
                        signal_val = signal.iloc[-1]
                        
                        if macd_val > signal_val:
                            reason_parts.append("MACD↑")
                        else:
                            reason_parts.append("MACD↓")
                    except:
                        pass
                    
                    reason = " | ".join(reason_parts)
                    
                    # ⭐ 코인 요약 개선
                    coin_summary = f"BTC {latest['close']:,.0f}원 {btc_change:+.1f}% | RSI {current_rsi:.0f}"
                    
                    # 업데이트
                    self.display.update_market_condition(market_phase, entry_condition, reason)
                    self.display.update_coin_summary(coin_summary)
                    
            except Exception as e:
                self.logger.log_warning(f"시장 분석 오류: {e}")
            
            # 4. ⭐ 거래 통계 업데이트 (매수/매도 횟수)
            trades = self.logger.get_daily_trades()
            if trades:
                buy_count = len([t for t in trades if t.get('action') == 'BUY'])
                sell_count = len([t for t in trades if t.get('action') == 'SELL'])
            else:
                buy_count = 0
                sell_count = 0
            
            self.display.update_trade_stats(buy_count, sell_count)
            
            # ⭐ 디버그: 거래 통계 확인 (로그 파일에만 기록)
            # print 대신 로거 사용 (v6.19 print 억제 대응)
            if trades and len(trades) > 0:
                pass  # 로그는 필요 시 logger 사용
            
            # 봇 상태 업데이트
            self.display.update_bot_status(f"{len(self.tickers)}개 모니터링")
            
            # 5. ⭐ 포지션 정보 실시간 업데이트
            # 현재 화면에 있는 모든 슬롯 가져오기
            current_display_tickers = set()
            for slot in range(1, self.display.max_positions + 1):
                if slot in self.display.positions:
                    current_display_tickers.add(self.display.positions[slot]['ticker'])
            
            # 실제 포지션
            actual_tickers = set(self.risk_manager.positions.keys()) | set(self.ultra_positions.keys())
            
            # ⭐ 사라진 포지션 제거 (매도된 코인)
            for ticker in current_display_tickers - actual_tickers:
                slot = self.display.get_slot_by_ticker(ticker)
                if slot:
                    # 슬롯만 제거 (매도 정보는 이미 표시됨)
                    if slot in self.display.positions:
                        del self.display.positions[slot]
            
            # 일반 포지션 (risk_manager)
            for ticker, position in self.risk_manager.positions.items():
                slot = self.display.get_slot_by_ticker(ticker)
                if not slot:
                    slot = self.display.get_available_slot()
                
                if slot:
                    current_price = self.api.get_current_price(ticker)
                    if current_price:
                        self.display.update_position(
                            slot=slot,
                            ticker=ticker,
                            entry_price=position.avg_buy_price,  # ⭐ 수정: avg_buy_price 사용
                            current_price=current_price,  # ⭐ 실시간 가격
                            amount=position.amount,
                            strategy=position.strategy,
                            entry_time=position.entry_time
                        )
            
            # 초단타 포지션 (ultra_positions)
            for ticker, position in self.ultra_positions.items():
                slot = self.display.get_slot_by_ticker(ticker)
                if not slot:
                    slot = self.display.get_available_slot()
                
                if slot:
                    current_price = self.api.get_current_price(ticker)
                    if current_price:
                        self.display.update_position(
                            slot=slot,
                            ticker=ticker,
                            entry_price=position['entry_price'],
                            current_price=current_price,  # ⭐ 실시간 가격
                            amount=position['amount'],
                            strategy='⚡초단타',
                            entry_time=position['entry_time']
                        )
            
            # 6. 화면 렌더링
            self.display.render()
        
        except Exception as e:
            self.logger.log_warning(f"화면 갱신 오류: {e}")


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description='Upbit AutoProfit Bot (Hybrid + Ultra Scalping)')
    parser.add_argument(
        '--mode',
        type=str,
        choices=['backtest', 'paper', 'live'],
        default='backtest',
        help='거래 모드 선택'
    )
    
    args = parser.parse_args()
    
    # 실거래 모드 경고
    if args.mode == 'live':
        print("=" * 60)
        print("⚠️  경고: 실거래 모드로 실행합니다!")
        print("⚠️  실제 자금이 사용되며 손실이 발생할 수 있습니다!")
        print("=" * 60)
        print("\n🔥 초단타 모드 안내:")
        print("   - 5분: 전체 코인 스캔")
        print("   - 30초: 급등/급락 감지 + 초단타 진입 (최대 2개)")
        print("   - 익절: 1% / 손절: 0.5% / 최대 보유: 5분\n")
        confirm = input("계속하시겠습니까? (yes/no): ")
        if confirm.lower() != 'yes':
            print("취소되었습니다.")
            return
    
    # 봇 실행
    bot = AutoProfitBot(mode=args.mode)
    bot.run()


if __name__ == "__main__":
    main()
