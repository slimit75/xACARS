# ----------------------------------------- #
# main.pyw                                  #
# Speed_Limit75                             #
# Additional contributions by Henry Shires  #
#                                           #
# This file runs the main window, and       #
# getBid.pyw will move here in the future.  #
# ----------------------------------------- #

# Import libarys
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import json
import time
import urllib.request as urllib
import os
import webbrowser

# Import local files
import config
import login as Login
import web
import track
import posUpdateLoop
import listAirlines
import settings as settingsWindow
import getBid

'''
Draw xACARS UI
'''


class App:

    def __init__(self, root):
        self.root = root
        self.root.config(menu=self.menu())
        self.root.iconbitmap('images/Favicon.ico')
        self.root.title('xACARS - ' + config.version)
        self.root.geometry("960x480")

        '''
        background = Image.open('images/background-main.png')
        self.bg = ImageTk.PhotoImage(background)
        self.background = tk.Label(self.root, image=self.bg)
        self.background.place(x=0, y=0, relwidth=1, relheight=1)
        '''

        # Frames
        self.loginFrame = tk.Frame(self.root)
        self.registerFrame = tk.Frame(self.root)
        self.body = tk.Frame(self.root)

        # Variables
        self.airline = tk.StringVar(self.root)
        self.username = tk.StringVar(self.root)
        self.key = tk.StringVar(self.root)
        self.website = tk.StringVar(self.root)

        self.List = config.list
        self.websites = config.websites
        self.savedAPIKeys = config.savedAPIKeys
        self.usernames = config.usernames

        self.flightTime = 0

        # Tkinter Styles
        self.h1 = tkFont.Font(family="Verdana", size=20)
        self.h2 = tkFont.Font(family="Verdana", size=18)
        self.h3 = tkFont.Font(family="Verdana", size=14)

        self.style = ttk.Style()

        # Widgets
        self.login()

    def menu(self):
        # Header
        self.title = tk.Label(self.root, text="Welcome to xACARS",
                              font="Arial")
        self.title.grid(row=2, column=0)

        # Toolbar
        self.toolbar = tk.Menu(self.root)

        self.mainMenu = tk.Menu(self.toolbar, tearoff=False)
        self.toolbar.add_cascade(label='Main', menu=self.mainMenu)
        self.mainMenu.add_command(label='Preferences', command=self.settings)
        self.mainMenu.add_command(label='Check for updates',
                                  command=web.checkForUpdates)
        self.mainMenu.add_separator()
        self.mainMenu.add_command(label='Exit', command=self.root.destroy)

        self.vaMenu = tk.Menu(self.toolbar, tearoff=False)
        self.toolbar.add_cascade(label='Virtual Airlines', menu=self.vaMenu)
        self.vaMenu.add_command(label='Login', command=self.login)
        self.vaMenu.add_command(
            label='List, Edit & Add Airlines', command=self.editAirlines)

        self.helpMenu = tk.Menu(self.toolbar, tearoff=False)
        self.toolbar.add_cascade(label='Help', menu=self.helpMenu)
        self.helpMenu.add_command(label='About xACARS', command=self.about)
        self.helpMenu.add_command(label='Simulator Connection Test',
                                  command=self.connectionTest)
        self.helpMenu.add_command(label='Wiki', command=self.openWiki)

    '''
    Main Menu (Login)
    '''

    def login(self):
        # Hide other components
        self.title.grid_forget()
        self.registerFrame.grid_forget()

        self.body.grid(row=0, column=1)

        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        img = Image.open("images/estafeta_red.png")
        img = img.resize((int(img.size[0] * 0.75), int(img.size[1] * 0.75)))

        self.img = ImageTk.PhotoImage(img)
        self.banner = tk.Label(self.body, image=self.img)
        self.banner.grid(row=0, column=1)

        self.headerLbl = tk.Label(self.body, text="xACARS - Estafeta Edition",
                              font=self.h1)
        self.headerLbl.grid(row=1, column=1, pady=20)

        self.loginFrame.grid(row=2, column=1)
        self.loginFrame.grid_rowconfigure(0, weight=0)
        self.loginFrame.grid_rowconfigure(2, weight=1)
        self.loginFrame.grid_columnconfigure(0, weight=1)
        self.loginFrame.grid_columnconfigure(2, weight=1)

        tk.Label(self.loginFrame, text="Select Airline").grid(row=0, column=1, sticky="w", pady=5)
        ttk.OptionMenu(self.loginFrame, self.airline, *self.List).grid(row=0, column=1, pady=5)

        ttk.Entry(self.loginFrame, textvariable=self.username, width=64).grid(row=1, column=1)
        tk.Label(self.loginFrame, text="Username").grid(row=2, column=1, sticky="w", pady=(0, 5))

        ttk.Entry(self.loginFrame, show="*", textvariable=self.key, width=64).grid(row=3, column=1)
        tk.Label(self.loginFrame, text="API Key").grid(row=4, column=1, sticky="w", pady=(0, 5))

        '''
        self.autofillBtn = ttk.Button(self.loginFrame, text="Autofill",
                                command=self.autofill)
        self.autofillBtn.grid(row=2, column=2)
        '''
        self.registerLink = tk.Label(self.loginFrame, text='New to xACARS? Add an account', fg="#CC2229")
        self.registerLink.grid(row=5, column=1, sticky="w", pady=10)
        self.registerLink.bind("<Enter>", lambda event, h=self.registerLink: self.registerLink.config(fg="#de3b40"))
        self.registerLink.bind("<Leave>", lambda event, h=self.registerLink: self.registerLink.config(fg="#CC2229"))
        self.registerLink.bind("<Button-1>", lambda e, h=self.registerLink: self.register())

        self.loginButton = tk.Button(self.loginFrame, text='Log In', command=self.doLogin, bg="#CC2229", fg='white', borderwidth=0, width=20, height=2)
        self.loginButton.grid(row=5, column=1, sticky="e", pady=10)
        self.loginButton.bind("<Enter>", lambda event, h=self.loginButton: self.loginButton.config(bg="#de3b40"))
        self.loginButton.bind("<Leave>", lambda event, h=self.loginButton: self.loginButton.config(bg="#CC2229"))

    '''
    Run Login function
    '''

    def doLogin(self):
        # Log('#######################################################')
        # Log("Logging in...")
        # Log("Signed in with " + config.airline)
        Login.login(self.airline, self.username, self.key)

    def doRegister(self):
        Login.register(self.airline, self.website, self.username, self.key)

    def autofill(self):
        index = self.List.index(self.airline.get())
        self.key.set(self.savedAPIKeys[index])
        return

    '''
        def autofillUsername(self):
            index = self.List.index(self.airline.get())
            self.username.set(self.usernames[index])
            return
    '''

    def register(self):
        self.loginFrame.grid_forget()

        self.registerFrame.grid(row=2, column=1)
        self.headerLbl.config(text="xACARS - Register")
        self.headerLbl.grid(row=1, column=1, pady=10)

        ttk.Entry(self.registerFrame, textvariable=self.airline, width=64).grid(row=3, column=1)
        tk.Label(self.registerFrame, text="Airline Name").grid(row=4, column=1, sticky="w", pady=(0, 5))

        ttk.Entry(self.registerFrame, width=64).grid(row=5, column=1)
        tk.Label(self.registerFrame, text="Airline Website (Format: https://myva.com - no slash at the end)").grid(row=6, column=1, sticky="w", pady=(0, 5))

        ttk.Entry(self.registerFrame, textvariable=self.username, width=64).grid(row=7, column=1)
        tk.Label(self.registerFrame, text="Username from phpVMS (Must be EXACT)").grid(row=8, column=1, sticky="w", pady=(0, 5))

        ttk.Entry(self.registerFrame, show="*", textvariable=self.key, width=64).grid(row=9, column=1)
        tk.Label(self.registerFrame, text="API Key").grid(row=10, column=1, sticky="w")

        self.registerButton = tk.Button(self.registerFrame, text='Add Account', command=self.doRegister, bg="#CC2229", fg='white', borderwidth=0, width=20, height=2)
        self.registerButton.grid(row=11, column=1, sticky="e", pady=10)
        self.registerButton.bind("<Enter>", lambda event, h=self.registerButton: self.registerButton.config(bg="#de3b40"))
        self.registerButton.bind("<Leave>", lambda event, h=self.registerButton: self.registerButton.config(bg="#CC2229"))

        self.link1 = tk.Label(self.registerFrame, text='Back', fg="#CC2229")
        self.link1.grid(row=11, column=1, sticky="w", pady=10)
        self.link1.bind("<Enter>", lambda event, h=self.link1: self.link1.config(fg="#de3b40"))
        self.link1.bind("<Leave>", lambda event, h=self.link1: self.link1.config(fg="#CC2229"))
        self.link1.bind("<Button-1>", lambda e, h=self.link1: self.login())

    def about(self):
        self.frame1 = tk.Frame(self.root)
        self.frame1.grid(row=6, column=6)
        self.header = tk.Label(self.frame1, text="xACARS " + config.version,
                               font="Arial")
        self.header.grid(row=0, column=0)
        self.bio = tk.Label(
            self.frame1, text="xACARS was developed by Speed_Limit75 - This version includes additional developments by Henry Shires.")
        self.bio.grid(
            row=1, column=0)
        self.space1 = ttk.Separator(self.frame1, orient=tk.HORIZONTAL)
        self.space1.grid(
            row=2, column=0, sticky="we")

        self.text = tk.Label(
            self.frame1, text="This program is currently in alpha testing, so expect major bugs and issues.")
        self.text.grid(
            row=3, column=0, sticky="w")

        self.text2 = tk.Label(
            self.frame1, text="xACARS is powered by FSUIPC/XPUIPC to gather data from the simulator.")
        self.text2.grid(row=4, column=0, sticky="w")
        ttk.Button(self.frame1, text='Close', command=self.hide).grid(
            row=5, column=0, sticky="we")

    def hide(self):
        hide = 1
        if hide == 0:
            self.frame1.destroy()
        else:
            pass

    def connectionTest(self):
        Log('#######################################################')
        Log('Attempting to connect to your simulator...')
        track.endTrack()
        isSuccess = track.beginTrack()
        if isSuccess == "Can Connect":
            Log('Connected to simulator!')
            track.posUpdate()
        else:
            Log('ERROR: Unable to connect.')
            Log(isSuccess)
        track.endTrack()

    def editAirlines(self):
        listAirlines.reload()
        return

    def setupFlight(self):
        global a
        global b
        global data

        # Get Data
        data = getBid.draw()

        Log('#######################################################')
        Log("Selected flight: " + str(data["flight"]["ident"]))
        Log("Departs from " + str(data["flight"]["dpt_airport_id"]) +
            " and arrives at " + str(data["flight"]["arr_airport_id"]))
        a.config(state="disabled")
        b.config(state="normal")
        return

    def settings(self):
        settingsWindow.drawWindow(window)
        return

    def preFile(self):
        global data
        global pirepID
        global Log

        preFileWindow = tk.Tk()
        cruiseAlt = tk.StringVar(preFileWindow)
        plannedFlightTime = tk.StringVar(preFileWindow)
        plannedDistance = tk.StringVar(preFileWindow)
        route = tk.StringVar(preFileWindow)
        selacf = tk.StringVar(preFileWindow)

        # Get subfleet from flight information
        flightId = data["flight_id"]
        flightData = json.loads(
            web.get(config.website + '/api/flights/' + flightId))["data"]

        acf = []
        acf2 = []
        ids = []
        acf.append("Please select an aircraft")

        for key in flightData["subfleets"]:
            for key2 in key["aircraft"]:
                acf2.append(str(key2["registration"]) +
                            " [" + str(key2["icao"]) + "]")
                ids.append(key2["id"])

        for key in acf2:
            acf.append(key)
        selacf.set(acf[0])

        preFileWindow.iconbitmap('Favicon.ico')
        preFileWindow.title('xACARS - Prefile')
        tk.Label(preFileWindow, text="Prefile", font="Arial").grid(
            row=0, column=0, columnspan=3, sticky="w")
        ttk.Separator(preFileWindow, orient=tk.HORIZONTAL).grid(
            row=1, columnspan=4, sticky="we")
        tk.Label(preFileWindow, text="Aircraft: ").grid(row=2, column=0)
        ttk.OptionMenu(preFileWindow, selacf, *
                       acf).grid(row=2, column=1, sticky="we")
        tk.Label(preFileWindow, text="Cruise FL: ").grid(row=3, column=0)
        ttk.Entry(preFileWindow, textvariable=cruiseAlt).grid(
            row=3, column=1, sticky="we")
        tk.Label(preFileWindow, text="Planned Time: ").grid(row=4, column=0)
        ttk.Entry(preFileWindow, textvariable=plannedFlightTime).grid(
            row=4, column=1, sticky="we")
        tk.Label(preFileWindow, text="minutes").grid(
            row=4, column=2, sticky="w")
        tk.Label(preFileWindow, text="Planned Distance: ").grid(
            row=5, column=0)
        ttk.Entry(preFileWindow, textvariable=plannedDistance).grid(
            row=5, column=1, sticky="we")
        tk.Label(preFileWindow, text="nm").grid(row=5, column=2, sticky="w")
        tk.Label(preFileWindow, text="Route:").grid(row=6, column=0)
        ttk.Entry(preFileWindow, textvariable=route).grid(
            row=6, column=1, sticky="we")
        ttk.Button(preFileWindow, text='Save & Exit', command=preFileWindow.quit).grid(
            row=7, columnspan=4, sticky="we")
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

    def startFlight(self):
        global pirepID
        global flightTime
        flightTime = int(time.time())
        posUpdateLoop.startLoop(pirepID)
        Log('#######################################################')
        Log("Now logging flight.")
        c.config(state="disabled")
        e.config(state="normal")

    def updateEnrouteTime(self):
        uetWindow = tk.Tk()
        newEnrouteTime = tk.StringVar(uetWindow)
        uetWindow.iconbitmap('Favicon.ico')
        uetWindow.title('xACARS - Enroute Time')
        tk.Label(uetWindow, text='Enroute Time', font="Arial").grid(
            row=0, columnspan=1, sticky="w")
        ttk.Separator(uetWindow, orient=tk.HORIZONTAL).grid(
            row=1, columnspan=4, sticky="we")
        ttk.Entry(uetWindow, textvariable=newEnrouteTime).grid(
            row=2, column=0, sticky="we")
        tk.Label(uetWindow, text='minutes').grid(row=2, column=1, sticky="w")
        ttk.Button(uetWindow, text='Save & Exit', command=uetWindow.quit).grid(
            row=3, columnspan=2, sticky="we")
        uetWindow.mainloop()

        newEnrouteTime = newEnrouteTime.get()
        data = {"planned_flight_time": int(newEnrouteTime)}
        print(data)
        data = web.post(config.website + '/api/pireps/' +
                        pirepID + '/update', data)

        uetWindow.destroy()

    def filePirep(self):
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
        ttk.Separator(fpWindow, orient=tk.HORIZONTAL).grid(
            row=1, columnspan=2, sticky="we")

        tk.Label(fpWindow, text='Fuel Used').grid(row=2, column=0, sticky="w")
        ttk.Entry(fpWindow, textvariable=fuel).grid(
            row=2, column=1, sticky="we")

        tk.Label(fpWindow, text='Distance').grid(row=3, column=0, sticky="w")
        ttk.Entry(fpWindow, textvariable=distance).grid(
            row=3, column=1, sticky="we")

        ttk.Checkbutton(fpWindow, text="Comment?",
                        variable=addComment).grid(row=4, sticky="w")
        ttk.Entry(fpWindow, textvariable=comment, width=50).grid(
            row=4, column=1, sticky="nwwe")

        ttk.Button(fpWindow, text='Save & Exit', command=fpWindow.quit).grid(
            row=5, columnspan=2, sticky="we")
        fpWindow.mainloop()

        flightTime = int(time.time()) - flightTime
        addComment = addComment.get()
        flightTime = time.strftime('%H%M', time.gmtime(flightTime))
        data = {"flight_time": flightTime,
                "fuel_used": fuel.get(), "distance": distance.get()}

        data = json.dumps(data)
        data = web.post(config.website + '/api/pireps/' +
                        pirepID + '/file', data)

        if addComment == 1:
            data = {"comment": str(comment.get()), }
            data = json.dumps(data)
            data = web.post(config.website + '/api/pireps/' +
                            pirepID + '/comments', data)

        f.config(state="disabled")
        Log('#######################################################')
        Log("Hope you had a great flight!")
        fpWindow.destroy()

    def finishFlight(self):
        posUpdateLoop.stopLoop()
        f.config(state="normal")
        d.config(state="disabled")
        e.config(state="disabled")

    def Log(self, text):
        log.insert(tk.END, text)

    def openWiki():
        webbrowser.open_new_tab("https://github.com/slimit75/xACARS/wiki")

        # Button Grid
        '''
        g = ttk.Button(window, text='Login', command=login)
        g.grid(row=1, column=0, sticky="wens")

        a = ttk.Button(window, text='Select Bid',
                    command=setupFlight, state="disabled")
        a.grid(row=2, column=0, sticky='wens')
        b = ttk.Button(window, text='Pre-File',
                       command=preFile, state="disabled")
        b.grid(row=3, column=0, sticky='wens')
        c = ttk.Button(window, text='Start Flight',
                    command=startFlight, state="disabled")
        c.grid(row=4, column=0, sticky='wens')
        d = ttk.Button(window, text='Update Enroute Time',
                    command=updateEnrouteTime, state="disabled")
        d.grid(row=5, column=0, sticky='wens')
        e = ttk.Button(window, text='Finish Flight',
                    command=finishFlight, state="disabled")
        e.grid(row=6, column=0, sticky='wens')
        f = ttk.Button(window, text='File PIREP',
                    command=filePirep, state="disabled")
        f.grid(row=7, column=0, sticky='wens')

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
                Log('#######################################################')
                Log("Checking for updates..")
                if (web.checkForUpdates()):
                    Log("There is a update avalible, please get it from")
                    Log("https://github.com/slimit75/xACARS/releases")
                else:
                    Log("No updates avalible.")
        '''


# Main loop
window = tk.Tk()
App(window)
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.mainloop()
