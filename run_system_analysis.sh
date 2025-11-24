#!/bin/bash

echo "=============================================="
echo "🤖 macOS STORAGE INTELLIGENCE"
echo "=============================================="
echo ""
echo "This will analyze your ENTIRE Mac, not just Downloads!"
echo ""
echo "What will be scanned:"
echo "  • Your entire home directory (~)"
echo "  • All caches (~/Library/Caches)"
echo "  • Development environments (node_modules, venv)"
echo "  • Installed applications (/Applications)"
echo "  • System storage"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 1
fi

echo ""
echo "🔍 Starting comprehensive analysis..."
echo "This may take 5-10 minutes..."
echo ""

python3 macos_storage_intelligence.py

echo ""
echo "✅ Analysis complete!"
echo ""
echo "📊 View results:"
echo "   cat ~/.storage_intelligence/analysis_*.json | jq ."
echo ""
echo "💡 See recommendations:"
echo "   cat ~/.storage_intelligence/analysis_*.json | jq '.recommendations'"
echo ""
echo "🎯 View storage plan:"
echo "   cat ~/.storage_intelligence/analysis_*.json | jq '.storage_plan'"
echo ""
