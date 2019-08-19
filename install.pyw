# ----------------------------------------- #
# install.pyw                               #
# Speed_Limit75                             #
#                                           #
# This file installs xACARS. Thats it.      #
# ----------------------------------------- #

# Import libarys
import tkinter as tk # Runs displays
from tkinter import ttk # Adds seperator in some windows
from tkinter import messagebox # Drives OS error, warning, or info message
from tkinter import filedialog # Drives file dialog
import tempfile # Gets location of temp folder
import requests # Downloads stuff
from zipfile import ZipFile # Unzips files
import os # Multiple Uses
import time

# Set variables
window = tk.Tk()
xpdir = ""
xpInstalled = tk.IntVar(window)
installFWL = tk.IntVar(window)
installFSUIPC4 = tk.IntVar(window)
installFSUIPC5 = tk.IntVar(window)

xpInstalled.set(1)
installFWL.set(1)
installFSUIPC4.set(1)

z = 0
y = 0

# Define download functions 
def download_file_from_google_drive(id, destination):   
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

# Define functions
def setStatus(x):
    global y
    y = x

def updateStatus():
    global a
    global y
    global z
    z = z + 1
    a['value'] = 100 * (z / y)

def Install():
    if xpInstalled.get() == 1:
        if xpdir == "":
            Log("Select your X-Plane directory!")
        else:
            install()
    else:
        install()
def install():
    global xpInstalled
    global installFWL
    global installFSUIPC4
    global installFSUIPC5
    global xpdir
    a = 3
    
    doInstallFWL = False
    doInstallFSUIPC4 = False
    doInstallFSUIPC5 = False
    doInstallScript = False

    Log('[ Preparing to install... ] #############################')
    Log("Checking options..")
    if xpInstalled.get() == 1:
        a = a + 1
        doInstallScript = True
        if installFWL.get() == 1:
            a = a + 2
            Log("   Need to install FlyWithLua NG")
            doInstallFWL = True

    if installFSUIPC4.get() == 1:
        a = a + 3
        Log("   Need to install FSUIPC v4")
        doInstallFSUIPC4 = True

    if installFSUIPC5.get() == 1:
        a = a + 3
        Log("   Need to install FSUIPC v5")
        doInstallFSUIPC5 = True
    Log("Done, finishing up.")
    setStatus(a)
    if doInstallFWL == True:
        Log('[ Installing FlyWithLua... ] ###########################')
        Log("Downloading FlyWithLua...")
        download_file_from_google_drive('17bfX7wDSr8E6Q1uhXfKiAjXpGjmif1ui', str(os.path.join(os.getcwd(), 'temp.zip')))
        
        updateStatus()
        Log("Extracting FlyWithLua...")
        with ZipFile(os.path.join(os.getcwd(), 'temp.zip'), 'r') as zipObj:
            zipObj.extractall(os.path.join(xpdir, str(os.path.join('Resources', 'plugins'))))
        updateStatus()

    if doInstallFSUIPC4 == True:
        Log('[ Installing FSUIPC v4... ] ############################')
        Log("Downloading FSUIPC v4")
        # Download zip
        updateStatus()
        Log("Extracting FSUIPC v4")
        # Extract zip
        updateStatus()
        Log("Running Installer")
        # Run Installer
        updateStatus()
    
    if doInstallFSUIPC5 == True:
        Log('[ Installing FSUIPC v5... ] ############################')
        Log("Downloading FSUIPC v5")
        # Download zip
        updateStatus()
        Log("Extracting FSUIPC v5")
        # Extract zip
        updateStatus()
        Log("Running Installer")
        # Run Installer
        updateStatus()
    
    Log('[ Installing xACARS... ] ###############################')
    Log("Downloading files..")
    # Download zip
    updateStatus()
    Log("Extracting files..")
    # Extract files
    updateStatus()

    if doInstallScript == True:
        Log("Installing FlyWithLua Script..")
        # install FlyWithLua Script
        updateStatus()

    Log("Cleaning up..")
    # Clean up files
    updateStatus()
    Log("Creating desktop icon..")
    # Create desktop icon
    updateStatus()

def pickDir():
    global xpdir
    xpdir = filedialog.askdirectory()
    Log('#######################################################')
    Log("Selected X-Plane Directory as " + str(xpdir))
    print(xpdir)

def Log(text):
    global log
    log.insert(tk.END, text)

# Draw window
window.title('xACARS Installer')
tk.Label(window, text="Welcome to xACARS", font="Arial").grid(row=0, column=0)
tk.Label(window, text="The program is installed to %APPDATA%").grid(row=1, column=0)
ttk.Checkbutton(window, text="X-Plane is installed", variable=xpInstalled).grid(row=2, sticky="w")
ttk.Checkbutton(window, text="Install FlyWithLua NG (X-Plane)", variable=installFWL).grid(row=3, sticky="w")
ttk.Checkbutton(window, text="Install FSUIPC v4 (FSX/P3D)", variable=installFSUIPC4).grid(row=4, sticky="w")
ttk.Checkbutton(window, text="Install FSUIPC v5 (P3Dv4)", variable=installFSUIPC5).grid(row=5, sticky="w")
ttk.Button(window, text='Select X-Plane Directory (if installed)', command=pickDir).grid(row=6, column=0, sticky='wens')
ttk.Button(window, text='Begin Install', command=Install).grid(row=7, column=0, sticky='wens')
a = ttk.Progressbar(window, orient = tk.HORIZONTAL, length = 100, mode = 'determinate')
a.grid(row=8, columnspan=2, sticky='wens')
a['value'] = 100

log = tk.Listbox(window, width=55, height=15)
Log('Thank you for downloading xACARS.')
Log("When you are ready, fill out the fields and click 'Begin Install'")
log.grid(row=0, column=1, rowspan=8)


window.mainloop()