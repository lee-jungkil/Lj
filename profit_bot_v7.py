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
            initial_capital=1000000,  # 초기 자본 100만원
            max_daily_loss=50000,     # 일일 최대 손실 5만원 (5%)
            max_cumulative_loss=100000,  # 누적 최대 손실 10만원
            max_positions=3,          # 최대 3개 포지션
            upbit_api=self.api
        )
        self.risk_manager.max_open_positions = 3  # 포지션 제한 명시
        
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
            for ticker in top_volume_tickers[:10]:  # 상위 10개만 빠르게 체크 (더 빠르게)
                try:
                    current_price = self.api.get_current_price(ticker)
                    if current_price and current_price > 0:
                        candidates.append(ticker)
                except:
                    continue
            
            logger.info(f"🎯 {len(candidates)}개 후보 발견, 상세 분석 중...")
            
            # 2차 상세 스캔: 후보들만 상세 분석 (최대 5개까지만)
            for i, ticker in enumerate(candidates[:5]):
                if len(self.positions) >= self.risk_manager.max_open_positions:
                    break  # 포지션 제한 도달
                
                # 시장 데이터 수집 (상세)
                market_data = self._get_market_data(ticker)
                if not market_data:
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
        """매수 실행"""
        try:
            logger.info(f"💰 매수 시작: {ticker}")
            
            # 현재 가격
            current_price = self.api.get_current_price(ticker)
            if not current_price:
                logger.error(f"❌ {ticker} 가격 조회 실패")
                return
            
            # 가용 자금 확인
            if self.mode == 'live':
                balance = self.api.get_balance()
                available_krw = balance.get('KRW', 0)
            else:
                available_krw = 1000000  # 시뮬레이션: 100만원
            
            if available_krw < 10000:
                logger.warning("⚠️ 가용 자금 부족 (최소 10,000원)")
                return
            
            # 포지션 크기 계산
            quantity = self.strategy.get_position_size(available_krw, current_price)
            
            # 최소 주문 금액 확인 (5000원)
            order_value = quantity * current_price
            if order_value < 5000:
                logger.warning(f"⚠️ {ticker} 주문 금액 부족: {order_value:.0f}원 < 5000원")
                return
            
            # 주문 실행
            if self.mode == 'live':
                # 실전: 실제 주문
                result = self.order_executor.execute_buy(
                    ticker=ticker,
                    volume=quantity,
                    method='market'  # 시장가 매수
                )
                
                if not result or 'error' in result:
                    logger.error(f"❌ {ticker} 매수 주문 실패: {result}")
                    return
                
                logger.info(f"✅ {ticker} 매수 완료! {quantity:.8f}개 @ {current_price:,.0f}원")
            else:
                # 시뮬레이션
                logger.info(f"✅ [시뮬] {ticker} 매수! {quantity:.8f}개 @ {current_price:,.0f}원 (금액: {order_value:,.0f}원)")
            
            # 포지션 생성
            position = Position(
                ticker=ticker,
                quantity=quantity,
                entry_price=current_price,
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
        """시장 데이터 수집"""
        try:
            # 현재 가격
            current_price = self.api.get_current_price(ticker)
            if not current_price:
                return {}
            
            # OHLCV 데이터 (1분봉)
            df_1m = self.api.get_ohlcv(ticker, interval='minute1', count=10)
            if df_1m is None or df_1m.empty:
                return {}
            
            # OHLCV 데이터 (5분봉)
            df_5m = self.api.get_ohlcv(ticker, interval='minute5', count=20)
            if df_5m is None or df_5m.empty:
                return {}
            
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
            from src.utils.technical_indicators import calculate_rsi
            rsi = calculate_rsi(df_5m, period=14)
            rsi_value = float(rsi.iloc[-1]) if rsi is not None and not rsi.empty else 50
            
            # 호가창 (매도 압력)
            orderbook = self.api.get_orderbook(ticker)
            if orderbook and 'orderbook_units' in orderbook:
                orderbook_units = orderbook['orderbook_units']
                # 매도 호가 (ask) 상위 5개
                sell_volume = sum([float(unit.get('ask_size', 0)) for unit in orderbook_units[:5]])
                # 매수 호가 (bid) 상위 5개
                buy_volume = sum([float(unit.get('bid_size', 0)) for unit in orderbook_units[:5]])
                sell_pressure = sell_volume / buy_volume if buy_volume > 0 else 1.0
            else:
                sell_pressure = 1.0
            
            return {
                'current_price': current_price,
                'current_volume': current_volume,
                'avg_volume_5m': avg_volume_5m,
                'price_change_1m': price_change_1m,
                'rsi': rsi_value,
                'sell_pressure': sell_pressure,
            }
        
        except Exception as e:
            logger.error(f"❌ {ticker} 시장 데이터 수집 실패: {e}")
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
