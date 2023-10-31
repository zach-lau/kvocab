const {app, BrowserWindow} = require('electron')
const electronReload = require('electron-reload');
const path = require('node:path')

electronReload(__dirname);
if (module.hot){
    module.hot.accept();
}

const createWindow = () => {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
    });
    win.loadFile('home.html');
}

app.whenReady().then(() => {
    createWindow()
})
