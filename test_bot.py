"""
Upbit AutoProfit Bot v5.8.1 테스트 스크립트
주요 기능 및 버그 수정 검증
"""

import sys
import os
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """1. 모든 모듈 import 테스트"""
    print("\n" + "="*60)
    print("🧪 테스트 1: 모듈 Import 검증")
    print("="*60)
    
    try:
        from config import Config
        print("✅ config.Config")
        
        from upbit_api import UpbitAPI
        print("✅ upbit_api.UpbitAPI")
        
        from utils.logger import TradingLogger
        print("✅ utils.logger.TradingLogger")
        
        from utils.risk_manager import RiskManager
        print("✅ utils.risk_manager.RiskManager")
        
        from utils.holding_protector import HoldingProtector
        print("✅ utils.holding_protector.HoldingProtector")
        
        from utils.surge_detector import SurgeDetector
        print("✅ utils.surge_detector.SurgeDetector")
        
        from utils.dynamic_coin_selector import DynamicCoinSelector
        print("✅ utils.dynamic_coin_selector.DynamicCoinSelector")
        
        from utils.fixed_screen_display import FixedScreenDisplay
        print("✅ utils.fixed_screen_display.FixedScreenDisplay")
        
        from utils.market_condition_analyzer import market_condition_analyzer
        print("✅ utils.market_condition_analyzer.market_condition_analyzer")
        
        from ai.learning_engine import LearningEngine
        print("✅ ai.learning_engine.LearningEngine")
        
        from strategies.ultra_scalping import UltraScalping
        print("✅ strategies.ultra_scalping.UltraScalping")
        
        print("\n✅ 모든 모듈 Import 성공!")
        return True
        
    except Exception as e:
        print(f"\n❌ Import 실패: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_learning_engine_get_stats():
    """2. LearningEngine.get_stats() 메서드 테스트 (v5.8.1 핫픽스)"""
    print("\n" + "="*60)
    print("🧪 테스트 2: LearningEngine.get_stats() 메서드")
    print("="*60)
    
    try:
        from ai.learning_engine import LearningEngine
        
        engine = LearningEngine()
        print("✅ LearningEngine 인스턴스 생성")
        
        # get_stats() 메서드 존재 확인
        assert hasattr(engine, 'get_stats'), "get_stats() 메서드가 없습니다!"
        print("✅ get_stats() 메서드 존재")
        
        # get_stats() 호출 테스트
        stats = engine.get_stats()
        print(f"✅ get_stats() 호출 성공: {stats}")
        
        # 반환 데이터 구조 검증
        assert 'total_trades' in stats, "total_trades 키 없음"
        assert 'profit_trades' in stats, "profit_trades 키 없음"
        assert 'loss_trades' in stats, "loss_trades 키 없음"
        assert 'win_rate' in stats, "win_rate 키 없음"
        print("✅ 반환 데이터 구조 검증 완료")
        
        # 데이터 타입 검증
        assert isinstance(stats['total_trades'], int), "total_trades는 int여야 함"
        assert isinstance(stats['profit_trades'], int), "profit_trades는 int여야 함"
        assert isinstance(stats['loss_trades'], int), "loss_trades는 int여야 함"
        assert isinstance(stats['win_rate'], (int, float)), "win_rate는 숫자여야 함"
        print("✅ 데이터 타입 검증 완료")
        
        # 초기값 검증 (거래 없음)
        assert stats['total_trades'] == 0, "초기 total_trades는 0이어야 함"
        assert stats['profit_trades'] == 0, "초기 profit_trades는 0이어야 함"
        assert stats['loss_trades'] == 0, "초기 loss_trades는 0이어야 함"
        assert stats['win_rate'] == 0.0, "초기 win_rate는 0.0이어야 함"
        print("✅ 초기값 검증 완료")
        
        print("\n✅ LearningEngine.get_stats() 테스트 통과!")
        return True
        
    except Exception as e:
        print(f"\n❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_fixed_screen_display():
    """3. FixedScreenDisplay 기능 테스트"""
    print("\n" + "="*60)
    print("🧪 테스트 3: FixedScreenDisplay 고정 화면")
    print("="*60)
    
    try:
        from utils.fixed_screen_display import FixedScreenDisplay
        import time
        
        # 7개 슬롯으로 초기화
        display = FixedScreenDisplay(max_positions=7)
        print("✅ FixedScreenDisplay(max_positions=7) 생성")
        
        # 메서드 존재 확인
        assert hasattr(display, 'clear_screen'), "clear_screen() 메서드 없음"
        assert hasattr(display, 'render'), "render() 메서드 없음"
        assert hasattr(display, 'update_ai_learning'), "update_ai_learning() 메서드 없음"
        assert hasattr(display, 'update_capital_status'), "update_capital_status() 메서드 없음"
        assert hasattr(display, 'update_market_condition'), "update_market_condition() 메서드 없음"
        assert hasattr(display, 'update_position'), "update_position() 메서드 없음"
        assert hasattr(display, 'get_available_slot'), "get_available_slot() 메서드 없음"
        assert hasattr(display, 'get_slot_by_ticker'), "get_slot_by_ticker() 메서드 없음"
        print("✅ 모든 필수 메서드 존재")
        
        # 화면 초기화
        display.clear_screen()
        print("✅ clear_screen() 호출 성공")
        
        # AI 학습 상태 업데이트
        display.update_ai_learning(
            total_trades=150,
            profit_trades=98,
            loss_trades=52
        )
        print("✅ update_ai_learning() 호출 성공")
        
        # 자본금 상태 업데이트
        display.update_capital_status(
            initial=1000000,
            current=1200000,
            profit=200000
        )
        print("✅ update_capital_status() 호출 성공")
        
        # 시장 조건 업데이트
        display.update_market_condition("강세장", "완화")
        print("✅ update_market_condition() 호출 성공")
        
        # 코인 요약 업데이트
        display.update_coin_summary({
            'price_change': 2.5,
            'volume_ratio': 1.8,
            'rsi': 58
        })
        print("✅ update_coin_summary() 호출 성공")
        
        # 봇 상태 업데이트
        display.update_bot_status("가동 중 | 35개 코인 모니터링")
        print("✅ update_bot_status() 호출 성공")
        
        # 포지션 추가 테스트
        slot = display.get_available_slot()
        assert slot == 1, "첫 번째 슬롯은 1이어야 함"
        print(f"✅ get_available_slot() = {slot}")
        
        from datetime import datetime
        display.update_position(
            slot=slot,
            ticker="KRW-BTC",
            entry_price=50000000,
            current_price=50600000,
            amount=0.001,
            strategy="⚡초단타",
            entry_time=datetime.now()  # datetime 객체로 전달
        )
        print("✅ update_position() 호출 성공")
        
        # 티커로 슬롯 찾기
        found_slot = display.get_slot_by_ticker("KRW-BTC")
        assert found_slot == 1, "KRW-BTC는 슬롯 1에 있어야 함"
        print(f"✅ get_slot_by_ticker('KRW-BTC') = {found_slot}")
        
        # 화면 렌더링
        print("\n📺 화면 렌더링 테스트:")
        print("-" * 60)
        display.render()
        print("-" * 60)
        
        print("\n✅ FixedScreenDisplay 테스트 통과!")
        return True
        
    except Exception as e:
        print(f"\n❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_config():
    """4. Config 설정 테스트"""
    print("\n" + "="*60)
    print("🧪 테스트 4: Config 설정 검증")
    print("="*60)
    
    try:
        from config import Config
        
        # 필수 설정 확인
        print(f"✅ FIXED_COIN_COUNT = {Config.FIXED_COIN_COUNT}")
        assert Config.FIXED_COIN_COUNT == 35, "코인 수는 35개여야 함"
        
        print(f"✅ MAX_POSITIONS = {Config.MAX_POSITIONS}")
        assert Config.MAX_POSITIONS == 7, "최대 포지션은 7개여야 함"
        
        print(f"✅ COIN_SELECTION_INTERVAL = {Config.COIN_SELECTION_INTERVAL}")
        assert Config.COIN_SELECTION_INTERVAL == 180, "코인 갱신 주기는 180초여야 함"
        
        print(f"✅ USE_REAL_BALANCE = {Config.USE_REAL_BALANCE}")
        assert Config.USE_REAL_BALANCE == True, "실시간 잔고 감지는 활성화되어야 함"
        
        print(f"✅ ENABLE_DYNAMIC_COIN_SELECTION = {Config.ENABLE_DYNAMIC_COIN_SELECTION}")
        
        print("\n✅ Config 설정 검증 통과!")
        return True
        
    except Exception as e:
        print(f"\n❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_main_update_display():
    """5. main.py의 _update_display() 메서드 통합 테스트"""
    print("\n" + "="*60)
    print("🧪 테스트 5: main.py _update_display() 통합")
    print("="*60)
    
    try:
        # main.py 파일 읽기
        main_path = Path(__file__).parent / "src" / "main.py"
        with open(main_path, 'r', encoding='utf-8') as f:
            main_content = f.read()
        
        # _update_display() 메서드 존재 확인
        assert "def _update_display(self):" in main_content, "_update_display() 메서드가 없습니다!"
        print("✅ _update_display() 메서드 존재")
        
        # get_stats() 호출 확인
        assert "self.learning_engine.get_stats()" in main_content, "get_stats() 호출이 없습니다!"
        print("✅ learning_engine.get_stats() 호출 확인")
        
        # display.render() 호출 확인
        assert "self.display.render()" in main_content, "display.render() 호출이 없습니다!"
        print("✅ display.render() 호출 확인")
        
        # update_ai_learning 호출 확인
        assert "self.display.update_ai_learning" in main_content, "update_ai_learning 호출이 없습니다!"
        print("✅ display.update_ai_learning() 호출 확인")
        
        # update_capital_status 호출 확인
        assert "self.display.update_capital_status" in main_content, "update_capital_status 호출이 없습니다!"
        print("✅ display.update_capital_status() 호출 확인")
        
        # update_position 호출 확인
        assert "self.display.update_position" in main_content, "update_position 호출이 없습니다!"
        print("✅ display.update_position() 호출 확인")
        
        print("\n✅ main.py 통합 테스트 통과!")
        return True
        
    except Exception as e:
        print(f"\n❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_holding_protector():
    """6. HoldingProtector 매도 정책 테스트 (v5.7)"""
    print("\n" + "="*60)
    print("🧪 테스트 6: HoldingProtector 매도 정책")
    print("="*60)
    
    try:
        from utils.holding_protector import HoldingProtector
        
        protector = HoldingProtector()
        print("✅ HoldingProtector 인스턴스 생성")
        
        # calculate_sellable_amount 메서드 확인
        assert hasattr(protector, 'calculate_sellable_amount'), "calculate_sellable_amount 메서드 없음"
        print("✅ calculate_sellable_amount() 메서드 존재")
        
        # 기존 코인 등록
        protector.register_existing_holding("KRW-BTC", 0.001, 50000000)
        print("✅ 기존 보유 등록: KRW-BTC 0.001개 (50,000,000원)")
        
        # 봇 포지션 추가
        protector.add_bot_position("KRW-BTC", 0.0005, 50000000, "aggressive_scalping")
        print("✅ 봇 포지션 추가: 0.0005개 (투자금 25,000원)")
        
        # 매도 가능 수량 계산 (손실 시)
        sellable, reason = protector.calculate_sellable_amount("KRW-BTC", current_price=49000000)
        print(f"✅ 손실 시 매도 가능: {sellable}개 ({reason})")
        assert sellable == 0.0005, "손실 시 투자금만 매도 가능해야 함"
        
        # 매도 가능 수량 계산 (수익 시)
        sellable, reason = protector.calculate_sellable_amount("KRW-BTC", current_price=51000000)
        print(f"✅ 수익 시 매도 가능: {sellable}개 ({reason})")
        # 수익 시: 투자금(0.0005) + 이익분 추가 가능
        assert sellable >= 0.0005, "수익 시 최소 투자금은 매도 가능해야 함"
        
        print("\n✅ HoldingProtector 테스트 통과!")
        return True
        
    except Exception as e:
        print(f"\n❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """모든 테스트 실행"""
    print("\n" + "="*60)
    print("🚀 Upbit AutoProfit Bot v5.8.1 통합 테스트")
    print("="*60)
    
    results = []
    
    # 테스트 실행
    results.append(("모듈 Import", test_imports()))
    results.append(("LearningEngine.get_stats()", test_learning_engine_get_stats()))
    results.append(("FixedScreenDisplay", test_fixed_screen_display()))
    results.append(("Config 설정", test_config()))
    results.append(("main.py 통합", test_main_update_display()))
    results.append(("HoldingProtector", test_holding_protector()))
    
    # 결과 요약
    print("\n" + "="*60)
    print("📊 테스트 결과 요약")
    print("="*60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ 통과" if result else "❌ 실패"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("\n" + "="*60)
    print(f"총 {len(results)}개 테스트 중 {passed}개 통과, {failed}개 실패")
    print("="*60)
    
    if failed == 0:
        print("\n🎉 모든 테스트 통과! 봇이 정상 작동합니다!")
        return 0
    else:
        print(f"\n⚠️  {failed}개 테스트 실패. 오류를 확인하세요.")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
