"""
main.py에 추가할 화면 갱신 메서드
"""

def update_display_info(self):
    """화면 표시 정보 업데이트"""
    try:
        # AI 학습 상태 업데이트
        if self.learning_engine:
            stats = self.learning_engine.get_stats()
            profit_trades = stats.get('profit_trades', 0)
            loss_trades = stats.get('loss_trades', 0)
            total_trades = profit_trades + loss_trades
            
            self.display.update_ai_learning(
                total_trades=total_trades,
                profit_trades=profit_trades,
                loss_trades=loss_trades
            )
        
        # 자본금 및 손익 상태 업데이트
        risk_status = self.risk_manager.get_risk_status()
        self.display.update_capital_status(
            initial=Config.INITIAL_CAPITAL,
            current=risk_status['current_balance'],
            profit=risk_status['cumulative_profit_loss']
        )
        
        # 시장 조건 분석 (BTC 기준)
        try:
            df = self.api.get_ohlcv('KRW-BTC', interval="minute5", count=200)
            if df is not None and not df.empty:
                market_phase, entry_condition, coin_summary = self.market_analyzer.analyze_market(df)
                
                self.display.update_market_condition(market_phase, entry_condition)
                self.display.update_coin_summary(coin_summary)
                self.display.update_bot_status(f"가동 중 | {len(self.tickers)}개 코인 모니터링")
        except:
            pass
    
    except Exception as e:
        self.logger.log_warning(f"화면 갱신 오류: {e}")


def update_display_positions(self):
    """포지션 정보를 화면에 업데이트"""
    try:
        # 1. 일반 포지션 (risk_manager)
        for ticker, position in self.risk_manager.positions.items():
            slot = self.display.get_slot_by_ticker(ticker)
            if not slot:
                slot = self.display.get_available_slot()
            
            if slot:
                current_price = self.api.get_current_price(ticker)
                if current_price:
                    self.display.update_position(
                        slot=slot,
                        ticker=ticker,
                        entry_price=position.entry_price,
                        current_price=current_price,
                        amount=position.amount,
                        strategy=position.strategy,
                        entry_time=position.entry_time
                    )
        
        # 2. 초단타 포지션 (ultra_positions)
        for ticker, position in self.ultra_positions.items():
            slot = self.display.get_slot_by_ticker(ticker)
            if not slot:
                slot = self.display.get_available_slot()
            
            if slot:
                current_price = self.api.get_current_price(ticker)
                if current_price:
                    self.display.update_position(
                        slot=slot,
                        ticker=ticker,
                        entry_price=position['entry_price'],
                        current_price=current_price,
                        amount=position['amount'],
                        strategy='ultra_scalping',
                        entry_time=position['entry_time']
                    )
        
        # 화면 렌더링
        self.display.render()
    
    except Exception as e:
        self.logger.log_warning(f"포지션 화면 갱신 오류: {e}")


def update_scan_status(self, status_text: str):
    """스캔 상태 업데이트"""
    self.display.update_scan_status(status_text)
