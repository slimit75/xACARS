const {app, BrowserWindow} = require('electron')
const path = require("path")

function createWindow () {
    const modalPath = path.join('file://', __dirname, "login.html")
    let win = new BrowserWindow({
        transparent: false,
        frame: false,
        resizable: false,
        webPreferences: {
            nodeIntegration: true
        },
        width: 800, 
        height: 600
    })

    win.on("close", () => {win = null})
    win.loadURL(modalPath)
    win.show()
}

app.allowRendererProcessReuse = true // Suppresses warning about default value (false) being depreciated
app.on('ready', createWindow)