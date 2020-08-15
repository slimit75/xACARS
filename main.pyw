# ----------------------------------------- #
# main.pyw                                  #
# Speed_Limit75                             #
# Additional contributions by Henry Shires  #
#                                           #
# This file runs the main window            #
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

'''
Draw xACARS UI
'''

class App:

    def __init__(self, root):
        self.root = root
        self.root.iconbitmap('images/Favicon.ico')
        self.root.title('xACARS - ' + config.version)
        self.root.geometry("960x530")

        # Frames
        self.loginFrame = tk.Frame(self.root)
        self.registerFrame = tk.Frame(self.root)
        self.body = tk.Frame(self.root)
        self.dbHeader = tk.Frame(self.root)
        self.dbBody = tk.Frame(self.root)
        self.bidsFrame = tk.Frame(self.root)
        self.prefileFrame = tk.Frame(self.root)
        self.fileFrame = tk.Frame(self.root)

        # Variables
        self.airline = tk.StringVar(self.root)
        self.username = tk.StringVar(self.root)
        self.key = tk.StringVar(self.root)
        self.website = tk.StringVar(self.root)
        self.rememberMe = tk.BooleanVar(self.root)

        self.List = config.List
        self.websites = config.websites
        self.savedAPIKeys = config.savedAPIKeys
        self.usernames = config.usernames

        self.pirepID = None
        self.data = None

        # Tkinter Styles
        self.h1 = tkFont.Font(family="Verdana", size=20)
        self.h2 = tkFont.Font(family="Verdana", size=18)
        self.h3 = tkFont.Font(family="Verdana", size=14)
        self.h4 = tkFont.Font(family="Verdana", size=12)

        self.style = ttk.Style()
        self.style.configure("TButton", padding=5)

        ## Dashboard Components
        self.dashboardViewRow = 0
        self.dashboardViewCol = 1
        self.dashboardViewSticky = "n"
        self.dashboardViewPadY = 100

        # Images
        img = Image.open("images/feature.png")
        img = img.resize((int(img.size[0] * 0.75), int(img.size[1] * 0.75)))

        img2 = img.resize((int(img.size[0] * 0.5), int(img.size[1] * 0.5)))

        self.img = ImageTk.PhotoImage(img)
        self.img2 = ImageTk.PhotoImage(img2)

        # Widgets
        if (config.rememberUser()):
            self.airline.set(config.airline)
            self.website.set(config.website)
            self.key.set(config.APIKey)
            self.username.set(config.username)
            self.rememberMe.set(True)

            self.doLogin()
        else:
            self.login()

    def menu(self):
        # Toolbar
        self.toolbar = tk.Menu(self.root)
        self.root.config(menu=self.toolbar)

        self.mainMenu = tk.Menu(self.toolbar, tearoff=False)
        self.toolbar.add_cascade(label='File', menu=self.mainMenu)
        self.mainMenu.add_command(label='Preferences', command=self.settings)
        self.mainMenu.add_command(label='Manage Accounts', command=self.accounts)
        self.mainMenu.add_command(label='Check for updates',
                                  command=self.doCheckForUpdates)
        self.mainMenu.add_separator()
        self.mainMenu.add_command(label='Sign Out', command=self.doSignOut)
        self.mainMenu.add_command(label='Exit', command=self.root.destroy)

        self.helpMenu = tk.Menu(self.toolbar, tearoff=False)
        self.toolbar.add_cascade(label='Help', menu=self.helpMenu)
        self.helpMenu.add_command(label='About xACARS', command=self.about)
        self.helpMenu.add_command(label='Simulator Connection Test',
                                  command=self.connectionTest)
        self.helpMenu.add_command(label='Wiki', command=web.openWiki)

    """
    Main Menu (Login)
    """
    def login(self):
        # Reload list of airlines
        config.reloadAirlines()

        self.List = config.List
        self.websites = config.websites
        self.savedAPIKeys = config.savedAPIKeys
        self.usernames = config.usernames

        # Hide other components
        self.registerFrame.grid_forget()

        self.body.grid(row=0, column=1)

        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        self.banner = tk.Label(self.body, image=self.img)
        self.banner.grid(row=0, column=1)

        self.headerLbl = tk.Label(self.body, text="xACARS - Estafeta Edition",
                              font=self.h1)
        self.headerLbl.grid(row=1, column=1, pady=40)

        self.loginFrame.grid(row=2, column=1)
        self.loginFrame.grid_rowconfigure(0, weight=0)
        self.loginFrame.grid_rowconfigure(2, weight=1)
        self.loginFrame.grid_columnconfigure(0, weight=1)
        self.loginFrame.grid_columnconfigure(2, weight=1)

        tk.Label(self.loginFrame, text="Select Airline").grid(row=0, column=1, sticky="w", pady=5)
        ttk.OptionMenu(self.loginFrame, self.airline, "Select an Airline", *self.List).grid(row=0, column=1, pady=5)

        ttk.Entry(self.loginFrame, textvariable=self.username, width=64).grid(row=1, column=1)
        tk.Label(self.loginFrame, text="Username").grid(row=2, column=1, sticky="w", pady=(0, 5))

        ttk.Entry(self.loginFrame, show="*", textvariable=self.key, width=64).grid(row=3, column=1)
        tk.Label(self.loginFrame, text="API Key").grid(row=4, column=1, sticky="w", pady=(0, 5))

        ttk.Checkbutton(self.loginFrame, text="Log in automatically", variable=self.rememberMe).grid(row=5, column=1, sticky="w")

        self.registerLink = tk.Label(self.loginFrame, text='New to xACARS? Add an account', fg="#CC2229")
        self.registerLink.grid(row=6, column=1, sticky="w", pady=10)
        self.registerLink.bind("<Enter>", lambda event, h=self.registerLink: self.registerLink.config(fg="#de3b40"))
        self.registerLink.bind("<Leave>", lambda event, h=self.registerLink: self.registerLink.config(fg="#CC2229"))
        self.registerLink.bind("<Button-1>", lambda e, h=self.registerLink: self.register())

        self.loginButton = tk.Button(self.loginFrame, text='Log In', command=self.doLogin, bg="#CC2229", fg='white', borderwidth=0, width=20, height=2)
        self.loginButton.grid(row=6, column=1, sticky="e", pady=10)
        self.loginButton.bind("<Enter>", lambda event, h=self.loginButton: self.loginButton.config(bg="#de3b40"))
        self.loginButton.bind("<Leave>", lambda event, h=self.loginButton: self.loginButton.config(bg="#CC2229"))

    def register(self):
        self.loginFrame.grid_forget()

        self.registerFrame.grid(row=2, column=1)
        self.headerLbl.config(text="xACARS - Register")
        self.headerLbl.grid(row=1, column=1, pady=10)

        ttk.Entry(self.registerFrame, textvariable=self.airline, width=64).grid(row=3, column=1)
        tk.Label(self.registerFrame, text="Airline Name").grid(row=4, column=1, sticky="w", pady=(0, 5))

        ttk.Entry(self.registerFrame, textvariable=self.website, width=64).grid(row=5, column=1)
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

    def accounts(self):
        config.reloadAirlines()

        self.accountsMenu = tk.Toplevel()
        self.accountsMenu.title('xACARS - Manage Accounts')
        self.accountsMenu.iconbitmap('images/Favicon.ico')
        self.accountsMenu.geometry("400x250")

        self.delAirline = tk.StringVar()

        tk.Label(self.accountsMenu, text='Airline to edit: ').grid(row=0, column=0)
        ttk.OptionMenu(self.accountsMenu, self.delAirline, 'Select an Airline', *self.List).grid(row=0, column=1)
        tk.Label(self.accountsMenu, text='Airline Name: ').grid(row=1, column=0)
        tk.Label(self.accountsMenu, text='Airline URL: ').grid(row=2, column=0)
        tk.Label(self.accountsMenu, text='Username: ').grid(row=3, column=0)
        tk.Label(self.accountsMenu, text='API Key: ').grid(row=4, column=0)
        ttk.Entry(self.accountsMenu, textvariable=self.airline, text=self.airline).grid(row=1, column=1)
        ttk.Entry(self.accountsMenu, textvariable=self.website, text=self.website).grid(row=2, column=1)
        ttk.Entry(self.accountsMenu, textvariable=self.username, text=self.username).grid(row=3, column=1)
        ttk.Entry(self.accountsMenu, show="*", textvariable=self.key, text=self.key).grid(row=4, column=1)
        ttk.Button(self.accountsMenu, text='Update', command=self.doEdit).grid(row=5, column=0, sticky='we')
        ttk.Button(self.accountsMenu, text='Delete Account', command=self.doDelete).grid(row=5, column=1)


    def dashboard(self):
        self.body.grid_forget()
        self.loginFrame.grid_forget()

        self.menu()

        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(2, weight=0)
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(2, weight=0)
        
        self.dbHeader.grid(row=0, column=0)
        tk.Label(self.dbHeader, image=self.img2).grid(row=0, column=0, pady=20)

        # Button Grid
        self.style.configure("TButton", padding=20)

        self.bidBtn = ttk.Button(self.dbHeader, text='Select Bid',
                    command=self.setupFlight, state="enabled")
        self.bidBtn.grid(row=2, column=0, sticky='wens')

        self.prefileBtn = ttk.Button(self.dbHeader, text='Pre-File',
                       command=self.preFile, state="disabled")
        self.prefileBtn.grid(row=3, column=0, sticky='wens')

        self.startBtn = ttk.Button(self.dbHeader, text='Start Flight',
                    command=self.startFlight, state="disabled")
        self.startBtn.grid(row=4, column=0, sticky='wens')

        self.updateBtn = ttk.Button(self.dbHeader, text='Update Enroute Time',
                    command=self.updateEnrouteTime, state="disabled")
        self.updateBtn.grid(row=5, column=0, sticky='wens')

        self.finishBtn = ttk.Button(self.dbHeader, text='Finish Flight',
                    command=self.finishFlight, state="disabled")
        self.finishBtn.grid(row=6, column=0, sticky='wens')

        self.fileBtn = ttk.Button(self.dbHeader, text='File PIREP',
                    command=self.filePirep, state="disabled")
        self.fileBtn.grid(row=7, column=0, sticky='wens')

        self.log = tk.Listbox(self.root, height=6, width=107)
        self.log.grid(row=0, column=1, sticky="s", padx=(0, 5))

        self.Log('View xACARS output here')

        self.dbBody.grid(row=self.dashboardViewRow, column=self.dashboardViewCol, sticky=self.dashboardViewSticky, pady=(5, 0))
        tk.Label(self.dbBody, text="Welcome to xACARS - Estafeta Edition", font=self.h1, fg="#cc2229").grid(row=0, column=0)
        tk.Label(self.dbBody, text="The official ACARS of Estafeta Virtual", font=self.h2).grid(row=1, column=0)
        tk.Label(self.dbBody, text="ESF Edition by Henry Shires", font=self.h3).grid(row=2, column=0, sticky="w", pady=(5, 0))

        link1 = tk.Label(self.dbBody, text="https://estafetava.com", font=self.h3, fg="#cc2229")
        link1.grid(row=2, column=0, pady=(10, 0), sticky="e")
        link1.bind("<Button-1>", lambda e: webbrowser.open_new("https://estafetava.com"))

        ttk.Separator(self.dbBody, orient="horizontal").grid(row=3, column=0, sticky="ew", pady=(10, 0))
        tk.Label(self.dbBody, text="Get Started - Track a flight:", font=self.h4, fg="#cc2229").grid(row=4, column=0, sticky="w", pady=(5, 0))
        tk.Label(self.dbBody, text="1. Click \"Select Bid\" and view the list of bids", font=self.h4).grid(row=5, column=0, sticky="w", pady=(10, 0))
        tk.Label(self.dbBody, text="    * Make sure to select a bid on your airline's website", font=self.h4).grid(row=6, column=0, sticky="w")
        tk.Label(self.dbBody, text="2. Pre-file your flight", font=self.h4).grid(row=7, column=0, sticky="w")
        tk.Label(self.dbBody, text="    * Input your aircraft, cruising altitude, estimated enroute time, distance, and route", font=self.h4).grid(row=8, column=0, sticky="w")
        tk.Label(self.dbBody, text="3. Enter your sim, enabled FSUIPC, and click \"Start\". Update your enroute time as needed", font=self.h4).grid(row=9, column=0, sticky="w")
        tk.Label(self.dbBody, text="4. After completion of your flight in sim, click \"Finish\"", font=self.h4).grid(row=10, column=0, sticky="w")
        tk.Label(self.dbBody, text="5. File your flight and upload it to your airline!", font=self.h4).grid(row=11, column=0, sticky="w")
        tk.Label(self.dbBody, text="    * Input your final enroute time, route, and fuel used, as well as any comments.", font=self.h4).grid(row=12, column=0, sticky="w")

        if config.checkUpdate == True:
            self.doCheckForUpdates()

    def about(self):
        about = tk.Toplevel()
        about.title('xACARS - About')
        about.iconbitmap('images/Favicon.ico')

        self.aboutFrame = tk.Frame(about)
        self.aboutFrame.grid(row=0, column=0)

        self.header = tk.Label(self.aboutFrame, text="xACARS " + config.version,
                               font="Arial")
        self.header.grid(row=0, column=0)
        self.bio = tk.Label(
            self.aboutFrame, text="xACARS was developed by Speed_Limit75 - This version includes additional developments by Henry Shires.")
        self.bio.grid(
            row=1, column=0)
        self.space1 = ttk.Separator(self.aboutFrame, orient=tk.HORIZONTAL)
        self.space1.grid(
            row=2, column=0, sticky="we")

        self.text = tk.Label(
            self.aboutFrame, text="This program is currently in alpha testing, so expect major bugs and issues.")
        self.text.grid(
            row=3, column=0, sticky="w")

        self.text2 = tk.Label(
            self.aboutFrame, text="xACARS is powered by FSUIPC/XPUIPC to gather data from the simulator.")
        self.text2.grid(row=4, column=0, sticky="w")

        about.mainloop()

    def settings(self):
        listOfBool = ["", "True", "False"]
        inputOptions = ["", "FSUIPC (FSX & P3D)", "FlyWithLua (X-Plane)"]

        self.settingsWin = tk.Toplevel()
        self.settingsWin.iconbitmap('images/Favicon.ico')

        config.reloadSettings()

        self.isfsuipc = tk.StringVar(self.settingsWin)
        if config.useFSUIPC == True:
            self.isfsuipc.set(str("FSUIPC (FSX & P3D)"))
        else:
            self.isfsuipc.set(str("FlyWithLua (X-Plane)"))

        self.darkMode = tk.StringVar(self.settingsWin)
        self.darkMode.set(str(config.darkMode))

        self.checkUpdate = tk.StringVar(self.settingsWin)
        self.checkUpdate.set(str(config.checkUpdate))

        self.getPreRel = tk.StringVar(self.settingsWin)
        self.getPreRel.set(str(config.getPreRel))

        # Draw window
        self.settingsWin.title('xACARS Settings')
        tk.Label(self.settingsWin, text='Settings', font="Arial").grid(row=0, columnspan=1, sticky="w") 
        tk.Label(self.settingsWin, text='Changes require restarting the program.').grid(row=1, columnspan=1, sticky="w")
        ttk.Separator(self.settingsWin, orient=tk.HORIZONTAL).grid(row=2, columnspan=4, sticky="we")

        tk.Label(self.settingsWin, text='Input Method: ').grid(row=3, column=0, sticky="e")
        ttk.OptionMenu(self.settingsWin, self.isfsuipc, *inputOptions).grid(row=3, column=1, sticky="we")
        tk.Label(self.settingsWin, text='Turn this off if you want an external program to write to the files in the input folder.').grid(row=3, column=3, sticky="w")

        tk.Label(self.settingsWin, text='Dark Mode: ').grid(row=4, column=0, sticky="e")
        ttk.OptionMenu(self.settingsWin, self.darkMode, *listOfBool).grid(row=4, column=1, sticky="we")
        tk.Label(self.settingsWin, text='This will enable dark mode, in the future.').grid(row=4, column=3, sticky="w")

        tk.Label(self.settingsWin, text='Check for updates on startup: ').grid(row=5, column=0, sticky="e")
        ttk.OptionMenu(self.settingsWin, self.checkUpdate, *listOfBool).grid(row=5, column=1, sticky="we")
        tk.Label(self.settingsWin, text='Turn this off if you want to manually check for updates.').grid(row=5, column=3, sticky="w")

        tk.Label(self.settingsWin, text='Download pre-release versions: ').grid(row=6, column=0, sticky="e")
        ttk.OptionMenu(self.settingsWin, self.getPreRel, *listOfBool).grid(row=6, column=1, sticky="we")
        tk.Label(self.settingsWin, text='This may be unstable.').grid(row=6, column=3, sticky="w")

        ttk.Button(self.settingsWin, text='Restore to defaults', command=self.restoreToDefaults).grid(row=8, columnspan=4, sticky="we")
        ttk.Button(self.settingsWin, text='Save & Exit', command=self.saveSettings).grid(row=9, columnspan=4, sticky="we")
        self.settingsWin.mainloop()

    def setupFlight(self):
        self.dbBody.grid_forget()

        self.bidsFrame.grid_rowconfigure(0, weight=0)
        self.bidsFrame.grid_rowconfigure(2, weight=1)
        self.bidsFrame.grid_columnconfigure(0, weight=1)
        self.bidsFrame.grid_columnconfigure(2, weight=1)

        self.bidsFrame.grid(row=self.dashboardViewRow, column=self.dashboardViewCol, sticky=self.dashboardViewSticky, pady=self.dashboardViewPadY)
        self.selBid = tk.StringVar(self.root)

        tk.Label(self.bidsFrame, text='Bids', font="Arial").grid(row=0, column=0)

        # Setup Fields
        self.bidList = []

        # Get bids from phpVMS
        data = web.get(config.website + '/api/user/bids')

        # Check for and list bids
        if data == '{"data":[]}':
            tk.Label(self.bidsFrame, text="No bids found! Please place a bid on your airline's website and restart xACARS.").grid(row=1, column=0)
            self.data = "No bids"
        else:
            self.bids = json.loads(data)["data"]
            for key in self.bids:
                self.bidList.append(str(key["flight"]["ident"]) + " (" + str(key["flight"]["dpt_airport_id"]) + " - " + str(key["flight"]["arr_airport_id"]) + ")")

            self.bidList.reverse()
        
            ttk.OptionMenu(self.bidsFrame, self.selBid, "Select a Bid", *self.bidList).grid(row=2, column=0, sticky="we")
            ttk.Button(self.bidsFrame, text='Select', command=self.selectBid).grid(row=2, column=1, sticky="we")

    def selectBid(self):
        selBid = self.selBid.get()

        if not(selBid.__eq__("Select a Bid")):
            selBidText = selBid.split(" ")
            selBidText = selBidText[0]

            a = 0
            for key in self.bids:
                if key["flight"]["ident"] == selBidText:
                    break
                else:
                    a = a + 1
        
            self.data = self.bids[a]
            self.Log('#######################################################')
            self.Log("Selected flight: " + str(self.data["flight"]["ident"]))
            self.Log("Departs from " + str(self.data["flight"]["dpt_airport_id"]) +
            " and arrives at " + str(self.data["flight"]["arr_airport_id"]))

            self.bidBtn.config(state="disabled")
            self.prefileBtn.config(state="normal")
            self.bidsFrame.grid_forget()
        else:
            tk.messagebox.showerror('xACARS Error', 'Please select a bid!')

    def preFile(self):
        self.cruiseAlt = tk.StringVar(self.root)
        self.plannedFlightTime = tk.StringVar(self.root)
        self.plannedDistance = tk.StringVar(self.root)
        self.route = tk.StringVar(self.root)
        self.selacf = tk.StringVar(self.root)

        # Get subfleet from flight information
        flightId = self.data["flight_id"]
        flightData = json.loads(
            web.get(config.website + '/api/flights/' + flightId))["data"]

        self.acf = []
        self.acf2 = []
        self.ids = []
        self.acf.append("Please select an aircraft")

        for key in flightData["subfleets"]:
            for key2 in key["aircraft"]:
                self.acf2.append(str(key2["registration"]) +
                            " [" + str(key2["icao"]) + "]")
                self.ids.append(key2["id"])

        for key in self.acf2:
            self.acf.append(key)
        self.selacf.set(self.acf[0])

        self.prefileFrame.grid(row=self.dashboardViewRow, column=self.dashboardViewCol, sticky=self.dashboardViewSticky, pady=self.dashboardViewPadY)

        tk.Label(self.prefileFrame, text="Prefile", font="Arial").grid(
            row=0, column=0, columnspan=3, sticky="w")
        ttk.Separator(self.prefileFrame, orient=tk.HORIZONTAL).grid(
            row=1, columnspan=4, sticky="we")
        tk.Label(self.prefileFrame, text="Aircraft: ").grid(row=2, column=0)
        ttk.OptionMenu(self.prefileFrame, self.selacf, *
                       self.acf).grid(row=2, column=1, sticky="we")
        tk.Label(self.prefileFrame, text="Cruise FL: ").grid(row=3, column=0)
        ttk.Entry(self.prefileFrame, textvariable=self.cruiseAlt).grid(
            row=3, column=1, sticky="we")
        tk.Label(self.prefileFrame, text="Planned Time: ").grid(row=4, column=0)
        ttk.Entry(self.prefileFrame, textvariable=self.plannedFlightTime).grid(
            row=4, column=1, sticky="we")
        tk.Label(self.prefileFrame, text="minutes").grid(
            row=4, column=2, sticky="w")
        tk.Label(self.prefileFrame, text="Planned Distance: ").grid(
            row=5, column=0)
        ttk.Entry(self.prefileFrame, textvariable=self.plannedDistance).grid(
            row=5, column=1, sticky="we")
        tk.Label(self.prefileFrame, text="nm").grid(row=5, column=2, sticky="w")
        tk.Label(self.prefileFrame, text="Route:").grid(row=6, column=0)
        ttk.Entry(self.prefileFrame, textvariable=self.route).grid(
            row=6, column=1, sticky="we")
        ttk.Button(self.prefileFrame, text='Pre-file', command=self.doPrefile).grid(
            row=7, columnspan=4, sticky="we")

    def startFlight(self):
        self.flightTime = int(time.time())

        if (self.connectionTest()):
            posUpdateLoop.startLoop(self.pirepID)
            self.Log('#######################################################')
            self.Log("Now logging flight.")
            self.startBtn.config(state="disabled")
            self.finishBtn.config(state="normal")

    def updateEnrouteTime(self):
        uetWindow = tk.Toplevel()
        newEnrouteTime = tk.StringVar(uetWindow)
        uetWindow.iconbitmap('images/Favicon.ico')
        uetWindow.title('Edit Enroute Time')
        uetWindow.geometry("300x150")

        uetFrame = tk.Frame(uetWindow)
        uetFrame.grid()

        uetWindow.grid_rowconfigure(0, weight=0)
        uetWindow.grid_rowconfigure(2, weight=1)
        uetWindow.grid_columnconfigure(0, weight=1)
        uetWindow.grid_columnconfigure(2, weight=1)

        uetFrame.grid_rowconfigure(0, weight=0)
        uetFrame.grid_rowconfigure(2, weight=1)
        uetFrame.grid_columnconfigure(0, weight=1)
        uetFrame.grid_columnconfigure(2, weight=1)

        tk.Label(uetFrame, text='Edit Enroute Time', font="Arial").grid(
            row=0, column=1)
        ttk.Entry(uetFrame, textvariable=newEnrouteTime).grid(
            row=1, column=1)
        tk.Label(uetFrame, text='minutes').grid(row=1, column=2, sticky="w")
        ttk.Button(uetFrame, text='Save', command=uetWindow.quit).grid(
            row=1, column=2, sticky="e")
        
        uetWindow.mainloop()

        newEnrouteTime = newEnrouteTime.get()
        updatedTime = {"planned_flight_time": int(newEnrouteTime)}
        updatedTime = web.post(config.website + '/api/pireps/' +
                        self.pirepID + '/update', updatedTime)

        self.Log("Enroute Time Updated!")

        uetWindow.destroy()

    def finishFlight(self):
        posUpdateLoop.stopLoop()

        self.fileBtn.config(state="normal")
        self.updateBtn.config(state="disabled")
        self.finishBtn.config(state="disabled")
        self.Log("Flight stopped")
        self.Log('#######################################################')

    def filePirep(self):
        self.addComment = tk.IntVar(self.root)
        self.comment = tk.StringVar(self.root)
        self.fuel = tk.StringVar(self.root)
        self.distance = tk.StringVar(self.root)

        self.fileFrame.grid(row=self.dashboardViewRow, column=self.dashboardViewCol, sticky=self.dashboardViewSticky, pady=self.dashboardViewPadY)

        tk.Label(self.fileFrame, text='File Pirep', font="Arial").grid(sticky="w")
        ttk.Separator(self.fileFrame, orient=tk.HORIZONTAL).grid(
            row=1, column=1, sticky="we")

        tk.Label(self.fileFrame, text='Fuel Used').grid(row=2, column=0, sticky="w")
        ttk.Entry(self.fileFrame, textvariable=self.fuel).grid(
            row=2, column=1, sticky="we")

        tk.Label(self.fileFrame, text='Distance').grid(row=3, column=0, sticky="w")
        ttk.Entry(self.fileFrame, textvariable=self.distance).grid(
            row=3, column=1, sticky="we")

        ttk.Checkbutton(self.fileFrame, text="Comment?",
                        variable=self.addComment).grid(row=5, sticky="w")
        ttk.Entry(self.fileFrame, textvariable=self.comment, width=50).grid(
            row=5, column=1, sticky="nwwe")

        ttk.Button(self.fileFrame, text='Submit PIREP', command=self.doFile).grid(
            row=6, columnspan=2, sticky="we")

    """
    Run Login function
    """
    def doLogin(self):
        if (Login.login(self.airline, self.username, self.key, self.rememberMe)):
            self.website.set(config.website)
            self.dashboard()

    def doRegister(self):
        Login.register(self.airline, self.website, self.username, self.key)
        self.login()

    def doEdit(self):
        Login.edit(self.airline, self.website, self.username, self.key)
        self.accountsMenu.destroy()

    def doDelete(self):
        proceed = tk.messagebox.askyesno('xACARS', 'Are you sure you want to delete ' + self.delAirline.get() + ' from xACARS?')
        if proceed:
            if not(self.isInFlight()):
                Login.delete(self.delAirline)
                
                if (self.delAirline.get() == self.airline.get()):
                    self.doSignOut()
                self.accountsMenu.destroy()
            else:
                tk.messagebox.showerror('xACARS Error', 'Unable to delete account. Complete your flight first!')

    def doSignOut(self):
        self.dbHeader.grid_forget()
        self.dbBody.grid_forget()
        self.log.grid_forget()
        self.bidsFrame.grid_forget()
        self.prefileFrame.grid_forget()
        self.fileFrame.grid_forget()

        config.airline = ""
        config.website = ""
        config.username = ""
        config.APIKey = ""

        self.airline.set("")
        self.website.set("")
        self.username.set("")
        self.key.set("")
        self.rememberMe.set(False)

        # Hide menu
        emptyMenu = tk.Menu(self.root)
        self.root.config(menu=emptyMenu)

        config.forgetUsers()

        self.login()

    """
    Check if the current version of xACARS is the latest, published version
    """
    def doCheckForUpdates(self):
        if (not(web.isLatestVersion())):
            tk.messagebox.showinfo("xACARS Update", "Update available! You can download the latest version of xACARS from https://github.com/slimit75/xACARS/releases")
        else:
            tk.messagebox.showinfo("xACARS Update", "No updates available")

    def doPrefile(self):
        selacf = self.selacf.get()

        a = 0
        for key in self.acf:
            if key == selacf:
                break
            else:
                a = a + 1

        self.data = {
            "airline_id": str(self.data["flight"]["airline_id"]),
            "aircraft_id": str(self.ids[a-1]),
            "flight_number": str(self.data["flight"]["flight_number"]),
            "route_code": "",
            "route_leg": "",
            "dpt_airport_id": str(self.data["flight"]["dpt_airport_id"]),
            "arr_airport_id": str(self.data["flight"]["arr_airport_id"]),
            "level": int(self.cruiseAlt.get()),
            "planned_distance": int(self.plannedDistance.get()),
            "planned_flight_time": int(self.plannedFlightTime.get()),
            "route": str(self.route.get()),
            "source_name": "xACARS",
            "flight_type": str(self.data["flight"]["flight_type"])
        }

        self.data = json.dumps(self.data)
        self.data = web.post(config.website + '/api/pireps/prefile', self.data)
        self.data = json.loads(self.data.text)

        try:
            self.data = self.data["data"]
            self.pirepID = self.data["id"]

            self.prefileBtn.config(state="disabled")
            self.startBtn.config(state="normal")
            self.updateBtn.config(state="normal")

            self.Log('#######################################################')
            self.Log("Pre-file successful!")

            self.prefileFrame.grid_forget()
        except:
            self.data = self.data["error"]
            self.Log("Error: " + str(self.data["message"]))

    def doFile(self):
        self.flightTime = int(time.time()) - self.flightTime

        self.data = {
            "flight_time": self.flightTime,
            "fuel_used": self.fuel.get(), 
            "distance": self.distance.get()
            }
        self.data = json.dumps(self.data)

        response = web.post(config.website + '/api/pireps/' +
                        self.pirepID + '/file', self.data)

        addComment = self.addComment.get()

        commentsResponse = ""

        if addComment == 1:
            self.data = {"comment": str(self.comment.get()), }
            self.data = json.dumps(self.data)
            commentsResponse = web.post(config.website + '/api/pireps/' +
                            self.pirepID + '/comments', self.data)

        if response.status_code == 200:
            self.finishBtn.config(state="disabled")
            self.bidBtn.config(state="enabled")
            self.Log("PIREP Submitted! Hope you had a great flight!")
            self.fileBtn.config(state="disabled")
            self.fileFrame.grid_forget()
            self.dbBody.grid(row=self.dashboardViewRow, column=self.dashboardViewCol, sticky=self.dashboardViewSticky, pady=(5, 0))
            
        else:
            self.Log("Error when attempting to file PIREP")
            self.Log(response.json())
            self.Log(commentsResponse.json())

    def connectionTest(self):
        track.endTrack()
        isSuccess = track.beginTrack()
        if isSuccess:
            tk.messagebox.showinfo("xACARS", "Connected to Sim!")
            track.posUpdate()
            return True
        else:
            tk.messagebox.showerror('xACARS Error','Unable to connect to sim. ' + isSuccess)
            return False
        track.endTrack()

    def isInFlight(self):
        try:
            return self.prefileFrame.winfo_ismapped() or self.fileFrame.winfo_ismapped() or self.startBtn.cget('state') == "active" or self.finishBtn.cget('state') == "active"
        except Exception as e:
            tk.messagebox.showerror('xACARS Error', e)
            return False

    def saveSettings(self):
        file = open("settings.ini", 'w')
        file.write("[DEFAULT]\n")

        if self.isfsuipc.get() == "FSUIPC (FSX & P3D)":
            file.write("fsuipc = True\n")
        else:
            file.write("fsuipc = False\n")

        file.write("darkMode = " + self.darkMode.get() + "\n")
        file.write("checkForUpdatesOnStart = " + self.checkUpdate.get() + "\n")
        file.write("getPreReleaseVersions = " + self.getPreRel.get() + "\n")
        file.close()

        self.settingsWin.destroy()

    def restoreToDefaults(self):
        self.restoreToDefault = False
        self.restoreToDefault = tk.messagebox.askyesno("xACARS","Are you sure you want to restore to defaults?")
        self.settingsWin.lift()

        if self.restoreToDefault == True:
            os.remove("settings.ini")
            config.reloadIni()
            tk.messagebox.showinfo("xACARS","Restored defaults.")

            self.settingsWin.destroy()

    def Log(self, text):
        self.log.insert(tk.END, text)

# Main loop
window = tk.Tk()
app = App(window)

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.mainloop()
