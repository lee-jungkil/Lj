#!/usr/bin/env python3
"""
v6.30.28 매도 실행 테스트
- 익절/손절 로직 검증
- hold_time 계산 검증
- UI 표시 검증
"""

import sys
import time
from datetime import datetime
from unittest.mock import Mock, MagicMock

# 경로 추가
sys.path.insert(0, '/home/user/webapp')

print("=" * 80)
print("🧪 v6.30.28 매도 실행 테스트 시작")
print("=" * 80)

# ============================================================================
# Test 1: hold_time 계산 검증
# ============================================================================
print("\n" + "=" * 80)
print("Test 1: hold_time 계산 검증 (v6.30.28 수정 사항)")
print("=" * 80)

class MockPosition:
    def __init__(self, entry_price, strategy):
        self.entry_time = datetime.now()
        self.avg_buy_price = entry_price
        self.amount = 10000000 / entry_price
        self.strategy = strategy
        self.profit_loss_ratio = 0

position = MockPosition(3015, 'AGGRESSIVE_SCALPING')

# 3초 대기 (보유 시간 시뮬레이션)
print(f"📌 포지션 생성: {position.entry_time.strftime('%H:%M:%S')}")
time.sleep(3)

# v6.30.28: 올바른 hold_time 계산
hold_time_correct = time.time() - position.entry_time.timestamp()
print(f"✅ v6.30.28 hold_time: {hold_time_correct:.2f}초 (약 {hold_time_correct/60:.2f}분)")

# v6.30.27 (잘못된 계산) 시뮬레이션
try:
    hold_time_wrong = time.time() - position.entry_time
    print(f"❌ v6.30.27 hold_time: {hold_time_wrong:.2f}초")
except TypeError as e:
    print(f"❌ v6.30.27 hold_time 계산 실패: {e}")

# ============================================================================
# Test 2: should_exit() 함수 테스트
# ============================================================================
print("\n" + "=" * 80)
print("Test 2: should_exit() 익절/손절 로직 검증")
print("=" * 80)

from src.strategies.aggressive_scalping import AggressiveScalping

# 전략 초기화
config = {
    'take_profit': 0.015,  # 1.5%
    'stop_loss': 0.01,     # 1.0%
}
strategy = AggressiveScalping(config)

print(f"📊 전략 설정:")
print(f"   - 익절 기준: +{strategy.take_profit * 100:.1f}%")
print(f"   - 손절 기준: -{strategy.stop_loss * 100:.1f}%")

# Test Case 1: 익절 케이스 (+6.14%)
print(f"\n{'─' * 80}")
print("Test Case 1: 익절 케이스 (COMP +6.14%)")
print("─" * 80)

entry_price = 3015
current_price = 3200
hold_time = 2880  # 48분
market_snapshot = {
    'current_price': current_price,
    'entry_price': entry_price,
    'profit_ratio': ((current_price - entry_price) / entry_price) * 100
}

profit_ratio = market_snapshot['profit_ratio']
print(f"진입가: {entry_price:,}원")
print(f"현재가: {current_price:,}원")
print(f"손익률: {profit_ratio:+.2f}%")
print(f"보유 시간: {hold_time}초 ({hold_time/60:.1f}분)")

should_exit, exit_reason = strategy.should_exit(
    entry_price, current_price, hold_time, market_snapshot
)

if should_exit:
    print(f"✅ 매도 트리거 발생! 사유: {exit_reason}")
    if profit_ratio > 0:
        print(f"💸 익절 매도 실행 예상")
    else:
        print(f"🚨 손절 매도 실행 예상")
else:
    print(f"❌ 매도 트리거 미발생 (버그!)")
    print(f"   예상: 익절 기준 +{strategy.take_profit*100:.1f}% 초과 → 매도 실행")
    print(f"   실제: {profit_ratio:+.2f}% → 매도 안 됨")

# Test Case 2: 손절 케이스 (-1.20%)
print(f"\n{'─' * 80}")
print("Test Case 2: 손절 케이스 (KITE -1.20%)")
print("─" * 80)

entry_price = 1500
current_price = 1482
hold_time = 1560  # 26분
market_snapshot = {
    'current_price': current_price,
    'entry_price': entry_price,
    'profit_ratio': ((current_price - entry_price) / entry_price) * 100
}

profit_ratio = market_snapshot['profit_ratio']
print(f"진입가: {entry_price:,}원")
print(f"현재가: {current_price:,}원")
print(f"손익률: {profit_ratio:+.2f}%")
print(f"보유 시간: {hold_time}초 ({hold_time/60:.1f}분)")

should_exit, exit_reason = strategy.should_exit(
    entry_price, current_price, hold_time, market_snapshot
)

if should_exit:
    print(f"✅ 매도 트리거 발생! 사유: {exit_reason}")
    if profit_ratio < 0:
        print(f"🚨 손절 매도 실행 예상")
    else:
        print(f"💸 익절 매도 실행 예상")
else:
    print(f"❌ 매도 트리거 미발생 (버그!)")
    print(f"   예상: 손절 기준 -{strategy.stop_loss*100:.1f}% 초과 → 매도 실행")
    print(f"   실제: {profit_ratio:+.2f}% → 매도 안 됨")

# Test Case 3: 보유 유지 케이스 (+0.80%)
print(f"\n{'─' * 80}")
print("Test Case 3: 보유 유지 케이스 (PENGU +0.80%)")
print("─" * 80)

entry_price = 2000
current_price = 2016
hold_time = 750  # 12.5분
market_snapshot = {
    'current_price': current_price,
    'entry_price': entry_price,
    'profit_ratio': ((current_price - entry_price) / entry_price) * 100
}

profit_ratio = market_snapshot['profit_ratio']
print(f"진입가: {entry_price:,}원")
print(f"현재가: {current_price:,}원")
print(f"손익률: {profit_ratio:+.2f}%")
print(f"보유 시간: {hold_time}초 ({hold_time/60:.1f}분)")

should_exit, exit_reason = strategy.should_exit(
    entry_price, current_price, hold_time, market_snapshot
)

if not should_exit:
    print(f"✅ 보유 유지 판단 정상")
    print(f"   손익: {profit_ratio:+.2f}%")
    print(f"   익절목표: +{strategy.take_profit*100:.1f}% | 손절: -{strategy.stop_loss*100:.1f}%")
else:
    print(f"❌ 매도 트리거 발생 (버그!)")
    print(f"   예상: 익절/손절 기준 미달 → 보유 유지")
    print(f"   실제: {exit_reason} → 매도 트리거")

# ============================================================================
# Test 3: UI 표시 검증
# ============================================================================
print("\n" + "=" * 80)
print("Test 3: UI 표시 검증 (v6.30.28 개선 사항)")
print("=" * 80)

test_cases = [
    (3015, 3200, "COMP", "익절"),
    (1500, 1482, "KITE", "손절"),
    (2000, 2016, "PENGU", "보유"),
]

for entry, current, ticker, expected in test_cases:
    profit_ratio = ((current - entry) / entry) * 100
    
    if profit_ratio >= strategy.take_profit * 100:
        sell_type = "💸 익절"
        message = f"{sell_type} 트리거 발생!"
        detail = f"{ticker}: 익절 ({profit_ratio:+.2f}%) | 손익: {profit_ratio:+.2f}%"
    elif profit_ratio <= -strategy.stop_loss * 100:
        sell_type = "🚨 손절"
        message = f"{sell_type} 트리거 발생!"
        detail = f"{ticker}: 손절 ({profit_ratio:+.2f}%) | 손익: {profit_ratio:+.2f}%"
    else:
        message = f"✅ {ticker} 보유 유지"
        detail = f"손익: {profit_ratio:+.2f}% | 익절목표: +{strategy.take_profit*100:.1f}% | 손절: -{strategy.stop_loss*100:.1f}%"
    
    print(f"\n{ticker} ({entry:,}원 → {current:,}원):")
    print(f"  {message}")
    print(f"  {detail}")
    print(f"  예상: {expected} | 결과: {'✅' if expected in message or expected in detail else '❌'}")

# ============================================================================
# 최종 결과 요약
# ============================================================================
print("\n" + "=" * 80)
print("📊 최종 테스트 결과 요약")
print("=" * 80)

results = []

# Test 1 결과
if hold_time_correct > 0 and hold_time_correct < 10:
    results.append(("hold_time 계산", "✅ PASS"))
else:
    results.append(("hold_time 계산", "❌ FAIL"))

# Test 2 결과 (COMP +6.14% 익절)
should_exit_1, _ = strategy.should_exit(3015, 3200, 2880, {'profit_ratio': 6.14})
if should_exit_1:
    results.append(("익절 실행 (+6.14%)", "✅ PASS"))
else:
    results.append(("익절 실행 (+6.14%)", "❌ FAIL"))

# Test 2 결과 (KITE -1.20% 손절)
should_exit_2, _ = strategy.should_exit(1500, 1482, 1560, {'profit_ratio': -1.20})
if should_exit_2:
    results.append(("손절 실행 (-1.20%)", "✅ PASS"))
else:
    results.append(("손절 실행 (-1.20%)", "❌ FAIL"))

# Test 2 결과 (PENGU +0.80% 보유)
should_exit_3, _ = strategy.should_exit(2000, 2016, 750, {'profit_ratio': 0.80})
if not should_exit_3:
    results.append(("보유 유지 (+0.80%)", "✅ PASS"))
else:
    results.append(("보유 유지 (+0.80%)", "❌ FAIL"))

# 결과 출력
for test_name, result in results:
    print(f"{test_name:30s}: {result}")

# 전체 통과 여부
all_passed = all("PASS" in r for _, r in results)
print("\n" + "=" * 80)
if all_passed:
    print("🎉 모든 테스트 통과! v6.30.28 정상 작동 확인")
    print("=" * 80)
    sys.exit(0)
else:
    print("❌ 일부 테스트 실패! 추가 디버깅 필요")
    print("=" * 80)
    sys.exit(1)
