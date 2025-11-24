# 🎨 Development Guide - Modifying Storage Intelligence

## ✅ YES! It's Very Easy to Modify!

The app is designed to be **developer-friendly** with clear separation of concerns:

```
Frontend (HTML/CSS/JS) ← Easy to modify!
    ↓
Electron Backend (Node.js) ← Moderate
    ↓
Python Backend (Python) ← Easy to modify!
```

---

## 🚀 Quick Modification Workflow

### 1. Edit Frontend (Most Common)

**What you can change:**
- UI layout & styling
- Colors, fonts, spacing
- Dashboard components
- Sidebar navigation
- Button actions
- Data visualization

**Files to edit:**
```
dashboard/index.html    # HTML structure & CSS styling
dashboard/renderer.js   # JavaScript logic & UI behavior
```

**Workflow:**
```bash
# 1. Edit the files
code dashboard/index.html
code dashboard/renderer.js

# 2. Test in development mode (see changes immediately!)
npm run dev

# 3. When happy, rebuild
npm run build-mac

# 4. Test the built app
open "dist/mac/Storage Intelligence.app"
```

**Hot Reload Available:** Changes to HTML/CSS/JS are visible with a simple refresh (Cmd+R)!

---

## 🎨 Frontend Modification Examples

### Example 1: Change Color Scheme

**File:** `dashboard/index.html`

**Find this:**
```css
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

**Change to:**
```css
body {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    /* Green theme! */
}

.stat-card {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    /* Blue cards! */
}
```

**Result:** Entire app now has green/blue theme!

---

### Example 2: Add New Stat Card

**File:** `dashboard/renderer.js`

**Find the `calculateStats()` function and add:**
```javascript
// Add new stat
stats.projectsCount = analysis.storage_plan?.tier_1_keep_local?.length || 0;
```

**Then in `loadDashboard()`, add to the grid:**
```javascript
statsGrid.innerHTML = `
    <!-- Existing cards -->
    <div class="stat-card">
        <div class="stat-label">Active Projects</div>
        <div class="stat-value">${stats.projectsCount}</div>
        <div class="stat-change">In use</div>
    </div>
`;
```

**Result:** New stat card appears on dashboard!

---

### Example 3: Add New Sidebar Section

**File:** `dashboard/index.html`

**Add to sidebar nav:**
```html
<div class="nav-item" data-page="my-new-section">
    <span class="nav-icon">🎯</span>
    <span>My New Section</span>
</div>
```

**Add page container:**
```html
<div id="my-new-section" class="page-view"></div>
```

**File:** `dashboard/renderer.js`

**Add to `loadPageContent()` switch:**
```javascript
case 'my-new-section':
    await this.loadMyNewSection();
    break;
```

**Add the function:**
```javascript
async loadMyNewSection() {
    const pageView = document.getElementById('my-new-section');
    pageView.innerHTML = `
        <div class="page-header">
            <h2>My New Section</h2>
            <p>Custom content here!</p>
        </div>
        <div class="content-section">
            <h3>Custom Feature</h3>
            <p>Add any content you want!</p>
        </div>
    `;
}
```

**Result:** New section in sidebar with custom content!

---

### Example 4: Modify Recommendation Display

**File:** `dashboard/renderer.js`

**Find `createRecommendationCard()` and modify:**
```javascript
createRecommendationCard(rec) {
    return `
        <div class="recommendation-card ${rec.priority}">
            <div class="rec-header">
                <div class="rec-title">
                    ${rec.priority === 'high' ? '🔥' : '💡'} ${rec.title}
                </div>
                <div class="rec-badge ${rec.priority}">
                    ${rec.priority} - ${rec.space_savings}
                </div>
            </div>
            <!-- Add custom fields -->
            <div class="rec-custom">
                <strong>Why this matters:</strong> ${rec.description}
            </div>
            <div class="rec-meta">
                <span>💾 ${rec.space_savings}</span>
                <span>⚠️ Risk: ${rec.risk}</span>
                <!-- Add estimated time -->
                <span>⏱️ Est: 5 min</span>
            </div>
            <div class="rec-actions">
                <button class="btn btn-primary btn-sm" data-action="${rec.category}">
                    Execute Now
                </button>
                <!-- Add schedule button -->
                <button class="btn btn-secondary btn-sm">
                    Schedule for Later
                </button>
            </div>
        </div>
    `;
}
```

**Result:** Enhanced recommendation cards with custom info!

---

## 🔧 Backend Modification Examples

### Example 1: Add Custom Analysis

**File:** `python/macos_storage_intelligence.py`

**Add new method:**
```python
def analyze_downloads_folder(self):
    """Analyze Downloads folder specifically"""
    downloads_path = self.home / 'Downloads'
    
    analysis = {
        'path': str(downloads_path),
        'files_by_type': {},
        'old_files': [],
        'large_files': []
    }
    
    for file in downloads_path.iterdir():
        if file.is_file():
            # Categorize by type
            ext = file.suffix.lower()
            analysis['files_by_type'][ext] = analysis['files_by_type'].get(ext, 0) + 1
            
            # Find old files (>180 days)
            stat = file.stat()
            age_days = (time.time() - stat.st_mtime) / (24 * 3600)
            if age_days > 180:
                analysis['old_files'].append({
                    'name': file.name,
                    'age_days': age_days,
                    'size': stat.st_size
                })
            
            # Find large files (>100MB)
            if stat.st_size > 100 * 1024 * 1024:
                analysis['large_files'].append({
                    'name': file.name,
                    'size': stat.st_size,
                    'size_formatted': self.format_size(stat.st_size)
                })
    
    return analysis
```

**Call it in `run_complete_analysis()`:**
```python
def run_complete_analysis(self):
    # ... existing code ...
    
    # Add custom analysis
    analysis['downloads_detailed'] = self.analyze_downloads_folder()
    
    return analysis
```

**Result:** More detailed Downloads analysis!

---

### Example 2: Custom Recommendation Type

**File:** `python/macos_storage_intelligence.py`

**Add to `generate_recommendations()`:**
```python
def generate_recommendations(self, analysis):
    recommendations = []
    
    # ... existing recommendations ...
    
    # Add custom recommendation for large downloads
    if 'downloads_detailed' in analysis:
        large_files = analysis['downloads_detailed']['large_files']
        if len(large_files) > 5:
            total_size = sum(f['size'] for f in large_files)
            recommendations.append({
                'priority': 'medium',
                'category': 'large_downloads',
                'title': f'Review {len(large_files)} Large Files in Downloads',
                'description': f'Found {len(large_files)} files over 100 MB in your Downloads folder. '
                              f'These may be temporary downloads that can be moved or deleted.',
                'actions': [
                    'Review large files',
                    'Move to external drive',
                    'Delete if no longer needed',
                    'Organize by project'
                ],
                'space_savings': self.format_size(total_size),
                'risk': 'low'
            })
    
    return sorted(recommendations, key=lambda x: {'high': 0, 'medium': 1, 'low': 2}[x['priority']])
```

**Result:** Custom recommendations appear!

---

### Example 3: Add User Preference

**File:** `main.js`

**Add to settings handling:**
```javascript
// Store user preferences
const Store = require('electron-store');
const store = new Store();

// Save preference
ipcMain.handle('save-preference', async (event, key, value) => {
    store.set(key, value);
    return { success: true };
});

// Get preference
ipcMain.handle('get-preference', async (event, key) => {
    return store.get(key);
});
```

**File:** `dashboard/renderer.js`

**Use in UI:**
```javascript
async loadSettingsPage() {
    const pageView = document.getElementById('settings');
    
    // Get current preferences
    const autoAnalyze = await window.storageAPI.getPreference('autoAnalyze') || false;
    
    pageView.innerHTML = `
        <div class="page-header">
            <h2>Settings</h2>
        </div>
        <div class="content-section">
            <h3>Analysis Preferences</h3>
            <label>
                <input type="checkbox" id="autoAnalyze" ${autoAnalyze ? 'checked' : ''}>
                Automatically analyze on startup
            </label>
        </div>
    `;
    
    // Add event listener
    document.getElementById('autoAnalyze').addEventListener('change', async (e) => {
        await window.storageAPI.savePreference('autoAnalyze', e.target.checked);
    });
}
```

**Result:** User preferences saved and loaded!

---

## 🔍 Development Tools

### Hot Reload Development

```bash
# Start in development mode
npm run dev
```

**Features:**
- Auto-opens DevTools
- Console logging visible
- Cmd+R to refresh
- No need to rebuild

### Debugging

**In renderer.js:**
```javascript
console.log('Current analysis:', this.currentAnalysis);
console.log('Stats calculated:', stats);
```

**In main.js:**
```javascript
console.log('Analysis started');
console.log('Python output:', output);
```

**View in:** DevTools Console (Cmd+Alt+I)

### Live Editing CSS

**In development mode:**
1. Open DevTools (Cmd+Alt+I)
2. Go to Elements tab
3. Edit styles in real-time
4. Copy changes back to `index.html`

---

## 📦 Adding New Dependencies

### Frontend (JavaScript)

```bash
# Install package
npm install chart.js

# Use in renderer.js
import Chart from 'chart.js/auto';
```

### Backend (Python)

```bash
# Install package
pip3 install pandas --break-system-packages

# Use in Python files
import pandas as pd
```

**Remember to update package.json and requirements.txt!**

---

## 🎨 Styling Tips

### Using CSS Variables

**Add to `<style>` in index.html:**
```css
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --success-color: #10b981;
    --warning-color: #f59e0b;
    --danger-color: #ef4444;
}

.stat-card {
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
}
```

**Now easy to change theme by updating variables!**

### Responsive Design

```css
@media (max-width: 1200px) {
    .stats-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 768px) {
    .stats-grid {
        grid-template-columns: 1fr;
    }
}
```

### Dark Mode Support

```css
@media (prefers-color-scheme: dark) {
    body {
        background: #1a1a1a;
        color: #ffffff;
    }
    
    .content-section {
        background: #2a2a2a;
    }
}
```

---

## 🚀 Building & Testing

### Development Workflow

```bash
# 1. Make changes
code dashboard/index.html

# 2. Test immediately
npm run dev

# 3. See changes
# Press Cmd+R to reload

# 4. When happy, build
npm run build-mac

# 5. Test production build
open "dist/mac/Storage Intelligence.app"

# 6. If good, commit
git add .
git commit -m "Added new feature"
git push
```

### Testing Changes

**Quick test checklist:**
- [ ] UI looks correct
- [ ] Buttons work
- [ ] Navigation works
- [ ] Analysis runs
- [ ] Data displays correctly
- [ ] No console errors

---

## 📝 File Structure Reference

### Frontend Files (Easy to Modify)

```
dashboard/
├── index.html          ← HTML structure & CSS styling
└── renderer.js         ← UI logic, API calls, event handlers
```

**Modify these 2 files for 90% of UI changes!**

### Backend Files (Moderate)

```
main.js                 ← Electron main process
preload.js              ← IPC communication bridge
```

### Python Files (Easy to Modify)

```
python/
├── macos_storage_intelligence.py  ← System analysis
└── intelligent_agent.py           ← Recommendations
```

### Configuration

```
package.json            ← Dependencies, build config
```

---

## 🎯 Common Modifications

### Change App Name

**File:** `package.json`
```json
{
  "name": "my-custom-name",
  "productName": "My Storage App"
}
```

### Change Window Size

**File:** `main.js`
```javascript
this.mainWindow = new BrowserWindow({
    width: 1600,      // Change this
    height: 1000,     // And this
    minWidth: 1200,
    minHeight: 700
});
```

### Add Custom Menu Item

**File:** `main.js`
```javascript
{
    label: 'Tools',
    submenu: [
        {
            label: 'My Custom Tool',
            click: () => this.myCustomTool()
        }
    ]
}
```

### Change Analysis Frequency

**File:** `python/macos_storage_intelligence.py`
```python
analysis_interval = 7200  # 2 hours instead of 1
```

---

## 💡 Best Practices

### 1. Keep Separation of Concerns

```
Frontend (dashboard/)   → UI only, no business logic
Backend (main.js)       → Coordination, IPC
Python (python/)        → Heavy computation, analysis
```

### 2. Use Consistent Naming

```javascript
// Good
async loadDashboard()
async loadRecommendationsPage()
async executeRecommendation()

// Bad
async load_dash()
async recPage()
async exec()
```

### 3. Comment Complex Logic

```javascript
// Calculate utility score based on multiple factors
// - Recency: More points for recently accessed
// - Type: Research papers get highest score
// - Project: Main projects get bonus points
const utilityScore = this.calculateUtilityScore(item);
```

### 4. Handle Errors Gracefully

```javascript
try {
    const result = await window.storageAPI.runAnalysis();
    if (result.success) {
        this.onAnalysisComplete(result);
    }
} catch (error) {
    console.error('Analysis failed:', error);
    this.showNotification('Error', 'Analysis failed. Please try again.');
}
```

---

## 🔥 Advanced Customizations

### Add Chart Visualization

```bash
npm install chart.js
```

**In renderer.js:**
```javascript
import Chart from 'chart.js/auto';

showStorageChart(data) {
    const ctx = document.getElementById('storageChart');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Caches', 'Dev Bloat', 'Apps', 'Files'],
            datasets: [{
                data: [15.2, 23.4, 8.7, 52.7],
                backgroundColor: ['#ef4444', '#f59e0b', '#10b981', '#3b82f6']
            }]
        }
    });
}
```

### Add Database Storage

```bash
npm install better-sqlite3
```

**Store analysis history:**
```javascript
const Database = require('better-sqlite3');
const db = new Database('storage-history.db');

// Create table
db.exec(`
    CREATE TABLE IF NOT EXISTS analyses (
        id INTEGER PRIMARY KEY,
        timestamp TEXT,
        total_size INTEGER,
        reclaimable INTEGER,
        data TEXT
    )
`);

// Insert analysis
const insert = db.prepare('INSERT INTO analyses VALUES (?, ?, ?, ?, ?)');
insert.run(null, new Date().toISOString(), totalSize, reclaimable, JSON.stringify(data));
```

### Add Export to Excel

```bash
npm install exceljs
```

**Export recommendations:**
```javascript
const ExcelJS = require('exceljs');

async exportToExcel() {
    const workbook = new ExcelJS.Workbook();
    const worksheet = workbook.addWorksheet('Recommendations');
    
    worksheet.columns = [
        { header: 'Priority', key: 'priority', width: 10 },
        { header: 'Title', key: 'title', width: 40 },
        { header: 'Space Savings', key: 'savings', width: 15 },
        { header: 'Risk', key: 'risk', width: 10 }
    ];
    
    this.currentAnalysis.recommendations.forEach(rec => {
        worksheet.addRow({
            priority: rec.priority,
            title: rec.title,
            savings: rec.space_savings,
            risk: rec.risk
        });
    });
    
    await workbook.xlsx.writeFile('recommendations.xlsx');
}
```

---

## 🎉 Summary

### Easy to Modify?

**YES! Extremely easy!**

**Frontend (HTML/CSS/JS):**
- ✅ Edit 2 files (index.html, renderer.js)
- ✅ See changes with Cmd+R
- ✅ No compilation needed
- ✅ Clear structure

**Backend (Python):**
- ✅ Simple Python scripts
- ✅ Clear functions
- ✅ Easy to extend

**Build Process:**
- ✅ npm run dev → test
- ✅ npm run build-mac → package
- ✅ Fast iteration

### Most Common Modifications

1. **Colors/Styling** → Edit CSS in index.html (5 min)
2. **Add UI section** → Add to sidebar + create function (15 min)
3. **Custom analysis** → Add function in Python (30 min)
4. **New recommendation** → Add to generate_recommendations() (20 min)
5. **Chart/visualization** → Install library + add component (30 min)

---

**Next: What should go in GitHub? →**
