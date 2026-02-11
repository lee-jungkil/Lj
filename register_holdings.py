#!/usr/bin/env python3
"""
기존 보유 코인 등록 도구
손실 중인 기존 코인을 보호 대상으로 등록
"""

import sys
import os

# 경로 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.holding_protector import HoldingProtector
from upbit_api import UpbitAPI
from config import Config


def register_existing_holdings():
    """기존 보유 코인 등록 대화형 프로그램"""
    print("=" * 60)
    print("🛡️  기존 보유 코인 보호 시스템 - 등록 도구")
    print("=" * 60)
    print()
    print("이 도구는 기존에 보유 중인 손실 코인을 보호 대상으로 등록합니다.")
    print("등록된 코인은 봇이 절대 매도하지 않습니다!")
    print()
    
    # HoldingProtector 초기화
    protector = HoldingProtector()
    
    # API 초기화 (실거래 모드)
    print("📡 업비트 연결 중...")
    try:
        api = UpbitAPI(Config.UPBIT_ACCESS_KEY, Config.UPBIT_SECRET_KEY)
        print("✅ 업비트 연결 성공\n")
    except:
        print("⚠️  업비트 연결 실패 (수동 입력 모드)\n")
        api = None
    
    # 현재 보유 코인 조회
    if api and api.upbit:
        print("💼 현재 보유 중인 코인:")
        print("-" * 60)
        
        balances = api.get_balances()
        
        if balances:
            for balance in balances:
                ticker_name = balance['currency']
                if ticker_name == 'KRW':
                    continue
                
                ticker = f"KRW-{ticker_name}"
                amount = float(balance['balance'])
                avg_price = float(balance['avg_buy_price'])
                
                # 현재가 조회
                current_price = api.get_current_price(ticker)
                
                if current_price and avg_price > 0:
                    current_value = current_price * amount
                    invested = avg_price * amount
                    profit_loss_ratio = ((current_value - invested) / invested) * 100
                    
                    print(f"\n{ticker}:")
                    print(f"  수량: {amount:.8f}")
                    print(f"  평균 매수가: {avg_price:,.0f}원")
                    print(f"  현재가: {current_price:,.0f}원")
                    print(f"  투자금액: {invested:,.0f}원")
                    print(f"  현재가치: {current_value:,.0f}원")
                    print(f"  손익: {profit_loss_ratio:+.2f}%")
                    
                    if profit_loss_ratio < -10:
                        print(f"  ⚠️  손실 중!")
        else:
            print("보유 중인 코인이 없습니다.")
        
        print("\n" + "-" * 60)
    
    print()
    print("=" * 60)
    print("등록 방법:")
    print("1. 자동 등록: 현재 보유 중인 모든 코인을 자동 등록")
    print("2. 선택 등록: 특정 코인만 선택해서 등록")
    print("3. 수동 입력: 티커, 수량, 평균가를 직접 입력")
    print("4. 종료")
    print("=" * 60)
    
    while True:
        choice = input("\n선택 (1-4): ").strip()
        
        if choice == '1':
            # 자동 등록
            if not api or not api.upbit:
                print("❌ 자동 등록은 업비트 연결이 필요합니다.")
                continue
            
            print("\n🔄 자동 등록 시작...")
            
            balances = api.get_balances()
            registered = 0
            
            for balance in balances:
                ticker_name = balance['currency']
                if ticker_name == 'KRW':
                    continue
                
                ticker = f"KRW-{ticker_name}"
                amount = float(balance['balance'])
                avg_price = float(balance['avg_buy_price'])
                
                if amount > 0 and avg_price > 0:
                    # 손익률 계산
                    current_price = api.get_current_price(ticker)
                    if current_price:
                        profit_loss_ratio = ((current_price - avg_price) / avg_price) * 100
                        note = f"자동 등록 (손익: {profit_loss_ratio:+.2f}%)"
                    else:
                        note = "자동 등록"
                    
                    protector.register_existing_holding(
                        ticker=ticker,
                        amount=amount,
                        avg_buy_price=avg_price,
                        note=note
                    )
                    registered += 1
            
            print(f"\n✅ 총 {registered}개 코인 등록 완료!")
            break
        
        elif choice == '2':
            # 선택 등록
            if not api or not api.upbit:
                print("❌ 선택 등록은 업비트 연결이 필요합니다.")
                continue
            
            balances = api.get_balances()
            holdings = []
            
            for balance in balances:
                ticker_name = balance['currency']
                if ticker_name == 'KRW':
                    continue
                
                ticker = f"KRW-{ticker_name}"
                amount = float(balance['balance'])
                avg_price = float(balance['avg_buy_price'])
                
                if amount > 0:
                    holdings.append({
                        'ticker': ticker,
                        'amount': amount,
                        'avg_price': avg_price
                    })
            
            if not holdings:
                print("등록 가능한 코인이 없습니다.")
                continue
            
            print("\n보유 코인 목록:")
            for i, h in enumerate(holdings, 1):
                current_price = api.get_current_price(h['ticker'])
                pl_ratio = 0.0
                if current_price and h['avg_price'] > 0:
                    pl_ratio = ((current_price - h['avg_price']) / h['avg_price']) * 100
                
                print(f"{i}. {h['ticker']}: {h['amount']:.8f}개 (손익: {pl_ratio:+.2f}%)")
            
            selected = input("\n등록할 코인 번호 (쉼표로 구분, 예: 1,3,5): ").strip()
            
            try:
                indices = [int(x.strip()) - 1 for x in selected.split(',')]
                
                for idx in indices:
                    if 0 <= idx < len(holdings):
                        h = holdings[idx]
                        
                        # 손익률 계산
                        current_price = api.get_current_price(h['ticker'])
                        if current_price:
                            profit_loss_ratio = ((current_price - h['avg_price']) / h['avg_price']) * 100
                            note = f"선택 등록 (손익: {profit_loss_ratio:+.2f}%)"
                        else:
                            note = "선택 등록"
                        
                        protector.register_existing_holding(
                            ticker=h['ticker'],
                            amount=h['amount'],
                            avg_buy_price=h['avg_price'],
                            note=note
                        )
                
                print(f"\n✅ {len(indices)}개 코인 등록 완료!")
                break
                
            except ValueError:
                print("❌ 잘못된 입력입니다.")
        
        elif choice == '3':
            # 수동 입력
            print("\n수동 입력 모드")
            
            ticker = input("티커 (예: KRW-BTC): ").strip().upper()
            if not ticker.startswith('KRW-'):
                ticker = f"KRW-{ticker}"
            
            try:
                amount = float(input("수량: ").strip())
                avg_price = float(input("평균 매수가: ").strip())
                note = input("메모 (선택사항): ").strip()
                
                protector.register_existing_holding(
                    ticker=ticker,
                    amount=amount,
                    avg_buy_price=avg_price,
                    note=note or "수동 입력"
                )
                
                print("\n✅ 등록 완료!")
                
                # 추가 등록 여부
                more = input("\n추가 등록하시겠습니까? (y/n): ").strip().lower()
                if more != 'y':
                    break
                    
            except ValueError:
                print("❌ 잘못된 입력입니다.")
        
        elif choice == '4':
            print("\n등록 종료")
            break
        
        else:
            print("❌ 1-4 중에서 선택하세요.")
    
    # 최종 상태 출력
    print("\n" + protector.get_status_report(api))
    print("\n✅ 설정 완료!")
    print("\n📝 등록된 코인은 trading_logs/existing_holdings.json에 저장됩니다.")
    print("⚠️  봇 실행 시 이 코인들은 절대 매도하지 않습니다!")


if __name__ == "__main__":
    try:
        register_existing_holdings()
    except KeyboardInterrupt:
        print("\n\n사용자 중단")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
