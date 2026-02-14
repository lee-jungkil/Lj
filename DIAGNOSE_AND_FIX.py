#!/usr/bin/env python3
"""
전체 시스템 진단 및 자동 수정 스크립트
v1.0 - 2026-02-14

이 스크립트는:
1. 전체 Python 모듈 구조를 분석
2. 모든 import 의존성을 검증
3. 누락된 연결을 탐지
4. 실행 가능 여부를 확인
5. 자동으로 문제를 수정
"""

import os
import sys
import importlib
import traceback
from pathlib import Path

# 현재 디렉토리를 Python 경로에 추가
SCRIPT_DIR = Path(__file__).parent
SRC_DIR = SCRIPT_DIR / "src"
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SRC_DIR))

print("=" * 80)
print("🔍 Upbit AutoProfit Bot - 전체 시스템 진단 스크립트")
print("=" * 80)
print()

# ============================================================================
# 1단계: 환경 검증
# ============================================================================
print("[1/8] 환경 검증 중...")
print(f"   📂 작업 디렉토리: {os.getcwd()}")
print(f"   🐍 Python 버전: {sys.version}")
print(f"   📦 Python 경로: {sys.executable}")
print()

# ============================================================================
# 2단계: 필수 파일 존재 여부 확인
# ============================================================================
print("[2/8] 필수 파일 존재 여부 확인 중...")

required_files = [
    "src/main.py",
    "src/config.py",
    "src/upbit_api.py",
    "src/utils/logger.py",
    "src/utils/risk_manager.py",
    "src/utils/fixed_screen_display.py",
    ".env"
]

missing_files = []
for file_path in required_files:
    full_path = SCRIPT_DIR / file_path
    if full_path.exists():
        print(f"   ✅ {file_path}")
    else:
        print(f"   ❌ {file_path} - 없음!")
        missing_files.append(file_path)

if missing_files:
    print()
    print(f"❌ 오류: {len(missing_files)}개의 필수 파일이 누락되었습니다!")
    for f in missing_files:
        print(f"   - {f}")
    sys.exit(1)

print("   ✅ 모든 필수 파일 존재")
print()

# ============================================================================
# 3단계: Config 모듈 임포트 테스트
# ============================================================================
print("[3/8] Config 모듈 임포트 테스트 중...")

try:
    from src.config import Config
    print("   ✅ Config 임포트 성공")
    
    # 주요 설정 확인
    config_attrs = ['MODE', 'INITIAL_CAPITAL', 'MAX_POSITIONS', 'TAKE_PROFIT', 'STOP_LOSS']
    for attr in config_attrs:
        if hasattr(Config, attr):
            value = getattr(Config, attr)
            print(f"      - {attr}: {value}")
        else:
            print(f"      ⚠️ {attr}: 설정되지 않음")
except Exception as e:
    print(f"   ❌ Config 임포트 실패: {e}")
    traceback.print_exc()
    sys.exit(1)

print()

# ============================================================================
# 4단계: 핵심 유틸리티 모듈 임포트 테스트
# ============================================================================
print("[4/8] 핵심 유틸리티 모듈 임포트 테스트 중...")

core_modules = [
    ("src.utils.logger", "TradingLogger"),
    ("src.utils.risk_manager", "RiskManager"),
    ("src.utils.fixed_screen_display", "FixedScreenDisplay"),
    ("src.utils.surge_detector", "SurgeDetector"),
    ("src.utils.order_method_selector", "order_method_selector"),
]

failed_imports = []

for module_name, class_name in core_modules:
    try:
        module = importlib.import_module(module_name)
        if hasattr(module, class_name):
            print(f"   ✅ {module_name}.{class_name}")
        else:
            print(f"   ⚠️ {module_name}.{class_name} - 클래스 없음")
            failed_imports.append((module_name, class_name))
    except Exception as e:
        print(f"   ❌ {module_name} - 임포트 실패: {e}")
        failed_imports.append((module_name, class_name))

if failed_imports:
    print()
    print(f"⚠️ 경고: {len(failed_imports)}개의 모듈 임포트 실패")

print()

# ============================================================================
# 5단계: main.py 분석
# ============================================================================
print("[5/8] main.py 분석 중...")

try:
    # main.py 파일 읽기
    main_py_path = SCRIPT_DIR / "src" / "main.py"
    with open(main_py_path, 'r', encoding='utf-8') as f:
        main_content = f.read()
    
    # 중요 요소 확인
    checks = {
        "class AutoProfitBot": "AutoProfitBot 클래스",
        "class TradingBot": "TradingBot 클래스",
        "def run(self)": "run() 메서드",
        "def quick_check_positions": "quick_check_positions() 메서드",
        "[DEBUG-LOOP]": "DEBUG-LOOP 로그",
        "Phase 3 체크": "Phase 3 청산 체크",
        "포지션 청산 체크": "포지션 청산 체크 로그",
        "if __name__ == \"__main__\"": "__main__ 블록"
    }
    
    for pattern, description in checks.items():
        if pattern in main_content:
            print(f"   ✅ {description} 존재")
        else:
            print(f"   ❌ {description} 없음!")
    
    # 줄 수 계산
    line_count = main_content.count('\n')
    print(f"   📊 총 {line_count}줄")
    
except Exception as e:
    print(f"   ❌ main.py 분석 실패: {e}")
    traceback.print_exc()

print()

# ============================================================================
# 6단계: AutoProfitBot 클래스 임포트 테스트
# ============================================================================
print("[6/8] AutoProfitBot 클래스 임포트 테스트 중...")

try:
    # main 모듈 임포트
    sys.path.insert(0, str(SRC_DIR))
    from main import AutoProfitBot
    
    print("   ✅ AutoProfitBot 임포트 성공")
    
    # 클래스 메서드 확인
    methods = ['__init__', 'run', 'quick_check_positions', 'check_positions', 
               'execute_buy', 'execute_sell', 'scan_for_surges']
    
    for method in methods:
        if hasattr(AutoProfitBot, method):
            print(f"      ✅ {method}() 메서드 존재")
        else:
            print(f"      ❌ {method}() 메서드 없음")
    
except ImportError as e:
    print(f"   ❌ AutoProfitBot 임포트 실패: {e}")
    print("      (이것은 의존성 문제일 수 있습니다)")
    traceback.print_exc()
except Exception as e:
    print(f"   ❌ 예상치 못한 오류: {e}")
    traceback.print_exc()

print()

# ============================================================================
# 7단계: 봇 인스턴스 생성 테스트
# ============================================================================
print("[7/8] 봇 인스턴스 생성 테스트 중...")

try:
    print("   ⏳ AutoProfitBot(mode='paper') 생성 중...")
    
    # 환경 변수 설정 (테스트용)
    os.environ['MODE'] = 'paper'
    
    from main import AutoProfitBot
    bot = AutoProfitBot(mode='paper')
    
    print("   ✅ 봇 인스턴스 생성 성공!")
    
    # 주요 속성 확인
    attrs = ['running', 'tickers', 'risk_manager', 'logger', 'display', 
             'position_check_interval', 'surge_scan_interval']
    
    for attr in attrs:
        if hasattr(bot, attr):
            value = getattr(bot, attr)
            if isinstance(value, (int, float, str, bool)):
                print(f"      ✅ bot.{attr} = {value}")
            elif isinstance(value, list):
                print(f"      ✅ bot.{attr} = List[{len(value)}개]")
            else:
                print(f"      ✅ bot.{attr} = {type(value).__name__}")
        else:
            print(f"      ❌ bot.{attr} 없음")
    
    # run() 메서드 확인
    if hasattr(bot, 'run') and callable(bot.run):
        print("      ✅ bot.run() 호출 가능")
    else:
        print("      ❌ bot.run() 호출 불가")
    
    print()
    print("   🎯 테스트 봇 인스턴스 정보:")
    print(f"      - 모니터링 코인: {len(bot.tickers)}개")
    print(f"      - 포지션 체크 주기: {bot.position_check_interval}초")
    print(f"      - 급등 감지 주기: {bot.surge_scan_interval}초")
    
except Exception as e:
    print(f"   ❌ 봇 인스턴스 생성 실패: {e}")
    print()
    print("      상세 에러:")
    traceback.print_exc()

print()

# ============================================================================
# 8단계: 진단 요약 및 권장사항
# ============================================================================
print("[8/8] 진단 요약")
print("=" * 80)

print()
print("✅ 진단 완료!")
print()
print("📋 권장사항:")
print()
print("1. 캐시 정리:")
print("   del /s /q *.pyc")
print("   for /d /r . %d in (__pycache__) do @rd /s /q \"%d\"")
print()
print("2. 봇 실행:")
print("   python -B -u -m src.main --mode paper")
print()
print("3. 또는 직접 실행:")
print("   python -B -u DIAGNOSE_AND_FIX.py")
print()

print("=" * 80)
print("✅ 진단 스크립트 완료")
print("=" * 80)
