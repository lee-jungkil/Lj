"""
스마트 주문 실행 시스템
호가창 분석 + 분할 전략 + AI 최적화를 통합한 지능형 주문 관리
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime
import time


class SmartOrderExecutor:
    """스마트 주문 실행기"""
    
    def __init__(
        self, 
        api_client,
        order_book_analyzer,
        split_strategies,
        holding_time_optimizer
    ):
        """
        Args:
            api_client: Upbit API 클라이언트
            order_book_analyzer: 호가창 분석기
            split_strategies: 분할 전략 관리자
            holding_time_optimizer: 보유 시간 최적화 AI
        """
        self.api = api_client
        self.orderbook_analyzer = order_book_analyzer
        self.split_strategies = split_strategies
        self.holding_optimizer = holding_time_optimizer
        
        # 실행 히스토리
        self.execution_history = []
        
        # 대기 중인 주문
        self.pending_orders = []
        
    def execute_smart_buy(
        self,
        ticker: str,
        total_amount: float,
        scenario_id: int,
        confidence: float,
        volatility: float,
        strategy_name: str,
        reason: str
    ) -> Dict:
        """
        스마트 매수 실행
        
        프로세스:
        1. 호가창 분석 → 실행 가능 여부 판단
        2. 분할 전략 선택
        3. 단계별 주문 실행
        
        Returns:
            {
                'success': bool,
                'executed_amount': float,
                'avg_price': float,
                'splits_executed': int,
                'total_splits': int,
                'execution_time': float,
                'details': List[Dict]
            }
        """
        start_time = time.time()
        
        print(f"\n{'='*60}")
        print(f"🤖 스마트 매수 시작: {ticker}")
        print(f"   투자금: {total_amount:,.0f}원")
        print(f"   시나리오: #{scenario_id}")
        print(f"   신뢰도: {confidence:.1f}%")
        print(f"   변동성: {volatility:.2f}%")
        print(f"{'='*60}")
        
        # 1. 호가창 분석
        orderbook_analysis = self.orderbook_analyzer.analyze_order_book(ticker)
        print(f"\n📊 호가창 분석:")
        print(f"   유동성: {orderbook_analysis['liquidity_score']:.1f}점")
        print(f"   스프레드: {orderbook_analysis['bid_ask_spread']:.3f}%")
        print(f"   슬리피지 위험: {orderbook_analysis['slippage_risk']}")
        
        # 실행 가능 여부 확인
        order_decision = self.orderbook_analyzer.should_execute_order(
            ticker, total_amount, "BUY"
        )
        
        if not order_decision['should_execute']:
            print(f"\n❌ 주문 취소: {order_decision['reason']}")
            return {
                'success': False,
                'executed_amount': 0.0,
                'avg_price': 0.0,
                'splits_executed': 0,
                'total_splits': 0,
                'execution_time': time.time() - start_time,
                'details': [],
                'reason': order_decision['reason']
            }
        
        # 2. 분할 전략 선택
        split_plan = self.split_strategies.select_buy_strategy(
            scenario_id=scenario_id,
            confidence=confidence,
            volatility=volatility,
            available_capital=total_amount
        )
        
        print(f"\n📋 분할 전략: {split_plan['strategy_name']}")
        print(f"   분할 수: {split_plan['splits']}회")
        print(f"   사유: {split_plan['use_case']}")
        
        # 3. 단계별 주문 실행
        execution_details = []
        total_executed_amount = 0.0
        total_executed_quantity = 0.0
        
        for i, (amount, interval) in enumerate(zip(split_plan['amounts'], split_plan['intervals'])):
            if i > 0:
                print(f"\n⏳ {interval}초 대기 중...")
                time.sleep(interval)
            
            # 개별 주문 실행
            order_result = self._execute_single_order(
                ticker=ticker,
                amount=amount,
                action="BUY",
                order_type=order_decision['order_type'],
                limit_price=order_decision.get('price', 0.0),
                split_index=i + 1,
                total_splits=split_plan['splits']
            )
            
            execution_details.append(order_result)
            
            if order_result['success']:
                total_executed_amount += order_result['executed_amount']
                total_executed_quantity += order_result['quantity']
        
        # 평균 매수가 계산
        avg_price = total_executed_amount / total_executed_quantity if total_executed_quantity > 0 else 0.0
        
        execution_time = time.time() - start_time
        
        result = {
            'success': total_executed_quantity > 0,
            'executed_amount': total_executed_amount,
            'avg_price': avg_price,
            'quantity': total_executed_quantity,
            'splits_executed': sum(1 for d in execution_details if d['success']),
            'total_splits': split_plan['splits'],
            'execution_time': execution_time,
            'details': execution_details,
            'strategy': split_plan['strategy_name'],
            'scenario_id': scenario_id,
            'timestamp': datetime.now()
        }
        
        # 히스토리 저장
        self.execution_history.append(result)
        
        print(f"\n{'='*60}")
        print(f"✅ 매수 완료!")
        print(f"   평균가: {avg_price:,.0f}원")
        print(f"   수량: {total_executed_quantity:.6f}")
        print(f"   실행 시간: {execution_time:.1f}초")
        print(f"{'='*60}\n")
        
        return result
    
    def execute_smart_sell(
        self,
        ticker: str,
        quantity: float,
        scenario_id: int,
        profit_ratio: float,
        holding_time: int,
        strategy_name: str,
        reason: str
    ) -> Dict:
        """
        스마트 매도 실행
        
        프로세스:
        1. 호가창 분석
        2. 보유 시간 AI 검증
        3. 분할 전략 선택
        4. 단계별 매도 실행
        
        Returns:
            실행 결과
        """
        start_time = time.time()
        
        print(f"\n{'='*60}")
        print(f"🤖 스마트 매도 시작: {ticker}")
        print(f"   수량: {quantity:.6f}")
        print(f"   수익률: {profit_ratio:+.2f}%")
        print(f"   보유 시간: {holding_time}초 ({holding_time//60}분)")
        print(f"{'='*60}")
        
        # 1. 호가창 분석
        orderbook_analysis = self.orderbook_analyzer.analyze_order_book(ticker)
        print(f"\n📊 호가창 분석:")
        print(f"   유동성: {orderbook_analysis['liquidity_score']:.1f}점")
        print(f"   슬리피지 위험: {orderbook_analysis['slippage_risk']}")
        
        # 2. 보유 시간 AI 검증
        holding_prediction = self.holding_optimizer.predict_optimal_holding_time(
            scenario_id=scenario_id,
            strategy=strategy_name,
            current_profit=profit_ratio
        )
        
        should_exit, exit_reason = self.holding_optimizer.should_exit_now(
            scenario_id=scenario_id,
            strategy=strategy_name,
            current_holding_time=holding_time,
            current_profit=profit_ratio
        )
        
        print(f"\n🧠 AI 분석:")
        print(f"   최적 보유 시간: {holding_prediction['optimal_time']}초")
        print(f"   예상 수익: {holding_prediction['expected_profit']:.2f}%")
        print(f"   청산 권장: {'✅ 예' if should_exit else '❌ 아니오'}")
        print(f"   사유: {exit_reason}")
        
        # 3. 포지션 크기 계산 (원화)
        current_price = orderbook_analysis['best_bid']
        position_size = quantity * current_price
        
        # 4. 분할 전략 선택
        split_plan = self.split_strategies.select_sell_strategy(
            scenario_id=scenario_id,
            profit_ratio=profit_ratio,
            holding_time=holding_time,
            position_size=position_size
        )
        
        print(f"\n📋 분할 전략: {split_plan['strategy_name']}")
        print(f"   분할 수: {split_plan['splits']}회")
        
        # 5. 단계별 매도 실행
        execution_details = []
        total_executed_amount = 0.0
        total_executed_quantity = 0.0
        
        remaining_quantity = quantity
        
        for i, (amount_ratio, interval) in enumerate(zip(split_plan['distribution'], split_plan['intervals'])):
            if i > 0:
                print(f"\n⏳ {interval}초 대기 중...")
                time.sleep(interval)
            
            # 이번 회차 매도 수량
            current_quantity = remaining_quantity * amount_ratio
            
            # 개별 주문 실행
            order_result = self._execute_single_order(
                ticker=ticker,
                amount=current_quantity,  # 매도는 수량
                action="SELL",
                order_type="MARKET",  # 매도는 항상 시장가
                limit_price=0.0,
                split_index=i + 1,
                total_splits=split_plan['splits']
            )
            
            execution_details.append(order_result)
            
            if order_result['success']:
                total_executed_amount += order_result['executed_amount']
                total_executed_quantity += order_result['quantity']
                remaining_quantity -= order_result['quantity']
        
        # 평균 매도가 계산
        avg_price = total_executed_amount / total_executed_quantity if total_executed_quantity > 0 else 0.0
        
        execution_time = time.time() - start_time
        
        result = {
            'success': total_executed_quantity > 0,
            'executed_amount': total_executed_amount,
            'avg_price': avg_price,
            'quantity': total_executed_quantity,
            'splits_executed': sum(1 for d in execution_details if d['success']),
            'total_splits': split_plan['splits'],
            'execution_time': execution_time,
            'details': execution_details,
            'strategy': split_plan['strategy_name'],
            'profit_ratio': profit_ratio,
            'holding_time': holding_time,
            'timestamp': datetime.now()
        }
        
        # 히스토리 저장
        self.execution_history.append(result)
        
        print(f"\n{'='*60}")
        print(f"✅ 매도 완료!")
        print(f"   평균가: {avg_price:,.0f}원")
        print(f"   수량: {total_executed_quantity:.6f}")
        print(f"   실행 시간: {execution_time:.1f}초")
        print(f"{'='*60}\n")
        
        return result
    
    def _execute_single_order(
        self,
        ticker: str,
        amount: float,
        action: str,
        order_type: str,
        limit_price: float,
        split_index: int,
        total_splits: int
    ) -> Dict:
        """
        개별 주문 실행
        
        Returns:
            {
                'success': bool,
                'executed_amount': float,
                'quantity': float,
                'price': float,
                'order_type': str,
                'split_index': int
            }
        """
        print(f"\n   [{split_index}/{total_splits}] {action} 주문 실행 중...")
        
        try:
            if action == "BUY":
                # 매수: amount는 원화 금액
                if order_type == "MARKET":
                    # 시장가 매수
                    result = self.api.buy_market_order(ticker, amount)
                else:
                    # 지정가 매수 (구현 필요)
                    result = self.api.buy_limit_order(ticker, limit_price, amount / limit_price)
                
                executed_amount = amount
                quantity = result.get('executed_volume', 0.0) if result else 0.0
                price = amount / quantity if quantity > 0 else 0.0
                
            else:  # SELL
                # 매도: amount는 코인 수량
                result = self.api.sell_market_order(ticker, amount)
                
                quantity = amount
                executed_amount = result.get('executed_volume', 0.0) * result.get('price', 0.0) if result else 0.0
                price = executed_amount / quantity if quantity > 0 else 0.0
            
            success = result is not None and quantity > 0
            
            if success:
                print(f"      ✅ 성공: {quantity:.6f} @ {price:,.0f}원")
            else:
                print(f"      ❌ 실패")
            
            return {
                'success': success,
                'executed_amount': executed_amount,
                'quantity': quantity,
                'price': price,
                'order_type': order_type,
                'split_index': split_index,
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            print(f"      ❌ 오류: {e}")
            return {
                'success': False,
                'executed_amount': 0.0,
                'quantity': 0.0,
                'price': 0.0,
                'order_type': order_type,
                'split_index': split_index,
                'error': str(e),
                'timestamp': datetime.now()
            }
    
    def get_execution_summary(self) -> Dict:
        """실행 히스토리 요약"""
        if not self.execution_history:
            return {'total_executions': 0}
        
        buy_executions = [e for e in self.execution_history if 'quantity' in e and e.get('executed_amount', 0) > 0]
        sell_executions = [e for e in self.execution_history if 'profit_ratio' in e]
        
        total_buy_amount = sum(e['executed_amount'] for e in buy_executions)
        total_sell_amount = sum(e['executed_amount'] for e in sell_executions)
        
        avg_execution_time = sum(e['execution_time'] for e in self.execution_history) / len(self.execution_history)
        
        return {
            'total_executions': len(self.execution_history),
            'buy_count': len(buy_executions),
            'sell_count': len(sell_executions),
            'total_buy_amount': total_buy_amount,
            'total_sell_amount': total_sell_amount,
            'avg_execution_time': round(avg_execution_time, 2),
            'success_rate': sum(1 for e in self.execution_history if e['success']) / len(self.execution_history) * 100
        }
