console.log('Testing electron require...');
try {
    const electron = require('electron');
    console.log('Electron loaded:', typeof electron);
    console.log('App:', typeof electron.app);
    if (electron.app) {
        console.log('SUCCESS! Electron is working');
    } else {
        console.log('electron.app is undefined');
    }
} catch (e) {
    console.log('Error:', e.message);
}
