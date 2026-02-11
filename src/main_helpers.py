"""
main.py 헬퍼 메서드
실시간 잔고 감지 및 기존 보유 코인 관리
"""

def _update_real_balance(self):
    """
    실시간 Upbit KRW 잔고 업데이트
    """
    try:
        if self.mode == 'live' and self.api.upbit:
            # Upbit API로 KRW 잔고 조회
            balances = self.api.upbit.get_balances()
            krw_balance = 0
            
            for balance in balances:
                if balance['currency'] == 'KRW':
                    krw_balance = float(balance['balance'])
                    break
            
            # Risk Manager 잔고 업데이트
            self.risk_manager.current_balance = krw_balance
            Config.INITIAL_CAPITAL = krw_balance
            
            self.logger.log_info(f"💰 실시간 잔고 업데이트: {krw_balance:,.0f}원")
            return krw_balance
        
        return Config.INITIAL_CAPITAL
    
    except Exception as e:
        self.logger.log_error("BALANCE_ERROR", "잔고 조회 실패", e)
        return Config.INITIAL_CAPITAL


def _load_existing_holdings(self):
    """
    기존 보유 코인 로드 (투자금으로 미사용)
    신규 투자는 KRW 잔고만 사용
    """
    try:
        if self.mode == 'live' and self.api.upbit:
            balances = self.api.upbit.get_balances()
            
            for balance in balances:
                currency = balance['currency']
                if currency == 'KRW':
                    continue
                
                ticker = f"KRW-{currency}"
                amount = float(balance['balance'])
                locked = float(balance.get('locked', 0))
                avg_buy_price = float(balance.get('avg_buy_price', 0))
                
                if amount > 0 or locked > 0:
                    self.existing_holdings[ticker] = {
                        'amount': amount,
                        'locked': locked,
                        'avg_buy_price': avg_buy_price,
                        'total_amount': amount + locked
                    }
                    
                    # HoldingProtector에 등록
                    self.holding_protector.add_existing_holding(
                        ticker=ticker,
                        amount=amount + locked,
                        avg_price=avg_buy_price
                    )
                    
                    self.logger.log_info(
                        f"📦 기존 보유: {ticker} | "
                        f"수량: {amount:.8f} | "
                        f"평단: {avg_buy_price:,.0f}원"
                    )
    
    except Exception as e:
        self.logger.log_error("HOLDINGS_ERROR", "기존 보유 코인 로드 실패", e)


def _can_invest_in_existing_coin(self, ticker: str) -> bool:
    """
    기존 보유 코인에 추가 투자 가능 여부
    
    Args:
        ticker: 코인 티커
    
    Returns:
        True: 추가 투자 가능 (기존 방식 유지)
        False: 투자 불가
    """
    # 기존 보유 코인이 아니면 항상 투자 가능
    if ticker not in self.existing_holdings:
        return True
    
    # 기존 보유 코인에 추가 투자는 허용 (기존 방식 유지)
    # 단, 투자금 계산 시 KRW 잔고만 사용
    return True


def _get_available_investment(self) -> float:
    """
    사용 가능한 투자금 계산
    
    Returns:
        투자 가능 금액 (KRW 잔고)
    """
    try:
        if self.use_real_balance:
            # 실시간 잔고 업데이트
            return self._update_real_balance()
        else:
            # Risk Manager 잔고 사용
            return self.risk_manager.current_balance
    
    except Exception as e:
        self.logger.log_error("INVESTMENT_ERROR", "투자금 계산 실패", e)
        return 0
