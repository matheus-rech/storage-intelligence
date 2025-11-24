#!/bin/bash

echo "================================================================"
echo "🚀 PUSHING TO YOUR GITHUB REPOSITORY"
echo "================================================================"
echo ""
echo "Repository: https://github.com/matheus-rech/storage-intelligence.git"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "${RED}❌ Error: Run this script from the electron-app directory${NC}"
    echo "   cd electron-app && ../push-to-github.sh"
    exit 1
fi

echo "${BLUE}Step 1: Setting up repository structure...${NC}"

# Run the GitHub setup script first
if [ -f "../setup-github-repo.sh" ]; then
    echo "${GREEN}Running setup-github-repo.sh...${NC}"
    bash ../setup-github-repo.sh
else
    echo "${YELLOW}Setup script not found, initializing git manually...${NC}"
    
    # Create .gitignore if it doesn't exist
    if [ ! -f ".gitignore" ]; then
        cat > .gitignore << 'GITIGNORE'
# Dependencies
node_modules/
python/__pycache__/
*.pyc
*.pyo

# Build outputs
dist/
build/
*.app
*.dmg
*.zip

# OS files
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# User data
*.log
.storage_intelligence/
analysis_*.json
archive_log.json

# Environment
.env
.env.local

# Temporary
tmp/
temp/
*.tmp
GITIGNORE
        echo "${GREEN}✅ Created .gitignore${NC}"
    fi
    
    # Initialize git if not already initialized
    if [ ! -d ".git" ]; then
        git init
        echo "${GREEN}✅ Initialized git repository${NC}"
    fi
    
    # Add all files
    git add .
    
    # Create initial commit if no commits exist
    if ! git log &> /dev/null; then
        git commit -m "Initial commit: Storage Intelligence v1.0.0

- Complete Electron app with Python backend
- System-wide storage analysis
- AI-powered recommendations
- Native macOS application
- Context-aware utility scoring
- Built with Electron + Python"
        echo "${GREEN}✅ Created initial commit${NC}"
    fi
fi

echo ""
echo "${BLUE}Step 2: Connecting to GitHub...${NC}"

# Check if remote already exists
if git remote get-url origin &> /dev/null; then
    echo "${YELLOW}⚠️  Remote 'origin' already exists${NC}"
    CURRENT_REMOTE=$(git remote get-url origin)
    echo "   Current remote: $CURRENT_REMOTE"
    echo ""
    read -p "Do you want to update it to https://github.com/matheus-rech/storage-intelligence.git? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git remote set-url origin https://github.com/matheus-rech/storage-intelligence.git
        echo "${GREEN}✅ Updated remote URL${NC}"
    fi
else
    git remote add origin https://github.com/matheus-rech/storage-intelligence.git
    echo "${GREEN}✅ Added remote 'origin'${NC}"
fi

echo ""
echo "${BLUE}Step 3: Preparing to push...${NC}"

# Get current branch name
CURRENT_BRANCH=$(git branch --show-current)
if [ -z "$CURRENT_BRANCH" ]; then
    CURRENT_BRANCH="main"
    git branch -M main
    echo "${GREEN}✅ Created 'main' branch${NC}"
fi

echo "Current branch: $CURRENT_BRANCH"
echo ""

# Check if there are uncommitted changes
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
    echo "${YELLOW}⚠️  You have uncommitted changes${NC}"
    echo ""
    read -p "Do you want to commit them now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add .
        echo ""
        echo "Enter commit message (or press Enter for default):"
        read -r COMMIT_MSG
        if [ -z "$COMMIT_MSG" ]; then
            COMMIT_MSG="Update: Storage Intelligence improvements"
        fi
        git commit -m "$COMMIT_MSG"
        echo "${GREEN}✅ Changes committed${NC}"
    fi
fi

echo ""
echo "${BLUE}Step 4: Pushing to GitHub...${NC}"
echo ""

# Push to GitHub
echo "Pushing to: https://github.com/matheus-rech/storage-intelligence.git"
echo "Branch: $CURRENT_BRANCH"
echo ""

if git push -u origin $CURRENT_BRANCH; then
    echo ""
    echo "================================================================"
    echo "${GREEN}✅ SUCCESS! Code pushed to GitHub!${NC}"
    echo "================================================================"
    echo ""
    echo "🌐 Your repository: https://github.com/matheus-rech/storage-intelligence"
    echo ""
    echo "${BLUE}Next steps:${NC}"
    echo ""
    echo "1. Visit your repository:"
    echo "   ${YELLOW}https://github.com/matheus-rech/storage-intelligence${NC}"
    echo ""
    echo "2. Add a description and topics:"
    echo "   - Description: 'AI-Powered Storage Optimization for macOS'"
    echo "   - Topics: electron, macos, storage, python, ai, optimization"
    echo ""
    echo "3. Update README.md with your details:"
    echo "   - Replace YOUR_USERNAME with 'matheus-rech'"
    echo "   - Add your contact email"
    echo ""
    echo "4. Add screenshots to docs/screenshots/"
    echo ""
    echo "5. Setup GitHub Actions (already included!)"
    echo ""
    echo "================================================================"
    echo "🎉 Your code is live on GitHub!"
    echo "================================================================"
else
    echo ""
    echo "${RED}❌ Push failed${NC}"
    echo ""
    echo "Possible issues:"
    echo "1. Authentication required - you may need to:"
    echo "   - Use GitHub CLI: gh auth login"
    echo "   - Or use HTTPS with Personal Access Token"
    echo "   - Or use SSH: git remote set-url origin git@github.com:matheus-rech/storage-intelligence.git"
    echo ""
    echo "2. Repository might not be empty. If so:"
    echo "   git pull origin main --allow-unrelated-histories"
    echo "   git push -u origin main"
    echo ""
    echo "3. Check if repository exists:"
    echo "   https://github.com/matheus-rech/storage-intelligence"
    echo ""
    exit 1
fi
