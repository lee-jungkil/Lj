#!/bin/bash
# Update Files Auto-Download Script for Linux/Mac
# Downloads ONLY the update folder from GitHub

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${YELLOW}============================================================${NC}"
echo -e "${YELLOW} Upbit AutoProfit Bot - Update Files Downloader${NC}"
echo -e "${YELLOW}============================================================${NC}"
echo
echo "This script will download update files from GitHub"
echo

# Create update directory
echo -e "${CYAN}Creating update directory...${NC}"
mkdir -p update
cd update

# Base URL
BASE_URL="https://raw.githubusercontent.com/lee-jungkil/Lj/main/update"

# Function to download file
download_file() {
    local file=$1
    local required=$2
    local status
    
    if [ "$required" = "true" ]; then
        status="${GREEN}[REQUIRED]${NC}"
    else
        status="${CYAN}[OPTIONAL]${NC}"
    fi
    
    echo -e "${status} Downloading ${file}..."
    
    if command -v wget &> /dev/null; then
        wget -q "$BASE_URL/$file" -O "$file" && \
        echo -e "  ${GREEN}+ Downloaded: ${file}${NC}" || \
        echo -e "  ${RED}! Failed: ${file}${NC}"
    elif command -v curl &> /dev/null; then
        curl -sS -L "$BASE_URL/$file" -o "$file" && \
        echo -e "  ${GREEN}+ Downloaded: ${file}${NC}" || \
        echo -e "  ${RED}! Failed: ${file}${NC}"
    else
        echo -e "  ${RED}! Error: Neither wget nor curl is installed${NC}"
        return 1
    fi
}

# Download files
SUCCESS_COUNT=0
FAIL_COUNT=0

echo
echo -e "${CYAN}[1/7] Downloading UPDATE.bat (required)...${NC}"
download_file "UPDATE.bat" "true" && ((SUCCESS_COUNT++)) || ((FAIL_COUNT++))

echo
echo -e "${CYAN}[2/7] Downloading fixed_screen_display.py (required)...${NC}"
download_file "fixed_screen_display.py" "true" && ((SUCCESS_COUNT++)) || ((FAIL_COUNT++))

echo
echo -e "${CYAN}[3/7] Downloading UPDATE_README.md (optional)...${NC}"
download_file "UPDATE_README.md" "false" && ((SUCCESS_COUNT++)) || ((FAIL_COUNT++))

echo
echo -e "${CYAN}[4/7] Downloading SELL_HISTORY_UPDATE.md (optional)...${NC}"
download_file "SELL_HISTORY_UPDATE.md" "false" && ((SUCCESS_COUNT++)) || ((FAIL_COUNT++))

echo
echo -e "${CYAN}[5/7] Downloading UPDATE_GUIDE.md (optional)...${NC}"
download_file "UPDATE_GUIDE.md" "false" && ((SUCCESS_COUNT++)) || ((FAIL_COUNT++))

echo
echo -e "${CYAN}[6/7] Downloading test_sell_history.py (optional)...${NC}"
download_file "test_sell_history.py" "false" && ((SUCCESS_COUNT++)) || ((FAIL_COUNT++))

echo
echo -e "${CYAN}[7/7] Downloading UPDATE_KR.bat (optional)...${NC}"
download_file "UPDATE_KR.bat" "false" && ((SUCCESS_COUNT++)) || ((FAIL_COUNT++))

echo
echo -e "${YELLOW}============================================================${NC}"
echo -e "${YELLOW} Download Complete!${NC}"
echo -e "${YELLOW}============================================================${NC}"
echo
echo -e "${CYAN}Summary:${NC}"
echo -e "  ${GREEN}Success: $SUCCESS_COUNT files${NC}"
echo -e "  ${RED}Failed:  $FAIL_COUNT files${NC}"
echo -e "  ${CYAN}Location: $(pwd)${NC}"
echo
echo -e "${YELLOW}Next Steps:${NC}"
echo "  1. Move this 'update' folder to your Lj-main project root"
echo "  2. Navigate to: Lj-main/update/"
echo "  3. Copy files: cp update/fixed_screen_display.py src/utils/"
echo
echo -e "${CYAN}For Windows users:${NC}"
echo "  Run: UPDATE.bat"
echo
