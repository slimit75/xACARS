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

# Import local files
import config
import login as Login
import web
import track
import posUpdateLoop
import listAirlines
import settings as settingsWindow

'''
Draw xACARS UI
'''

class App:

    def __init__(self, root):
        self.root = root
        self.root.iconbitmap('images/Favicon.ico')
        self.root.title('xACARS - ' + config.version)
        self.root.geometry("960x480")

        # Frames
        self.loginFrame = tk.Frame(self.root)
        self.registerFrame = tk.Frame(self.root)
        self.body = tk.Frame(self.root)
        self.dbHeader = tk.Frame(self.root)
        self.dbBody = tk.Frame(self.root)
        self.buttonGroup = tk.Frame(self.root)
        self.bidsFrame = tk.Frame(self.root)

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
        self.bidList = []
        self.selBid = ""
        self.data = None

        # Tkinter Styles
        self.h1 = tkFont.Font(family="Verdana", size=20)
        self.h2 = tkFont.Font(family="Verdana", size=18)
        self.h3 = tkFont.Font(family="Verdana", size=14)

        self.style = ttk.Style()
        self.style.configure("TButton", padding=5)

        # Images
        img = Image.open("images/estafeta_red.png")
        img = img.resize((int(img.size[0] * 0.75), int(img.size[1] * 0.75)))

        img2 = img.resize((int(img.size[0] * 0.5), int(img.size[1] * 0.5)))

        self.img = ImageTk.PhotoImage(img)
        self.img2 = ImageTk.PhotoImage(img2)

        # Widgets
        self.login()

    def menu(self):
        # Toolbar
        self.toolbar = tk.Menu(self.root)
        self.root.config(menu=self.toolbar)

        self.mainMenu = tk.Menu(self.toolbar, tearoff=False)
        self.toolbar.add_cascade(label='Main', menu=self.mainMenu)
        self.mainMenu.add_command(label='Preferences', command=self.settings)
        self.mainMenu.add_command(label='Check for updates',
                                  command=self.doCheckForUpdates)
        self.mainMenu.add_separator()
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

    def dashboard(self):
        self.body.grid_forget()
        self.loginFrame.grid_forget()

        self.menu()

        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(2, weight=0)
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(2, weight=0)
        
        self.dbHeader.grid(row=0, column=0)
        self.dbBody.grid(row=0, column=1)
        tk.Label(self.dbHeader, image=self.img2).grid(row=0, column=0, pady=5)

        # Button Grid
        self.style.configure("TButton", padding=20)

        self.bidBtn = ttk.Button(self.dbHeader, text='Select Bid',
                    command=self.setupFlight, state="enabled").grid(row=2, column=0, sticky='wens')
        self.prefileBtn = ttk.Button(self.dbHeader, text='Pre-File',
                       command=self.preFile, state="disabled").grid(row=3, column=0, sticky='wens')
        self.startBtn = ttk.Button(self.dbHeader, text='Start Flight',
                    command=self.startFlight, state="disabled").grid(row=4, column=0, sticky='wens')
        self.updateBtn = ttk.Button(self.dbHeader, text='Update Enroute Time',
                    command=self.updateEnrouteTime, state="disabled").grid(row=5, column=0, sticky='wens')
        self.finishBtn = ttk.Button(self.dbHeader, text='Finish Flight',
                    command=self.finishFlight, state="disabled").grid(row=6, column=0, sticky='wens')
        self.fileBtn = ttk.Button(self.dbHeader, text='File PIREP',
                    command=self.filePirep, state="disabled").grid(row=7, column=0, sticky='wens')

        self.dbBody.grid_rowconfigure(0, weight=0)
        self.dbBody.grid_rowconfigure(2, weight=1)
        self.dbBody.grid_columnconfigure(0, weight=1)
        self.dbBody.grid_columnconfigure(2, weight=1)

        # tk.Label(self.dbBody, text="Welcome to xACARS\nEstafeta Edition by Henry Shires", font=self.h1).grid(row=0, column=0)
        self.log = tk.Listbox(self.dbBody)
        self.log.grid(row=2, column=0, sticky="n")

        self.Log('View ACARS output here')
        self.log.grid(row=0, column=1)

        if config.checkUpdate == True:
            self.doCheckForUpdates()

    def about(self):
        self.dbBody.grid_forget()

        self.aboutFrame = tk.Frame(self.root)
        self.aboutFrame.grid(row=6, column=6)

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

    def setupFlight(self):
        self.data = self.getBids()

        self.Log('#######################################################')
        self.Log("Selected flight: " + str(self.data["flight"]["ident"]))
        self.Log("Departs from " + str(self.data["flight"]["dpt_airport_id"]) +
            " and arrives at " + str(self.data["flight"]["arr_airport_id"]))

        self.bidBtn.config(state="disabled")
        self.prefileBtn.config(state="normal")

    def preFile(self):
        global pirepID

        preFileWindow = tk.Tk()
        cruiseAlt = tk.StringVar(preFileWindow)
        plannedFlightTime = tk.StringVar(preFileWindow)
        plannedDistance = tk.StringVar(preFileWindow)
        route = tk.StringVar(preFileWindow)
        selacf = tk.StringVar(preFileWindow)

        # Get subfleet from flight information
        flightId = self.data["flight_id"]
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

            #b.config(state="disabled")
            #c.config(state="normal")
            #d.config(state="normal")
        except:
            data = data["error"]
            self.Log("Error: " + str(data["message"]))

    def startFlight(self):
        global pirepID
        global flightTime
        flightTime = int(time.time())
        posUpdateLoop.startLoop(pirepID)
        self.Log('#######################################################')
        self.Log("Now logging flight.")
        # c.config(state="disabled")
        # e.config(state="normal")

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
        self.Log('#######################################################')
        self.Log("Hope you had a great flight!")
        fpWindow.destroy()

    def finishFlight(self):
        posUpdateLoop.stopLoop()
        #f.config(state="normal")
        #d.config(state="disabled")
        #e.config(state="disabled")

    def getBids(self):
        self.bidsFrame.grid()
        selBid = tk.StringVar(self.root)

        tk.Label(self.dbBody, text='Bids', font="Arial").grid(row=0, columnspan=1, sticky="w") 
        ttk.Separator(self.dbBody, orient=tk.HORIZONTAL).grid(row=1, columnspan=4, sticky="we")

        # Get bids from phpVMS
        data = web.get(config.website + '/api/user/bids')

        # Check for and list bids
        if data == '{"data":[]}':
            tk.Label(self.dbBody, text="No bids found! Please place a bid on your airline's website and restart xACARS.").grid(row=1, column=0)
        else:
            bids = json.loads(data)["data"]
            self.bidList.append(str(bids[0]["flight"]["ident"]) + " (" + str(bids[0]["flight"]["dpt_airport_id"]) + " - " + str(bids[0]["flight"]["arr_airport_id"]) + ")")
            for key in bids:
                self.bidList.append(str(key["flight"]["ident"]) + " (" + str(key["flight"]["dpt_airport_id"]) + " - " + str(key["flight"]["arr_airport_id"]) + ")")

            self.bidList.reverse()
        
            selBid.set(self.bidList[0])
            ttk.OptionMenu(window, selBid, *self.bidList).grid(row=2, column=0, sticky="we")
            ttk.Button(window, text='Select', command=self.bidsFrame.grid_forget).grid(row=2, column=1, sticky="we")

        if data == '{"data":[]}':
            return "No bids"
        else:
            selBid = selBid.get()

            selBidText = selBid.split(" ")
            selBidText = selBidText[0]

            a = 0
            for key in bids:
                if key["flight"]["ident"] == selBidText:
                    break
                else:
                    a = a + 1
        
            return bids[a]

    """
    Run Login function
    """
    def doLogin(self):
        if (Login.login(self.airline, self.username, self.key)):
            self.dashboard()

    def doRegister(self):
        Login.register(self.airline, self.website, self.username, self.key)

    """
    Check if the current version of xACARS is the latest, published version
    """
    def doCheckForUpdates(self):
        if (not(web.isLatestVersion())):
            tk.messagebox.showinfo("xACARS Update", "Update available! You can download the latest version of xACARS from https://github.com/slimit75/xACARS/releases")
        else:
            tk.messagebox.showinfo("xACARS Update", "No updates available")

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

    def connectionTest(self):
        track.endTrack()
        isSuccess = track.beginTrack()
        if isSuccess == "Can Connect":
            tk.messagebox.showinfo("xACARS UIPC", "Connected to Sim!")
            track.posUpdate()
        else:
            tk.messagebox.showerror('Error','Unable to connect to sim. ' + isSuccess)
        track.endTrack()

    def editAirlines(self):
        listAirlines.reload()
        return

    def settings(self):
        settingsWindow.drawWindow(window)
        return

    def Log(self, text):
        self.log.insert(tk.END, text)


# Main loop
window = tk.Tk()
App(window)
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.mainloop()
