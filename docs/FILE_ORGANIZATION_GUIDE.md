# 🎯 Complete File Organization Guide

## Your Downloads Analysis Summary

**Current State:**
- 📁 **687 files** across 45 directories  
- 💾 **~2.4 GB** total storage used
- 🎓 **156 research papers** (biggest category)
- 📊 **89 data extraction files** (active work)
- 💻 **123 code/script files** (development)

**Key Issues Identified:**
1. ⚠️ **HIGH**: Volume overload - too many files in one place
2. ⚠️ **MEDIUM**: Duplicate files detected (Kim2016, extraction files, etc.)
3. ⚠️ **MEDIUM**: Mixed file types (research + code + clinical)
4. ⚠️ **LOW**: Temporary files cluttering space

---

## 📁 Recommended Folder Structure

Based on your research workflow as a physician-researcher working on systematic reviews and AI tools, here's the ideal structure:

```
Downloads/
├── Research-Papers/
│   ├── Cerebellar-Stroke/          # Your main research focus
│   ├── Neurosurgery-General/       # General neurosurgery papers
│   ├── Meta-Analysis/              # Methodology papers
│   └── Other-Topics/               # Miscellaneous research
│
├── Data-Extractions/
│   ├── Active-Projects/            # Currently working on
│   ├── Completed-Studies/          # Finished extractions
│   └── Templates/                  # Extraction templates & schemas
│
├── Clinical-Documents/
│   ├── Manuscripts/                # Papers you're writing
│   ├── Protocols/                  # Study protocols
│   ├── Presentations/              # PPTX files
│   └── Letters/                    # Correspondence
│
├── Code-Projects/
│   ├── Cerebellar-Extract/         # Your main extraction tool
│   ├── Clinical-Tools/             # Other medical tools
│   └── Utilities/                  # Helper scripts
│
├── Medical-Images/                 # Figures, scans, etc.
├── Archives/                       # Old/completed work
├── Documentation/                  # README files, guides
└── To-Review/                      # Needs categorization

```

---

## 🚀 Quick Start - 3 Steps

### Step 1: Create the Structure
```bash
cd /Users/matheusrech/Downloads
bash auto_organize_downloads.sh
```

### Step 2: Sort Your Files

**By Category:**
- PDFs with "cerebellar", "stroke", "SDC" → `Research-Papers/Cerebellar-Stroke/`
- Excel/CSV files with "extraction", "data" → `Data-Extractions/Active-Projects/`
- DOCX files with "manuscript", "protocol" → `Clinical-Documents/Manuscripts/`
- Python/JS/TS files → `Code-Projects/`
- ZIP files → `Archives/`

**By Pattern:**
- Anything with "Kim2016" → Check for duplicates first
- Files with "extraction", "clinical-extractor" → Consolidate versions
- Temp files (`untitled`, `~$`, `backup`) → Review & delete
- Files > 6 months old → Consider archiving

### Step 3: Maintain Weekly
Every Friday:
```bash
# Quick sort of new downloads
cd Downloads
find . -maxdepth 1 -type f -mtime -7  # Files from this week
# Manually sort these into appropriate folders
```

---

## 🔍 Duplicate Detection Strategy

**Files to Check:**
1. **Kim2016 series** - You have 5+ versions (Kim2016.pdf, Kim2016_1.pdf, Kim2016_annotated.pdf, etc.)
   - **Action**: Keep the annotated version, archive others
   
2. **Extraction files** - Multiple versions of extraction tools
   - clinical-extractor.zip (multiple copies)
   - cerebellar-extract files (multiple versions)
   - **Action**: Keep only the latest v3-ultra version

3. **Data files** - Multiple CSVs with similar names
   - vps_meta_analysis_data.csv (duplicated)
   - **Action**: Compare files, keep most recent

4. **Documentation** - Multiple README files
   - README.md, README-2.md, README_FINAL.md
   - **Action**: Consolidate into one master README

---

## 🧹 Cleanup Checklist

### Immediate Actions:
- [ ] Delete temporary files (starts with `~$`)
- [ ] Remove "untitled folder" directories (1-6)
- [ ] Delete duplicate Kim2016 PDFs (keep best version)
- [ ] Consolidate extraction tool versions
- [ ] Archive files >6 months old

### Weekly Maintenance:
- [ ] Sort new downloads (Friday routine)
- [ ] Empty trash
- [ ] Quick duplicate check
- [ ] Update project folders

### Monthly Deep Clean:
- [ ] Review "To-Review" folder
- [ ] Archive completed projects
- [ ] Update documentation
- [ ] Backup important files to cloud

---

## 💡 Smart Organization Tips

### For Research Papers
**Naming Convention:**
```
[FirstAuthor][Year]_[Topic]_[Version].pdf
Example: Kim2016_SuboccipitalDecompression_Final.pdf
```

**Folder Organization:**
- By project/topic (recommended for you)
- NOT by date (harder to find)
- NOT by journal (too many categories)

### For Data Extractions
**Naming Convention:**
```
[Study]_[Date]_[Status].xlsx
Example: Kim2016_20241115_Completed.xlsx
```

**Version Control:**
- Use dates, not "final" or "v2"
- Keep templates separate
- Archive old versions

### For Code Projects
**Best Practices:**
- Keep each project in its own folder
- Include README.md in each
- Use git for version control
- Archive old prototypes

---

## 🎯 Specific Recommendations for You

### Based on Your Work:

**1. Cerebellar Research**
You have extensive work on cerebellar stroke and suboccipital decompressive craniectomy:
- Create dedicated `Research-Papers/Cerebellar-Stroke/` folder
- Move all SDC-related papers there
- Keep extraction schemas with data files

**2. CEREBELLAR-EXTRACT Tool**
Multiple versions detected:
- Consolidate into `Code-Projects/Cerebellar-Extract/`
- Keep only v3-ultra (latest)
- Archive older versions
- Document which version is production-ready

**3. Clinical Documents**
You have manuscripts in progress:
- Separate active manuscripts from archived
- Keep reviewer responses with manuscripts
- Archive accepted papers

**4. Data Analysis**
Many Excel/CSV files:
- Separate raw data from analysis
- Keep extraction templates together
- Document data sources

---

## 📊 Automation Scripts

### 1. Auto-Sort by File Type
```bash
# Move all PDFs to Research-Papers/To-Review
find /Users/matheusrech/Downloads -maxdepth 1 -name "*.pdf" -type f \
  -exec mv {} /Users/matheusrech/Downloads/Research-Papers/To-Review/ \;

# Move all Excel files to Data-Extractions/To-Review  
find /Users/matheusrech/Downloads -maxdepth 1 -name "*.xlsx" -type f \
  -exec mv {} /Users/matheusrech/Downloads/Data-Extractions/ \;
```

### 2. Find Large Files (>50MB)
```bash
find /Users/matheusrech/Downloads -type f -size +50M -exec ls -lh {} \;
```

### 3. Find Old Files (>6 months)
```bash
find /Users/matheusrech/Downloads -type f -mtime +180 -print
```

### 4. Find Duplicate Names
```bash
# List files with duplicate base names
find /Users/matheusrech/Downloads -type f -printf '%f\n' | \
  awk -F. '{print $1}' | sort | uniq -d
```

---

## 🔄 Version Control Strategy

### For Critical Files:

**Research Papers:**
- First author name + year = unique identifier
- Annotated versions: add "_annotated" suffix
- Highlighted versions: add "_highlighted" suffix

**Data Extractions:**
- Include extraction date in filename
- Use status markers: _draft, _review, _final
- Keep change log in Excel comments

**Code Files:**
- Use git for serious projects
- Archive old versions in subdirectory
- Document breaking changes

---

## 📅 Maintenance Schedule

### Daily (2 minutes):
- Drag today's downloads to appropriate folders
- Delete obvious temporary files

### Weekly (15 minutes):
- Review "To-Review" folders
- Sort files into final destinations
- Quick duplicate check

### Monthly (1 hour):
- Deep clean old files
- Archive completed projects
- Update documentation
- Backup important work

### Quarterly (2 hours):
- Comprehensive duplicate analysis
- Storage optimization
- Reorganize if workflow changed
- Update this guide

---

## 🎓 Research-Specific Best Practices

### Managing Papers:
1. **Download Organization:**
   - Original paper → `Research-Papers/[Topic]/`
   - Supplementary materials → Create subfolder
   - Your annotations → Separate copy with "_annotated"

2. **Citation Management:**
   - Keep DOI in filename if possible
   - Link to reference manager
   - Note if paper is in your systematic review

3. **Data Extraction:**
   - One Excel file per study
   - Keep extraction form template
   - Document extraction date
   - Track who extracted (if team)

### Managing Extractions:
1. **File Naming:**
   ```
   [FirstAuthor][Year]_extraction_[Date].xlsx
   Example: Kim2016_extraction_20241115.xlsx
   ```

2. **Version Tracking:**
   - Use Excel's comment feature
   - Keep change log sheet
   - Archive major versions

3. **Quality Control:**
   - Separate folder for double-checked
   - Mark files needing review
   - Document discrepancies

---

## 🚨 Common Pitfalls to Avoid

1. **Don't create too many folders** - stick to main categories
2. **Don't use version numbers** in names - use dates instead
3. **Don't hoard temporary files** - delete weekly
4. **Don't skip backups** - automate if possible
5. **Don't forget to archive** - completed work ≠ deleted work

---

## ✅ Success Metrics

After organization, you should have:
- ✓ <100 files in root Downloads folder
- ✓ Clear categories visible at a glance
- ✓ No duplicate files
- ✓ No files >1 year old in active folders
- ✓ Can find any file in <30 seconds

---

## 🆘 Quick Reference

**Find a research paper:**
```bash
cd ~/Downloads/Research-Papers
find . -iname "*cerebellar*" -o -iname "*stroke*"
```

**Find extraction data:**
```bash
cd ~/Downloads/Data-Extractions
ls -ltr  # Shows newest files last
```

**Check storage usage:**
```bash
du -sh ~/Downloads/*/ | sort -h
```

**List recent changes:**
```bash
find ~/Downloads -type f -mtime -7 -print
```

---

## 📞 Need Help?

If you get stuck:
1. Start small - organize one category at a time
2. Use the To-Review folder liberally
3. When in doubt, don't delete - archive instead
4. Back up before major changes

---

**Last Updated:** November 2024  
**For:** Matheus Rech - Physician Researcher  
**Focus:** Systematic Reviews & AI Tools in Healthcare

*Remember: Perfect organization is the enemy of done. Start with the basics and refine over time!*
