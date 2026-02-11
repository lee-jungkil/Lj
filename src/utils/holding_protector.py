"""
기존 보유 코인 보호 시스템
손실 중인 기존 포지션을 유지하면서 봇 거래만 분리
"""

from typing import Dict, Optional
from datetime import datetime
from dataclasses import dataclass, field
import json
import os


@dataclass
class ExistingHolding:
    """기존 보유 코인 정보"""
    ticker: str
    amount: float  # 기존 보유 수량
    avg_buy_price: float  # 기존 평균 매수가
    current_value: float = 0.0  # 현재 가치
    loss_ratio: float = 0.0  # 손실률 (%)
    lock_date: datetime = field(default_factory=datetime.now)
    note: str = ""  # 메모
    
    def to_dict(self) -> Dict:
        """딕셔너리로 변환"""
        return {
            'ticker': self.ticker,
            'amount': self.amount,
            'avg_buy_price': self.avg_buy_price,
            'current_value': self.current_value,
            'loss_ratio': self.loss_ratio,
            'lock_date': self.lock_date.isoformat(),
            'note': self.note
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ExistingHolding':
        """딕셔너리에서 생성"""
        # lock_date 처리
        lock_date_value = data.get('lock_date')
        if isinstance(lock_date_value, str):
            lock_date = datetime.fromisoformat(lock_date_value)
        elif isinstance(lock_date_value, datetime):
            lock_date = lock_date_value
        else:
            lock_date = datetime.now()
        
        return cls(
            ticker=data['ticker'],
            amount=data['amount'],
            avg_buy_price=data['avg_buy_price'],
            current_value=data.get('current_value', 0.0),
            loss_ratio=data.get('loss_ratio', 0.0),
            lock_date=lock_date,
            note=data.get('note', '')
        )


@dataclass
class BotPosition:
    """봇 거래 포지션 (기존 보유와 분리)"""
    ticker: str
    bot_amount: float  # 봇이 추가 매수한 수량만
    bot_avg_price: float  # 봇 매수 평균가
    bot_investment: float  # 봇 투자 금액
    entry_time: datetime = field(default_factory=datetime.now)
    strategy: str = ""
    
    def calculate_bot_profit(self, current_price: float) -> float:
        """봇 거래분 손익만 계산"""
        current_value = current_price * self.bot_amount
        return current_value - self.bot_investment
    
    def get_sellable_amount(self) -> float:
        """매도 가능한 수량 (봇이 산 수량만)"""
        return self.bot_amount


class HoldingProtector:
    """기존 보유 코인 보호 관리자"""
    
    def __init__(self, data_dir: str = "trading_logs"):
        """
        초기화
        
        Args:
            data_dir: 데이터 저장 디렉토리
        """
        self.data_dir = data_dir
        self.holdings_file = os.path.join(data_dir, "existing_holdings.json")
        
        # 기존 보유 코인 (절대 건드리지 않음)
        self.existing_holdings: Dict[str, ExistingHolding] = {}
        
        # 봇 거래 포지션 (기존과 분리)
        self.bot_positions: Dict[str, BotPosition] = {}
        
        # 로드
        self.load_existing_holdings()
    
    def register_existing_holding(self,
                                  ticker: str,
                                  amount: float,
                                  avg_buy_price: float,
                                  note: str = "") -> bool:
        """
        기존 보유 코인 등록 (보호 대상)
        
        Args:
            ticker: 코인 티커
            amount: 보유 수량
            avg_buy_price: 평균 매수가
            note: 메모
        
        Returns:
            등록 성공 여부
        """
        try:
            holding = ExistingHolding(
                ticker=ticker,
                amount=amount,
                avg_buy_price=avg_buy_price,
                note=note
            )
            
            self.existing_holdings[ticker] = holding
            self.save_existing_holdings()
            
            print(f"✅ 기존 보유 등록: {ticker}")
            print(f"   수량: {amount:.8f}")
            print(f"   평균가: {avg_buy_price:,.0f}원")
            print(f"   메모: {note}")
            
            return True
            
        except Exception as e:
            print(f"❌ 기존 보유 등록 실패: {e}")
            return False
    
    def is_existing_holding(self, ticker: str) -> bool:
        """기존 보유 코인인지 확인"""
        return ticker in self.existing_holdings
    
    def add_existing_holding(self, ticker: str, amount: float, avg_price: float):
        """
        기존 보유 코인 추가 (별칭 메서드)
        
        Args:
            ticker: 코인 티커
            amount: 보유 수량
            avg_price: 평균 매수가
        """
        return self.register_existing_holding(ticker, amount, avg_price)
    
    def get_existing_amount(self, ticker: str) -> float:
        """기존 보유 수량 조회"""
        if ticker in self.existing_holdings:
            return self.existing_holdings[ticker].amount
        return 0.0
    
    def add_bot_position(self,
                        ticker: str,
                        amount: float,
                        price: float,
                        strategy: str = "") -> bool:
        """
        봇 거래 포지션 추가 (기존 보유와 완전 분리)
        
        Args:
            ticker: 코인 티커
            amount: 매수 수량
            price: 매수 가격
            strategy: 전략 이름
        
        Returns:
            성공 여부
        """
        try:
            # 기존에 봇 포지션이 있으면 추가 매수로 평균가 계산
            if ticker in self.bot_positions:
                existing = self.bot_positions[ticker]
                
                # 평균 매수가 재계산
                total_investment = existing.bot_investment + (price * amount)
                total_amount = existing.bot_amount + amount
                new_avg_price = total_investment / total_amount
                
                existing.bot_amount = total_amount
                existing.bot_avg_price = new_avg_price
                existing.bot_investment = total_investment
                
                print(f"📝 봇 포지션 추가 매수: {ticker}")
                print(f"   추가 수량: {amount:.8f}")
                print(f"   총 봇 수량: {total_amount:.8f}")
                print(f"   평균가: {new_avg_price:,.0f}원")
            else:
                # 새로운 봇 포지션 생성
                position = BotPosition(
                    ticker=ticker,
                    bot_amount=amount,
                    bot_avg_price=price,
                    bot_investment=price * amount,
                    strategy=strategy
                )
                
                self.bot_positions[ticker] = position
                
                print(f"✅ 봇 포지션 신규 추가: {ticker}")
                print(f"   수량: {amount:.8f}")
                print(f"   가격: {price:,.0f}원")
                
                # 기존 보유가 있으면 경고
                if self.is_existing_holding(ticker):
                    existing_amount = self.get_existing_amount(ticker)
                    print(f"⚠️  주의: 기존 보유 {existing_amount:.8f}개 보호 중")
                    print(f"   → 봇 매수분 {amount:.8f}개만 별도 관리")
            
            return True
            
        except Exception as e:
            print(f"❌ 봇 포지션 추가 실패: {e}")
            return False
    
    def calculate_sellable_amount(self, ticker: str, current_price: float = 0.0, upbit_api=None) -> tuple[float, str]:
        """
        매도 가능한 수량 계산 (투자금 + 이익분만 매도, 원금 보호)
        
        v5.7 정책:
        - 기존 보유: 절대 매도 불가 (원금 보호)
        - 봇 투자금: 매도 가능
        - 이익분: 매도 가능
        
        Args:
            ticker: 코인 티커
            current_price: 현재 가격
            upbit_api: 업비트 API (실제 보유량 확인용)
        
        Returns:
            (매도 가능 수량, 설명)
        """
        # 기존 보유 수량 (원금 - 절대 보호)
        existing_amount = self.get_existing_amount(ticker)
        
        # 봇 포지션 수량
        bot_amount = 0.0
        bot_avg_price = 0.0
        if ticker in self.bot_positions:
            bot_amount = self.bot_positions[ticker].bot_amount
            bot_avg_price = self.bot_positions[ticker].bot_avg_price
        
        # 실제 거래소 보유량 확인
        if upbit_api:
            try:
                actual_amount = upbit_api.get_amount(ticker)
                
                # 안전 확인: 실제 보유량이 기존 보유량보다 적으면
                if actual_amount < existing_amount:
                    print(f"⚠️  경고: 실제 보유량({actual_amount:.8f})이 기존 보유({existing_amount:.8f})보다 적음")
                    return 0.0, "원금 보호 대상 부족"
                
                # 기본 매도 가능 = 실제 보유 - 기존 보유(원금 보호)
                sellable = actual_amount - existing_amount
                
                if sellable <= 0:
                    return 0.0, "원금 보호 - 매도 불가"
                
                # 이익이 발생한 경우 이익분 추가
                if current_price > 0 and bot_avg_price > 0 and current_price > bot_avg_price:
                    # 이익률 계산
                    profit_ratio = (current_price - bot_avg_price) / bot_avg_price
                    
                    # 이익분 수량 계산
                    profit_amount = bot_amount * profit_ratio
                    
                    # 매도 가능 = 봇 투자금 + 이익분
                    sellable_with_profit = bot_amount + profit_amount
                    
                    # 실제 보유량과 비교하여 안전하게 제한
                    sellable = min(sellable, sellable_with_profit)
                    
                    return sellable, f"투자금 + 이익분 {sellable:.8f}개 매도 가능 (원금 {existing_amount:.8f}개 보호)"
                else:
                    # 손실 또는 동일가: 봇 투자금만 매도 가능
                    sellable = min(sellable, bot_amount)
                    return sellable, f"투자금 {sellable:.8f}개만 매도 가능 (원금 {existing_amount:.8f}개 보호)"
                
            except Exception as e:
                print(f"⚠️  실제 보유량 확인 실패: {e}")
        
        # API 없으면 봇 포지션 수량만 반환
        if bot_amount > 0:
            return bot_amount, f"투자금 {bot_amount:.8f}개 (원금 {existing_amount:.8f}개 보호)"
        
        return 0.0, f"매도 불가 (원금 {existing_amount:.8f}개 보호)"
    
    def close_bot_position(self, ticker: str, sell_amount: float, sell_price: float) -> Optional[float]:
        """
        봇 포지션 청산 (기존 보유 절대 건드리지 않음)
        
        Args:
            ticker: 코인 티커
            sell_amount: 매도 수량
            sell_price: 매도 가격
        
        Returns:
            봇 거래분 손익
        """
        if ticker not in self.bot_positions:
            return None
        
        position = self.bot_positions[ticker]
        
        # 매도 수량이 봇 보유량보다 크면 제한
        if sell_amount > position.bot_amount:
            print(f"⚠️  매도 수량 초과: 요청 {sell_amount:.8f} > 봇 보유 {position.bot_amount:.8f}")
            sell_amount = position.bot_amount
        
        # 손익 계산 (봇 투자분만)
        sell_value = sell_price * sell_amount
        invested_value = position.bot_avg_price * sell_amount
        profit_loss = sell_value - invested_value
        
        # 수수료 (0.05% x 2)
        fee = (invested_value + sell_value) * 0.0005
        profit_loss -= fee
        
        # 전량 매도인 경우
        if sell_amount >= position.bot_amount * 0.999:  # 소수점 오차 고려
            print(f"✅ 봇 포지션 전량 청산: {ticker}")
            print(f"   매도 수량: {sell_amount:.8f}")
            print(f"   매도가: {sell_price:,.0f}원")
            print(f"   손익: {profit_loss:+,.0f}원")
            
            # 기존 보유 있으면 알림
            if self.is_existing_holding(ticker):
                existing = self.get_existing_amount(ticker)
                print(f"✅ 기존 보유 {existing:.8f}개 보호 완료 (매도하지 않음)")
            
            del self.bot_positions[ticker]
        else:
            # 부분 매도
            position.bot_amount -= sell_amount
            position.bot_investment -= invested_value
            
            print(f"📝 봇 포지션 부분 청산: {ticker}")
            print(f"   매도 수량: {sell_amount:.8f}")
            print(f"   남은 수량: {position.bot_amount:.8f}")
            print(f"   손익: {profit_loss:+,.0f}원")
        
        return profit_loss
    
    def get_status_report(self, upbit_api=None) -> str:
        """상태 리포트 생성"""
        lines = []
        lines.append("=" * 60)
        lines.append("🛡️  기존 보유 코인 보호 시스템")
        lines.append("=" * 60)
        
        # 기존 보유
        if self.existing_holdings:
            lines.append("\n📦 보호 중인 기존 보유:")
            for ticker, holding in self.existing_holdings.items():
                lines.append(f"\n  {ticker}:")
                lines.append(f"    수량: {holding.amount:.8f}")
                lines.append(f"    평균가: {holding.avg_price:,.0f}원")
                
                if upbit_api:
                    try:
                        current_price = upbit_api.get_current_price(ticker)
                        if current_price:
                            current_value = current_price * holding.amount
                            invested = holding.avg_buy_price * holding.amount
                            loss = ((current_value - invested) / invested) * 100
                            
                            lines.append(f"    현재가: {current_price:,.0f}원")
                            lines.append(f"    현재가치: {current_value:,.0f}원")
                            lines.append(f"    손익률: {loss:+.2f}%")
                    except:
                        pass
                
                if holding.note:
                    lines.append(f"    메모: {holding.note}")
                
                lines.append(f"    ⚠️  절대 매도하지 않음!")
        else:
            lines.append("\n보호 중인 기존 보유 없음")
        
        # 봇 포지션
        if self.bot_positions:
            lines.append("\n\n🤖 봇 거래 포지션 (매도 가능):")
            for ticker, position in self.bot_positions.items():
                lines.append(f"\n  {ticker}:")
                lines.append(f"    봇 수량: {position.bot_amount:.8f}")
                lines.append(f"    봇 평균가: {position.bot_avg_price:,.0f}원")
                lines.append(f"    봇 투자액: {position.bot_investment:,.0f}원")
                
                if upbit_api:
                    try:
                        current_price = upbit_api.get_current_price(ticker)
                        if current_price:
                            profit = position.calculate_bot_profit(current_price)
                            lines.append(f"    현재가: {current_price:,.0f}원")
                            lines.append(f"    봇 손익: {profit:+,.0f}원")
                    except:
                        pass
                
                lines.append(f"    ✅ 매도 가능!")
        else:
            lines.append("\n\n봇 거래 포지션 없음")
        
        lines.append("\n" + "=" * 60)
        
        return "\n".join(lines)
    
    def save_existing_holdings(self):
        """기존 보유 저장"""
        try:
            data = {
                'holdings': {
                    ticker: holding.to_dict()
                    for ticker, holding in self.existing_holdings.items()
                },
                'updated_at': datetime.now().isoformat()
            }
            
            with open(self.holdings_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"⚠️  기존 보유 저장 실패: {e}")
    
    def auto_detect_existing_holdings(self, upbit_api, prompt_user: bool = True) -> bool:
        """
        업비트에서 기존 보유 코인 자동 감지
        
        Args:
            upbit_api: UpbitAPI 인스턴스
            prompt_user: 사용자 확인 받을지 여부
        
        Returns:
            감지 성공 여부
        """
        if not upbit_api or not upbit_api.upbit:
            print("⚠️  업비트 API 연결 필요")
            return False
        
        try:
            # 현재 보유 조회
            balances = upbit_api.get_balances()
            
            if not balances:
                print("✅ 기존 보유 코인 없음")
                return True
            
            # KRW 제외하고 코인만 필터
            holdings = []
            for balance in balances:
                ticker_name = balance['currency']
                if ticker_name == 'KRW':
                    continue
                
                ticker = f"KRW-{ticker_name}"
                amount = float(balance['balance'])
                avg_price = float(balance['avg_buy_price'])
                
                if amount > 0 and avg_price > 0:
                    # 현재 손익 계산
                    current_price = upbit_api.get_current_price(ticker)
                    profit_loss_ratio = 0.0
                    
                    if current_price and avg_price > 0:
                        profit_loss_ratio = ((current_price - avg_price) / avg_price) * 100
                    
                    holdings.append({
                        'ticker': ticker,
                        'amount': amount,
                        'avg_price': avg_price,
                        'current_price': current_price,
                        'profit_loss_ratio': profit_loss_ratio
                    })
            
            if not holdings:
                print("✅ 기존 보유 코인 없음")
                return True
            
            # 기존 보유 발견
            print("\n" + "=" * 60)
            print("🔍 기존 보유 코인 발견!")
            print("=" * 60)
            
            for h in holdings:
                print(f"\n{h['ticker']}:")
                print(f"  수량: {h['amount']:.8f}")
                print(f"  평균가: {h['avg_price']:,.0f}원")
                if h['current_price']:
                    print(f"  현재가: {h['current_price']:,.0f}원")
                    print(f"  손익: {h['profit_loss_ratio']:+.2f}%")
                    
                    if h['profit_loss_ratio'] < -10:
                        print(f"  ⚠️  손실 중!")
            
            print("\n" + "-" * 60)
            
            # 사용자 확인
            if prompt_user:
                print("\n⚠️  중요: 이 코인들을 보호 대상으로 등록할까요?")
                print("   등록 시: 봇이 절대 매도하지 않습니다.")
                print("   미등록 시: 봇이 매도 신호 시 매도할 수 있습니다.")
                
                response = input("\n기존 보유 코인을 보호할까요? (Y/n): ").strip().lower()
                
                if response == 'n' or response == 'no':
                    print("\n⚠️  보호하지 않음 - 봇이 자유롭게 거래합니다.")
                    return False
            
            # 자동 등록
            print("\n🔄 기존 보유 자동 등록 중...")
            
            for h in holdings:
                note = f"자동 감지 (손익: {h['profit_loss_ratio']:+.2f}%)"
                
                self.register_existing_holding(
                    ticker=h['ticker'],
                    amount=h['amount'],
                    avg_buy_price=h['avg_price'],
                    note=note
                )
            
            print(f"\n✅ 총 {len(holdings)}개 코인 보호 등록 완료!")
            print("🛡️  이 코인들은 봇이 절대 매도하지 않습니다.\n")
            
            return True
            
        except Exception as e:
            print(f"❌ 자동 감지 실패: {e}")
            return False
    
    def load_existing_holdings(self):
        """저장된 기존 보유 로드"""
        try:
            if not os.path.exists(self.holdings_file):
                return
            
            with open(self.holdings_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for ticker, holding_data in data.get('holdings', {}).items():
                self.existing_holdings[ticker] = ExistingHolding.from_dict(holding_data)
            
            if self.existing_holdings:
                print(f"✅ 기존 보유 {len(self.existing_holdings)}개 로드 완료")
                
        except Exception as e:
            print(f"⚠️  기존 보유 로드 실패: {e}")
