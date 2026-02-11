"""
빠른 테스트 스크립트
설치 및 기본 기능 확인
"""

import sys
import os

# 프로젝트 루트 경로 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 50)
print("Upbit AutoProfit Bot - Quick Test")
print("=" * 50)
print()

# 1. Python 버전 확인
print("[1/6] Python 버전 확인...")
print(f"Python {sys.version}")
print()

# 2. 필수 패키지 확인
print("[2/6] 패키지 설치 확인...")
packages = [
    ('pyupbit', 'pyupbit'),
    ('pandas', 'pandas'),
    ('numpy', 'numpy'),
    ('requests', 'requests'),
    ('dotenv', 'python-dotenv'),
    ('schedule', 'schedule'),
    ('colorlog', 'colorlog'),
]

all_ok = True
for module_name, package_name in packages:
    try:
        __import__(module_name)
        print(f"  ✓ {package_name}")
    except ImportError:
        print(f"  ✗ {package_name} NOT INSTALLED")
        all_ok = False

print()

if not all_ok:
    print("[ERROR] 일부 패키지가 설치되지 않았습니다!")
    print("setup.bat을 다시 실행하세요.")
    sys.exit(1)

# 3. 설정 파일 확인
print("[3/6] 설정 파일 확인...")
if os.path.exists('.env'):
    print("  ✓ .env 파일 존재")
else:
    print("  ✗ .env 파일 없음")
    print("  setup.bat을 실행하여 .env 파일을 생성하세요.")

print()

# 4. 소스 파일 확인
print("[4/6] 소스 파일 확인...")
critical_files = [
    'src/main.py',
    'src/config.py',
    'src/upbit_api.py',
    'src/utils/risk_manager.py',
]

for filepath in critical_files:
    if os.path.exists(filepath):
        print(f"  ✓ {filepath}")
    else:
        print(f"  ✗ {filepath} 없음!")

print()

# 5. 기술지표 모듈 테스트
print("[5/6] 기술지표 모듈 테스트...")
try:
    from src.utils.technical_indicators import calculate_rsi, calculate_sma
    import pandas as pd
    import numpy as np
    
    # 테스트 데이터
    test_df = pd.DataFrame({
        'close': np.random.randint(100, 110, 20),
        'high': np.random.randint(110, 120, 20),
        'low': np.random.randint(90, 100, 20),
        'volume': np.random.randint(1000, 2000, 20)
    })
    
    rsi = calculate_rsi(test_df, period=14)
    sma = calculate_sma(test_df, period=10)
    
    print(f"  ✓ RSI 계산 성공 (마지막 값: {rsi.iloc[-1]:.2f})")
    print(f"  ✓ SMA 계산 성공 (마지막 값: {sma.iloc[-1]:.2f})")
    
except Exception as e:
    print(f"  ✗ 기술지표 모듈 오류: {e}")

print()

# 6. Config 로드 테스트
print("[6/6] Config 로드 테스트...")
try:
    from src.config import Config
    
    print(f"  ✓ TRADING_MODE: {Config.TRADING_MODE}")
    print(f"  ✓ INITIAL_CAPITAL: {Config.INITIAL_CAPITAL:,}원")
    print(f"  ✓ MAX_DAILY_LOSS: {Config.MAX_DAILY_LOSS:,}원")
    print(f"  ✓ MAX_CUMULATIVE_LOSS: {Config.MAX_CUMULATIVE_LOSS:,}원")
    print(f"  ✓ MAX_POSITIONS: {Config.MAX_POSITIONS}개")
    
except Exception as e:
    print(f"  ✗ Config 로드 오류: {e}")

print()
print("=" * 50)
print("테스트 완료!")
print("=" * 50)
print()

if all_ok:
    print("✓ 모든 기본 요구사항이 충족되었습니다!")
    print()
    print("다음 단계:")
    print("  1. run_backtest.bat - 백테스트 실행")
    print("  2. run_paper.bat - 모의투자 실행")
    print("  3. run_live.bat - 실거래 실행")
else:
    print("✗ 일부 문제가 발견되었습니다.")
    print("setup.bat을 다시 실행해주세요.")

print()
input("Press Enter to exit...")
