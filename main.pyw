# ----------------------------------------- #
# main.pyw                                  #
# Speed_Limit75                             #
#                                           #
# This file runs the main window, and       #
# getBid.pyw/setupFlight.pyw will move here #
# in the future.                            #
# ----------------------------------------- #

# Import libarys
import tkinter as tk # Runs displays
from tkinter import ttk # Adds seperator in some windows
from tkinter import messagebox # Drives OS error, warning, or info message

# Import local files
import config
import login as loginWindow
import web
import track
import posUpdateLoop
import listAirlines 
import settings as settingsWindow 
import getBid
import webbrowser

# Tells track.pyw to begin updating the input folder
if config.useFSUIPC == True:
    track.beginTrack()

# Set variables
window = tk.Tk()
window.iconbitmap('Favicon.ico')
airline = tk.StringVar()

# Define functions
def about():
    aboutWindow = tk.Tk()
    aboutWindow.iconbitmap('Favicon.ico')
    aboutWindow.title('xACARS - About')
    tk.Label(aboutWindow, text="xACARS " + config.version, font="Arial").grid(row=0, column=0)
    tk.Label(aboutWindow, text="xACARS was developed by Speed_Limit75.").grid(row=1, column=0)
    ttk.Separator(aboutWindow, orient=tk.HORIZONTAL).grid(row=2, column=0, sticky="we")
    tk.Label(aboutWindow, text="This program is currently a beta, so you should expect broken things.").grid(row=3, column=0, sticky="w")
    tk.Label(aboutWindow, text="xACARS is powered by FSUIPC/XPUIPC to gather data from the simulator.").grid(row=4, column=0, sticky="w")
    tk.Button(aboutWindow, text='Close', command=aboutWindow.quit).grid(row=5, column=0, sticky="we")
    aboutWindow.mainloop()
    aboutWindow.destroy()

def Log(text):
    log.insert(tk.END, text) 

def connectionTest():
    Log('#######################################################') 
    Log('Attempting to connect to FSUIPC/XPUIPC...')
    track.endTrack()
    isSuccess = track.beginTrack()
    if isSuccess == "Can Connect":
        Log('Can connect to FSUIPC.')
        track.posUpdate()
    else:
        Log('Unable to connect.')
        Log(isSuccess)

def login():
    global a
    Log('#######################################################')
    Log("Attempting login..")
    loginWindow.login()
    Log("Logged in under " + config.airline)
    a.config(state="normal")

def editAirlines():
    listAirlines.reload()
    return

def setupFlight():
    global a
    global b

    data = getBid.draw()
    Log('#######################################################')
    Log("Selected flight: " + str(data["flight"]["ident"]))
    Log("Departs from " + str(data["flight"]["dpt_airport_id"]) + " and arrives at " + str(data["flight"]["arr_airport_id"]))
    a.config(state="disabled")
    b.config(state="normal")
    return

def settings():
    settingsWindow.drawWindow(window)
    return

def preFile():
    preFileWindow = tk.Tk()

    cruiseAlt = tk.StringVar(preFileWindow)
    plannedFlightTime = tk.StringVar(preFileWindow)
    plannedDistance = tk.StringVar(preFileWindow)
    route = tk.StringVar(preFileWindow)

    preFileWindow.iconbitmap('Favicon.ico')
    preFileWindow.title('xACARS - Prefile')
    tk.Label(preFileWindow, text="Prefile", font="Arial").grid(row=0, column=0, columnspan=3, sticky="w")
    ttk.Separator(preFileWindow, orient=tk.HORIZONTAL).grid(row=1, columnspan=4, sticky="we")
    #tk.Label(preFileWindow, text="This screen does nothing- yet").grid(row=1, column=0)
    tk.Label(preFileWindow, text="Cruise FL: ").grid(row=2, column=0)
    tk.Entry(preFileWindow, textvariable=cruiseAlt).grid(row=2, column=1, sticky="we")
    tk.Label(preFileWindow, text="Planned Time: ").grid(row=3, column=0)
    tk.Entry(preFileWindow, textvariable=plannedFlightTime).grid(row=3, column=1, sticky="we")
    tk.Label(preFileWindow, text="minutes").grid(row=3, column=2, sticky="w")
    tk.Label(preFileWindow, text="Planned Distance: ").grid(row=4, column=0)
    tk.Entry(preFileWindow, textvariable=plannedDistance).grid(row=4, column=1, sticky="we")
    tk.Label(preFileWindow, text="nm").grid(row=4, column=2, sticky="w")
    tk.Label(preFileWindow, text="Route:").grid(row=5, column=0)
    tk.Entry(preFileWindow, textvariable=route).grid(row=5, column=1, sticky="we")
    tk.Button(preFileWindow, text='Save & Exit', command=preFileWindow.quit).grid(row=6, columnspan=4, sticky="we")
    preFileWindow.mainloop()
    preFileWindow.destroy()

    b.config(state="disabled")
    c.config(state="normal")
    d.config(state="normal")

def openWiki():
    webbrowser.open_new_tab("https://github.com/slimit75/xACARS/wiki")

def updateCheck():
    messagebox.showinfo("xACARS","This feature doesnt exist.. yet.")

def startFlight():
    posUpdateLoop.startLoop()
    Log('#######################################################')
    Log("Now logging flight.")
    c.config(state="disabled")
    e.config(state="normal")

def updateEnrouteTime():
    uetWindow = tk.Tk()
    newEnrouteTime = tk.StringVar(uetWindow)
    uetWindow.iconbitmap('Favicon.ico')
    window.title('xACARS - Enroute Time')
    tk.Label(uetWindow, text='Enroute Time', font="Arial").grid(row=0, columnspan=1, sticky="w") 
    ttk.Separator(uetWindow, orient=tk.HORIZONTAL).grid(row=1, columnspan=4, sticky="we")
    tk.Entry(uetWindow, textvariable=newEnrouteTime).grid(row=2, column=0, sticky="we")
    tk.Label(uetWindow, text='minutes').grid(row=2, column=1, sticky="w")
    tk.Button(uetWindow, text='Save & Exit', command=uetWindow.quit).grid(row=3, columnspan=2, sticky="we")
    uetWindow.mainloop()

    # Update enroute time

    uetWindow.destroy()

# Draw window
window.title('xACARS ' + config.version)
tk.Label(window, text="Welcome to xACARS", font="Arial").grid(row=0, column=0)
a = tk.Button(window, text='Select Bid', command=setupFlight, state="disabled")
a.grid(row=1, column=0, sticky='wens')
b = tk.Button(window, text='Pre-File', command=preFile, state="disabled")
b.grid(row=2, column=0, sticky='wens')
c = tk.Button(window, text='Start Flight', command=startFlight, state="disabled")
c.grid(row=3, column=0, sticky='wens')
d = tk.Button(window, text='Update Enroute Time', command=updateEnrouteTime, state="disabled")
d.grid(row=4, column=0, sticky='wens')
e = tk.Button(window, text='Finish Flight', state="disabled")
e.grid(row=5, column=0, sticky='wens')
f = tk.Button(window, text='File PIREP', state="disabled")
f.grid(row=6, column=0, sticky='wens')

menu = tk.Menu(window) 
window.config(menu=menu) 

log = tk.Listbox(window, width=55, height=15)
Log('Welcome to xACARS.') 
log.grid(row=0, column=1, rowspan=7)
Log('Please login.')
if config.loginMessage == True:
    Log('#######################################################')
    Log("You can log in by going to the 'Virtual Airlines' tab, and")
    Log("selecting 'Connect to a airline'. If you are new, you can")
    Log("add a airline by going to the same tab and click 'List, Edit &")
    Log("Add airlines'.")
    Log('#######################################################')
    Log("You can disable this message in settings.")

mainMenu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label='Main', menu=mainMenu) 
mainMenu.add_command(label='Preferences', command=settings)
mainMenu.add_command(label='Check for updates', command=updateCheck)
mainMenu.add_separator()
mainMenu.add_command(label='Exit', command=window.destroy) 

vaMenu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label='Virtual Airlines', menu=vaMenu) 
vaMenu.add_command(label='Connect to an Airline', command=login)
vaMenu.add_command(label='List, Edit & Add Airlines', command=editAirlines)

helpMenu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label='Help', menu=helpMenu) 
helpMenu.add_command(label='About xACARS', command=about)
helpMenu.add_command(label='Simulator Connection Test', command=connectionTest)
helpMenu.add_command(label='Wiki', command=openWiki)

window.mainloop()
posUpdateLoop.stopLoop()