#!/bin/bash

echo "================================================================"
echo "🚀 STORAGE INTELLIGENCE - GITHUB REPOSITORY SETUP"
echo "================================================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if we're in the electron-app directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Run this script from the electron-app directory"
    echo "   cd electron-app && ../setup-github-repo.sh"
    exit 1
fi

echo "${BLUE}This script will:${NC}"
echo "  1. Create proper directory structure for GitHub"
echo "  2. Move files to correct locations"
echo "  3. Create essential GitHub files (.gitignore, README, etc.)"
echo "  4. Initialize git repository"
echo "  5. Create initial commit"
echo ""

read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 0
fi

echo ""
echo "${GREEN}📁 Creating directory structure...${NC}"

# Create new structure
mkdir -p src/main
mkdir -p src/renderer/{js,css,assets/images}
mkdir -p src/python
mkdir -p build
mkdir -p docs/screenshots
mkdir -p scripts
mkdir -p .github/{workflows,ISSUE_TEMPLATE}

echo "${GREEN}✅ Directories created${NC}"

echo ""
echo "${GREEN}📦 Moving files to new structure...${NC}"

# Move main process files
mv main.js src/main/ 2>/dev/null || echo "  main.js already in place"
mv preload.js src/main/ 2>/dev/null || echo "  preload.js already in place"

# Move renderer files
mv dashboard/index.html src/renderer/ 2>/dev/null || echo "  index.html already in place"
mv dashboard/renderer.js src/renderer/js/app.js 2>/dev/null || echo "  renderer.js already in place"

# Move Python files
cp -r python/* src/python/ 2>/dev/null || echo "  Python files already in place"

# Move docs
cp -r docs/* docs/ 2>/dev/null || echo "  Docs already in place"

echo "${GREEN}✅ Files moved${NC}"

echo ""
echo "${GREEN}📝 Creating essential files...${NC}"

# Create .gitignore
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

# Create README.md
cat > README.md << 'README'
# 💾 Storage Intelligence

AI-Powered Storage Optimization for macOS

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-macOS-lightgrey)](https://www.apple.com/macos)

## 🎯 Features

- 🔍 System-wide storage analysis
- 🤖 AI-powered recommendations with context awareness
- 🎯 Utility scoring (0-100) based on your work
- 🗑️ Safe cache cleanup
- 🔧 Development environment optimization
- 📱 Native macOS application

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/storage-intelligence.git
cd storage-intelligence

# Install dependencies
npm install

# Build the app
npm run build-mac

# Or run in development mode
npm run dev
```

### Usage

1. Launch the app
2. Click "Run Analysis"
3. Review AI recommendations
4. Execute optimizations
5. Reclaim 50-80 GB!

## 📸 Screenshots

![Dashboard](docs/screenshots/dashboard.png)
*System-wide analysis with real-time stats*

![Recommendations](docs/screenshots/recommendations.png)
*AI-powered recommendations with priority ranking*

## 🎨 Key Features

### Context-Aware Intelligence

The app understands your workflow:
- Research papers → HIGH priority (never delete)
- Active code → HIGH priority (keep local)
- Old node_modules → LOW priority (safe delete)
- Caches → ZERO priority (delete freely)

### Multi-Tier Storage Plan

- **Tier 1**: Keep Local (critical, frequently accessed)
- **Tier 2**: Cloud Backup (important, infrequent)
- **Tier 3**: Archive (historical)
- **Tier 4**: Safe Delete (regenerable)

### Expected Results

- Caches: 10-20 GB (safe to delete)
- node_modules: 15-30 GB (old projects)
- Python venvs: 5-10 GB (old projects)
- Unused apps: 5-10 GB (can reinstall)

**Total: 50-80 GB reclaimable!**

## 📚 Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [Development Guide](docs/DEVELOPMENT.md)
- [GitHub Setup](docs/GITHUB_REPOSITORY_GUIDE.md)

## 🛠️ Development

```bash
# Run in development mode (hot reload)
npm run dev

# Run tests
npm test

# Lint code
npm run lint

# Format code
npm run format

# Build for production
npm run build-mac
```

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

### Quick Contribution Guide

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

- Built with [Electron](https://electronjs.org/)
- Powered by Python for heavy analysis
- Designed for researchers and developers

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/storage-intelligence/issues)
- **Email**: your@email.com

---

**Made with ❤️ for macOS users who need more space!**
README

# Create LICENSE
cat > LICENSE << 'LICENSE'
MIT License

Copyright (c) 2024 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
LICENSE

# Create CONTRIBUTING.md
cat > CONTRIBUTING.md << 'CONTRIBUTING'
# Contributing to Storage Intelligence

Thank you for your interest in contributing! 🎉

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported
2. Use the bug report template
3. Include macOS version, app version, steps to reproduce

### Suggesting Features

1. Check if the feature has been suggested
2. Use the feature request template
3. Explain the problem and proposed solution

### Pull Requests

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Create a Pull Request

## Development Setup

```bash
git clone https://github.com/YOUR_USERNAME/storage-intelligence.git
cd storage-intelligence
npm install
npm run dev
```

## Code Style

- Use ESLint and Prettier
- Follow existing patterns
- Add meaningful comments
- Write descriptive commit messages

## Questions?

Open an issue or contact via email.
CONTRIBUTING

# Create GitHub Actions workflow
cat > .github/workflows/build.yml << 'WORKFLOW'
name: Build

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: macos-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Build app
      run: npm run build-mac
WORKFLOW

# Create issue template
cat > .github/ISSUE_TEMPLATE/bug_report.md << 'BUGREPORT'
---
name: Bug Report
about: Report a bug
title: '[BUG] '
labels: bug
---

**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen.

**Environment:**
 - macOS Version: [e.g. Sonoma 14.5]
 - App Version: [e.g. 1.0.0]
 - Architecture: [Intel/Apple Silicon]

**Screenshots**
If applicable, add screenshots.
BUGREPORT

echo "${GREEN}✅ Essential files created${NC}"

echo ""
echo "${GREEN}🔧 Initializing git repository...${NC}"

# Initialize git
git init
git add .
git commit -m "Initial commit: Storage Intelligence v1.0.0

- Complete Electron app with Python backend
- System-wide storage analysis
- AI-powered recommendations
- Native macOS application
- Context-aware utility scoring"

echo "${GREEN}✅ Git repository initialized${NC}"

echo ""
echo "================================================================"
echo "${GREEN}✅ SETUP COMPLETE!${NC}"
echo "================================================================"
echo ""
echo "${BLUE}Next steps:${NC}"
echo ""
echo "1. Create repository on GitHub:"
echo "   https://github.com/new"
echo ""
echo "2. Add remote and push:"
echo "   ${YELLOW}git remote add origin https://github.com/YOUR_USERNAME/storage-intelligence.git${NC}"
echo "   ${YELLOW}git branch -M main${NC}"
echo "   ${YELLOW}git push -u origin main${NC}"
echo ""
echo "3. Update README.md with your GitHub username"
echo ""
echo "4. Add screenshots to docs/screenshots/"
echo ""
echo "5. Setup GitHub Actions in repository settings"
echo ""
echo "================================================================"
echo "📚 Documentation created:"
echo "   - README.md"
echo "   - LICENSE"
echo "   - CONTRIBUTING.md"
echo "   - .gitignore"
echo "   - .github/workflows/build.yml"
echo ""
echo "🎉 Your repository is ready for GitHub!"
echo "================================================================"
echo ""

