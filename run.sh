#!/bin/bash

# Upbit AutoProfit Bot - 빠른 실행 스크립트
# 이 스크립트는 봇을 쉽게 실행할 수 있도록 도와줍니다.

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║           🚀 Upbit AutoProfit Bot 🚀                        ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# 색상 정의
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Python 확인
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3가 설치되지 않았습니다!${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python3 발견: $(python3 --version)${NC}"

# 가상환경 확인
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 가상환경이 없습니다. 생성 중...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ 가상환경 생성 완료!${NC}"
fi

# 가상환경 활성화
echo -e "${GREEN}🔧 가상환경 활성화 중...${NC}"
source venv/bin/activate

# 의존성 확인 및 설치
if [ ! -f "venv/lib/python*/site-packages/pyupbit/__init__.py" ]; then
    echo -e "${YELLOW}📦 의존성 패키지 설치 중...${NC}"
    pip install -q -r requirements.txt
    echo -e "${GREEN}✅ 의존성 설치 완료!${NC}"
fi

# .env 파일 확인
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env 파일이 없습니다!${NC}"
    echo -e "${YELLOW}   .env.example을 복사하여 API 키를 입력하세요.${NC}"
    cp .env.example .env
    echo -e "${GREEN}✅ .env 파일 생성 완료!${NC}"
    echo -e "${RED}   ⚠️  .env 파일을 편집하여 Upbit API 키를 입력해주세요!${NC}"
    echo ""
    read -p "API 키를 입력하셨나요? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${RED}API 키를 먼저 입력해주세요!${NC}"
        exit 1
    fi
fi

# 모드 선택
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  거래 모드를 선택하세요:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  1) backtest  - 백테스트 (실제 거래 없음, API 키 불필요)"
echo "  2) paper     - 모의투자 (가상 거래)"
echo "  3) live      - 실거래 (⚠️  실제 자금 사용!)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
read -p "선택 (1-3): " mode_choice

case $mode_choice in
    1)
        MODE="backtest"
        ;;
    2)
        MODE="paper"
        ;;
    3)
        MODE="live"
        echo ""
        echo -e "${RED}╔══════════════════════════════════════════════════════════════╗${NC}"
        echo -e "${RED}║                                                              ║${NC}"
        echo -e "${RED}║                  ⚠️  경고: 실거래 모드 ⚠️                   ║${NC}"
        echo -e "${RED}║                                                              ║${NC}"
        echo -e "${RED}║  실제 자금이 사용되며 손실이 발생할 수 있습니다!             ║${NC}"
        echo -e "${RED}║                                                              ║${NC}"
        echo -e "${RED}╚══════════════════════════════════════════════════════════════╝${NC}"
        echo ""
        read -p "정말 실거래를 진행하시겠습니까? (yes/no): " confirm
        if [ "$confirm" != "yes" ]; then
            echo -e "${YELLOW}취소되었습니다.${NC}"
            exit 0
        fi
        ;;
    *)
        echo -e "${RED}잘못된 선택입니다. 백테스트 모드로 실행합니다.${NC}"
        MODE="backtest"
        ;;
esac

# 봇 실행
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🚀 봇 시작 중... (모드: $MODE)${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${YELLOW}💡 중지하려면 Ctrl+C를 누르세요${NC}"
echo ""

python3 src/main.py --mode $MODE
