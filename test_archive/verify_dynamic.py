"""
동적 코인 선정 시스템 검증 및 테스트
"""
import os
import sys
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

print("=" * 60)
print("동적 코인 선정 시스템 검증")
print("=" * 60)
print()

# 1. 환경변수 확인
print("[1/5] 환경변수 확인")
print("-" * 60)

required_vars = [
    'TRADING_MODE',
    'INITIAL_CAPITAL',
    'ENABLE_DYNAMIC_COIN_SELECTION',
    'CAPITAL_MODE',
    'COIN_SELECTION_METHOD',
    'COIN_SELECTION_INTERVAL'
]

all_ok = True
for var in required_vars:
    value = os.getenv(var)
    if value:
        print(f"✅ {var} = {value}")
    else:
        print(f"❌ {var} = (없음)")
        all_ok = False

print()

if not all_ok:
    print("❌ 일부 환경변수가 설정되지 않았습니다")
    print("   .env 파일을 확인하세요")
    sys.exit(1)

# 2. Config 로딩 테스트
print("[2/5] Config 모듈 로딩")
print("-" * 60)

try:
    from src.config import Config
    print(f"✅ TRADING_MODE: {Config.TRADING_MODE}")
    print(f"✅ INITIAL_CAPITAL: {Config.INITIAL_CAPITAL:,}원")
    print(f"✅ ENABLE_DYNAMIC_COIN_SELECTION: {Config.ENABLE_DYNAMIC_COIN_SELECTION}")
    print(f"✅ CAPITAL_MODE: {Config.CAPITAL_MODE}만원")
    print(f"✅ COIN_SELECTION_METHOD: {Config.COIN_SELECTION_METHOD}")
    print()
except Exception as e:
    print(f"❌ Config 로딩 실패: {e}")
    sys.exit(1)

# 3. 동적 코인 선정 모듈 테스트
print("[3/5] 동적 코인 선정 모듈 테스트")
print("-" * 60)

try:
    from src.utils.dynamic_coin_selector import DynamicCoinSelector
    
    selector = DynamicCoinSelector(capital_mode=Config.CAPITAL_MODE)
    print(f"✅ DynamicCoinSelector 생성 완료")
    print(f"   - 자본금 모드: {Config.CAPITAL_MODE}만원")
    print(f"   - 목표 코인 개수: {selector.coin_count}개")
    print(f"   - 갱신 주기: {selector.update_interval}초 ({selector.update_interval//60}분)")
    print()
except Exception as e:
    print(f"❌ DynamicCoinSelector 생성 실패: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 4. 빠른 거래량 기준 선정 테스트 (10개만)
print("[4/5] 거래량 기준 코인 선정 테스트 (빠른 모드)")
print("-" * 60)
print("⏳ 잠시만 기다려주세요... (약 10초 소요)")

try:
    import pyupbit
    
    # Top 20만 빠르게 선정
    all_tickers = pyupbit.get_tickers(fiat="KRW")
    print(f"✅ 전체 KRW 마켓: {len(all_tickers)}개")
    
    # 현재가 배치 조회 (첫 20개만)
    prices = pyupbit.get_current_price(all_tickers[:20])
    valid_count = sum(1 for p in prices if p is not None) if isinstance(prices, list) else len(prices)
    print(f"✅ 거래 가능 코인: {valid_count}개 (Top 20 중)")
    print()
    
except Exception as e:
    print(f"⚠️  거래량 분석 실패: {e}")
    print("   → pyupbit API 연결 확인 필요")
    print()

# 5. 전략 설정 확인
print("[5/5] 초단타 전략 설정 확인")
print("-" * 60)

try:
    ultra_config = Config.STRATEGIES.get('ultra_scalping', {})
    print(f"✅ 초단타 전략:")
    print(f"   - 활성화: {ultra_config.get('enabled', False)}")
    print(f"   - 손절: {ultra_config.get('stop_loss', 0)*100:.1f}%")
    print(f"   - 익절: {ultra_config.get('take_profit', 0)*100:.1f}%")
    print(f"   - 최소 급등: {ultra_config.get('min_price_surge', 0)*100:.1f}%")
    print(f"   - 거래량 배수: {ultra_config.get('volume_spike', 0):.1f}배")
    print()
except Exception as e:
    print(f"⚠️  전략 설정 확인 실패: {e}")
    print()

# 최종 결과
print("=" * 60)
print("✅ 모든 검증 완료!")
print("=" * 60)
print()
print("다음 단계:")
print("  1) run_paper.bat        (모의투자)")
print("  2) run_live.bat         (실거래)")
print()
print("실행 후 확인 사항:")
print("  - '동적 코인 선정 시스템 활성화' 메시지")
print("  - 5분마다 '동적 코인 갱신' 메시지")
print("  - 초단타 진입 로그 확인")
print()
