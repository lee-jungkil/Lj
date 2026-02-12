"""
설정 관리 모듈
환경변수 및 봇 설정을 중앙에서 관리
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()


class Config:
    """봇 설정 클래스"""
    
    # Upbit API 설정
    UPBIT_ACCESS_KEY = os.getenv('UPBIT_ACCESS_KEY', '')
    UPBIT_SECRET_KEY = os.getenv('UPBIT_SECRET_KEY', '')
    
    # 자본 및 리스크 설정
    INITIAL_CAPITAL = int(os.getenv('INITIAL_CAPITAL', 500000))
    MAX_DAILY_LOSS = int(os.getenv('MAX_DAILY_LOSS', 50000))
    MAX_CUMULATIVE_LOSS = int(os.getenv('MAX_CUMULATIVE_LOSS', 100000))
    MAX_POSITIONS = int(os.getenv('MAX_POSITIONS', 7))  # 5개 → 7개로 확대
    MAX_POSITION_RATIO = float(os.getenv('MAX_POSITION_RATIO', 0.3))
    
    # 거래 모드
    TRADING_MODE = os.getenv('TRADING_MODE', 'backtest')  # backtest, paper, live
    
    # 로깅 설정
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    ENABLE_TRADING_LOG = os.getenv('ENABLE_TRADING_LOG', 'true').lower() == 'true'
    ENABLE_ERROR_LOG = os.getenv('ENABLE_ERROR_LOG', 'true').lower() == 'true'
    
    # 감정 분석 설정
    ENABLE_SENTIMENT = os.getenv('ENABLE_SENTIMENT', 'true').lower() == 'true'
    NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')
    
    # 알림 설정 (Phase 1)
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
    
    # Gmail 설정
    GMAIL_SENDER = os.getenv('GMAIL_SENDER', '')
    GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD', '')
    GMAIL_RECEIVER = os.getenv('GMAIL_RECEIVER', '')
    
    # 동적 청산 설정
    ENABLE_DYNAMIC_EXIT = os.getenv('ENABLE_DYNAMIC_EXIT', 'true').lower() == 'true'
    EXIT_MODE = os.getenv('EXIT_MODE', 'moderate')  # aggressive, moderate, conservative
    
    # ⭐ Phase 2-B/2-C AI 고급 시스템 설정
    ENABLE_ADVANCED_AI = os.getenv('ENABLE_ADVANCED_AI', 'true').lower() == 'true'
    ENABLE_ORDERBOOK_ANALYSIS = os.getenv('ENABLE_ORDERBOOK_ANALYSIS', 'true').lower() == 'true'
    ENABLE_SCENARIO_DETECTION = os.getenv('ENABLE_SCENARIO_DETECTION', 'true').lower() == 'true'
    ENABLE_SMART_SPLIT = os.getenv('ENABLE_SMART_SPLIT', 'true').lower() == 'true'
    ENABLE_HOLDING_TIME_AI = os.getenv('ENABLE_HOLDING_TIME_AI', 'true').lower() == 'true'
    
    # 호가창 분석 설정
    ORDERBOOK_CONFIG = {
        'min_liquidity_score': 30.0,  # 최소 유동성 점수
        'max_slippage_risk': 'MEDIUM',  # 허용 슬리피지 위험도
        'cache_duration': 3,  # 캐시 유효 시간 (초)
    }
    
    # 분할 전략 설정
    SPLIT_CONFIG = {
        'min_split_amount': 5000,  # 최소 분할 금액 (원)
        'max_splits': 5,  # 최대 분할 수
        'default_buy_interval': 30,  # 매수 간격 (초)
        'default_sell_interval': 15,  # 매도 간격 (초)
    }
    
    # 보유 시간 AI 설정
    HOLDING_TIME_CONFIG = {
        'min_samples_for_prediction': 3,  # 예측 최소 샘플 수
        'max_holding_data': 5000,  # 최대 저장 거래 수
        'confidence_threshold': 60.0,  # 신뢰도 임계값
    }
    
    # ⭐ v6.29 Advanced Order System 설정
    # 주문 방식 설정
    BUY_ORDER_TYPE = os.getenv('BUY_ORDER_TYPE', 'auto')  # auto, market, limit, best
    SELL_ORDER_TYPE = os.getenv('SELL_ORDER_TYPE', 'auto')
    SLIPPAGE_TOLERANCE = float(os.getenv('SLIPPAGE_TOLERANCE', 0.5))
    ORDER_MAX_RETRIES = int(os.getenv('ORDER_MAX_RETRIES', 3))
    ORDER_RETRY_DELAY = float(os.getenv('ORDER_RETRY_DELAY', 1.0))
    LIMIT_ORDER_TIMEOUT = int(os.getenv('LIMIT_ORDER_TIMEOUT', 5))
    LIMIT_ORDER_FALLBACK = os.getenv('LIMIT_ORDER_FALLBACK', 'true').lower() == 'true'
    
    # 추격매수 설정
    ENABLE_CHASE_BUY = os.getenv('ENABLE_CHASE_BUY', 'true').lower() == 'true'
    SURGE_THRESHOLD_1M = float(os.getenv('SURGE_THRESHOLD_1M', 1.5))
    SURGE_THRESHOLD_5M = float(os.getenv('SURGE_THRESHOLD_5M', 3.0))
    SURGE_THRESHOLD_15M = float(os.getenv('SURGE_THRESHOLD_15M', 5.0))
    VOLUME_SURGE_RATIO = float(os.getenv('VOLUME_SURGE_RATIO', 2.0))
    CHASE_MIN_SCORE = float(os.getenv('CHASE_MIN_SCORE', 50))
    CHASE_TAKE_PROFIT = float(os.getenv('CHASE_TAKE_PROFIT', 2.0))
    CHASE_STOP_LOSS = float(os.getenv('CHASE_STOP_LOSS', -3.0))
    CHASE_MAX_HOLD_TIME = int(os.getenv('CHASE_MAX_HOLD_TIME', 300))
    CHASE_MAX_CONCURRENT = int(os.getenv('CHASE_MAX_CONCURRENT', 2))
    CHASE_DAILY_LIMIT = int(os.getenv('CHASE_DAILY_LIMIT', 10))
    
    # ⭐ v6.30 Phase 2B: Advanced Trading Features
    # Dynamic Stop Loss 설정
    ENABLE_DYNAMIC_STOP_LOSS = os.getenv('ENABLE_DYNAMIC_STOP_LOSS', 'true').lower() == 'true'
    
    # Scaled Sell 설정 (환경변수로 관리)
    ENABLE_SCALED_SELL = os.getenv('ENABLE_SCALED_SELL', 'false').lower() == 'true'
    SCALED_SELL_LEVELS = os.getenv('SCALED_SELL_LEVELS', '2.0:30,4.0:40,6.0:30')
    
    # Conditional Sell 설정
    ENABLE_CONDITIONAL_SELL = os.getenv('ENABLE_CONDITIONAL_SELL', 'false').lower() == 'true'
    CONDITIONAL_SELL_MIN_CONDITIONS = int(os.getenv('CONDITIONAL_SELL_MIN_CONDITIONS', 2))
    
    # 트레일링 스탑 설정
    ENABLE_TRAILING_STOP = os.getenv('ENABLE_TRAILING_STOP', 'true').lower() == 'true'
    TRAILING_STOP_OFFSET = float(os.getenv('TRAILING_STOP_OFFSET', 1.0))
    TRAILING_STOP_MIN_PROFIT = float(os.getenv('TRAILING_STOP_MIN_PROFIT', 1.0))
    
    # 스프레드 임계값
    SPREAD_THRESHOLD_LOW = float(os.getenv('SPREAD_THRESHOLD_LOW', 0.1))
    SPREAD_THRESHOLD_HIGH = float(os.getenv('SPREAD_THRESHOLD_HIGH', 0.5))
    
    # 전략별 최대 보유 시간 (초)
    MAX_HOLD_TIME_CHASE = int(os.getenv('MAX_HOLD_TIME_CHASE', 300))
    MAX_HOLD_TIME_ULTRA = int(os.getenv('MAX_HOLD_TIME_ULTRA', 600))
    MAX_HOLD_TIME_AGGRESSIVE = int(os.getenv('MAX_HOLD_TIME_AGGRESSIVE', 1800))
    MAX_HOLD_TIME_CONSERVATIVE = int(os.getenv('MAX_HOLD_TIME_CONSERVATIVE', 3600))
    MAX_HOLD_TIME_MEAN_REVERSION = int(os.getenv('MAX_HOLD_TIME_MEAN_REVERSION', 7200))
    MAX_HOLD_TIME_GRID = int(os.getenv('MAX_HOLD_TIME_GRID', 86400))
    
    # 급락 및 거래량 급감 감지
    SUDDEN_DROP_THRESHOLD = float(os.getenv('SUDDEN_DROP_THRESHOLD', -1.5))
    VOLUME_DROP_THRESHOLD = float(os.getenv('VOLUME_DROP_THRESHOLD', 0.5))
    
    # 차트 신호 청산 설정
    ENABLE_CHART_SIGNAL_EXIT = os.getenv('ENABLE_CHART_SIGNAL_EXIT', 'true').lower() == 'true'
    CHART_SIGNAL_MIN_PROFIT = float(os.getenv('CHART_SIGNAL_MIN_PROFIT', 0.5))
    
    # 전략별 설정
    STRATEGIES = {
        'aggressive_scalping': {
            'enabled': True,
            'stop_loss': 0.03,      # 3% 손절 (완화)
            'take_profit': 0.02,    # 2% 익절 (완화)
            'rsi_oversold': 40,     # 40으로 완화 (더 자주 진입)
            'rsi_overbought': 60,   # 60으로 완화
            'volume_threshold': 1.2,  # 120%로 완화 (더 쉽게 진입)
            'min_price_change': 0.005,  # 0.5%로 완화 (더 쉽게 진입)
        },
        'conservative_scalping': {
            'enabled': True,
            'stop_loss': 0.02,      # 2% 손절 (완화)
            'take_profit': 0.015,   # 1.5% 익절 (완화)
            'rsi_min': 35,          # 35로 완화
            'rsi_max': 65,          # 65로 완화
            'bb_threshold': 0.9,    # 90%로 완화 (더 자주 진입)
        },
        'mean_reversion': {
            'enabled': True,
            'stop_loss': 0.04,      # 4% 손절
            'take_profit': 0.03,    # 3% 익절 (완화)
            'ma_period': 20,
            'deviation_threshold': 0.03,  # 3%로 완화 (더 자주 진입)
        },
        'grid_trading': {
            'enabled': True,
            'stop_loss': 0.05,      # 5% 손절 (완화)
            'grid_count': 10,
            'grid_spacing': 0.005,  # 0.5% 간격
            'max_volatility': 0.03,  # 3%로 완화 (더 쉽게 진입)
        },
        # ⭐ 초단타 전략 (Ultra Scalping) - 스마트 버전
        'ultra_scalping': {
            'enabled': True,
            'stop_loss': 0.01,       # 1% 손절 (완화)
            'take_profit': 0.015,    # 1.5% 익절 (완화)
            'min_price_surge': 0.015, # 1.5%로 완화 (더 자주 진입)
            'volume_spike': 2.0,     # 2배로 완화 (더 쉽게 진입)
            'max_hold_time': 300,    # 최대 5분 보유 (초)
            # ⭐ 스마트 매도 설정
            'smart_exit': True,      # 스마트 매도 활성화
            'profit_recheck_threshold': 0.005,  # 0.5% 이상부터 재확인
            'momentum_threshold': 0.001,  # 0.1% 모멘텀 기준
        }
    }
    
    # 시간대별 전략 가중치 (ultra_scalping은 제외 - 별도 운영)
    TIME_STRATEGY_WEIGHTS = {
        'morning_rush': {  # 09:00-11:00
            'hours': [(9, 10, 11)],
            'aggressive_scalping': 0.4,
            'conservative_scalping': 0.3,
            'mean_reversion': 0.2,
            'grid_trading': 0.1,
        },
        'midday': {  # 11:00-14:00
            'hours': [(11, 12, 13, 14)],
            'aggressive_scalping': 0.2,
            'conservative_scalping': 0.4,
            'mean_reversion': 0.2,
            'grid_trading': 0.2,
        },
        'afternoon_rush': {  # 14:00-16:00
            'hours': [(14, 15, 16)],
            'aggressive_scalping': 0.35,
            'conservative_scalping': 0.35,
            'mean_reversion': 0.2,
            'grid_trading': 0.1,
        },
        'night': {  # 21:00-09:00
            'hours': [(21, 22, 23, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)],
            'aggressive_scalping': 0.15,
            'conservative_scalping': 0.25,
            'mean_reversion': 0.4,
            'grid_trading': 0.2,
        },
    }
    
    # ⭐ 초단타 시스템 설정 (v5.4 업데이트)
    ULTRA_SCALPING_CONFIG = {
        'enabled': True,
        'default_positions': 3,      # 기본 3개
        'max_positions': 5,          # 최대 5개 (확신 있을 때)
        'scan_interval': 5,          # 5초마다 스캔 (빠른 감지)
        'position_check_interval': 3, # 3초마다 포지션 체크
        'max_investment_ratio': 0.15, # 잔고의 15%
        'max_investment_amount': 100000, # 최대 10만원
        'high_confidence_threshold': 0.8, # 80% 이상 확신 시 5개까지
    }
    
    # ⭐ 동적 코인 선정 시스템
    ENABLE_DYNAMIC_COIN_SELECTION = os.getenv('ENABLE_DYNAMIC_COIN_SELECTION', 'true').lower() == 'true'
    COIN_SELECTION_METHOD = os.getenv('COIN_SELECTION_METHOD', 'volume')  # volume, rsi, multi
    COIN_SELECTION_INTERVAL = int(os.getenv('COIN_SELECTION_INTERVAL', 180))  # 3분 = 180초
    FIXED_COIN_COUNT = int(os.getenv('FIXED_COIN_COUNT', 35))  # 고정 35개 코인
    
    # ⭐ 실시간 잔고 감지 (Upbit 실제 KRW 잔고 사용)
    USE_REAL_BALANCE = os.getenv('USE_REAL_BALANCE', 'true').lower() == 'true'
    
    # 코인 화이트리스트 (동적 선정 비활성화 시 사용)
    WHITELIST_COINS = [
        'KRW-BTC',   # 비트코인
        'KRW-ETH',   # 이더리움
        'KRW-XRP',   # 리플
        'KRW-ADA',   # 카르다노
        'KRW-SOL',   # 솔라나
        'KRW-DOGE',  # 도지코인
        'KRW-DOT',   # 폴카닷
        'KRW-AVAX',  # 아발란체
        'KRW-LINK',  # 체인링크
        'KRW-ATOM',  # 코스모스
    ]
    
    # 수익 관리 설정
    PROFIT_MANAGEMENT = {
        'withdrawal_ratio': 0.5,  # 월간 수익의 50% 출금
        'reinvest_ratio': 0.5,    # 50% 재투자
        'check_day': 1,           # 매월 1일 확인
    }
    
    @classmethod
    def validate(cls) -> bool:
        """설정 유효성 검사"""
        if cls.TRADING_MODE == 'live':
            if not cls.UPBIT_ACCESS_KEY or not cls.UPBIT_SECRET_KEY:
                raise ValueError("실거래 모드에서는 Upbit API 키가 필수입니다!")
        
        if cls.INITIAL_CAPITAL < 5000:
            raise ValueError("초기 자본은 최소 5,000원 이상이어야 합니다!")
        
        return True
    
    @classmethod
    def get_strategy_config(cls, strategy_name: str) -> Dict[str, Any]:
        """특정 전략 설정 가져오기"""
        return cls.STRATEGIES.get(strategy_name, {})
    
    @classmethod
    def get_time_weights(cls, hour: int) -> Dict[str, float]:
        """현재 시간대의 전략 가중치 가져오기"""
        for period, config in cls.TIME_STRATEGY_WEIGHTS.items():
            if hour in config['hours'][0]:
                return {
                    'aggressive_scalping': config['aggressive_scalping'],
                    'conservative_scalping': config['conservative_scalping'],
                    'mean_reversion': config['mean_reversion'],
                    'grid_trading': config['grid_trading'],
                }
        
        # 기본값 (균등 분배)
        return {
            'aggressive_scalping': 0.25,
            'conservative_scalping': 0.25,
            'mean_reversion': 0.25,
            'grid_trading': 0.25,
        }
    
    @classmethod
    def is_live_mode(cls) -> bool:
        """실거래 모드 여부"""
        return cls.TRADING_MODE == 'live'
    
    @classmethod
    def is_paper_mode(cls) -> bool:
        """모의투자 모드 여부"""
        return cls.TRADING_MODE == 'paper'
    
    @classmethod
    def is_backtest_mode(cls) -> bool:
        """백테스트 모드 여부"""
        return cls.TRADING_MODE == 'backtest'


# 설정 검증
try:
    Config.validate()
except Exception as e:
    print(f"⚠️ 설정 오류: {e}")
    print("📝 .env 파일을 확인하세요!")
