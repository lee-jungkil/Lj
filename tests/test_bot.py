"""
자동매매 봇 테스트
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from strategies.aggressive_scalping import AggressiveScalping
from strategies.conservative_scalping import ConservativeScalping
from strategies.mean_reversion import MeanReversion
from strategies.grid_trading import GridTrading
from utils.risk_manager import RiskManager


class MockUpbitAPI:
    """테스트용 모의 Upbit API"""
    
    def __init__(self, initial_balance=500000):
        self.balance = initial_balance
    
    def get_balance(self, ticker='KRW'):
        """잔고 조회"""
        if ticker == 'KRW':
            return self.balance
        return 0
    
    def deposit(self, amount):
        """입금 시뮬레이션"""
        self.balance += amount
    
    def withdraw(self, amount):
        """출금 시뮬레이션"""
        self.balance -= amount


def generate_sample_ohlcv(length=200, trend='sideways'):
    """
    샘플 OHLCV 데이터 생성
    
    Args:
        length: 데이터 길이
        trend: 추세 (uptrend, downtrend, sideways)
    
    Returns:
        DataFrame
    """
    dates = pd.date_range(end=datetime.now(), periods=length, freq='5min')
    
    base_price = 50000000  # 5천만원 (비트코인 가격)
    
    if trend == 'uptrend':
        trend_factor = np.linspace(0, 0.1, length)
    elif trend == 'downtrend':
        trend_factor = np.linspace(0, -0.1, length)
    else:
        trend_factor = np.zeros(length)
    
    # 랜덤 변동
    noise = np.random.randn(length) * 0.01
    
    prices = base_price * (1 + trend_factor + noise)
    
    df = pd.DataFrame({
        'open': prices * 0.998,
        'high': prices * 1.002,
        'low': prices * 0.997,
        'close': prices,
        'volume': np.random.randint(100, 1000, length),
        'value': np.random.randint(1000000, 10000000, length)
    }, index=dates)
    
    return df


class TestStrategies:
    """전략 테스트"""
    
    def test_aggressive_scalping_buy_signal(self):
        """극공격적 단타 매수 신호 테스트"""
        config = {
            'stop_loss': 0.02,
            'take_profit': 0.015,
            'rsi_oversold': 30,
            'rsi_overbought': 70,
            'volume_threshold': 1.5,
            'min_price_change': 0.01
        }
        
        strategy = AggressiveScalping(config)
        df = generate_sample_ohlcv(200, trend='downtrend')
        
        signal, reason, indicators = strategy.generate_signal(df, 'KRW-BTC')
        
        assert signal in ['BUY', 'SELL', 'HOLD']
        assert 'rsi' in indicators
        assert 'volume_ratio' in indicators
    
    def test_conservative_scalping_buy_signal(self):
        """보수적 단타 매수 신호 테스트"""
        config = {
            'stop_loss': 0.015,
            'take_profit': 0.01,
            'rsi_min': 40,
            'rsi_max': 60,
            'bb_threshold': 0.95
        }
        
        strategy = ConservativeScalping(config)
        df = generate_sample_ohlcv(200, trend='sideways')
        
        signal, reason, indicators = strategy.generate_signal(df, 'KRW-BTC')
        
        assert signal in ['BUY', 'SELL', 'HOLD']
        assert 'bb_position' in indicators
    
    def test_mean_reversion_signal(self):
        """평균 회귀 신호 테스트"""
        config = {
            'stop_loss': 0.03,
            'take_profit': 0.025,
            'ma_period': 20,
            'deviation_threshold': 0.05
        }
        
        strategy = MeanReversion(config)
        df = generate_sample_ohlcv(200, trend='sideways')
        
        signal, reason, indicators = strategy.generate_signal(df, 'KRW-BTC')
        
        assert signal in ['BUY', 'SELL', 'HOLD']
        assert 'deviation' in indicators
    
    def test_grid_trading_initialization(self):
        """그리드 거래 초기화 테스트"""
        config = {
            'stop_loss': 0.04,
            'grid_count': 10,
            'grid_spacing': 0.005,
            'max_volatility': 0.02
        }
        
        strategy = GridTrading(config)
        strategy.initialize_grids(50000000)
        
        assert strategy.grid_initialized == True
        assert len(strategy.grids) > 0
        assert strategy.base_price == 50000000


class TestRiskManager:
    """리스크 관리자 테스트"""
    
    def test_risk_manager_initialization(self):
        """리스크 관리자 초기화 테스트"""
        rm = RiskManager(
            initial_capital=500000,
            max_daily_loss=50000,
            max_cumulative_loss=100000,
            max_positions=3,
            max_position_ratio=0.3
        )
        
        assert rm.current_balance == 500000
        assert rm.max_daily_loss == 50000
        assert rm.max_cumulative_loss == 100000
    
    def test_can_open_position(self):
        """포지션 개설 가능 여부 테스트"""
        rm = RiskManager(500000, 50000, 100000)
        
        can_open, msg = rm.can_open_position('KRW-BTC')
        assert can_open == True
    
    def test_add_position(self):
        """포지션 추가 테스트"""
        rm = RiskManager(500000, 50000, 100000)
        
        success = rm.add_position(
            ticker='KRW-BTC',
            amount=0.001,
            price=50000000,
            strategy='test'
        )
        
        assert success == True
        assert 'KRW-BTC' in rm.positions
        assert rm.current_balance < 500000
    
    def test_close_position(self):
        """포지션 청산 테스트"""
        rm = RiskManager(500000, 50000, 100000)
        
        # 포지션 추가
        rm.add_position('KRW-BTC', 0.001, 50000000, 'test')
        
        # 포지션 청산 (수익)
        profit_loss = rm.close_position('KRW-BTC', 51000000)
        
        assert profit_loss is not None
        assert profit_loss > 0
        assert 'KRW-BTC' not in rm.positions
    
    def test_max_positions_limit(self):
        """최대 포지션 수 제한 테스트"""
        rm = RiskManager(500000, 50000, 100000, max_positions=2)
        
        rm.add_position('KRW-BTC', 0.001, 50000000, 'test')
        rm.add_position('KRW-ETH', 0.01, 3000000, 'test')
        
        can_open, msg = rm.can_open_position('KRW-XRP')
        assert can_open == False
    
    def test_daily_loss_limit(self):
        """일일 손실 한도 테스트"""
        rm = RiskManager(500000, 50000, 100000)
        
        # 큰 손실 발생 (여러 번 - 더 큰 손실)
        for i in range(5):
            rm.add_position(f'KRW-BTC{i}', 0.002, 50000000, 'test')  # 10만원 투자
            rm.close_position(f'KRW-BTC{i}', 45000000)  # 10% 손실 (약 -1만원)
        
        # 총 약 -5만원 이상 손실로 한도 초과
        print(f"일일 손실: {rm.daily_profit_loss}")
        can_open, msg = rm.can_open_position('KRW-ETH')
        assert can_open == False
        assert rm.is_trading_stopped == True
    
    def test_win_rate_calculation(self):
        """승률 계산 테스트"""
        rm = RiskManager(500000, 50000, 100000)
        
        # 승리 거래
        rm.add_position('KRW-BTC', 0.001, 50000000, 'test')
        rm.close_position('KRW-BTC', 51000000)
        
        # 패배 거래
        rm.add_position('KRW-ETH', 0.01, 3000000, 'test')
        rm.close_position('KRW-ETH', 2900000)
        
        win_rate = rm.get_win_rate()
        assert win_rate == 50.0
    
    def test_balance_sync_deposit(self):
        """외부 입금 시 잔고 동기화 테스트"""
        mock_api = MockUpbitAPI(initial_balance=500000)
        rm = RiskManager(500000, 50000, 100000, upbit_api=mock_api)
        
        # 초기 잔고 확인
        assert rm.current_balance == 500000
        
        # 외부에서 200,000원 입금
        mock_api.deposit(200000)
        
        # 동기화 전에는 봇이 모름
        assert rm.current_balance == 500000
        
        # 동기화 실행
        sync_result = rm.sync_balance_from_exchange()
        
        # 동기화 성공
        assert sync_result == True
        assert rm.current_balance == 700000
    
    def test_balance_sync_withdrawal(self):
        """외부 출금 시 잔고 동기화 테스트"""
        mock_api = MockUpbitAPI(initial_balance=500000)
        rm = RiskManager(500000, 50000, 100000, upbit_api=mock_api)
        
        # 외부에서 100,000원 출금
        mock_api.withdraw(100000)
        
        # 동기화 실행
        rm.sync_balance_from_exchange()
        
        # 잔고 감소 확인
        assert rm.current_balance == 400000
    
    def test_balance_sync_small_difference(self):
        """작은 잔고 차이는 무시 테스트"""
        mock_api = MockUpbitAPI(initial_balance=500500)  # 500원 차이
        rm = RiskManager(500000, 50000, 100000, upbit_api=mock_api)
        
        # 동기화 실행
        rm.sync_balance_from_exchange()
        
        # 1000원 미만 차이는 무시됨
        assert rm.current_balance == 500000
    
    def test_position_size_after_deposit(self):
        """입금 후 포지션 크기 자동 조정 테스트"""
        mock_api = MockUpbitAPI(initial_balance=500000)
        rm = RiskManager(500000, 50000, 100000, max_position_ratio=0.3, upbit_api=mock_api)
        
        # 초기 포지션 크기
        initial_size = rm.calculate_position_size(50000000)
        assert initial_size == 500000 * 0.3  # 150,000원
        
        # 200,000원 입금
        mock_api.deposit(200000)
        
        # 강제 동기화 후 포지션 크기
        new_size = rm.calculate_position_size(50000000, force_sync=True)
        assert rm.current_balance == 700000
        assert new_size == 700000 * 0.3  # 210,000원


if __name__ == "__main__":
    pytest.main([__file__, '-v'])


class TestStrategyOptimizer:
    """전략 최적화 테스트"""
    
    def test_optimizer_initialization(self):
        """최적화 엔진 초기화 테스트"""
        from utils.strategy_optimizer import StrategyOptimizer
        
        optimizer = StrategyOptimizer()
        
        assert len(optimizer.performances) == 4
        assert 'aggressive_scalping' in optimizer.performances
        assert 'conservative_scalping' in optimizer.performances
        assert 'mean_reversion' in optimizer.performances
        assert 'grid_trading' in optimizer.performances
    
    def test_record_trade_learning(self):
        """거래 기록 및 학습 테스트"""
        from utils.strategy_optimizer import StrategyOptimizer, MarketCondition
        import tempfile
        
        # 임시 디렉토리 사용
        with tempfile.TemporaryDirectory() as tmpdir:
            optimizer = StrategyOptimizer(data_dir=tmpdir)
            
            # 시장 상황
            market = MarketCondition(
                volatility='high',
                trend='uptrend',
                volume='high',
                sentiment='positive'
            )
            
            # 성공 거래 기록
            optimizer.record_trade(
                strategy='aggressive_scalping',
                profit_loss=15000,
                market_condition=market,
                entry_price=50000000,
                exit_price=50750000,
                hold_time=300
            )
            
            perf = optimizer.performances['aggressive_scalping']
            assert perf.trades == 1
            assert perf.wins == 1
            assert perf.total_profit == 15000
    
    def test_weight_optimization(self):
        """가중치 최적화 테스트"""
        from utils.strategy_optimizer import StrategyOptimizer, MarketCondition
        
        optimizer = StrategyOptimizer()
        market = MarketCondition('high', 'uptrend', 'high', 'positive')
        
        # 여러 거래 기록 (aggressive_scalping이 유리)
        for i in range(5):
            optimizer.record_trade('aggressive_scalping', 10000, market, 50000000, 50500000, 300)
            optimizer.record_trade('conservative_scalping', -5000, market, 50000000, 49750000, 300)
        
        # 기본 가중치
        base_weights = {
            'aggressive_scalping': 25,
            'conservative_scalping': 25,
            'mean_reversion': 25,
            'grid_trading': 25
        }
        
        # 최적화된 가중치
        optimized = optimizer.get_optimized_weights(market, base_weights)
        
        # aggressive_scalping 가중치가 증가했어야 함
        assert optimized['aggressive_scalping'] > base_weights['aggressive_scalping']
    
    def test_best_strategy_selection(self):
        """최적 전략 선택 테스트"""
        from utils.strategy_optimizer import StrategyOptimizer, MarketCondition
        
        optimizer = StrategyOptimizer()
        market = MarketCondition('low', 'sideways', 'medium', 'neutral')
        
        # grid_trading이 횡보장에서 성공
        for i in range(10):
            optimizer.record_trade('grid_trading', 5000, market, 50000000, 50250000, 600)
            optimizer.record_trade('aggressive_scalping', -3000, market, 50000000, 49850000, 300)
        
        # 최적 전략 추천
        best = optimizer.get_best_strategy(market)
        assert best == 'grid_trading'
    
    def test_market_analysis(self):
        """시장 상황 분석 테스트"""
        from utils.market_analyzer import analyze_market_condition
        
        # 샘플 데이터 생성
        df = generate_sample_ohlcv(200, trend='uptrend')
        
        volatility, trend, volume, sentiment = analyze_market_condition(df, 0.7)
        
        assert volatility in ['high', 'medium', 'low']
        assert trend in ['uptrend', 'downtrend', 'sideways']
        assert volume in ['high', 'medium', 'low']
        assert sentiment in ['positive', 'neutral', 'negative']


if __name__ == "__main__":
    pytest.main([__file__, '-v'])


class TestHoldingProtector:
    """기존 보유 보호 테스트"""
    
    def test_register_existing_holding(self):
        """기존 보유 등록 테스트"""
        from utils.holding_protector import HoldingProtector
        import tempfile
        
        with tempfile.TemporaryDirectory() as tmpdir:
            protector = HoldingProtector(data_dir=tmpdir)
            
            # 기존 보유 등록
            success = protector.register_existing_holding(
                ticker='KRW-DOGE',
                amount=10000,
                avg_buy_price=100,
                note='테스트'
            )
            
            assert success == True
            assert 'KRW-DOGE' in protector.existing_holdings
            assert protector.get_existing_amount('KRW-DOGE') == 10000
    
    def test_bot_position_separation(self):
        """봇 포지션 분리 테스트"""
        from utils.holding_protector import HoldingProtector
        import tempfile
        
        with tempfile.TemporaryDirectory() as tmpdir:
            protector = HoldingProtector(data_dir=tmpdir)
            
            # 기존 보유 등록
            protector.register_existing_holding('KRW-DOGE', 10000, 100)
            
            # 봇 포지션 추가
            protector.add_bot_position('KRW-DOGE', 5000, 10, 'test')
            
            # 분리 확인
            assert protector.get_existing_amount('KRW-DOGE') == 10000
            assert protector.bot_positions['KRW-DOGE'].bot_amount == 5000
    
    def test_sellable_amount_calculation(self):
        """매도 가능 수량 계산 테스트"""
        from utils.holding_protector import HoldingProtector
        import tempfile
        
        with tempfile.TemporaryDirectory() as tmpdir:
            protector = HoldingProtector(data_dir=tmpdir)
            
            # 기존 보유 등록
            protector.register_existing_holding('KRW-DOGE', 10000, 100)
            
            # 봇 포지션 추가
            protector.add_bot_position('KRW-DOGE', 5000, 10)
            
            # 매도 가능 수량 (API 없이)
            sellable, msg = protector.calculate_sellable_amount('KRW-DOGE')
            
            assert sellable == 5000  # 봇 투자분만
            assert "봇 투자분" in msg
    
    def test_bot_position_close(self):
        """봇 포지션 청산 테스트"""
        from utils.holding_protector import HoldingProtector
        import tempfile
        
        with tempfile.TemporaryDirectory() as tmpdir:
            protector = HoldingProtector(data_dir=tmpdir)
            
            # 기존 보유 등록
            protector.register_existing_holding('KRW-DOGE', 10000, 100)
            
            # 봇 포지션 추가
            protector.add_bot_position('KRW-DOGE', 5000, 10)
            
            # 봇 포지션 청산 (수익)
            profit = protector.close_bot_position('KRW-DOGE', 5000, 15)
            
            assert profit is not None
            assert profit > 0  # 수익 발생
            assert 'KRW-DOGE' not in protector.bot_positions  # 청산 완료
            assert protector.is_existing_holding('KRW-DOGE')  # 기존 보유 유지


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
