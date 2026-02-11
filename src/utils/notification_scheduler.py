"""
알림 스케줄러
일일/주간/월간 알림 자동 전송
"""

import time
import threading
from datetime import datetime
from typing import Callable, Dict


class NotificationScheduler:
    """알림 스케줄링 관리"""
    
    def __init__(self, telegram_notifier, email_reporter, get_summary_callback: Callable):
        """
        Args:
            telegram_notifier: 텔레그램 알림기
            email_reporter: 이메일 리포터
            get_summary_callback: 요약 데이터 가져오는 콜백 함수
        """
        self.telegram = telegram_notifier
        self.email = email_reporter
        self.get_summary = get_summary_callback
        
        self.running = False
        self.thread = None
        
        # 마지막 전송 시간
        self.last_daily_telegram = None
        self.last_weekly_email = None
        self.last_monthly_email = None
    
    def start(self):
        """스케줄러 시작 (백그라운드 스레드)"""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.thread.start()
        print("✅ 알림 스케줄러 시작")
    
    def stop(self):
        """스케줄러 중지"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("⏹️ 알림 스케줄러 중지")
    
    def _scheduler_loop(self):
        """스케줄 체크 루프 (1분마다)"""
        while self.running:
            try:
                now = datetime.now()
                
                # 일일 텔레그램 알림 (오전 10시, 오후 5시)
                if now.hour in [10, 17] and now.minute == 0:
                    today_key = now.strftime('%Y-%m-%d-%H')
                    if self.last_daily_telegram != today_key:
                        self._send_daily_telegram()
                        self.last_daily_telegram = today_key
                
                # 주간 이메일 (월요일 오전 10시)
                if now.weekday() == 0 and now.hour == 10 and now.minute == 0:
                    week_key = now.strftime('%Y-W%U')
                    if self.last_weekly_email != week_key:
                        self._send_weekly_email()
                        self.last_weekly_email = week_key
                
                # 월간 이메일 (매월 1일 오전 10시)
                if now.day == 1 and now.hour == 10 and now.minute == 0:
                    month_key = now.strftime('%Y-%m')
                    if self.last_monthly_email != month_key:
                        self._send_monthly_email()
                        self.last_monthly_email = month_key
                
                # 1분 대기
                time.sleep(60)
            except Exception as e:
                print(f"❌ 스케줄러 오류: {e}")
                time.sleep(60)
    
    def _send_daily_telegram(self):
        """일일 텔레그램 요약 전송"""
        try:
            summary = self.get_summary('daily')
            if self.telegram.enabled:
                self.telegram.send_daily_summary(summary)
                print(f"📤 일일 텔레그램 알림 전송 완료")
        except Exception as e:
            print(f"❌ 일일 텔레그램 전송 실패: {e}")
    
    def _send_weekly_email(self):
        """주간 이메일 리포트 전송"""
        try:
            report = self.get_summary('weekly')
            if self.email.enabled:
                self.email.send_weekly_report(report)
                print(f"📧 주간 이메일 리포트 전송 완료")
        except Exception as e:
            print(f"❌ 주간 이메일 전송 실패: {e}")
    
    def _send_monthly_email(self):
        """월간 이메일 리포트 전송"""
        try:
            report = self.get_summary('monthly')
            if self.email.enabled:
                self.email.send_monthly_report(report)
                print(f"📧 월간 이메일 리포트 전송 완료")
        except Exception as e:
            print(f"❌ 월간 이메일 전송 실패: {e}")
