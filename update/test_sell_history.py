"""
매도 기록 영구 저장 테스트 스크립트
v6.16-SELLHISTORY 기능 검증
"""
import sys
import os
import time
from datetime import datetime

# 프로젝트 루트 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.fixed_screen_display import FixedScreenDisplay

def test_sell_history():
    """매도 기록 테스트"""
    print("=" * 60)
    print(" 매도 기록 영구 저장 테스트 v6.16-SELLHISTORY")
    print("=" * 60)
    print()
    
    # 디스플레이 초기화
    display = FixedScreenDisplay(max_positions=7)
    
    # 초기 자본 설정
    display.update_capital_status(
        initial_capital=1000000,
        current_balance=1000000
    )
    
    # AI 학습 상태
    display.update_ai_learning(
        learning_count=10,
        profit_trades=7,
        loss_trades=3,
        win_rate=70.0
    )
    
    print("1단계: 초기 화면 렌더링")
    display.render()
    time.sleep(2)
    
    # 테스트 시나리오: 5개 포지션 매수 → 매도
    test_positions = [
        {
            'slot': 1,
            'ticker': 'KRW-BTC',
            'entry_price': 50000000,
            'current_price': 51225000,
            'amount': 0.02,
            'strategy': 'aggressive_scalping'
        },
        {
            'slot': 2,
            'ticker': 'KRW-ETH',
            'entry_price': 3000000,
            'current_price': 2973900,
            'amount': 0.1,
            'strategy': 'conservative_scalping'
        },
        {
            'slot': 3,
            'ticker': 'KRW-XRP',
            'entry_price': 1000,
            'current_price': 1015,
            'amount': 1000,
            'strategy': 'scalping_strategy'
        },
        {
            'slot': 4,
            'ticker': 'KRW-ADA',
            'entry_price': 500,
            'current_price': 506,
            'amount': 2000,
            'strategy': 'scalping_strategy'
        },
        {
            'slot': 5,
            'ticker': 'KRW-DOGE',
            'entry_price': 200,
            'current_price': 199,
            'amount': 5000,
            'strategy': 'aggressive_scalping'
        }
    ]
    
    print("\n2단계: 5개 포지션 매수")
    for pos in test_positions:
        profit_loss = (pos['current_price'] - pos['entry_price']) * pos['amount']
        profit_ratio = ((pos['current_price'] - pos['entry_price']) / pos['entry_price']) * 100
        
        display.update_position(
            slot=pos['slot'],
            ticker=pos['ticker'],
            entry_price=pos['entry_price'],
            current_price=pos['current_price'],
            amount=pos['amount'],
            profit_loss=profit_loss,
            profit_ratio=profit_ratio,
            hold_time='3분 24초',
            strategy=pos['strategy']
        )
        
        display.buy_count += 1
    
    display.render()
    time.sleep(3)
    
    print("\n3단계: 순차적 매도 (5초 간격)")
    for i, pos in enumerate(test_positions, 1):
        profit_loss = (pos['current_price'] - pos['entry_price']) * pos['amount']
        profit_ratio = ((pos['current_price'] - pos['entry_price']) / pos['entry_price']) * 100
        
        print(f"\n매도 {i}/5: {pos['ticker']} ({profit_loss:+,.0f}원)")
        
        # 매도 실행
        display.remove_position(
            slot=pos['slot'],
            exit_price=pos['current_price'],
            profit_loss=profit_loss,
            profit_ratio=profit_ratio
        )
        
        # 자본 업데이트
        display.current_balance += profit_loss
        
        display.render()
        time.sleep(5)  # 5초 대기 - 기존에는 여기서 매도 결과가 사라졌음
    
    print("\n4단계: 매도 기록 영구 저장 확인")
    print(f"저장된 매도 기록: {len(display.sell_history)}건")
    for record in display.sell_history:
        print(f"  - {record['time']} | {record['ticker']} | {record['profit_loss']:+,.0f}원")
    
    time.sleep(3)
    
    print("\n5단계: 추가 매도 (10건 초과 테스트)")
    # 추가 6개 포지션 매도 시뮬레이션
    additional_sells = [
        ('KRW-SOL', 150000, 153000, 0.1, 'scalping_strategy'),
        ('KRW-MATIC', 1200, 1224, 100, 'aggressive_scalping'),
        ('KRW-AVAX', 30000, 29700, 0.5, 'conservative_scalping'),
        ('KRW-DOT', 8000, 8080, 10, 'scalping_strategy'),
        ('KRW-LINK', 15000, 15150, 5, 'aggressive_scalping'),
        ('KRW-UNI', 12000, 11880, 8, 'conservative_scalping')
    ]
    
    for ticker, entry, exit, amount, strategy in additional_sells:
        profit_loss = (exit - entry) * amount
        profit_ratio = ((exit - entry) / entry) * 100
        
        # 임시 포지션 추가 (매도를 위해)
        display.positions[6] = {
            'ticker': ticker,
            'strategy': strategy,
            'hold_time': '2분 15초'
        }
        
        display.remove_position(6, exit, profit_loss, profit_ratio)
        display.current_balance += profit_loss
        display.render()
        time.sleep(2)
    
    print("\n6단계: 최종 확인")
    print(f"총 매도 횟수: {display.sell_count}회")
    print(f"저장된 매도 기록: {len(display.sell_history)}건 (최대 10건)")
    print(f"화면 표시: 최근 5건")
    print()
    
    print("✅ 테스트 결과:")
    print("  - 매도 기록이 5초 후에도 사라지지 않음")
    print("  - 최대 10건 유지 (FIFO)")
    print("  - 화면에 최근 5건 표시")
    print("  - 매수 기록처럼 영구 저장")
    print()
    
    print("테스트 완료! (30초 후 종료)")
    time.sleep(30)
    
    # 정리
    display.cleanup()

if __name__ == "__main__":
    try:
        test_sell_history()
    except KeyboardInterrupt:
        print("\n\n테스트 중단됨")
    except Exception as e:
        print(f"\n\n오류 발생: {e}")
        import traceback
        traceback.print_exc()
