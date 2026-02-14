#!/usr/bin/env python3
"""
익절/손절 매도 시스템 실제 검증 스크립트 v6.30.21
실제 포지션을 시뮬레이션하여 매도 로직 테스트
"""

import sys
import time
from datetime import datetime

# src 모듈 경로 추가
sys.path.insert(0, '/home/user/webapp')

from src.strategies.aggressive_scalping import AggressiveScalping
from src.strategies.conservative_scalping import ConservativeScalping
from src.strategies.ultra_scalping import UltraScalping

def print_header(title):
    """헤더 출력"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def test_strategy_should_exit(strategy_name, strategy, entry_price, test_cases):
    """전략별 should_exit 테스트"""
    print_header(f"{strategy_name} 전략 테스트")
    
    for i, (current_price, expected_result, description) in enumerate(test_cases, 1):
        # 손익률 계산
        profit_ratio = ((current_price - entry_price) / entry_price) * 100
        
        # 보유 시간 (임의값) - UltraScalping은 120초로 설정 (시간손실 청산 회피)
        if strategy_name == "UltraScalping":
            hold_time = 120  # 2분 (시간손실 청산 기준 180초 미만)
        else:
            hold_time = 180  # 3분
        
        # UltraScalping은 price_history, 다른 전략은 market_snapshot
        if strategy_name == "UltraScalping":
            # price_history는 None으로 전달 (스마트 로직 비활성화)
            price_history = None
            should_exit, exit_reason = strategy.should_exit(
                entry_price, 
                current_price,
                hold_time,
                price_history
            )
        else:
            # 시장 스냅샷
            market_snapshot = {
                'current_price': current_price,
                'entry_price': entry_price,
                'profit_ratio': profit_ratio
            }
            # should_exit 호출 (v6.30.21: 4개 인자 전달)
            should_exit, exit_reason = strategy.should_exit(
                entry_price, 
                current_price,
                hold_time,
                market_snapshot
            )
        
        # 결과 출력
        result_emoji = "✅" if should_exit == expected_result else "❌"
        print(f"\n{result_emoji} 테스트 케이스 #{i}: {description}")
        print(f"   진입가: {entry_price:,.0f}원 → 현재가: {current_price:,.0f}원")
        print(f"   손익률: {profit_ratio:+.2f}%")
        print(f"   보유시간: {hold_time}초")
        print(f"   예상: {'매도' if expected_result else '보유'}")
        print(f"   실제: {'매도' if should_exit else '보유'} ({exit_reason})")
        
        if should_exit != expected_result:
            print(f"   ⚠️  불일치 발견!")
            return False
    
    return True

def main():
    """메인 테스트 실행"""
    print_header("익절/손절 매도 시스템 검증 v6.30.21")
    print(f"실행 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"버전: v6.30.21-PROFIT-SELL-CRITICAL-FIX")
    print(f"수정 사항: should_exit() 4개 인자 전달 (hold_time, market_snapshot 추가)")
    
    # 전략 초기화
    aggressive_config = {
        'stop_loss': 0.01,   # 1.0%
        'take_profit': 0.015  # 1.5%
    }
    
    conservative_config = {
        'stop_loss': 0.01,   # 1.0%
        'take_profit': 0.01  # 1.0%
    }
    
    ultra_config = {
        'stop_loss': 0.008,   # 0.8%
        'take_profit': 0.015  # 1.5%
    }
    
    aggressive = AggressiveScalping(aggressive_config)
    conservative = ConservativeScalping(conservative_config)
    ultra = UltraScalping(ultra_config)
    
    # 테스트 시나리오
    entry_price = 1000  # 진입가 1,000원
    
    # AggressiveScalping 테스트
    aggressive_tests = [
        # (현재가, 예상결과, 설명)
        (1015, True, "익절 +1.5% 정확히 도달"),
        (1020, True, "익절 +2.0% 초과"),
        (990, True, "손절 -1.0% 정확히 도달"),
        (985, True, "손절 -1.5% 초과"),
        (1010, False, "익절 미달 +1.0%"),
        (995, False, "손절 미달 -0.5%"),
        (1000, False, "손익 0%"),
    ]
    
    # ConservativeScalping 테스트
    conservative_tests = [
        (1010, True, "익절 +1.0% 정확히 도달"),
        (1015, True, "익절 +1.5% 초과"),
        (990, True, "손절 -1.0% 정확히 도달"),
        (985, True, "손절 -1.5% 초과"),
        (1005, False, "익절 미달 +0.5%"),
        (995, False, "손절 미달 -0.5%"),
    ]
    
    # UltraScalping 테스트 (v6.30.21: 시간손실 청산 조건 제외)
    ultra_tests = [
        (1015, True, "익절 +1.5% 정확히 도달"),
        (1020, True, "익절 +2.0% 초과"),
        (992, True, "손절 -0.8% 정확히 도달"),
        (987, True, "손절 -1.3% 초과"),
        (1010, False, "익절 미달 +1.0%"),
        (997, False, "손절 미달 -0.3%"),
    ]
    
    # 테스트 실행
    all_passed = True
    
    all_passed &= test_strategy_should_exit(
        "AggressiveScalping",
        aggressive,
        entry_price,
        aggressive_tests
    )
    
    all_passed &= test_strategy_should_exit(
        "ConservativeScalping",
        conservative,
        entry_price,
        conservative_tests
    )
    
    all_passed &= test_strategy_should_exit(
        "UltraScalping",
        ultra,
        entry_price,
        ultra_tests
    )
    
    # 최종 결과
    print_header("최종 검증 결과")
    
    if all_passed:
        print("✅ 모든 테스트 통과!")
        print("\n주요 검증 항목:")
        print("  ✅ AggressiveScalping 익절 1.5% 작동")
        print("  ✅ AggressiveScalping 손절 -1.0% 작동")
        print("  ✅ ConservativeScalping 익절 1.0% 작동")
        print("  ✅ ConservativeScalping 손절 -1.0% 작동")
        print("  ✅ UltraScalping 익절 1.5% 작동")
        print("  ✅ UltraScalping 손절 -0.8% 작동")
        print("\n결론: v6.30.21 수정으로 익절/손절 매도 정상 작동 확인!")
        return 0
    else:
        print("❌ 일부 테스트 실패")
        print("\n추가 디버깅 필요")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
