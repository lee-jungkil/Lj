#!/usr/bin/env python3
"""
Fixed Screen Display Test
고정 화면 테스트 - 스크롤 없이 실시간 업데이트
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import time
from datetime import datetime
from src.utils.fixed_screen_display import FixedScreenDisplay

def main():
    """테스트 메인"""
    print("=" * 80)
    print("🎯 Fixed Screen Display Test - v6.14-FIXED")
    print("=" * 80)
    print()
    print("✅ 이 테스트는 화면이 완전히 고정되어 있는지 확인합니다:")
    print("   1. 화면 경계를 벗어나지 않음")
    print("   2. 스크롤이 발생하지 않음")
    print("   3. 고정된 프레임 내에서만 내용이 업데이트됨")
    print()
    print("🔄 30초 동안 실시간 데이터 업데이트를 시뮬레이션합니다...")
    print("   (Ctrl+C로 중지)")
    print()
    input("Press Enter to start test...")
    
    # Display 초기화
    display = FixedScreenDisplay(max_positions=7)
    
    # 초기 상태 설정
    display.update_bot_status("✅ 테스트 모드 실행 중")
    display.update_scan_status("🔍 실시간 데이터 업데이트 테스트...")
    display.update_capital_status(10000000, 10000000, 0)
    display.update_ai_learning(0, 0, 0)
    display.update_market_condition("횡보장", "기본", "테스트 모드")
    display.update_coin_summary("테스트 진행 중...")
    display.update_trade_stats(0, 0)
    display.update_monitoring("테스트 시작", "", "")
    
    # 첫 렌더링
    display.render()
    time.sleep(2)
    
    # 시뮬레이션 시작
    start_time = time.time()
    iteration = 0
    
    try:
        while time.time() - start_time < 30:  # 30초 테스트
            iteration += 1
            
            # === 1. 포지션 시뮬레이션 ===
            if iteration % 3 == 1:
                # 포지션 추가
                display.update_position(
                    slot=1,
                    ticker="KRW-BTC",
                    entry_price=50000000,
                    current_price=50000000 + (iteration * 10000),
                    amount=0.001,
                    strategy="ultra_scalping",
                    entry_time=datetime.now()
                )
                display.update_position(
                    slot=2,
                    ticker="KRW-ETH",
                    entry_price=3000000,
                    current_price=3000000 - (iteration * 5000),
                    amount=0.01,
                    strategy="aggressive_scalping",
                    entry_time=datetime.now()
                )
            
            # === 2. AI 학습 데이터 업데이트 ===
            ai_trades = iteration // 2
            ai_wins = int(ai_trades * 0.6)
            ai_losses = ai_trades - ai_wins
            display.update_ai_learning(ai_trades, ai_wins, ai_losses)
            
            # === 3. 자본금 변동 ===
            profit = (iteration * 5000) - 25000
            display.update_capital_status(10000000, 10000000 + int(profit), profit)
            
            # === 4. 시장 조건 변경 ===
            phases = ["강세장", "약세장", "횡보장"]
            reasons = ["BTC +2.5%", "거래량 감소", "변동성 낮음"]
            phase_idx = (iteration // 5) % 3
            display.update_market_condition(phases[phase_idx], "기본", reasons[phase_idx])
            
            # === 5. 거래 통계 업데이트 ===
            buy_count = iteration // 4
            sell_count = iteration // 5
            display.update_trade_stats(buy_count, sell_count)
            
            # === 6. 스캔 상태 업데이트 ===
            scan_statuses = [
                "🔍 전체 코인 스캔 중... (1/200)",
                "📊 포지션 체크 중...",
                "⚡ 급등 감지 중...",
                "💡 AI 분석 중..."
            ]
            display.update_scan_status(scan_statuses[iteration % 4])
            
            # === 7. 모니터링 상태 업데이트 ===
            monitor_msgs = [
                ("📈 BTC: 상승 추세 확인", "변동률: +2.3%", "거래량: 증가"),
                ("⚠️ ETH: 조정 구간 진입", "지지선: 2,950,000원", "관망 중"),
                ("🔥 XRP: 급등 감지!", "5분간 +5.2%", "진입 검토 중"),
                ("💰 ADA: 익절 조건 충족", "목표가 도달", "매도 대기")
            ]
            msg_idx = (iteration // 3) % 4
            display.update_monitoring(*monitor_msgs[msg_idx])
            
            # === 8. 매도 결과 시뮬레이션 ===
            if iteration == 10:
                display.remove_position(2, 3015000, 150, 0.5)
            
            # 렌더링
            display.render()
            
            # 3초 대기 (실제 봇과 동일)
            time.sleep(3)
        
        # 테스트 완료
        display.cleanup()
        print("\n" * 3)
        print("=" * 80)
        print("✅ 테스트 완료!")
        print("=" * 80)
        print()
        print("🎯 확인사항:")
        print("   ✓ 화면이 스크롤되지 않았나요?")
        print("   ✓ 고정된 프레임 내에서만 내용이 업데이트되었나요?")
        print("   ✓ 모든 데이터가 실시간으로 동기화되었나요?")
        print()
        print("✨ v6.14-FIXED: True Fixed-Screen Display")
        print()
    
    except KeyboardInterrupt:
        display.cleanup()
        print("\n\n⚠️ 테스트 중단됨")
    
    except Exception as e:
        display.cleanup()
        print(f"\n\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
