const { contextBridge, ipcRenderer } = require('electron');

// Expose secure APIs to the renderer process
contextBridge.exposeInMainWorld('storageAPI', {
    // Analysis operations
    runAnalysis: (options) => ipcRenderer.invoke('run-analysis', options),
    getAnalysis: () => ipcRenderer.invoke('get-analysis'),
    
    // Action operations
    executeAction: (action, params) => ipcRenderer.invoke('execute-action', action, params),
    
    // Archive log
    getArchiveLog: () => ipcRenderer.invoke('get-archive-log'),
    
    // File operations
    openPath: (filePath) => ipcRenderer.invoke('open-path', filePath),
    openExternal: (url) => ipcRenderer.invoke('open-external', url),
    
    // Event listeners
    onAnalysisStarted: (callback) => {
        ipcRenderer.on('analysis-started', () => callback());
    },
    
    onAnalysisProgress: (callback) => {
        ipcRenderer.on('analysis-progress', (event, progress) => callback(progress));
    },
    
    onAnalysisComplete: (callback) => {
        ipcRenderer.on('analysis-complete', (event, analysis) => callback(analysis));
    },
    
    onAnalysisError: (callback) => {
        ipcRenderer.on('analysis-error', (event, error) => callback(error));
    },
    
    onOpenSettings: (callback) => {
        ipcRenderer.on('open-settings', () => callback());
    },
    
    // Remove listeners
    removeAllListeners: (channel) => {
        ipcRenderer.removeAllListeners(channel);
    }
});

// Log when preload script is loaded
console.log('Storage Intelligence preload script loaded');
