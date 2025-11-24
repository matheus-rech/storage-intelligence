#!/bin/bash

echo "=========================================="
echo "📱 STORAGE INTELLIGENCE - INSTALLATION"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Node.js is installed
echo "🔍 Checking dependencies..."
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js not found${NC}"
    echo ""
    echo "Please install Node.js first:"
    echo "  brew install node"
    echo ""
    echo "Or download from: https://nodejs.org"
    exit 1
fi

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found${NC}"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

echo -e "${GREEN}✅ Node.js $(node --version)${NC}"
echo -e "${GREEN}✅ Python $(python3 --version)${NC}"
echo ""

# Install Node dependencies
echo "📦 Installing Node.js dependencies..."
npm install
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Dependencies installed${NC}"
echo ""

# Build the application
echo "🏗️  Building macOS application..."
npm run build-mac
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Build failed${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Build complete${NC}"
echo ""

# Install to Applications
echo "📲 Installing to Applications folder..."
if [ -d "dist/mac/Storage Intelligence.app" ]; then
    sudo cp -R "dist/mac/Storage Intelligence.app" /Applications/
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Installed to /Applications${NC}"
    else
        echo -e "${RED}❌ Failed to install (try running with sudo)${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ Build output not found${NC}"
    exit 1
fi
echo ""

# Create Desktop shortcut (optional)
read -p "Create Desktop shortcut? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    ln -sf "/Applications/Storage Intelligence.app" ~/Desktop/
    echo -e "${GREEN}✅ Desktop shortcut created${NC}"
fi
echo ""

# Success message
echo "=========================================="
echo -e "${GREEN}🎉 INSTALLATION COMPLETE!${NC}"
echo "=========================================="
echo ""
echo "To launch the app:"
echo "  • Open from Applications folder"
echo "  • Or use Spotlight: Cmd+Space, type 'Storage Intelligence'"
echo ""
echo "First time?"
echo "  1. Click 'Run Analysis' to scan your Mac"
echo "  2. Wait 5-10 minutes for complete scan"
echo "  3. Review recommendations"
echo "  4. Execute actions with one click!"
echo ""
echo "Need help?"
echo "  • Open the app and go to Help menu"
echo "  • Or read: cat INSTALLATION.md"
echo ""
echo -e "${BLUE}Enjoy your organized Mac! 💾${NC}"
echo ""
