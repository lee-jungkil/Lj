"""
거래 로그 시스템
거래 내역, 에러, 성과를 JSON 형식으로 저장
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import colorlog


class TradingLogger:
    """거래 로깅 클래스"""
    
    def __init__(self, log_dir: str = "trading_logs"):
        """
        초기화
        
        Args:
            log_dir: 로그 저장 디렉토리
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # 거래 로그 파일 경로 (먼저 정의)
        self.trade_log_path = self.log_dir / f"trade_{datetime.now().strftime('%Y%m%d')}.json"
        self.error_log_path = self.log_dir / f"error_{datetime.now().strftime('%Y%m%d')}.log"
        
        # 컬러 로거 설정
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """컬러 로거 설정 (고정 화면 모드: 콘솔 출력 완전 제거)"""
        logger = logging.getLogger('TradingBot')
        
        # ⭐ 콘솔 출력 완전 차단: 레벨을 CRITICAL보다 높게 설정
        logger.setLevel(logging.CRITICAL + 1)
        
        # 핸들러가 이미 있으면 추가하지 않음
        if logger.handlers:
            return logger
        
        # 파일 핸들러만 추가 (에러 로그용)
        file_handler = logging.FileHandler(self.error_log_path, encoding='utf-8')
        file_handler.setLevel(logging.ERROR)
        file_formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        # ⭐ 부모 로거로의 전파 차단
        logger.propagate = False
        
        return logger
    
    def log_trade(self, 
                  action: str, 
                  ticker: str, 
                  price: float, 
                  amount: float, 
                  strategy: str,
                  reason: str = "",
                  profit_loss: float = 0.0,
                  balance: float = 0.0,
                  metadata: Optional[Dict[str, Any]] = None):
        """
        거래 로그 저장
        
        Args:
            action: 거래 행동 (BUY, SELL)
            ticker: 코인 티커
            price: 거래 가격
            amount: 거래 수량
            strategy: 사용한 전략
            reason: 거래 이유
            profit_loss: 손익
            balance: 잔고
            metadata: 추가 메타데이터
        """
        trade_data = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "ticker": ticker,
            "price": price,
            "amount": amount,
            "total_krw": price * amount,
            "strategy": strategy,
            "reason": reason,
            "profit_loss": profit_loss,
            "balance": balance,
            "metadata": metadata or {}
        }
        
        # JSON 파일에 추가
        try:
            # 기존 데이터 로드 (안전장치 추가)
            trades = []
            if self.trade_log_path.exists():
                try:
                    with open(self.trade_log_path, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                        if content:  # 파일이 비어있지 않을 때만 로드
                            trades = json.loads(content)
                        if not isinstance(trades, list):  # 리스트가 아니면 초기화
                            trades = []
                except json.JSONDecodeError as e:
                    self.logger.warning(f"⚠️ 기존 로그 파일 손상 감지 - 백업 후 새로 시작: {e}")
                    # 손상된 파일 백업 (기존 백업 파일 삭제 후 생성)
                    backup_path = self.trade_log_path.with_suffix('.json.backup')
                    if backup_path.exists():
                        backup_path.unlink()  # 기존 백업 삭제
                    self.trade_log_path.rename(backup_path)
                    trades = []
            
            # 새 거래 추가
            trades.append(trade_data)
            
            # 저장 (안전하게)
            with open(self.trade_log_path, 'w', encoding='utf-8') as f:
                json.dump(trades, f, ensure_ascii=False, indent=2)
            
            # 콘솔 출력
            emoji = "🟢" if action == "BUY" else "🔴"
            self.logger.info(
                f"{emoji} {action} | {ticker} | "
                f"가격: {price:,.0f} | 수량: {amount:.8f} | "
                f"전략: {strategy} | 손익: {profit_loss:+,.0f}원"
            )
            
        except Exception as e:
            self.logger.error(f"거래 로그 저장 실패: {e}")
            # 저장 실패해도 콘솔 출력은 시도
            try:
                emoji = "🟢" if action == "BUY" else "🔴"
                self.logger.info(
                    f"{emoji} {action} | {ticker} | "
                    f"가격: {price:,.0f} | 수량: {amount:.8f} | "
                    f"전략: {strategy}"
                )
            except:
                pass
    
    def log_signal(self, ticker: str, signal: str, strategy: str, indicators: Dict[str, Any]):
        """
        매매 신호 로그
        
        Args:
            ticker: 코인 티커
            signal: 신호 (BUY, SELL, HOLD)
            strategy: 전략 이름
            indicators: 지표 데이터
        """
        self.logger.debug(
            f"📊 신호 | {ticker} | {signal} | {strategy} | "
            f"지표: {indicators}"
        )
    
    def log_error(self, error_type: str, message: str, exception: Optional[Exception] = None):
        """
        에러 로그
        
        Args:
            error_type: 에러 타입
            message: 에러 메시지
            exception: 예외 객체
        """
        error_msg = f"{error_type}: {message}"
        if exception:
            error_msg += f" | Exception: {str(exception)}"
        
        self.logger.error(f"❌ {error_msg}")
    
    def log_info(self, message: str):
        """정보 로그"""
        self.logger.info(message)
    
    def log_warning(self, message: str):
        """경고 로그"""
        self.logger.warning(f"⚠️ {message}")
    
    def log_performance(self, 
                       total_profit: float,
                       win_rate: float,
                       total_trades: int,
                       current_balance: float,
                       daily_profit: float):
        """
        성과 로그
        
        Args:
            total_profit: 총 수익
            win_rate: 승률
            total_trades: 총 거래 수
            current_balance: 현재 잔고
            daily_profit: 일일 수익
        """
        performance_data = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "timestamp": datetime.now().isoformat(),
            "total_profit": total_profit,
            "win_rate": win_rate,
            "total_trades": total_trades,
            "current_balance": current_balance,
            "daily_profit": daily_profit
        }
        
        # 월별 성과 파일
        month_str = datetime.now().strftime("%Y%m")
        performance_path = self.log_dir / f"performance_{month_str}.json"
        
        try:
            # 기존 데이터 로드
            if performance_path.exists():
                with open(performance_path, 'r', encoding='utf-8') as f:
                    performances = json.load(f)
            else:
                performances = []
            
            # 새 성과 추가
            performances.append(performance_data)
            
            # 저장
            with open(performance_path, 'w', encoding='utf-8') as f:
                json.dump(performances, f, ensure_ascii=False, indent=2)
            
            # 콘솔 출력
            self.logger.info(
                f"📈 성과 | 총 수익: {total_profit:+,.0f}원 | "
                f"승률: {win_rate:.1f}% | 거래 수: {total_trades} | "
                f"잔고: {current_balance:,.0f}원 | 일일 수익: {daily_profit:+,.0f}원"
            )
            
        except Exception as e:
            self.logger.error(f"성과 로그 저장 실패: {e}")
    
    def log_risk_alert(self, alert_type: str, current_value: float, limit_value: float):
        """
        리스크 경고 로그
        
        Args:
            alert_type: 경고 타입 (DAILY_LOSS, CUMULATIVE_LOSS, etc.)
            current_value: 현재 값
            limit_value: 한계 값
        """
        self.logger.warning(
            f"🚨 리스크 경고 | {alert_type} | "
            f"현재: {current_value:,.0f}원 / 한계: {limit_value:,.0f}원"
        )
    
    def get_daily_trades(self) -> list:
        """오늘의 거래 내역 가져오기"""
        try:
            if self.trade_log_path.exists():
                with open(self.trade_log_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            self.logger.error(f"거래 내역 로드 실패: {e}")
            return []
    
    def get_monthly_performance(self, year_month: str) -> Optional[Dict]:
        """
        월별 성과 가져오기
        
        Args:
            year_month: 년월 (예: "202402")
        
        Returns:
            성과 데이터
        """
        performance_path = self.log_dir / f"performance_{year_month}.json"
        try:
            if performance_path.exists():
                with open(performance_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
        except Exception as e:
            self.logger.error(f"성과 데이터 로드 실패: {e}")
            return None
    
    def clear_old_logs(self, days: int = 30):
        """
        오래된 로그 파일 삭제
        
        Args:
            days: 보관 기간 (일)
        """
        try:
            from datetime import timedelta
            cutoff_date = datetime.now() - timedelta(days=days)
            
            for log_file in self.log_dir.glob("*.json"):
                file_date = datetime.fromtimestamp(log_file.stat().st_mtime)
                if file_date < cutoff_date:
                    log_file.unlink()
                    self.logger.info(f"🗑️ 오래된 로그 삭제: {log_file.name}")
        except Exception as e:
            self.logger.error(f"로그 정리 실패: {e}")
