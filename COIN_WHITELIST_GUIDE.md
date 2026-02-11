# 📊 거래 코인 화이트리스트 가이드

## 🎯 현재 설정: 10개 코인

### 선정된 코인 목록
```
1. KRW-BTC   (비트코인)     - 시가총액 1위
2. KRW-ETH   (이더리움)     - 시가총액 2위
3. KRW-XRP   (리플)        - 대형 알트코인
4. KRW-ADA   (카르다노)     - 대형 알트코인
5. KRW-SOL   (솔라나)      - 고성장 L1
6. KRW-DOGE  (도지코인)     - 밈코인 대표
7. KRW-DOT   (폴카닷)      - L0 프로토콜
8. KRW-AVAX  (아발란체)     - 고속 L1
9. KRW-LINK  (체인링크)     - 오라클 선두
10. KRW-ATOM (코스모스)     - 인터체인
```

---

## 📋 선정 기준

### 1. 시가총액 (Market Cap)
```
✅ 상위 20~30위권 코인
✅ 충분한 거래량
✅ 가격 안정성
```

### 2. 유동성 (Liquidity)
```
✅ 일일 거래량 > 100억원
✅ 호가창 깊이 충분
✅ 슬리피지 최소화
```

### 3. 변동성 (Volatility)
```
✅ 적절한 변동성 (일일 2~5%)
✅ 너무 안정적 ✗ (BTC만큼)
✅ 너무 변동 심함 ✗ (저시총 알트)
```

### 4. Upbit 지원
```
✅ KRW 마켓 상장
✅ 거래 활성화
✅ 입출금 정상
```

### 5. 분산투자
```
✅ L1 블록체인: BTC, ETH, SOL, AVAX, ADA
✅ 인프라: DOT, ATOM, LINK
✅ 기타: XRP, DOGE
```

---

## 🔧 코인 추가/변경 방법

### 방법 1: config.py 직접 수정

**파일 위치:** `src/config.py`

```python
# 171번째 줄 근처
WHITELIST_COINS = [
    'KRW-BTC',   # 비트코인
    'KRW-ETH',   # 이더리움
    'KRW-XRP',   # 리플
    # ... 기존 코인들 ...
    
    # ✨ 새로운 코인 추가
    'KRW-MATIC', # 폴리곤
    'KRW-ALGO',  # 알고랜드
    'KRW-NEAR',  # 니어
]
```

### 방법 2: 전체 Upbit 코인으로 확장

**config.py 수정:**
```python
# 화이트리스트를 동적으로 가져오기
@classmethod
def get_all_krw_coins(cls) -> List[str]:
    """모든 KRW 마켓 코인 가져오기"""
    import pyupbit
    try:
        all_tickers = pyupbit.get_tickers(fiat="KRW")
        # 시가총액 상위 50개만 (선택사항)
        return all_tickers[:50]
    except:
        return cls.WHITELIST_COINS  # 실패 시 기본값
```

### 방법 3: 조건부 필터링

**시가총액 기준:**
```python
# 시총 상위 30개만
WHITELIST_COINS = get_top_market_cap_coins(limit=30)
```

**거래량 기준:**
```python
# 일일 거래량 100억 이상만
WHITELIST_COINS = get_high_volume_coins(min_volume=10_000_000_000)
```

---

## 🚀 추천 코인 추가 목록

### Tier 1: 안전한 추가 (대형 알트)
```python
'KRW-MATIC',  # 폴리곤 - L2 선두
'KRW-ALGO',   # 알고랜드 - 고속 블록체인
'KRW-SAND',   # 샌드박스 - 메타버스
'KRW-MANA',   # 디센트럴랜드 - 메타버스
'KRW-CRO',    # 크로노스 - 거래소 코인
```

### Tier 2: 중형 알트 (변동성 높음)
```python
'KRW-NEAR',   # 니어 - 샤딩 블록체인
'KRW-FTM',    # 팬텀 - 고속 L1
'KRW-HBAR',   # 헤데라 - 엔터프라이즈
'KRW-IMX',    # 이뮤터블X - NFT L2
'KRW-APT',    # 앱토스 - Meta 블록체인
```

### Tier 3: 소형 알트 (고위험/고수익)
```python
'KRW-ARDR',   # 아더
'KRW-FLOW',   # 플로우
'KRW-KLAY',   # 클레이튼
'KRW-WEMIX',  # 위믹스
```

---

## ⚙️ 설정 예시

### 1. 보수적 (10개 - 현재 설정)
```python
WHITELIST_COINS = [
    'KRW-BTC', 'KRW-ETH', 'KRW-XRP', 'KRW-ADA', 'KRW-SOL',
    'KRW-DOGE', 'KRW-DOT', 'KRW-AVAX', 'KRW-LINK', 'KRW-ATOM',
]
```
**장점:** 안정적, 유동성 높음  
**단점:** 기회 제한적

### 2. 균형형 (20개)
```python
WHITELIST_COINS = [
    # 대형 (10개)
    'KRW-BTC', 'KRW-ETH', 'KRW-XRP', 'KRW-ADA', 'KRW-SOL',
    'KRW-DOGE', 'KRW-DOT', 'KRW-AVAX', 'KRW-LINK', 'KRW-ATOM',
    # 중형 (10개)
    'KRW-MATIC', 'KRW-ALGO', 'KRW-NEAR', 'KRW-FTM', 'KRW-SAND',
    'KRW-MANA', 'KRW-CRO', 'KRW-HBAR', 'KRW-IMX', 'KRW-APT',
]
```
**장점:** 다양한 기회, 분산투자  
**단점:** 관리 복잡

### 3. 공격적 (50개+)
```python
# 모든 KRW 코인
WHITELIST_COINS = pyupbit.get_tickers(fiat="KRW")
```
**장점:** 최대 기회 포착  
**단점:** API 호출 증가, 리스크 높음

---

## 📊 코인 수에 따른 영향

### API 호출 빈도
```
10개:  매 스캔당 ~20회 호출 (안전)
20개:  매 스캔당 ~40회 호출 (안전)
50개:  매 스캔당 ~100회 호출 (주의)
100개: 매 스캔당 ~200회 호출 (위험)

Upbit 제한: 초당 10회
```

### 메모리 사용량
```
10개:  ~50MB
20개:  ~100MB
50개:  ~250MB
100개: ~500MB
```

### 학습 속도
```
10개:  집중 학습, 정확도 높음
20개:  균형적 학습
50개:  광범위 학습, 정확도 낮을 수 있음
```

---

## 💡 권장 설정

### 초보자
```python
WHITELIST_COINS = [
    'KRW-BTC',   # 비트코인만
    'KRW-ETH',   # 이더리움만
]
```
→ 안전하게 메이저 코인으로 시작

### 중급자 (현재 설정)
```python
WHITELIST_COINS = [
    # 상위 10개 대형 알트
]
```
→ 다양성과 안정성의 균형

### 고급자
```python
WHITELIST_COINS = [
    # 상위 20~30개
    # 대형 + 중형 알트 혼합
]
```
→ 더 많은 기회 포착

---

## 🔧 즉시 적용 방법

### 1단계: config.py 열기
```
메모장 또는 VS Code로 열기:
src/config.py
```

### 2단계: 171번째 줄 찾기
```python
# 코인 화이트리스트 (거래할 코인 목록)
WHITELIST_COINS = [
```

### 3단계: 코인 추가
```python
WHITELIST_COINS = [
    'KRW-BTC',
    'KRW-ETH',
    # ... 기존 코인 ...
    
    # ✨ 새로운 코인 추가
    'KRW-MATIC',  # 폴리곤
    'KRW-ALGO',   # 알고랜드
]
```

### 4단계: 저장 후 재시작
```
1. config.py 저장
2. 봇 종료 (Ctrl+C)
3. 다시 실행 (run_paper.bat 또는 run_test.bat)
```

---

## ⚠️ 주의사항

### 1. 티커 확인
```
반드시 'KRW-'로 시작
예: 'KRW-BTC' ✓
    'BTC'      ✗
    'USDT-BTC' ✗
```

### 2. Upbit 상장 여부
```
추가 전 확인:
1. Upbit에서 검색
2. KRW 마켓 거래 가능 확인
3. 입출금 정상 확인
```

### 3. 성능 고려
```
✅ 10~20개: 최적
⚠️ 30~50개: 주의
❌ 50개+:   비추천 (API 한도)
```

---

## 🎯 요약

### 현재 설정
```
✅ 10개 코인 (대형 알트)
✅ 안정적이고 유동성 높음
✅ API 호출 효율적
```

### 변경하려면
```
1. src/config.py 열기
2. WHITELIST_COINS 수정
3. 저장 후 봇 재시작
```

### 추천
```
초보: 2~5개 (BTC, ETH 중심)
중급: 10~15개 (현재 + α)
고급: 20~30개 (다양한 기회)
```

---

**더 많은 코인을 추가하시겠어요? 알려주시면 최적의 목록을 추천해드리겠습니다!**
