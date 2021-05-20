const { app, BrowserWindow, ipcMain } = require('electron')
const path = require('path')
const activeWin = require('./index');
let win = null;

function createWindow () {
  win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'ui-preload.js')
    }
  })

  win.loadFile('ui.html')
}

const handleTracking = async () => {
  try {
        const appData = await activeWin();
        win.webContents.send('render', JSON.stringify(appData));
  } catch (error) {
      console.log(error);
  } finally {
      setTimeout(handleTracking, 3000);
  }
}

ipcMain.handleOnce('start-loop', () => {
  handleTracking();
});

app.whenReady().then(() => {

  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})