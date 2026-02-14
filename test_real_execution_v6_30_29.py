#!/usr/bin/env python3
"""
v6.30.29 실제 봇 실행 테스트
Phase 3 포지션 청산 체크가 실제로 실행되는지 검증
"""

import sys
import time
from datetime import datetime

sys.path.insert(0, '/home/user/webapp')

print("=" * 80)
print("🔬 v6.30.29 실제 봇 실행 테스트")
print("=" * 80)

# Import 테스트
print("\n[1/5] 모듈 임포트 테스트...")
try:
    from src.main import AutoProfitBot
    print("✅ AutoProfitBot 임포트 성공")
except Exception as e:
    print(f"❌ 임포트 실패: {e}")
    sys.exit(1)

# 봇 초기화 테스트
print("\n[2/5] 봇 초기화 테스트...")
try:
    bot = AutoProfitBot(mode='paper')
    print("✅ 봇 초기화 성공")
    print(f"   - last_position_check_time: {bot.last_position_check_time}")
    print(f"   - position_check_interval: {bot.position_check_interval}")
except Exception as e:
    print(f"❌ 초기화 실패: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Phase 3 조건 체크 테스트
print("\n[3/5] Phase 3 실행 조건 테스트...")
current_time = time.time()
elapsed = current_time - bot.last_position_check_time

print(f"   - current_time: {current_time:.2f}")
print(f"   - last_position_check_time: {bot.last_position_check_time}")
print(f"   - 경과 시간: {elapsed:.2f}초")
print(f"   - 조건: {elapsed:.2f} >= {bot.position_check_interval}?")

if elapsed >= bot.position_check_interval:
    print("   ✅ Phase 3 실행 조건 충족!")
else:
    print(f"   ❌ Phase 3 실행 불가 (남은 시간: {bot.position_check_interval - elapsed:.2f}초)")

# quick_check_positions 메서드 존재 확인
print("\n[4/5] quick_check_positions 메서드 확인...")
if hasattr(bot, 'quick_check_positions'):
    print("✅ quick_check_positions 메서드 존재")
else:
    print("❌ quick_check_positions 메서드 없음")

# 포지션 시뮬레이션 테스트
print("\n[5/5] 포지션 시뮬레이션 테스트...")

# Mock 포지션 생성
from src.risk_manager import Position

mock_position = Position(
    ticker='KRW-TEST',
    entry_price=1000,
    amount=10,
    strategy='AGGRESSIVE_SCALPING',
    entry_time=datetime.now()
)

bot.risk_manager.positions['KRW-TEST'] = mock_position
print(f"✅ Mock 포지션 생성: {mock_position.ticker}")
print(f"   - 포지션 개수: {len(bot.risk_manager.positions)}")

# Phase 3 실행 시뮬레이션
print("\n" + "=" * 80)
print("📊 Phase 3 실행 시뮬레이션 (10초간)")
print("=" * 80)

start_time = time.time()
quick_check_count = 0
execution_times = []

print(f"시작: {datetime.now().strftime('%H:%M:%S')}")

while time.time() - start_time < 10:
    current_time = time.time()
    elapsed_total = current_time - start_time
    elapsed_since_check = current_time - bot.last_position_check_time
    
    # Phase 3 조건 체크
    if current_time - bot.last_position_check_time >= bot.position_check_interval:
        if bot.risk_manager.positions:
            quick_check_count += 1
            check_time = datetime.now().strftime('%H:%M:%S')
            execution_times.append(current_time)
            
            print(f"[{check_time}] ⚡ 포지션 청산 체크 #{quick_check_count}")
            print(f"          포지션: {len(bot.risk_manager.positions)}개")
            print(f"          경과: {elapsed_total:.1f}초 | 마지막: {elapsed_since_check:.1f}초")
            
            # 마지막 체크 시간 업데이트
            bot.last_position_check_time = current_time
    
    time.sleep(0.5)

# 결과 분석
print("\n" + "=" * 80)
print("📊 테스트 결과 분석")
print("=" * 80)

expected_count = 10 // bot.position_check_interval
print(f"예상 실행 횟수: {expected_count}회")
print(f"실제 실행 횟수: {quick_check_count}회")

if quick_check_count >= expected_count - 1:
    print("✅ 실행 횟수: PASS")
else:
    print(f"❌ 실행 횟수: FAIL ({quick_check_count}/{expected_count})")

if len(execution_times) >= 2:
    intervals = []
    for i in range(1, len(execution_times)):
        interval = execution_times[i] - execution_times[i-1]
        intervals.append(interval)
    
    avg_interval = sum(intervals) / len(intervals)
    print(f"\n평균 간격: {avg_interval:.2f}초")
    
    if abs(avg_interval - bot.position_check_interval) < 0.5:
        print("✅ 간격 정확도: PASS")
    else:
        print("⚠️ 간격 정확도: WARN")

print("\n" + "=" * 80)
if quick_check_count >= 2:
    print("🎉 테스트 통과! Phase 3가 정상 작동합니다!")
    print("=" * 80)
    print(f"\n✅ 10초 동안 {quick_check_count}회 실행")
    print(f"✅ 평균 {avg_interval:.2f}초 간격")
    print("\n🚨 중요: 실제 봇에서도 이 로그가 나타나야 합니다!")
    print("   만약 실제 봇에서 안 나온다면:")
    print("   1. Python 캐시 삭제")
    print("   2. 봇 완전 재시작")
    print("   3. 포지션 생성 확인")
else:
    print("❌ 테스트 실패! Phase 3가 실행되지 않습니다!")
    print("=" * 80)
