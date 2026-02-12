"""
텔레그램 알림 시스템
실시간 손익 알림 및 긴급 알림
"""

import requests
from datetime import datetime
from typing import Dict, Optional


class TelegramNotifier:
    """텔레그램 봇 알림"""
    
    def __init__(self, bot_token: str, chat_id: str):
        """
        Args:
            bot_token: 텔레그램 봇 토큰
            chat_id: 텔레그램 채팅 ID
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.enabled = bool(bot_token and chat_id)
        
        if not self.enabled:
            print("⚠️ 텔레그램 알림 비활성화 (토큰 또는 채팅 ID 없음)")
    
    def send_message(self, message: str, parse_mode: str = "Markdown") -> bool:
        """
        텔레그램 메시지 전송
        
        Args:
            message: 전송할 메시지
            parse_mode: 파싱 모드 (Markdown, HTML)
        
        Returns:
            전송 성공 여부
        """
        if not self.enabled:
            return False
        
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': parse_mode
            }
            response = requests.post(url, json=payload, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ 텔레그램 전송 실패: {e}")
            return False
    
    def send_daily_summary(self, summary_data: Dict) -> bool:
        """
        일일 손익 요약 전송
        
        Args:
            summary_data: {
                'start_balance': 시작 투자금,
                'current_balance': 현재 잔고,
                'total_equity': 총 자산,
                'daily_profit': 오늘 손익,
                'daily_profit_ratio': 오늘 손익률,
                'weekly_profit': 주간 손익,
                'monthly_profit': 월간 손익,
                'total_trades': 총 거래 수,
                'win_rate': 승률,
                'positions': 보유 포지션,
                'ai_confidence': AI 신뢰도,
                'best_trade': 최고 거래,
                'worst_trade': 최저 거래
            }
        """
        message = f"""
📊 *일일 손익 요약* - {datetime.now().strftime('%Y-%m-%d %H:%M')}

💰 *투자 현황*
├ 시작 투자금: {summary_data.get('start_balance', 0):,.0f}원
├ 현재 잔고: {summary_data.get('current_balance', 0):,.0f}원
└ 총 자산: {summary_data.get('total_equity', 0):,.0f}원

📈 *손익 분석*
├ 오늘: {summary_data.get('daily_profit', 0):+,.0f}원 ({summary_data.get('daily_profit_ratio', 0):+.2f}%)
├ 주간: {summary_data.get('weekly_profit', 0):+,.0f}원
└ 월간: {summary_data.get('monthly_profit', 0):+,.0f}원

📊 *거래 통계*
├ 총 거래: {summary_data.get('total_trades', 0)}회
└ 승률: {summary_data.get('win_rate', 0):.1f}%

🎯 *보유 포지션* ({len(summary_data.get('positions', []))}/{summary_data.get('max_positions', 3)})
"""
        
        # 포지션 상세
        for pos in summary_data.get('positions', [])[:3]:
            profit_ratio = pos.get('profit_loss_ratio', 0) * 100
            emoji = "📈" if profit_ratio > 0 else "📉"
            message += f"{emoji} {pos.get('ticker', 'N/A')}: {profit_ratio:+.2f}%\n"
        
        # AI 신뢰도
        ai_conf = summary_data.get('ai_confidence', 0)
        if ai_conf > 0:
            message += f"\n🤖 *AI 신뢰도*: {ai_conf:.1f}%\n"
        
        # 최고/최저 거래
        if summary_data.get('best_trade'):
            best = summary_data['best_trade']
            message += f"\n🏆 *최고 거래*: {best.get('ticker', 'N/A')} ({best.get('profit_ratio', 0):+.2f}%)\n"
        
        if summary_data.get('worst_trade'):
            worst = summary_data['worst_trade']
            message += f"💀 *최저 거래*: {worst.get('ticker', 'N/A')} ({worst.get('profit_ratio', 0):+.2f}%)\n"
        
        return self.send_message(message)
    
    def send_emergency_alert(self, alert_type: str, details: Dict) -> bool:
        """
        긴급 알림 전송
        
        Args:
            alert_type: 'loss_limit', 'trading_stop', 'system_error'
            details: 상세 정보
        """
        if alert_type == 'loss_limit':
            message = f"""
🚨 *긴급 알림: 손실 한도 도달*

⚠️ {details.get('limit_type', '일일')} 손실 한도에 도달했습니다.

📉 현재 손실: {details.get('current_loss', 0):,.0f}원
🛑 한도: {details.get('limit', 0):,.0f}원

거래가 자동 중단되었습니다.
"""
        elif alert_type == 'trading_stop':
            message = f"""
⏸️ *알림: 거래 중단*

사유: {details.get('reason', '알 수 없음')}
시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

거래가 일시 중단되었습니다.
"""
        elif alert_type == 'system_error':
            message = f"""
❌ *긴급: 시스템 에러*

오류: {details.get('error', '알 수 없는 오류')}
시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

즉시 확인이 필요합니다.
"""
        else:
            message = f"🔔 알림: {alert_type}\n{details}"
        
        return self.send_message(message)
    
    def send_trade_notification(self, action: str, ticker: str, price: float, 
                                 amount: float, reason: str, 
                                 strategy: str = None,
                                 order_method: str = None,
                                 surge_score: float = None,
                                 confidence: float = None,
                                 profit_loss: float = None,
                                 profit_ratio: float = None) -> bool:
        """
        거래 알림 전송 (⭐ v6.29 확장: 상세 정보 추가)
        
        Args:
            action: 'BUY' 또는 'SELL'
            ticker: 티커
            price: 가격
            amount: 수량
            reason: 거래 사유
            strategy: 전략 이름
            order_method: 주문 방식 (market, limit, best, etc.)
            surge_score: 급등 점수 (추격매수 시)
            confidence: 신뢰도
            profit_loss: 손익금액 (매도 시)
            profit_ratio: 손익률 (매도 시)
        """
        emoji = "🟢" if action == "BUY" else "🔴"
        action_kr = "매수" if action == "BUY" else "매도"
        
        # 기본 메시지
        message = f"""
{emoji} *{action_kr} 체결*

코인: {ticker}
가격: {price:,.0f}원
수량: {amount:.6f}
금액: {price * amount:,.0f}원
"""
        
        # ⭐ 전략 추가
        if strategy:
            message += f"
전략: {strategy}"
        
        # ⭐ 주문 방식 추가
        if order_method:
            method_kr = {
                'market': '시장가',
                'limit': '지정가',
                'best': '최유리',
                'ioc': 'IOC',
                'post_only': 'Post Only'
            }.get(order_method, order_method.upper())
            message += f"
주문: {method_kr}"
        
        # ⭐ 추격매수 정보 (매수시)
        if action == "BUY" and surge_score is not None:
            message += f"""

🚀 급등 감지
점수: {surge_score:.1f}/100
신뢰도: {confidence*100:.1f}%"""
        
        # ⭐ 손익 정보 (매도시)
        if action == "SELL" and profit_loss is not None:
            result_emoji = "📈" if profit_loss > 0 else "📉"
            result_kr = "수익" if profit_loss > 0 else "손실"
            message += f"""

{result_emoji} {result_kr}
금액: {profit_loss:+,.0f}원
수익률: {profit_ratio:+.2f}%"""
        
        # 사유 & 시간
        message += f"""

사유: {reason}
시간: {datetime.now().strftime('%H:%M:%S')}
"""
        
        return self.send_message(message)
