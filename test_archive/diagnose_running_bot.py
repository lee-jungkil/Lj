#!/usr/bin/env python3
"""
실행 중인 봇의 Phase 3 로직 실시간 진단
포지션이 있는데 청산 체크가 안 되는 이유를 찾습니다
"""

import sys
import time
import os
from datetime import datetime

# 경로 추가
sys.path.insert(0, '/home/user/webapp')

def check_bot_state():
    """실행 중인 봇의 상태 체크"""
    
    print("=" * 80)
    print("🔍 실행 중인 봇 상태 진단")
    print("=" * 80)
    print()
    
    # 1. 로그 파일 확인
    print("[1/5] 로그 파일 확인...")
    log_dir = "/home/user/webapp/trading_logs"
    today = datetime.now().strftime("%Y%m%d")
    log_file = f"{log_dir}/trading_{today}.log"
    
    if os.path.exists(log_file):
        print(f"   OK: 로그 파일 존재 - {log_file}")
        
        # 최근 로그 확인
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            recent_lines = lines[-50:] if len(lines) > 50 else lines
            
            # "⚡ 포지션 청산 체크" 검색
            check_logs = [l for l in recent_lines if "포지션 청산 체크" in l or "Position liquidation check" in l]
            if check_logs:
                print(f"   ✅ 청산 체크 로그 발견: {len(check_logs)}건")
                print(f"   마지막 청산 체크: {check_logs[-1].strip()}")
            else:
                print(f"   ❌ 청산 체크 로그 없음!")
                print(f"   최근 로그 {len(recent_lines)}줄 중 청산 체크 없음")
            
            # "매수" 로그 검색
            buy_logs = [l for l in recent_lines if "매수" in l or "BUY" in l]
            if buy_logs:
                print(f"   📊 매수 로그: {len(buy_logs)}건")
                print(f"   마지막 매수: {buy_logs[-1].strip()}")
            
            # "PHASE 3" 로그 검색
            phase3_logs = [l for l in recent_lines if "PHASE 3" in l]
            if phase3_logs:
                print(f"   ✅ PHASE 3 로그: {len(phase3_logs)}건")
            else:
                print(f"   ❌ PHASE 3 로그 없음!")
    else:
        print(f"   ❌ 로그 파일 없음: {log_file}")
    print()
    
    # 2. main.py Phase 3 코드 확인
    print("[2/5] main.py Phase 3 코드 확인...")
    main_py = "/home/user/webapp/src/main.py"
    with open(main_py, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Line 2143 확인
    if len(lines) > 2142:
        line_2143 = lines[2142].strip()
        if "current_time - self.last_position_check_time >= self.position_check_interval" in line_2143:
            print("   ✅ Line 2143: Phase 3 시간 체크 로직 존재")
        else:
            print(f"   ❌ Line 2143: Phase 3 시간 체크 로직 없음!")
            print(f"   실제 코드: {line_2143}")
    
    # Line 2144 확인
    if len(lines) > 2143:
        line_2144 = lines[2143].strip()
        if "if self.risk_manager.positions:" in line_2144:
            print("   ✅ Line 2144: 포지션 확인 로직 존재")
        else:
            print(f"   ❌ Line 2144: 포지션 확인 로직 이상!")
            print(f"   실제 코드: {line_2144}")
    
    # Line 2160 확인 (로그 출력)
    if len(lines) > 2159:
        line_2160 = lines[2159].strip()
        if "포지션 청산 체크" in line_2160:
            print("   ✅ Line 2160: 청산 체크 로그 출력 코드 존재")
        else:
            print(f"   ⚠️  Line 2160: 로그 출력 코드 다름")
            print(f"   실제 코드: {line_2160}")
    
    # Line 2169 확인 (시간 업데이트)
    if len(lines) > 2168:
        line_2169 = lines[2168].strip()
        if "self.last_position_check_time = current_time" in line_2169:
            print("   ✅ Line 2169: 마지막 체크 시간 업데이트 코드 존재")
        else:
            print(f"   ❌ Line 2169: 시간 업데이트 코드 없음!")
            print(f"   실제 코드: {line_2169}")
    print()
    
    # 3. __init__ 메서드에서 변수 초기화 확인
    print("[3/5] 변수 초기화 확인...")
    init_found = False
    for i, line in enumerate(lines, 1):
        if "self.last_position_check_time = 0" in line:
            print(f"   ✅ Line {i}: last_position_check_time 초기화 확인")
            init_found = True
            break
    
    if not init_found:
        print("   ❌ last_position_check_time 초기화 코드 없음!")
    
    interval_found = False
    for i, line in enumerate(lines, 1):
        if "self.position_check_interval" in line and "=" in line:
            print(f"   ✅ Line {i}: position_check_interval 설정 확인")
            interval_found = True
            break
    
    if not interval_found:
        print("   ❌ position_check_interval 설정 코드 없음!")
    print()
    
    # 4. Python 캐시 확인
    print("[4/5] Python 캐시 확인...")
    cache_files = []
    for root, dirs, files in os.walk("/home/user/webapp"):
        for d in dirs:
            if d == "__pycache__":
                cache_path = os.path.join(root, d)
                cache_files.append(cache_path)
    
    if cache_files:
        print(f"   ⚠️  캐시 폴더 발견: {len(cache_files)}개")
        for cache in cache_files[:5]:
            print(f"      - {cache}")
        if len(cache_files) > 5:
            print(f"      ... 외 {len(cache_files) - 5}개")
        print("   ⚠️  캐시 삭제 필요!")
    else:
        print("   ✅ 캐시 폴더 없음")
    print()
    
    # 5. 루프 구조 확인
    print("[5/5] 메인 루프 구조 확인...")
    
    # while self.running: 찾기
    while_found = False
    phase3_found = False
    
    for i, line in enumerate(lines, 1):
        if "while self.running:" in line or "while True:" in line:
            while_found = True
            print(f"   ✅ Line {i}: 메인 루프 시작 확인")
            
            # 이후 100줄 내에서 Phase 3 확인
            for j in range(i, min(i + 500, len(lines))):
                if "PHASE 3" in lines[j] or "포지션 청산 체크" in lines[j]:
                    phase3_found = True
                    print(f"   ✅ Line {j+1}: Phase 3 코드 메인 루프 내 존재")
                    break
            break
    
    if not while_found:
        print("   ❌ 메인 루프를 찾을 수 없음!")
    
    if not phase3_found:
        print("   ❌ Phase 3 코드가 메인 루프 안에 없음!")
    print()
    
    # 최종 진단
    print("=" * 80)
    print("📊 최종 진단")
    print("=" * 80)
    
    issues = []
    
    # 로그 파일 체크
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if "포지션 청산 체크" not in content and "Position liquidation check" not in content:
                issues.append("❌ 청산 체크 로그가 로그 파일에 전혀 없음")
    
    # 코드 체크
    if len(lines) > 2142:
        if "current_time - self.last_position_check_time" not in lines[2142]:
            issues.append("❌ Phase 3 시간 체크 코드 없음 (Line 2143)")
    
    if len(lines) > 2168:
        if "self.last_position_check_time = current_time" not in lines[2168]:
            issues.append("❌ 시간 업데이트 코드 없음 (Line 2169)")
    
    # 캐시 체크
    if cache_files:
        issues.append(f"⚠️  Python 캐시 {len(cache_files)}개 발견 - 삭제 필요")
    
    # 변수 초기화 체크
    if not init_found:
        issues.append("❌ last_position_check_time 초기화 코드 없음")
    
    if not interval_found:
        issues.append("❌ position_check_interval 설정 코드 없음")
    
    # 결과 출력
    if issues:
        print()
        print("발견된 문제:")
        for issue in issues:
            print(f"   {issue}")
        print()
        print("=" * 80)
        print("🔧 해결 방법")
        print("=" * 80)
        print()
        
        if any("캐시" in i for i in issues):
            print("1. Python 캐시 삭제:")
            print("   cd C:\\Users\\admin\\Downloads\\Lj-main\\Lj-main")
            print("   for /d /r . %d in (__pycache__) do @rd /s /q \"%d\"")
            print("   del /s /q *.pyc")
            print()
        
        if any("Line" in i for i in issues):
            print("2. 최신 코드 받기:")
            print("   git pull origin main")
            print()
        
        print("3. 봇 재시작:")
        print("   RUN_PAPER_CLEAN.bat")
        print()
    else:
        print()
        print("✅ 코드 상태: 모두 정상")
        print()
        print("코드는 정상인데 로그가 안 나온다면:")
        print("   1. 봇이 실제로 실행 중인지 확인")
        print("   2. 포지션이 실제로 있는지 확인")
        print("   3. Python 캐시 문제 (SIMPLE_FIX.bat 실행)")
        print()
    
    print("=" * 80)

if __name__ == "__main__":
    try:
        check_bot_state()
    except Exception as e:
        print(f"\n❌ 진단 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
