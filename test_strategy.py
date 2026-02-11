"""
전략 설정 테스트 및 진단 도구
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config import Config
import pyupbit
import pandas as pd

print("=" * 60)
print("전략 설정 진단 도구")
print("=" * 60)
print()

# 1. 전략 설정 확인
print("[1/5] 전략 설정 확인...")
for strategy_name, settings in Config.STRATEGIES.items():
    status = "✓ 활성화" if settings['enabled'] else "✗ 비활성화"
    print(f"  {status} {strategy_name}")
    print(f"      손절: {settings['stop_loss']*100:.1f}%")
    print(f"      익절: {settings['take_profit']*100:.1f}%")

print()

# 2. 리스크 설정 확인
print("[2/5] 리스크 설정 확인...")
print(f"  초기 자본: {Config.INITIAL_CAPITAL:,}원")
print(f"  최대 포지션: {Config.MAX_POSITIONS}개")
print(f"  포지션당 최대: {Config.MAX_POSITION_RATIO*100:.0f}%")
print(f"  일일 최대 손실: {Config.MAX_DAILY_LOSS:,}원")
print(f"  누적 최대 손실: {Config.MAX_CUMULATIVE_LOSS:,}원")
print()

# 3. AI 시스템 확인
print("[3/5] AI 시스템 확인...")
print(f"  고급 AI: {'✓' if Config.ENABLE_ADVANCED_AI else '✗'}")
print(f"  호가창 분석: {'✓' if Config.ENABLE_ORDERBOOK_ANALYSIS else '✗'}")
print(f"  시나리오 감지: {'✓' if Config.ENABLE_SCENARIO_DETECTION else '✗'}")
print(f"  스마트 분할: {'✓' if Config.ENABLE_SMART_SPLIT else '✗'}")
print(f"  보유 시간 AI: {'✓' if Config.ENABLE_HOLDING_TIME_AI else '✗'}")
print(f"  동적 청산: {'✓' if Config.ENABLE_DYNAMIC_EXIT else '✗'}")
print()

# 4. 실시간 시장 데이터 테스트
print("[4/5] 실시간 시장 데이터 테스트...")
try:
    # 비트코인 데이터로 테스트
    df = pyupbit.get_ohlcv("KRW-BTC", interval="minute5", count=50)
    
    if df is not None and not df.empty:
        print(f"  ✓ OHLCV 데이터 조회 성공")
        print(f"  ✓ 최근 가격: {df['close'].iloc[-1]:,.0f}원")
        
        # RSI 간단 계산
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        current_rsi = rsi.iloc[-1]
        
        print(f"  ✓ 현재 RSI: {current_rsi:.1f}")
        
        # 진입 가능성 판단
        aggressive_rsi_ok = 35 < current_rsi < 65
        conservative_rsi_ok = 30 < current_rsi < 70
        
        print()
        print("  진입 조건 분석:")
        print(f"    Aggressive Scalping RSI: {'✓ 가능' if aggressive_rsi_ok else '✗ 불가'} (40~60 필요)")
        print(f"    Conservative Scalping RSI: {'✓ 가능' if conservative_rsi_ok else '✗ 불가'} (35~65 필요)")
        
        # 볼륨 체크
        avg_volume = df['volume'].rolling(window=20).mean().iloc[-1]
        current_volume = df['volume'].iloc[-1]
        volume_ratio = current_volume / avg_volume if avg_volume > 0 else 0
        
        print(f"    현재 거래량 비율: {volume_ratio:.2f}x")
        print(f"    Aggressive 진입: {'✓ 가능' if volume_ratio >= 1.2 else '✗ 불가'} (1.2배 이상 필요)")
        
    else:
        print("  ✗ 데이터 조회 실패")
        
except Exception as e:
    print(f"  ✗ 에러: {e}")

print()

# 5. 권장사항
print("[5/5] 권장사항...")
print()
print("💡 거래가 발생하지 않는 경우:")
print("   1. 시장 변동성이 낮음 → 정상 (변동성 기다림)")
print("   2. RSI가 중립 구간 (45~55) → 정상 (극단값 기다림)")
print("   3. 거래량이 평균 이하 → 정상 (거래량 증가 기다림)")
print()
print("✅ 테스트 모드 사용:")
print("   run_test.bat 실행")
print("   → 진입 조건 완화")
print("   → 더 자주 거래 발생")
print("   → 빠른 학습 데이터 수집")
print()
print("⏱️ 권장 대기 시간:")
print("   백테스트: 30분~1시간")
print("   모의투자: 최소 1시간")
print("   → 다양한 시장 상황 경험")
print()

print("=" * 60)
input("Press Enter to exit...")
