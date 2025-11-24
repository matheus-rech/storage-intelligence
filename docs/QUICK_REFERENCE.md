# 🚀 Quick Reference Card - File Organization

## 📋 Most Useful Commands

### Finding Files Fast
```bash
# Find research papers about cerebellar stroke
find ~/Downloads -iname "*cerebellar*" -o -iname "*stroke*"

# Find all Kim2016 files
find ~/Downloads -iname "*kim2016*"

# Find extraction files
find ~/Downloads -iname "*extraction*"

# Show newest files first
ls -lt ~/Downloads | head -20

# Show largest files
find ~/Downloads -type f -exec ls -lh {} \; | sort -k5 -h | tail -20
```

### Quick Organization
```bash
# Move all PDFs to Research-Papers/To-Review
find ~/Downloads -maxdepth 1 -name "*.pdf" \
  -exec mv {} ~/Downloads/Research-Papers/To-Review/ \;

# Move all Excel files to Data-Extractions
find ~/Downloads -maxdepth 1 -name "*.xlsx" \
  -exec mv {} ~/Downloads/Data-Extractions/ \;

# Move all code files
find ~/Downloads -maxdepth 1 \( -name "*.py" -o -name "*.js" -o -name "*.ts" \) \
  -exec mv {} ~/Downloads/Code-Projects/Utilities/ \;
```

### Storage Management
```bash
# Check total storage
du -sh ~/Downloads

# Check storage by folder
du -sh ~/Downloads/*/ | sort -h

# Find files larger than 50MB
find ~/Downloads -type f -size +50M -exec ls -lh {} \;

# Find old files (>6 months)
find ~/Downloads -type f -mtime +180
```

### Duplicate Detection
```bash
# Find files with same name (different locations)
find ~/Downloads -type f -printf '%f\n' | sort | uniq -d

# Count files by extension
find ~/Downloads -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn

# Or use the Python script
python3 duplicate_finder.py
```

---

## 🎯 Weekly Workflow

### Friday 3:00 PM (15 minutes)

```bash
# 1. Check what's new this week
find ~/Downloads -maxdepth 1 -type f -mtime -7 -print

# 2. Sort by type
# - PDFs → Research-Papers/To-Review/
# - XLSX → Data-Extractions/
# - Code → Code-Projects/
# - DOCX → Clinical-Documents/

# 3. Quick duplicate check
python3 duplicate_finder.py | head -50

# 4. Delete obvious temp files
# Look for: ~$, untitled, (1), (2), backup
```

---

## 📁 Folder Quick Guide

```
When you download a...           → Put it in...
────────────────────────────────────────────────────────────
Research paper (PDF)              → Research-Papers/[Topic]/
Extraction data (XLSX/CSV)        → Data-Extractions/Active-Projects/
Manuscript you're writing (DOCX)  → Clinical-Documents/Manuscripts/
Code file (PY/JS/TS)             → Code-Projects/
Presentation (PPTX)               → Clinical-Documents/Presentations/
Image/Figure (PNG/JPG)            → Medical-Images/
Archive (ZIP)                     → Archives/
Documentation (MD/TXT)            → Documentation/
Not sure?                         → To-Review/
```

---

## 🔍 Your Most Common Files

Based on analysis of your Downloads:

**Research Papers** (156 files)
- Cerebellar stroke studies
- Neurosurgery papers  
- Meta-analysis methodology
- → Put in: `Research-Papers/Cerebellar-Stroke/`

**Data Extractions** (89 files)
- Study data in Excel
- Kim2016 extraction
- Other clinical data
- → Put in: `Data-Extractions/Active-Projects/`

**Code Projects** (123 files)
- Python scripts
- JS/TS files
- CEREBELLAR-EXTRACT versions
- → Put in: `Code-Projects/Cerebellar-Extract/`

**Clinical Documents** (142 files)
- Manuscripts
- Protocols
- Letters
- → Put in: `Clinical-Documents/Manuscripts/`

---

## ⚡ Power User Shortcuts

### Aliases (Add to ~/.zshrc)
```bash
# Quick navigation
alias dl="cd ~/Downloads"
alias rp="cd ~/Downloads/Research-Papers"
alias de="cd ~/Downloads/Data-Extractions"
alias cd="cd ~/Downloads/Clinical-Documents"
alias cp="cd ~/Downloads/Code-Projects"

# Quick operations
alias dlclean="python3 ~/Downloads/duplicate_finder.py"
alias dlsize="du -sh ~/Downloads/*/ | sort -h"
alias dlnew="find ~/Downloads -type f -mtime -7 -print"
```

---

## 🚨 Emergency Recovery

If you accidentally delete something:

```bash
# Check trash
ls ~/.Trash

# Restore from backup (if you created one)
# Before cleanup, always run:
cp -r ~/Downloads ~/Downloads_BACKUP_$(date +%Y%m%d)

# Time Machine (if enabled)
# Right-click folder → Enter Time Machine
```

---

## 💡 Daily Habits

### Download Something New?
1. ✅ Immediately decide: Research? Data? Code? Clinical?
2. ✅ Move to appropriate folder
3. ✅ Rename if needed (use convention)
4. ✅ Delete download notification

### Finished a Project?
1. ✅ Move all files to Archive/
2. ✅ Create README with summary
3. ✅ Delete duplicates/drafts
4. ✅ Backup if important

### Can't Find a File?
1. ✅ Use `find` command with keyword
2. ✅ Check To-Review folders
3. ✅ Check recent files: `ls -lt | head`
4. ✅ Use Spotlight if desperate

---

## 🎯 Your Top Duplicates to Check

From the analysis, these need attention:

1. **Kim2016** - 5+ versions
   - Keep: `Kim2016_GROUNDTRUTH_ANNOTATED.pdf`
   - Review others

2. **clinical-extractor** - 3+ ZIPs
   - Keep: Latest version only
   - Delete: Old copies

3. **extraction files** - Multiple versions
   - Use date-based naming
   - Archive old versions

4. **Untitled folders** (1-6)
   - Review contents
   - Rename or delete

5. **Temp files** (~$xxx)
   - Safe to delete
   - Office lock files

---

## 📊 Success Metrics

Check these weekly:

```bash
# Root file count (goal: <100)
find ~/Downloads -maxdepth 1 -type f | wc -l

# Total storage (monitor growth)
du -sh ~/Downloads

# Duplicate count (goal: 0)
find ~/Downloads -type f -printf '%f\n' | sort | uniq -d | wc -l

# Old file count (goal: declining)
find ~/Downloads -type f -mtime +180 | wc -l
```

**Target Stats After Organization:**
- Root files: <100 (vs 687 now)
- Duplicates: 0 (vs 45+ now)
- Categories: 9 clear folders
- Find time: <30 seconds

---

## 🛟 Help Commands

```bash
# Get help on a command
man find
man du
man ls

# Or use online resources
# tldr.sh - simplified man pages
# explainshell.com - visual command explanation
```

---

## 📞 Quick Support

**Problems?**
1. Check README.md for detailed help
2. Review FILE_ORGANIZATION_GUIDE.md
3. Open dashboard for visual analysis
4. Run duplicate_finder.py for insights

**Tools:**
- `README.md` - Complete overview
- `FILE_ORGANIZATION_GUIDE.md` - Detailed guide
- `file-organization-dashboard.html` - Visual analysis
- `duplicate_finder.py` - Duplicate analysis
- `auto_organize_downloads.sh` - Setup structure

---

## ⏱️ Time Estimates

**Initial Setup:** 2-4 hours
- Create structure: 30 min
- Sort existing files: 1-2 hours  
- Clean duplicates: 30-60 min
- Set up automation: 30 min

**Weekly Maintenance:** 15 min
- Review new files: 5 min
- Sort into folders: 5 min
- Quick cleanup: 5 min

**Monthly Deep Clean:** 1 hour
- Archive old projects: 30 min
- Comprehensive duplicate check: 20 min
- Storage optimization: 10 min

---

## 🎓 Remember

1. **Organization is a habit**, not a one-time task
2. **Use To-Review liberally** - sort later is okay
3. **Archive, don't delete** - you never know
4. **Weekly maintenance** prevents chaos
5. **Backup before major changes** - always!

---

## 🔖 Bookmarks

Save these locations:
- Downloads: `/Users/matheusrech/Downloads`
- Research: `~/Downloads/Research-Papers`
- Data: `~/Downloads/Data-Extractions`
- Code: `~/Downloads/Code-Projects`
- Archive: `~/Downloads/Archives`

---

**Print this card and keep it handy!**

*Last updated: November 2024*
*For: Matheus Rech*
