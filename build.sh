#!/bin/bash
# LlamaPhone Build Script
# ==========================
# Builds LlamaPhone as a standalone executable
#
# Usage:
#   ./build.sh          # Build in current directory
#   ./build.sh --clean # Clean and rebuild
#   ./build.sh --onefile # Single file executable

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   LlamaPhone Build Script${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check for clean flag
if [ "$1" = "--clean" ]; then
    echo -e "${YELLOW}Cleaning build artifacts...${NC}"
    rm -rf build dist *.spec 2>/dev/null || true
    echo -e "${GREEN}Clean complete!${NC}"
    echo ""
fi

# Check for onefile flag
ONEFILE=""
if [ "$1" = "--onefile" ]; then
    ONEFILE="--onefile"
fi

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
python --version

# Install dependencies
echo ""
echo -e "${YELLOW}Installing build dependencies...${NC}"
pip install -e . --quiet 2>/dev/null || pip install pyinstaller --quiet
pip install PyQt6 httpx ruff --quiet

# Build the application
echo ""
echo -e "${YELLOW}Building LlamaPhone executable...${NC}"
echo ""

if [ -n "$ONEFILE" ]; then
    echo -e "${YELLOW}Building single-file executable...${NC}"
    pyinstaller --onefile --windowed --name LlamaPhone llamaphone.py
else
    echo -e "${YELLOW}Building directory executable...${NC}"
    pyinstaller llamaphone.spec
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   Build Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "Executable location:"
if [ -n "$ONEFILE" ]; then
    echo -e "  ${YELLOW}dist/LlamaPhone${NC}"
else
    echo -e "  ${YELLOW}dist/LlamaPhone/LlamaPhone.exe${NC}"
fi
echo ""
