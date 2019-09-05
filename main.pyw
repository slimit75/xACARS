# ----------------------------------------- #
# main.pyw                                  #
# Speed_Limit75                             #
#                                           #
# This file runs the main window, and       #
# getBid.pyw/setupFlight.pyw will move here #
# in the future.                            #
# ----------------------------------------- #

# Import libarys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import time
import urllib.request as urllib
import os

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

# Set variables
window = tk.Tk()
window.iconbitmap('Favicon.ico')
airline = tk.StringVar()
flightTime = 0

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
    ttk.Button(aboutWindow, text='Close', command=aboutWindow.quit).grid(row=5, column=0, sticky="we")
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
    g.config(state="disabled")

def editAirlines():
    listAirlines.reload()
    return

def setupFlight():
    global a
    global b
    global data

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
    global data
    global pirepID
    global Log
    global data

    preFileWindow = tk.Tk()
    cruiseAlt = tk.StringVar(preFileWindow)
    plannedFlightTime = tk.StringVar(preFileWindow)
    plannedDistance = tk.StringVar(preFileWindow)
    route = tk.StringVar(preFileWindow)
    selacf = tk.StringVar(preFileWindow)

    acf = []
    acf2 = []
    ids = []
    acf.append("Please select an aircraft")
    for key in data["flight"]["subfleets"]:
        for key2 in key["aircraft"]:
            acf2.append(str(key2["registration"]) + " [" + str(key2["icao"]) + "]")
            ids.append(key2["id"])

    #acf2.reverse()
    
    for key in acf2:
        acf.append(key)
    selacf.set(acf[0])
    
    preFileWindow.iconbitmap('Favicon.ico')
    preFileWindow.title('xACARS - Prefile')
    tk.Label(preFileWindow, text="Prefile", font="Arial").grid(row=0, column=0, columnspan=3, sticky="w")
    ttk.Separator(preFileWindow, orient=tk.HORIZONTAL).grid(row=1, columnspan=4, sticky="we")
    tk.Label(preFileWindow, text="Aircraft: ").grid(row=2, column=0)
    ttk.OptionMenu(preFileWindow, selacf, *acf).grid(row=2, column=1, sticky="we")
    tk.Label(preFileWindow, text="Cruise FL: ").grid(row=3, column=0)
    ttk.Entry(preFileWindow, textvariable=cruiseAlt).grid(row=3, column=1, sticky="we")
    tk.Label(preFileWindow, text="Planned Time: ").grid(row=4, column=0)
    ttk.Entry(preFileWindow, textvariable=plannedFlightTime).grid(row=4, column=1, sticky="we")
    tk.Label(preFileWindow, text="minutes").grid(row=4, column=2, sticky="w")
    tk.Label(preFileWindow, text="Planned Distance: ").grid(row=5, column=0)
    ttk.Entry(preFileWindow, textvariable=plannedDistance).grid(row=5, column=1, sticky="we")
    tk.Label(preFileWindow, text="nm").grid(row=5, column=2, sticky="w")
    tk.Label(preFileWindow, text="Route:").grid(row=6, column=0)
    ttk.Entry(preFileWindow, textvariable=route).grid(row=6, column=1, sticky="we")
    ttk.Button(preFileWindow, text='Save & Exit', command=preFileWindow.quit).grid(row=7, columnspan=4, sticky="we")
    preFileWindow.mainloop()
    preFileWindow.destroy()

    selacf = selacf.get()

    a = 0
    for key in acf:
        print(key)
        if key == selacf:
            break
        else:
            a = a + 1
    
    data = {
    "airline_id": str(data["flight"]["airline_id"]),
    "aircraft_id": str(ids[a-1]),
    "flight_number": str(data["flight"]["flight_number"]),
    "route_code": str(data["flight"]["route_code"]),
    "route_leg": str(data["flight"]["route_leg"]),
    "dpt_airport_id": str(data["flight"]["dpt_airport_id"]),
    "arr_airport_id": str(data["flight"]["arr_airport_id"]),
    "level": int(cruiseAlt.get()),
    "planned_distance": int(plannedDistance.get()),
    "planned_flight_time": int(plannedFlightTime.get()),
    "route": str(route.get()),
    "source_name": "xACARS",
    "flight_type": str(data["flight"]["flight_type"])
    }  
    
    data = json.dumps(data)
    data = web.post(config.website + '/api/pireps/prefile', data)
    data = json.loads(data.text)
    try:
        data = data["data"]
        pirepID = data["id"]

        b.config(state="disabled")
        c.config(state="normal")
        d.config(state="normal")
    except:
        data = data["error"]
        Log("Error: " + str(data["message"]))

def openWiki():
    webbrowser.open_new_tab("https://github.com/slimit75/xACARS/wiki")

def startFlight():
    global pirepID
    global flightTime
    flightTime = int(time.time())
    posUpdateLoop.startLoop(pirepID)
    Log('#######################################################')
    Log("Now logging flight.")
    c.config(state="disabled")
    e.config(state="normal")

def updateEnrouteTime():
    uetWindow = tk.Tk()
    newEnrouteTime = tk.StringVar(uetWindow)
    uetWindow.iconbitmap('Favicon.ico')
    uetWindow.title('xACARS - Enroute Time')
    tk.Label(uetWindow, text='Enroute Time', font="Arial").grid(row=0, columnspan=1, sticky="w") 
    ttk.Separator(uetWindow, orient=tk.HORIZONTAL).grid(row=1, columnspan=4, sticky="we")
    ttk.Entry(uetWindow, textvariable=newEnrouteTime).grid(row=2, column=0, sticky="we")
    tk.Label(uetWindow, text='minutes').grid(row=2, column=1, sticky="w")
    ttk.Button(uetWindow, text='Save & Exit', command=uetWindow.quit).grid(row=3, columnspan=2, sticky="we")
    uetWindow.mainloop()

    newEnrouteTime = newEnrouteTime.get()
    data = {"planned_flight_time": int(newEnrouteTime)}
    print(data)
    data = web.post(config.website + '/api/pireps/' + pirepID + '/update', data) 

    uetWindow.destroy()
    
def filePirep():
    global pirepID
    global flightTime

    fpWindow = tk.Tk()
    addComment = tk.IntVar(fpWindow)
    comment = tk.StringVar(fpWindow)
    fuel = tk.StringVar(fpWindow)
    distance = tk.StringVar(fpWindow)

    fpWindow.iconbitmap('Favicon.ico')
    fpWindow.title('xACARS - File Pirep')

    tk.Label(fpWindow, text='File Pirep', font="Arial").grid(sticky="w") 
    ttk.Separator(fpWindow, orient=tk.HORIZONTAL).grid(row=1, columnspan=2, sticky="we")

    tk.Label(fpWindow, text='Fuel Used').grid(row=2, column=0, sticky="w") 
    ttk.Entry(fpWindow, textvariable=fuel).grid(row=2, column=1, sticky="we")

    tk.Label(fpWindow, text='Distance').grid(row=3, column=0, sticky="w") 
    ttk.Entry(fpWindow, textvariable=distance).grid(row=3, column=1, sticky="we")

    ttk.Checkbutton(fpWindow, text="Comment?", variable=addComment).grid(row=4, sticky="w")
    ttk.Entry(fpWindow, textvariable=comment, width=50).grid(row=4, column=1, sticky="nwwe")

    ttk.Button(fpWindow, text='Save & Exit', command=fpWindow.quit).grid(row=5, columnspan=2, sticky="we")
    fpWindow.mainloop()

    flightTime = int(time.time()) - flightTime
    addComment = addComment.get()  
    flightTime = time.strftime('%H%M', time.gmtime(flightTime))
    data = {"flight_time": flightTime,"fuel_used": fuel.get(),"distance": distance.get()}       
    
    data = json.dumps(data)
    data = web.post(config.website + '/api/pireps/' + pirepID + '/file', data)

    if addComment == 1:
        data = {"comment": str(comment.get()),}       
        data = json.dumps(data)
        data = web.post(config.website + '/api/pireps/' + pirepID + '/comments', data) 
    
    f.config(state="disabled")
    Log('#######################################################')
    Log("Hope you had a great flight!")
    fpWindow.destroy()

def finishFlight():
    posUpdateLoop.stopLoop()
    f.config(state="normal")
    d.config(state="disabled")
    e.config(state="disabled")

def checkForUpdates():
    Log('#######################################################')
    Log("Checking for updates..")

    data = web.get('https://raw.githubusercontent.com/slimit75/xACARS/update-system/updates.json')
    data = json.loads(data)

    if config.getPreRel == True:
        if str(data["latestBeta"]) == config.version:
            Log("No updates avalible.")
        else:
            Log("There is a update avalible, please get it from")
            Log("https://github.com/slimit75/xACARS/releases")
    else:
        if str(data["latestStable"]) == config.version:
            Log("No updates avalible.")
        else:
            Log("There is a update avalible, please get it from")
            Log("https://github.com/slimit75/xACARS/releases")


# Draw window
window.title('xACARS ' + config.version)
tk.Label(window, text="Welcome to xACARS", font="Arial").grid(row=0, column=0)
g = ttk.Button(window, text='Login', command=login)
g.grid(row=1, column=0, sticky="wens")
a = ttk.Button(window, text='Select Bid', command=setupFlight, state="disabled")
a.grid(row=2, column=0, sticky='wens')
b = ttk.Button(window, text='Pre-File', command=preFile, state="disabled")
b.grid(row=3, column=0, sticky='wens')
c = ttk.Button(window, text='Start Flight', command=startFlight, state="disabled")
c.grid(row=4, column=0, sticky='wens')
d = ttk.Button(window, text='Update Enroute Time', command=updateEnrouteTime, state="disabled")
d.grid(row=5, column=0, sticky='wens')
e = ttk.Button(window, text='Finish Flight', command=finishFlight, state="disabled")
e.grid(row=6, column=0, sticky='wens')
f = ttk.Button(window, text='File PIREP', command=filePirep, state="disabled")
f.grid(row=7, column=0, sticky='wens')

menu = tk.Menu(window) 
window.config(menu=menu) 

log = tk.Listbox(window, width=55, height=15)
Log('Welcome to xACARS.') 
log.grid(row=0, column=1, rowspan=8)
Log('Please login.')
if config.loginMessage == True:
    Log('#######################################################')
    Log("You can log in by going to the 'Virtual Airlines' tab, and")
    Log("selecting 'Connect to a airline'. If you are new, you can")
    Log("add a airline by going to the same tab and click 'List, Edit &")
    Log("Add airlines'.")
    Log('#######################################################')
    Log("You can disable this message in settings.")

if config.checkUpdate == True:
    checkForUpdates()

mainMenu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label='Main', menu=mainMenu) 
mainMenu.add_command(label='Preferences', command=settings)
mainMenu.add_command(label='Check for updates', command=checkForUpdates)
mainMenu.add_separator()
mainMenu.add_command(label='Exit', command=window.destroy) 

vaMenu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label='Virtual Airlines', menu=vaMenu) 
vaMenu.add_command(label='Login', command=login)
vaMenu.add_command(label='List, Edit & Add Airlines', command=editAirlines)

helpMenu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label='Help', menu=helpMenu) 
helpMenu.add_command(label='About xACARS', command=about)
helpMenu.add_command(label='Simulator Connection Test', command=connectionTest)
helpMenu.add_command(label='Wiki', command=openWiki)
window.mainloop()