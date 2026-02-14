#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
직접 실행 스크립트 - 모든 캐시 및 경로 문제 우회
v1.0 - 2026-02-14

이 스크립트는:
1. Python 캐시를 무시
2. 올바른 경로 설정
3. AutoProfitBot을 직접 임포트하고 실행
4. DEBUG 로그 강제 활성화
"""

import os
import sys
from pathlib import Path

# 스크립트 디렉토리
SCRIPT_DIR = Path(__file__).parent.resolve()
SRC_DIR = SCRIPT_DIR / "src"

# Python 경로 설정 (최우선)
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SRC_DIR))

# 캐시 무시 플래그
sys.dont_write_bytecode = True

print("=" * 80)
print("🚀 Upbit AutoProfit Bot - 직접 실행 스크립트")
print("=" * 80)
print()

# 환경 정보 출력
print("📋 환경 정보:")
print(f"   - 작업 디렉토리: {os.getcwd()}")
print(f"   - 스크립트 위치: {SCRIPT_DIR}")
print(f"   - Python 버전: {sys.version.split()[0]}")
print(f"   - Python 경로: {sys.executable}")
print()

# src 디렉토리 확인
if not SRC_DIR.exists():
    print(f"❌ 오류: src 디렉토리가 없습니다: {SRC_DIR}")
    print()
    print("현재 디렉토리로 이동하세요:")
    print("   cd C:\\Users\\admin\\Downloads\\Lj-FRESH\\Lj-main")
    sys.exit(1)

# main.py 확인
main_py_path = SRC_DIR / "main.py"
if not main_py_path.exists():
    print(f"❌ 오류: main.py가 없습니다: {main_py_path}")
    sys.exit(1)

print("✅ 필수 파일 확인 완료")
print()

# 모드 설정
mode = 'paper'
if len(sys.argv) > 1:
    if sys.argv[1] in ['paper', 'live', 'backtest']:
        mode = sys.argv[1]

print(f"🎯 실행 모드: {mode.upper()}")
print()

# 환경 변수 설정
os.environ['MODE'] = mode
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
os.environ['PYTHONUNBUFFERED'] = '1'

print("⏳ 봇 모듈 임포트 중...")
print()

try:
    # main 모듈 임포트
    import main as bot_module
    
    # AutoProfitBot 클래스 확인
    if not hasattr(bot_module, 'AutoProfitBot'):
        print("❌ 오류: AutoProfitBot 클래스를 찾을 수 없습니다!")
        print()
        print("main.py에 다음 클래스가 있는지 확인하세요:")
        print("   class AutoProfitBot:")
        sys.exit(1)
    
    print("✅ AutoProfitBot 클래스 임포트 성공")
    print()
    
    # 봇 인스턴스 생성
    print(f"🤖 봇 인스턴스 생성 중 (mode={mode})...")
    bot = bot_module.AutoProfitBot(mode=mode)
    
    print("✅ 봇 생성 완료")
    print()
    
    # 봇 정보 출력
    print("📊 봇 설정:")
    print(f"   - 모니터링 코인: {len(bot.tickers)}개")
    print(f"   - 포지션 체크 주기: {bot.position_check_interval}초")
    print(f"   - 급등 감지 주기: {bot.surge_scan_interval}초")
    print(f"   - 전체 스캔 주기: {bot.full_scan_interval}초")
    print()
    
    # 실행 전 메시지
    print("=" * 80)
    print("🟢 봇 실행 시작!")
    print("=" * 80)
    print()
    print("📺 예상 로그 출력:")
    print("   - [DEBUG-LOOP] 메인 루프 #N 시작")
    print("   - [DEBUG] Phase 3 체크 - 포지션 체크")
    print("   - ⚡ 포지션 청산 체크 (포지션이 있을 때)")
    print()
    print("⏹️  중지하려면 Ctrl+C를 누르세요")
    print()
    print("=" * 80)
    print()
    
    # 봇 실행
    bot.run()

except KeyboardInterrupt:
    print()
    print()
    print("=" * 80)
    print("⏹️  사용자에 의해 중지됨")
    print("=" * 80)

except ImportError as e:
    print(f"❌ 모듈 임포트 오류: {e}")
    print()
    print("가능한 원인:")
    print("   1. 필수 패키지가 설치되지 않음")
    print("   2. .env 파일이 없거나 잘못됨")
    print("   3. Python 경로 문제")
    print()
    print("해결 방법:")
    print("   1. pip install -r requirements.txt")
    print("   2. .env 파일 확인")
    print("   3. 현재 디렉토리 확인")
    
    import traceback
    traceback.print_exc()
    sys.exit(1)

except Exception as e:
    print(f"❌ 예상치 못한 오류: {e}")
    print()
    
    import traceback
    traceback.print_exc()
    sys.exit(1)

finally:
    print()
    print("=" * 80)
    print("👋 봇 종료")
    print("=" * 80)
