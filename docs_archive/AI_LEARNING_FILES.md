# 📊 AI 학습 데이터 파일 목록

## 📁 학습 데이터 저장 위치

AI 학습 데이터는 다음 디렉토리에 저장됩니다:

---

## 🎯 주요 학습 데이터 파일

### 1. 거래 경험 데이터 (LearningEngine)

**디렉토리**: `trading_logs/learning/`

#### `experiences.json`
- **용도**: 모든 거래 경험 데이터 저장
- **내용**:
  - 거래 기본 정보 (시간, 티커, 전략, 액션)
  - 진입 정보 (진입가, 투자금액)
  - 청산 정보 (청산가, 손익, 손익률, 보유시간)
  - 시장 상황 (진입 시점의 시장 데이터)
  - 결과 (성공/실패)
- **최대 저장**: 10,000개 경험
- **형식**: JSON

**예시 구조**:
```json
[
  {
    "timestamp": "2026-02-11 14:30:26",
    "ticker": "KRW-BTC",
    "strategy": "aggressive_scalping",
    "action": "SELL",
    "entry_price": 95234000.0,
    "entry_amount": 50000.0,
    "exit_price": 97568000.0,
    "profit_loss": 1230.0,
    "profit_loss_ratio": 2.45,
    "holding_duration": 900.0,
    "market_condition": {
      "price": 95234000.0,
      "rsi": 65.3,
      "macd": 234.5,
      "volume_ratio": 1.8,
      "trend": "up"
    },
    "success": true
  }
]
```

#### `strategy_stats.json`
- **용도**: 전략별 성과 통계
- **내용**:
  - 총 거래 수
  - 수익 거래 수
  - 손실 거래 수
  - 총 손익
  - 승률
  - 평균 손익
  - 평균 보유시간
- **형식**: JSON

**예시 구조**:
```json
{
  "aggressive_scalping": {
    "total_trades": 123,
    "winning_trades": 78,
    "losing_trades": 45,
    "total_profit_loss": 45300.0,
    "win_rate": 63.4,
    "avg_profit_loss": 368.3,
    "avg_holding_time": 1200.0
  },
  "conservative_scalping": {
    "total_trades": 89,
    "winning_trades": 62,
    "losing_trades": 27,
    "total_profit_loss": 32100.0,
    "win_rate": 69.7,
    "avg_profit_loss": 360.7,
    "avg_holding_time": 1800.0
  }
}
```

#### `optimized_params.json`
- **용도**: 학습된 최적 파라미터
- **내용**: AI가 학습한 최적화된 전략 파라미터
- **형식**: JSON

**예시 구조**:
```json
{
  "aggressive_scalping": {
    "stop_loss": -2.1,
    "take_profit": 1.6,
    "rsi_buy_threshold": 28,
    "rsi_sell_threshold": 72
  },
  "conservative_scalping": {
    "stop_loss": -1.3,
    "take_profit": 0.9,
    "rsi_buy_threshold": 38,
    "rsi_sell_threshold": 62
  }
}
```

---

### 2. 보유 시간 최적화 (HoldingTimeOptimizer)

**디렉토리**: `trading_logs/learning/`

#### `holding_times.json`
- **용도**: 코인별/전략별 보유 시간 학습 데이터
- **내용**:
  - 티커별 보유 시간 기록
  - 전략별 최적 보유 시간
  - 수익률과 보유 시간 상관관계
- **형식**: JSON

**예시 구조**:
```json
{
  "KRW-BTC": {
    "aggressive_scalping": {
      "optimal_holding_time": 900.0,
      "avg_profit_at_optimal": 1.8,
      "total_samples": 45
    },
    "conservative_scalping": {
      "optimal_holding_time": 1800.0,
      "avg_profit_at_optimal": 1.2,
      "total_samples": 32
    }
  },
  "KRW-ETH": {
    "aggressive_scalping": {
      "optimal_holding_time": 1200.0,
      "avg_profit_at_optimal": 2.1,
      "total_samples": 38
    }
  }
}
```

---

### 3. 전략 성능 (StrategySelector)

**디렉토리**: `trading_logs/learning/`

#### `strategy_performance.json`
- **용도**: 전략별 실시간 성능 데이터
- **내용**:
  - 시간대별 전략 성능
  - 시장 상황별 전략 성능
  - 최근 성과 추이
- **형식**: JSON

**예시 구조**:
```json
{
  "aggressive_scalping": {
    "morning_rush": {
      "win_rate": 68.5,
      "avg_profit": 1.8,
      "sample_count": 45
    },
    "midday": {
      "win_rate": 52.3,
      "avg_profit": 0.9,
      "sample_count": 67
    }
  },
  "conservative_scalping": {
    "afternoon_rush": {
      "win_rate": 71.2,
      "avg_profit": 1.2,
      "sample_count": 52
    }
  }
}
```

---

### 4. 적응형 학습 (AdaptiveLearner)

**디렉토리**: `trading_logs/learning/`

#### `adaptive_stats.json`
- **용도**: 적응형 학습 통계
- **내용**:
  - 시장 변화 감지
  - 전략 적응 기록
  - 학습 성과 추이
- **형식**: JSON

**예시 구조**:
```json
{
  "market_adaptations": [
    {
      "timestamp": "2026-02-11 10:00:00",
      "detected_change": "volatility_increase",
      "strategy_adjustment": "reduce_position_size",
      "result": "positive"
    }
  ],
  "learning_progress": {
    "total_adaptations": 234,
    "successful_adaptations": 178,
    "success_rate": 76.1
  }
}
```

---

### 5. 자동 최적화 (AutoOptimizer)

**디렉토리**: `learning_data/optimization/`

#### `optimization_history.json`
- **용도**: 파라미터 최적화 기록
- **내용**:
  - 최적화 실행 기록
  - 파라미터 변경 이력
  - 최적화 결과
- **형식**: JSON

**예시 구조**:
```json
{
  "optimizations": [
    {
      "timestamp": "2026-02-11 00:00:00",
      "strategy": "aggressive_scalping",
      "old_params": {
        "stop_loss": -2.0,
        "take_profit": 1.5
      },
      "new_params": {
        "stop_loss": -2.1,
        "take_profit": 1.6
      },
      "improvement": 8.5
    }
  ]
}
```

---

### 6. 손실 분석 (LossAnalyzer)

**디렉토리**: `learning_data/losses/`

#### `loss_analysis.json`
- **용도**: 손실 패턴 분석
- **내용**:
  - 손실 원인 분류
  - 패턴별 손실 통계
  - 개선 제안
- **형식**: JSON

**예시 구조**:
```json
{
  "loss_patterns": {
    "premature_exit": {
      "count": 23,
      "avg_loss": -1.2,
      "improvement_suggestion": "increase_holding_time"
    },
    "late_exit": {
      "count": 18,
      "avg_loss": -2.8,
      "improvement_suggestion": "faster_stop_loss"
    }
  },
  "total_losses": 45,
  "total_loss_amount": -67500.0
}
```

---

## 📂 전체 디렉토리 구조

```
프로젝트 루트/
├── trading_logs/
│   └── learning/
│       ├── experiences.json          # 거래 경험 (10,000개 최대)
│       ├── strategy_stats.json       # 전략별 통계
│       ├── optimized_params.json     # 최적 파라미터
│       ├── holding_times.json        # 보유 시간 학습
│       ├── strategy_performance.json # 전략 성능
│       └── adaptive_stats.json       # 적응형 학습
│
└── learning_data/
    ├── optimization/
    │   └── optimization_history.json # 최적화 기록
    │
    └── losses/
        └── loss_analysis.json        # 손실 분석
```

---

## 🔍 파일 확인 방법

### Windows
```batch
REM 학습 데이터 디렉토리 확인
dir trading_logs\learning
dir learning_data\optimization
dir learning_data\losses

REM 특정 파일 확인
type trading_logs\learning\experiences.json
type trading_logs\learning\strategy_stats.json
```

### Linux/Unix
```bash
# 학습 데이터 디렉토리 확인
ls -la trading_logs/learning/
ls -la learning_data/optimization/
ls -la learning_data/losses/

# 특정 파일 확인
cat trading_logs/learning/experiences.json
cat trading_logs/learning/strategy_stats.json

# JSON 파일 예쁘게 보기
python -m json.tool trading_logs/learning/strategy_stats.json
```

---

## 💾 데이터 저장 시점

### 자동 저장
1. **봇 종료 시**: 모든 학습 데이터 자동 저장
2. **주기적 저장**: 100개 거래마다 자동 저장
3. **전략 변경 시**: 통계 자동 저장

### 수동 저장
코드에서 명시적으로 호출:
```python
# 경험 데이터 저장
learning_engine.save_experiences()

# 전략 통계 저장
learning_engine.save_strategy_stats()

# 최적 파라미터 저장
learning_engine.save_optimized_params()
```

---

## 🔄 데이터 로드

봇 시작 시 자동으로 이전 학습 데이터 로드:

```python
# 자동 로드
learning_engine = LearningEngine()
learning_engine.load_experiences()
learning_engine.load_strategy_stats()
learning_engine.load_optimized_params()
```

---

## 📊 데이터 크기 관리

### 최대 저장 개수
- **experiences.json**: 10,000개 (초과 시 오래된 것부터 삭제)
- **strategy_stats.json**: 제한 없음 (전략별 누적)
- **holding_times.json**: 코인당 최대 5,000개
- **optimization_history.json**: 제한 없음 (시간순 기록)

### 디스크 공간
- 평균 파일 크기:
  - experiences.json: 5-10MB (10,000개 기준)
  - strategy_stats.json: 50-100KB
  - 기타 파일: 각 10-50KB

---

## 🛠️ 유지보수

### 데이터 백업
```bash
# 학습 데이터 백업
cp -r trading_logs/learning backup/learning_$(date +%Y%m%d)
cp -r learning_data backup/learning_data_$(date +%Y%m%d)
```

### 데이터 초기화
```bash
# 학습 데이터 초기화 (신중하게!)
rm -rf trading_logs/learning/*.json
rm -rf learning_data/**/*.json
```

### 데이터 확인
```python
# Python에서 확인
import json

# 경험 데이터 확인
with open('trading_logs/learning/experiences.json', 'r') as f:
    experiences = json.load(f)
    print(f"총 경험: {len(experiences)}개")

# 전략 통계 확인
with open('trading_logs/learning/strategy_stats.json', 'r') as f:
    stats = json.load(f)
    for strategy, data in stats.items():
        print(f"{strategy}: 승률 {data['win_rate']:.1f}%")
```

---

## 🎯 요약

**주요 학습 파일 (8개)**:

1. **experiences.json** - 거래 경험 데이터베이스
2. **strategy_stats.json** - 전략별 성과 통계
3. **optimized_params.json** - AI 학습 파라미터
4. **holding_times.json** - 보유 시간 최적화
5. **strategy_performance.json** - 전략 성능 분석
6. **adaptive_stats.json** - 적응형 학습 통계
7. **optimization_history.json** - 최적화 기록
8. **loss_analysis.json** - 손실 패턴 분석

**저장 위치**:
- `trading_logs/learning/` (주요 학습 데이터)
- `learning_data/optimization/` (최적화 기록)
- `learning_data/losses/` (손실 분석)

**자동 관리**: 
- ✅ 봇 종료 시 자동 저장
- ✅ 봇 시작 시 자동 로드
- ✅ 주기적 백업 권장

---

**이 파일들이 AI 학습의 핵심입니다!** 📚
