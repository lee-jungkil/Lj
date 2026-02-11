"""
뉴스/감정 분석 모듈
암호화폐 관련 뉴스와 시장 감정 분석
"""

import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import re


class SentimentAnalyzer:
    """감정 분석 클래스"""
    
    def __init__(self, news_api_key: str = ""):
        """
        초기화
        
        Args:
            news_api_key: News API 키 (선택)
        """
        self.news_api_key = news_api_key
        
        # 감정 키워드
        self.positive_keywords = [
            '상승', '급등', '돌파', '강세', '호재', '긍정', '성공', 
            '채택', '협력', '투자', '증가', '확대', '개선', '발전',
            'bull', 'bullish', 'surge', 'rise', 'gain', 'positive',
            'adoption', 'partnership', 'upgrade'
        ]
        
        self.negative_keywords = [
            '하락', '급락', '붕괴', '약세', '악재', '부정', '실패',
            '규제', '금지', '해킹', '사기', '감소', '축소', '악화',
            'bear', 'bearish', 'crash', 'fall', 'drop', 'negative',
            'regulation', 'ban', 'hack', 'scam', 'decline'
        ]
    
    def get_upbit_notices(self) -> List[Dict]:
        """
        업비트 공지사항 가져오기
        
        Returns:
            공지사항 리스트
        """
        try:
            url = "https://api.upbit.com/v1/notices"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                notices = response.json()
                return notices[:10]  # 최근 10개
            
            return []
        except Exception as e:
            print(f"❌ 업비트 공지 조회 실패: {e}")
            return []
    
    def analyze_text_sentiment(self, text: str) -> float:
        """
        텍스트 감정 점수 계산
        
        Args:
            text: 분석할 텍스트
        
        Returns:
            감정 점수 (0.0 ~ 1.0)
            - 0.0 ~ 0.3: 부정
            - 0.3 ~ 0.7: 중립
            - 0.7 ~ 1.0: 긍정
        """
        text_lower = text.lower()
        
        positive_count = sum(1 for keyword in self.positive_keywords if keyword in text_lower)
        negative_count = sum(1 for keyword in self.negative_keywords if keyword in text_lower)
        
        total_count = positive_count + negative_count
        
        if total_count == 0:
            return 0.5  # 중립
        
        # 긍정 비율 계산
        positive_ratio = positive_count / total_count
        
        return positive_ratio
    
    def get_market_sentiment(self) -> Dict[str, any]:
        """
        시장 전반 감정 분석
        
        Returns:
            감정 분석 결과
        """
        sentiment_data = {
            'timestamp': datetime.now().isoformat(),
            'score': 0.5,
            'label': 'NEUTRAL',
            'sources': []
        }
        
        # 업비트 공지사항 분석
        notices = self.get_upbit_notices()
        if notices:
            notice_sentiments = []
            for notice in notices:
                title = notice.get('title', '')
                sentiment = self.analyze_text_sentiment(title)
                notice_sentiments.append(sentiment)
                
                sentiment_data['sources'].append({
                    'type': 'upbit_notice',
                    'title': title,
                    'sentiment': sentiment
                })
            
            if notice_sentiments:
                avg_sentiment = sum(notice_sentiments) / len(notice_sentiments)
                sentiment_data['score'] = avg_sentiment
        
        # 감정 라벨
        if sentiment_data['score'] < 0.3:
            sentiment_data['label'] = 'NEGATIVE'
        elif sentiment_data['score'] > 0.7:
            sentiment_data['label'] = 'POSITIVE'
        else:
            sentiment_data['label'] = 'NEUTRAL'
        
        return sentiment_data
    
    def get_coin_sentiment(self, ticker: str) -> Dict[str, any]:
        """
        특정 코인 감정 분석
        
        Args:
            ticker: 코인 티커 (예: KRW-BTC)
        
        Returns:
            감정 분석 결과
        """
        coin_name = ticker.split('-')[1] if '-' in ticker else ticker
        
        sentiment_data = {
            'ticker': ticker,
            'timestamp': datetime.now().isoformat(),
            'score': 0.5,
            'label': 'NEUTRAL',
            'sources': []
        }
        
        # 업비트 공지사항에서 코인 관련 검색
        notices = self.get_upbit_notices()
        coin_notices = [n for n in notices if coin_name.upper() in n.get('title', '').upper()]
        
        if coin_notices:
            notice_sentiments = []
            for notice in coin_notices:
                title = notice.get('title', '')
                sentiment = self.analyze_text_sentiment(title)
                notice_sentiments.append(sentiment)
                
                sentiment_data['sources'].append({
                    'type': 'upbit_notice',
                    'title': title,
                    'sentiment': sentiment
                })
            
            avg_sentiment = sum(notice_sentiments) / len(notice_sentiments)
            sentiment_data['score'] = avg_sentiment
        
        # 감정 라벨
        if sentiment_data['score'] < 0.3:
            sentiment_data['label'] = 'NEGATIVE'
        elif sentiment_data['score'] > 0.7:
            sentiment_data['label'] = 'POSITIVE'
        else:
            sentiment_data['label'] = 'NEUTRAL'
        
        return sentiment_data
    
    def should_trade_based_on_sentiment(self, sentiment_score: float) -> tuple[bool, str]:
        """
        감정 점수 기반 거래 여부 판단
        
        Args:
            sentiment_score: 감정 점수 (0.0 ~ 1.0)
        
        Returns:
            (거래 가능 여부, 사유)
        """
        if sentiment_score < 0.2:
            return False, "극도로 부정적인 시장 감정 (신규 진입 제한)"
        
        if sentiment_score < 0.3:
            return True, "부정적 감정 (보수적 전략 권장)"
        
        if sentiment_score > 0.8:
            return True, "매우 긍정적 감정 (공격적 전략 가능)"
        
        return True, "중립적 감정 (일반 전략 유지)"
    
    def get_sentiment_adjusted_weights(self, base_weights: Dict[str, float], sentiment_score: float) -> Dict[str, float]:
        """
        감정 점수에 따른 전략 가중치 조정
        
        Args:
            base_weights: 기본 전략 가중치
            sentiment_score: 감정 점수
        
        Returns:
            조정된 가중치
        """
        adjusted_weights = base_weights.copy()
        
        # 긍정적 감정 (0.7~1.0): 공격적 전략 강화
        if sentiment_score > 0.7:
            adjusted_weights['aggressive_scalping'] = min(1.0, adjusted_weights.get('aggressive_scalping', 0.25) * 1.3)
            adjusted_weights['conservative_scalping'] = adjusted_weights.get('conservative_scalping', 0.25) * 0.8
        
        # 부정적 감정 (0.0~0.3): 보수적 전략 강화
        elif sentiment_score < 0.3:
            adjusted_weights['aggressive_scalping'] = adjusted_weights.get('aggressive_scalping', 0.25) * 0.5
            adjusted_weights['conservative_scalping'] = min(1.0, adjusted_weights.get('conservative_scalping', 0.25) * 1.5)
            adjusted_weights['mean_reversion'] = min(1.0, adjusted_weights.get('mean_reversion', 0.25) * 1.2)
        
        # 가중치 정규화
        total = sum(adjusted_weights.values())
        if total > 0:
            adjusted_weights = {k: v/total for k, v in adjusted_weights.items()}
        
        return adjusted_weights
