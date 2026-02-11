"""
Gmail 이메일 리포트 시스템
주간/월간 손익 리포트 전송
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, List


class EmailReporter:
    """Gmail 리포트 전송"""
    
    def __init__(self, sender_email: str, sender_password: str, receiver_email: str):
        """
        Args:
            sender_email: 발신자 Gmail 주소
            sender_password: Gmail 앱 비밀번호
            receiver_email: 수신자 이메일
        """
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.receiver_email = receiver_email
        self.enabled = bool(sender_email and sender_password and receiver_email)
        
        if not self.enabled:
            print("⚠️ 이메일 리포트 비활성화 (계정 정보 없음)")
    
    def send_report(self, subject: str, html_content: str) -> bool:
        """
        HTML 리포트 전송
        
        Args:
            subject: 이메일 제목
            html_content: HTML 본문
        
        Returns:
            전송 성공 여부
        """
        if not self.enabled:
            return False
        
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = self.receiver_email
            
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            print(f"✅ 이메일 리포트 전송 완료: {subject}")
            return True
        except Exception as e:
            print(f"❌ 이메일 전송 실패: {e}")
            return False
    
    def send_weekly_report(self, report_data: Dict) -> bool:
        """
        주간 리포트 전송
        
        Args:
            report_data: {
                'period': 기간,
                'start_balance': 시작 투자금,
                'end_balance': 종료 잔고,
                'total_equity': 총 자산,
                'total_profit': 총 손익,
                'profit_ratio': 수익률,
                'daily_avg_profit': 일평균 손익,
                'total_trades': 총 거래,
                'wins': 승리,
                'losses': 패배,
                'win_rate': 승률,
                'strategy_performance': 전략별 성과,
                'fees': 수수료,
                'daily_profits': 일별 손익
            }
        """
        html = self._generate_weekly_html(report_data)
        subject = f"[Upbit Bot] 주간 리포트 - {report_data.get('period', datetime.now().strftime('%Y-%m-%d'))}"
        return self.send_report(subject, html)
    
    def send_monthly_report(self, report_data: Dict) -> bool:
        """월간 리포트 전송"""
        html = self._generate_monthly_html(report_data)
        subject = f"[Upbit Bot] 월간 리포트 - {report_data.get('period', datetime.now().strftime('%Y-%m'))}"
        return self.send_report(subject, html)
    
    def _generate_weekly_html(self, data: Dict) -> str:
        """주간 리포트 HTML 생성"""
        profit = data.get('total_profit', 0)
        profit_color = "green" if profit > 0 else "red"
        
        html = f"""
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #4CAF50; color: white; padding: 20px; text-align: center; }}
        .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
        .profit {{ font-size: 24px; font-weight: bold; color: {profit_color}; }}
        table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
        th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #f2f2f2; }}
        .positive {{ color: green; }}
        .negative {{ color: red; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 주간 손익 리포트</h1>
        <p>{data.get('period', 'N/A')}</p>
    </div>
    
    <div class="section">
        <h2>💰 투자금 정보</h2>
        <table>
            <tr><td>시작 투자금</td><td>{data.get('start_balance', 0):,.0f}원</td></tr>
            <tr><td>종료 잔고</td><td>{data.get('end_balance', 0):,.0f}원</td></tr>
            <tr><td>총 자산</td><td><strong>{data.get('total_equity', 0):,.0f}원</strong></td></tr>
        </table>
    </div>
    
    <div class="section">
        <h2>📈 손익률</h2>
        <p class="profit">{profit:+,.0f}원 ({data.get('profit_ratio', 0):+.2f}%)</p>
        <p>일평균 손익: {data.get('daily_avg_profit', 0):+,.0f}원</p>
    </div>
    
    <div class="section">
        <h2>📊 거래 통계</h2>
        <table>
            <tr><td>총 거래</td><td>{data.get('total_trades', 0)}회</td></tr>
            <tr><td>승리</td><td class="positive">{data.get('wins', 0)}회</td></tr>
            <tr><td>패배</td><td class="negative">{data.get('losses', 0)}회</td></tr>
            <tr><td>승률</td><td><strong>{data.get('win_rate', 0):.1f}%</strong></td></tr>
        </table>
    </div>
    
    <div class="section">
        <h2>🎯 전략별 성과</h2>
        <table>
            <tr><th>전략</th><th>거래 수</th><th>승률</th><th>평균 수익</th></tr>
"""
        
        for strategy, perf in data.get('strategy_performance', {}).items():
            html += f"""
            <tr>
                <td>{strategy}</td>
                <td>{perf.get('trades', 0)}회</td>
                <td>{perf.get('win_rate', 0):.1f}%</td>
                <td class="{'positive' if perf.get('avg_profit', 0) > 0 else 'negative'}">
                    {perf.get('avg_profit', 0):+.2f}%
                </td>
            </tr>
"""
        
        html += f"""
        </table>
    </div>
    
    <div class="section">
        <h2>💸 수수료</h2>
        <p>총 수수료: {data.get('fees', 0):,.0f}원</p>
    </div>
    
    <div class="section">
        <h2>📅 일별 손익</h2>
        <table>
            <tr><th>날짜</th><th>손익</th></tr>
"""
        
        for day, profit in data.get('daily_profits', {}).items():
            profit_class = "positive" if profit > 0 else "negative"
            html += f'<tr><td>{day}</td><td class="{profit_class}">{profit:+,.0f}원</td></tr>\n'
        
        html += """
        </table>
    </div>
    
    <div style="text-align: center; margin-top: 30px; color: #888;">
        <p>Upbit AutoProfit Bot - Automated Trading System</p>
    </div>
</body>
</html>
"""
        return html
    
    def _generate_monthly_html(self, data: Dict) -> str:
        """월간 리포트 HTML 생성 (주간과 유사하지만 더 상세)"""
        # 주간 리포트와 동일한 구조, 기간만 월간
        return self._generate_weekly_html(data)
