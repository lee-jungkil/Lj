#!/usr/bin/env python3
"""
v6.30.29 디버깅 스크립트
Phase 3가 왜 실행되지 않는지 완전 분석
"""

import sys
import time
from datetime import datetime

sys.path.insert(0, '/home/user/webapp')

print("=" * 80)
print("🔍 v6.30.29 Phase 3 미실행 원인 분석")
print("=" * 80)

# ============================================================================
# Test 1: 코드 라인 확인
# ============================================================================
print("\n[Test 1] src/main.py Line 2142-2169 코드 확인")
print("=" * 80)

with open('/home/user/webapp/src/main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Line 2142-2144 확인
target_lines = {
    2142: '# ⭐ PHASE 3',
    2143: 'if current_time - self.last_position_check_time >= self.position_check_interval:',
    2144: 'if self.risk_manager.positions:',
    2169: 'self.last_position_check_time = current_time'
}

all_correct = True
for line_num, expected_substr in target_lines.items():
    actual_line = lines[line_num - 1].strip()
    
    if expected_substr in actual_line:
        print(f"✅ Line {line_num}: 정상")
        print(f"   {actual_line[:80]}...")
    else:
        print(f"❌ Line {line_num}: 오류!")
        print(f"   예상: {expected_substr}")
        print(f"   실제: {actual_line[:80]}")
        all_correct = False

if all_correct:
    print("\n✅ 코드가 정상적으로 수정되어 있습니다!")
else:
    print("\n❌ 코드가 올바르지 않습니다! git pull 필요")
    sys.exit(1)

# ============================================================================
# Test 2: Phase 3 실행 로직 시뮬레이션
# ============================================================================
print("\n[Test 2] Phase 3 실행 로직 시뮬레이션")
print("=" * 80)

class MockRiskManager:
    def __init__(self):
        self.positions = {
            'KRW-KITE': 'pos1',
            'KRW-BIRB': 'pos2'
        }

position_check_interval = 3
last_position_check_time = 0
risk_manager = MockRiskManager()

print(f"초기 상태:")
print(f"  position_check_interval: {position_check_interval}")
print(f"  last_position_check_time: {last_position_check_time}")
print(f"  포지션 개수: {len(risk_manager.positions)}")

print(f"\n10초 시뮬레이션:")
start = time.time()
quick_check_count = 0

for i in range(20):  # 0.5초씩 20번 = 10초
    current_time = time.time()
    elapsed = current_time - start
    
    # v6.30.29 로직
    if current_time - last_position_check_time >= position_check_interval:
        if risk_manager.positions:
            quick_check_count += 1
            print(f"[{elapsed:.1f}s] ⚡ 청산 체크 #{quick_check_count}")
            last_position_check_time = current_time
    
    time.sleep(0.5)

print(f"\n실행 횟수: {quick_check_count}회")
if quick_check_count >= 2:
    print("✅ Phase 3 로직 정상 작동!")
else:
    print("❌ Phase 3 로직 문제 있음!")

# ============================================================================
# Test 3: 실제 봇 메인 루프 구조 분석
# ============================================================================
print("\n[Test 3] 메인 루프 구조 분석")
print("=" * 80)

# 메인 루프 주변 코드 확인
loop_lines = list(range(2010, 2020)) + list(range(2140, 2180))

print("메인 루프 관련 코드:")
for line_num in loop_lines:
    if line_num < len(lines):
        line = lines[line_num - 1].rstrip()
        if line.strip() and not line.strip().startswith('#'):
            print(f"{line_num:4d}: {line[:100]}")

# ============================================================================
# Test 4: 가능한 문제점 분석
# ============================================================================
print("\n[Test 4] 가능한 문제점 분석")
print("=" * 80)

problems = []

# 문제 1: Phase 3가 else 블록 안에 있는지 확인
if 'else:' in lines[2171]:  # Line 2172 근처
    problems.append("⚠️  Phase 3가 else 블록 안에 있을 수 있음")

# 문제 2: while True 루프 확인
while_found = False
for i in range(2000, 2100):
    if i < len(lines) and 'while True:' in lines[i]:
        while_found = True
        print(f"✅ while True 루프 발견: Line {i+1}")
        break

if not while_found:
    problems.append("❌ while True 루프를 찾을 수 없음")

# 문제 3: Phase 3 들여쓰기 확인
phase3_indent = len(lines[2142]) - len(lines[2142].lstrip())
print(f"\nPhase 3 들여쓰기 레벨: {phase3_indent // 4}단계")

if problems:
    print("\n⚠️  발견된 잠재적 문제:")
    for p in problems:
        print(f"   {p}")
else:
    print("\n✅ 구조적 문제 없음")

# ============================================================================
# 최종 진단
# ============================================================================
print("\n" + "=" * 80)
print("🎯 최종 진단")
print("=" * 80)

diagnoses = []

if all_correct:
    diagnoses.append("✅ 코드가 v6.30.29로 정상 업데이트됨")
else:
    diagnoses.append("❌ 코드 업데이트 필요 (git pull)")

if quick_check_count >= 2:
    diagnoses.append("✅ Phase 3 로직이 정상적으로 작동함")
else:
    diagnoses.append("❌ Phase 3 로직에 문제 있음")

for d in diagnoses:
    print(d)

print("\n" + "=" * 80)
print("💡 권장 조치 사항")
print("=" * 80)

print("""
1. Python 캐시 완전 삭제:
   for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"
   del /s /q *.pyc

2. 코드 강제 업데이트:
   git reset --hard HEAD
   git pull origin main --force

3. 버전 확인:
   type VERSION.txt
   → v6.30.29-POSITION-CHECK-INTERVAL-FIX 확인

4. 봇 완전 재시작:
   taskkill /F /IM python.exe
   RUN_PAPER_CLEAN.bat

5. 로그 모니터링 (3초 간격으로 출력되어야 함):
   ⚡ 포지션 청산 체크 #N
   🔍 quick_check_positions 실행 - 포지션 X개

6. 만약 여전히 로그가 안 나오면:
   - 포지션이 실제로 있는지 확인
   - 로그 파일 직접 확인: trading_logs\\trading_2026-02-14.log
   - 콘솔에 에러 메시지 있는지 확인
""")

print("=" * 80)
print("테스트 완료")
print("=" * 80)
