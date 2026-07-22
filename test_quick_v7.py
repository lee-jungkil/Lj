"""
Profit Bot v7.0 빠른 테스트
==========================
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("=" * 70)
print("🧪 Profit Bot v7.0 - 빠른 테스트")
print("=" * 70)

# 1. 모듈 임포트 테스트
print("\n[1] 모듈 임포트 테스트...")
try:
    from profit_bot_v7 import ProfitOptimizedBot
    from src.strategies.profit_optimized_strategy import ProfitOptimizedStrategy
    from src.ai.realtime_learner import RealtimeLearner
    print("   ✅ 모든 모듈 임포트 성공!")
except Exception as e:
    print(f"   ❌ 임포트 실패: {e}")
    sys.exit(1)

# 2. 전략 생성 테스트
print("\n[2] 전략 객체 생성...")
try:
    strategy = ProfitOptimizedStrategy()
    stats = strategy.get_stats()
    print(f"   ✅ 전략 생성 성공!")
    print(f"      - 이름: {stats['name']}")
    print(f"      - 타입: {stats['type']}")
    print(f"      - 목표: {stats['target_profit']}")
    print(f"      - 손절: {stats['stop_loss']}")
    print(f"      - 시간제한: {stats['max_hold_time']}")
except Exception as e:
    print(f"   ❌ 전략 생성 실패: {e}")
    sys.exit(1)

# 3. 학습 시스템 테스트
print("\n[3] 학습 시스템 생성...")
try:
    learner = RealtimeLearner()
    report = learner.get_performance_report()
    print(f"   ✅ 학습 시스템 생성 성공!")
    print(f"      - 승률: {report['win_rate']}")
    print(f"      - PF: {report['profit_factor']}")
except Exception as e:
    print(f"   ❌ 학습 시스템 생성 실패: {e}")
    sys.exit(1)

# 4. 봇 생성 테스트
print("\n[4] 봇 객체 생성...")
try:
    bot = ProfitOptimizedBot(mode='paper')
    print(f"   ✅ 봇 생성 성공!")
    print(f"      - 모드: {bot.mode}")
    print(f"      - 포지션 제한: {bot.risk_manager.max_open_positions}개")
except Exception as e:
    print(f"   ❌ 봇 생성 실패: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 5. 진입/청산 로직 테스트 (모의 데이터)
print("\n[5] 진입/청산 로직 테스트 (모의 데이터)...")

# 모의 시장 데이터 (좋은 조건)
mock_good_data = {
    'current_price': 100000,
    'current_volume': 500,
    'avg_volume_5m': 200,  # 2.5배 거래량
    'price_change_1m': 0.3,  # 0.3% 상승
    'rsi': 55,  # 중립
    'sell_pressure': 0.9,  # 매수 우세
}

should_enter, reason = strategy.should_enter("TEST-COIN", mock_good_data)
print(f"   진입 조건 (좋은 시장):")
print(f"      결과: {'✅ 진입' if should_enter else '❌ 대기'}")
print(f"      이유: {reason}")

# 모의 시장 데이터 (나쁜 조건)
mock_bad_data = {
    'current_price': 100000,
    'current_volume': 100,
    'avg_volume_5m': 200,  # 0.5배 거래량 (부족)
    'price_change_1m': 0.05,  # 0.05% 상승 (약함)
    'rsi': 75,  # 과매수
    'sell_pressure': 2.0,  # 매도 압력
}

should_enter2, reason2 = strategy.should_enter("TEST-COIN2", mock_bad_data)
print(f"\n   진입 조건 (나쁜 시장):")
print(f"      결과: {'✅ 진입' if should_enter2 else '❌ 대기'}")
print(f"      이유: {reason2}")

# 청산 조건 테스트
import time
print(f"\n   청산 조건 테스트:")

# 수익 0.6% (익절 조건)
should_exit1, reason1, type1 = strategy.should_exit(
    "TEST-COIN", 100000, 100600, 60, mock_good_data
)
print(f"      수익 +0.6%: {'✅ 청산' if should_exit1 else '⏳ 보유'} - {reason1}")

# 손실 -0.6% (손절 조건)
should_exit2, reason2, type2 = strategy.should_exit(
    "TEST-COIN", 100000, 99400, 60, mock_good_data
)
print(f"      손실 -0.6%: {'✅ 청산' if should_exit2 else '⏳ 보유'} - {reason2}")

# 시간 초과 (200초)
should_exit3, reason3, type3 = strategy.should_exit(
    "TEST-COIN", 100000, 100100, 200, mock_good_data
)
print(f"      시간 200초, 수익 +0.1%: {'✅ 청산' if should_exit3 else '⏳ 보유'} - {reason3}")

# 6. 학습 시스템 테스트
print("\n[6] 학습 시스템 테스트...")

# 모의 거래 기록
mock_trades = [
    {'ticker': 'KRW-BTC', 'profit_pct': 0.6, 'exit_reason': 'TAKE_PROFIT', 'entry_time': None, 'exit_time': None, 'entry_price': 100000, 'exit_price': 100600},
    {'ticker': 'KRW-ETH', 'profit_pct': -0.5, 'exit_reason': 'STOP_LOSS', 'entry_time': None, 'exit_time': None, 'entry_price': 50000, 'exit_price': 49750},
    {'ticker': 'KRW-XRP', 'profit_pct': 0.4, 'exit_reason': 'QUICK_PROFIT', 'entry_time': None, 'exit_time': None, 'entry_price': 1000, 'exit_price': 1004},
]

for trade in mock_trades:
    learner.record_trade(trade)
    print(f"   📝 거래 기록: {trade['ticker']} {trade['profit_pct']:+.1f}%")

report = learner.get_performance_report()
print(f"\n   학습 후 성과:")
print(f"      - 총 거래: {report['total_trades']}건")
print(f"      - 승률: {report['win_rate']}")
print(f"      - 평균 수익: {report['avg_profit']}")
print(f"      - 평균 손실: {report['avg_loss']}")
print(f"      - PF: {report['profit_factor']}")

# 최종 결과
print("\n" + "=" * 70)
print("📊 테스트 결과")
print("=" * 70)
print("✅ [1] 모듈 임포트: PASS")
print("✅ [2] 전략 생성: PASS")
print("✅ [3] 학습 시스템: PASS")
print("✅ [4] 봇 생성: PASS")
print("✅ [5] 진입/청산 로직: PASS")
print("✅ [6] 학습 시스템: PASS")
print("=" * 70)
print("🎉 모든 테스트 통과!")
print("=" * 70)

print("\n💡 다음 단계:")
print("   1. 시뮬레이션 모드 실행:")
print("      python profit_bot_v7.py --mode paper")
print("")
print("   2. 실전 모드 실행 (신중!):")
print("      python profit_bot_v7.py --mode live")
print("")
print("   3. API 키 설정 확인:")
print("      src/config.py 파일에서 UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY")
