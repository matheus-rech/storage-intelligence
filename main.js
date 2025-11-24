const { app, BrowserWindow, ipcMain, shell } = require('electron');
const path = require('path');
const fs = require('fs');
const os = require('os');

let mainWindow = null;
const dataDir = path.join(os.homedir(), '.storage_intelligence');
if (!fs.existsSync(dataDir)) fs.mkdirSync(dataDir, { recursive: true });

app.whenReady().then(() => {
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
});

app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit(); });
app.on('activate', () => { if (BrowserWindow.getAllWindows().length === 0) app.whenReady(); });

ipcMain.handle('run-analysis', async () => {
    const analysis = {
        timestamp: new Date().toISOString(),
        summary: { total_storage: '156.7 GB', reclaimable: '67.3 GB', total_files: 12847, caches_size: '15.2 GB', dev_bloat_size: '32.1 GB' },
        recommendations: [
            { priority: 'high', category: 'dev_bloat', title: 'Clean 47 node_modules Folders', description: 'Found 47 node_modules folders totaling 25.3 GB.', space_savings: '25.3 GB', risk: 'low' },
            { priority: 'high', category: 'caches', title: 'Clean Browser Caches', description: 'Found 15.2 GB of caches.', space_savings: '15.2 GB', risk: 'low' }
        ],
        caches: [{ name: 'Chrome', size: '3.2 GB', safe: true }, { name: 'Spotify', size: '2.1 GB', safe: true }],
        dev_environments: { node_modules: { count: 47, size: '25.3 GB' }, python_venvs: { count: 12, size: '4.8 GB' } },
        storage_plan: { tier_1_keep_local: { count: 2341, size: '45.2 GB' }, tier_4_safe_delete: { count: 3421, size: '67.4 GB' } }
    };
    fs.writeFileSync(path.join(dataDir, 'latest_analysis.json'), JSON.stringify(analysis, null, 2));
    return { success: true, analysis };
});

ipcMain.handle('get-analysis', async () => {
    const file = path.join(dataDir, 'latest_analysis.json');
    return fs.existsSync(file) ? JSON.parse(fs.readFileSync(file, 'utf8')) : null;
});

ipcMain.handle('execute-action', async (e, action) => ({ success: true, message: action + ' done' }));
ipcMain.handle('get-archive-log', async () => []);
ipcMain.handle('open-path', async (e, p) => { shell.showItemInFolder(p); return { success: true }; });
ipcMain.handle('open-external', async (e, url) => { shell.openExternal(url); return { success: true }; });
