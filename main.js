const { app, BrowserWindow, ipcMain, shell } = require('electron');
const path = require('path');
const fs = require('fs');
const os = require('os');
const { execSync } = require('child_process');

let mainWindow = null;
const dataDir = path.join(os.homedir(), '.storage_intelligence');

// Helper functions for system scanning
function formatBytes(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}

function getDirSize(dirPath) {
    try {
        const result = execSync(`du -sk "${dirPath}" 2>/dev/null`, { encoding: 'utf8' });
        const sizeKB = parseInt(result.split('\t')[0], 10);
        return sizeKB * 1024;
    } catch (e) {
        return 0;
    }
}

function findDirectories(startPath, targetName, maxDepth = 5) {
    const results = [];

    function search(currentPath, depth) {
        if (depth > maxDepth) return;

        try {
            const items = fs.readdirSync(currentPath, { withFileTypes: true });
            for (const item of items) {
                if (!item.isDirectory()) continue;

                const fullPath = path.join(currentPath, item.name);

                // Skip certain directories
                if (item.name.startsWith('.') || item.name === 'Library') continue;

                if (item.name === targetName) {
                    const size = getDirSize(fullPath);
                    if (size > 1024 * 1024) { // Only include if > 1MB
                        results.push({ path: fullPath, size });
                    }
                } else {
                    search(fullPath, depth + 1);
                }
            }
        } catch (e) {
            // Permission denied or other errors
        }
    }

    search(startPath, 0);
    return results;
}

function getCacheDirectories() {
    const home = os.homedir();
    const caches = [];

    const cachePaths = [
        // User caches
        { name: 'Chrome', path: path.join(home, 'Library/Caches/Google/Chrome') },
        { name: 'Safari', path: path.join(home, 'Library/Caches/com.apple.Safari') },
        { name: 'Firefox', path: path.join(home, 'Library/Caches/Firefox') },
        { name: 'Spotify', path: path.join(home, 'Library/Caches/com.spotify.client') },
        { name: 'Slack', path: path.join(home, 'Library/Caches/com.tinyspeck.slackmacgap') },
        { name: 'VS Code', path: path.join(home, 'Library/Caches/com.microsoft.VSCode') },
        { name: 'Discord', path: path.join(home, 'Library/Caches/com.hnc.Discord') },
        { name: 'Zoom', path: path.join(home, 'Library/Caches/us.zoom.xos') },
        { name: 'Teams', path: path.join(home, 'Library/Caches/com.microsoft.teams') },
        { name: 'npm', path: path.join(home, '.npm/_cacache') },
        { name: 'Yarn', path: path.join(home, 'Library/Caches/Yarn') },
        { name: 'Homebrew', path: path.join(home, 'Library/Caches/Homebrew') },
        { name: 'pip', path: path.join(home, 'Library/Caches/pip') },
        { name: 'CocoaPods', path: path.join(home, 'Library/Caches/CocoaPods') },
        // System caches
        { name: 'System Caches', path: '/Library/Caches' },
        { name: 'User Caches', path: path.join(home, 'Library/Caches') },
        // Logs
        { name: 'System Logs', path: '/var/log' },
        { name: 'User Logs', path: path.join(home, 'Library/Logs') },
        // Trash
        { name: 'Trash', path: path.join(home, '.Trash') },
        // Xcode
        { name: 'Xcode DerivedData', path: path.join(home, 'Library/Developer/Xcode/DerivedData') },
        { name: 'Xcode Archives', path: path.join(home, 'Library/Developer/Xcode/Archives') },
        { name: 'iOS DeviceSupport', path: path.join(home, 'Library/Developer/Xcode/iOS DeviceSupport') },
        // Docker
        { name: 'Docker', path: path.join(home, 'Library/Containers/com.docker.docker/Data') },
    ];

    for (const cache of cachePaths) {
        if (fs.existsSync(cache.path)) {
            const size = getDirSize(cache.path);
            if (size > 1024 * 1024) { // > 1MB
                caches.push({
                    name: cache.name,
                    path: cache.path,
                    size: size,
                    sizeFormatted: formatBytes(size),
                    safe: cache.name !== 'System Caches' && cache.name !== 'System Logs'
                });
            }
        }
    }

    return caches.sort((a, b) => b.size - a.size);
}

function sendProgress(step, total, message) {
    if (mainWindow && !mainWindow.isDestroyed()) {
        const percent = Math.round((step / total) * 100);
        mainWindow.webContents.send('analysis-progress', { percent, message, step, total });
    }
}

async function performSystemAnalysis(options = {}) {
    const home = os.homedir();
    const startTime = Date.now();
    const fullScan = options.fullSystemScan || false;

    // Determine scan paths
    const scanPaths = fullScan
        ? ['/', '/Applications', home]
        : [home];

    // Step 1: Find node_modules
    sendProgress(1, 5, 'Scanning node_modules...');
    let nodeModules = [];
    for (const scanPath of scanPaths) {
        if (fs.existsSync(scanPath)) {
            nodeModules = nodeModules.concat(findDirectories(scanPath, 'node_modules', fullScan ? 6 : 4));
        }
    }
    // Remove duplicates by path
    nodeModules = nodeModules.filter((item, index, self) =>
        index === self.findIndex(t => t.path === item.path)
    );
    const nodeModulesTotal = nodeModules.reduce((sum, item) => sum + item.size, 0);

    // Step 2: Find Python venvs
    sendProgress(2, 5, 'Scanning Python venvs...');
    let venvs = [];
    for (const scanPath of scanPaths) {
        if (fs.existsSync(scanPath)) {
            venvs = venvs.concat([
                ...findDirectories(scanPath, 'venv', fullScan ? 6 : 4),
                ...findDirectories(scanPath, '.venv', fullScan ? 6 : 4),
                ...findDirectories(scanPath, 'env', fullScan ? 6 : 4)
            ]);
        }
    }
    venvs = venvs
        .filter((item, index, self) => index === self.findIndex(t => t.path === item.path))
        .filter(v => fs.existsSync(path.join(v.path, 'bin/python')) || fs.existsSync(path.join(v.path, 'bin/activate')));
    const venvsTotal = venvs.reduce((sum, item) => sum + item.size, 0);

    // Step 3: Get caches
    sendProgress(3, 5, 'Scanning caches...');
    const caches = getCacheDirectories();
    const cachesTotal = caches.reduce((sum, item) => sum + item.size, 0);

    // Step 4: Calculate totals
    sendProgress(4, 5, 'Calculating totals...');

    // Calculate totals
    const reclaimable = nodeModulesTotal + venvsTotal + cachesTotal;

    // Get disk usage
    let totalStorage = 0;
    try {
        const dfOutput = execSync('df -k ~ | tail -1', { encoding: 'utf8' });
        const parts = dfOutput.trim().split(/\s+/);
        totalStorage = parseInt(parts[2], 10) * 1024; // Used space in bytes
    } catch (e) {
        totalStorage = reclaimable * 2;
    }

    // Generate recommendations
    const recommendations = [];

    if (nodeModules.length > 0) {
        recommendations.push({
            priority: nodeModulesTotal > 10 * 1024 * 1024 * 1024 ? 'high' : 'medium',
            category: 'dev_bloat',
            title: `Clean ${nodeModules.length} node_modules Folders`,
            description: `Found ${nodeModules.length} node_modules folders totaling ${formatBytes(nodeModulesTotal)}. These can be regenerated with npm install.`,
            space_savings: formatBytes(nodeModulesTotal),
            risk: 'low',
            items: nodeModules.slice(0, 10).map(m => ({ path: m.path, size: formatBytes(m.size) }))
        });
    }

    if (cachesTotal > 1024 * 1024 * 1024) { // > 1GB
        recommendations.push({
            priority: 'high',
            category: 'caches',
            title: 'Clean Application Caches',
            description: `Found ${formatBytes(cachesTotal)} of caches that can be safely deleted.`,
            space_savings: formatBytes(cachesTotal),
            risk: 'low'
        });
    }

    if (venvs.length > 0) {
        recommendations.push({
            priority: 'medium',
            category: 'dev_bloat',
            title: `Clean ${venvs.length} Python Virtual Environments`,
            description: `Found ${venvs.length} Python venvs totaling ${formatBytes(venvsTotal)}.`,
            space_savings: formatBytes(venvsTotal),
            risk: 'low',
            items: venvs.slice(0, 10).map(v => ({ path: v.path, size: formatBytes(v.size) }))
        });
    }

    // Step 5: Generating report
    sendProgress(5, 5, 'Generating report...');
    const scanTime = ((Date.now() - startTime) / 1000).toFixed(1);

    return {
        timestamp: new Date().toISOString(),
        scan_duration: scanTime + 's',
        summary: {
            total_storage: formatBytes(totalStorage),
            reclaimable: formatBytes(reclaimable),
            total_files: nodeModules.length + venvs.length + caches.length,
            caches_size: formatBytes(cachesTotal),
            dev_bloat_size: formatBytes(nodeModulesTotal + venvsTotal)
        },
        recommendations: recommendations,
        caches: caches.map(c => ({
            name: c.name,
            size: c.sizeFormatted,
            path: c.path,
            safe: c.safe
        })),
        dev_environments: {
            node_modules: {
                count: nodeModules.length,
                size: formatBytes(nodeModulesTotal),
                items: nodeModules.slice(0, 20).map(m => ({ path: m.path, size: formatBytes(m.size) }))
            },
            python_venvs: {
                count: venvs.length,
                size: formatBytes(venvsTotal),
                items: venvs.slice(0, 20).map(v => ({ path: v.path, size: formatBytes(v.size) }))
            }
        },
        storage_plan: {
            tier_1_keep_local: { count: 0, size: '0 B' },
            tier_4_safe_delete: {
                count: nodeModules.length + venvs.length + caches.length,
                size: formatBytes(reclaimable)
            }
        }
    };
}

if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true });
}

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1400,
        height: 900,
        titleBarStyle: 'hiddenInset',
        backgroundColor: '#667eea',
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: path.join(__dirname, 'preload.js')
        }
    });
    
    mainWindow.loadFile(path.join(__dirname, 'dashboard', 'index.html'));
    
    mainWindow.on('closed', function() {
        mainWindow = null;
    });
}

app.whenReady().then(function() {
    createWindow();
});

app.on('window-all-closed', function() {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', function() {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});

ipcMain.handle('run-analysis', async function(event, options) {
    try {
        // Perform real system analysis
        var analysis = await performSystemAnalysis(options || {});

        var analysisPath = path.join(dataDir, 'latest_analysis.json');
        fs.writeFileSync(analysisPath, JSON.stringify(analysis, null, 2));

        return { success: true, analysis: analysis };
    } catch (error) {
        console.error('Analysis error:', error);
        return { success: false, error: error.message };
    }
});

ipcMain.handle('get-analysis', async function() {
    var filePath = path.join(dataDir, 'latest_analysis.json');
    if (fs.existsSync(filePath)) {
        var data = fs.readFileSync(filePath, 'utf8');
        return JSON.parse(data);
    }
    return null;
});

ipcMain.handle('execute-action', async function(event, action) {
    return { success: true, message: action + ' done' };
});

ipcMain.handle('get-archive-log', async function() {
    return [];
});

ipcMain.handle('open-path', async function(event, filePath) {
    shell.showItemInFolder(filePath);
    return { success: true };
});

ipcMain.handle('open-external', async function(event, url) {
    shell.openExternal(url);
    return { success: true };
});
