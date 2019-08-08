# ----------------------------------------- #
# settings.pyw                              #
# Speed_Limit75                             #
#                                           #
# This file changes the settings. There are #
# no settings right now, but that wont be   # 
# true in the near future.                  #
# ----------------------------------------- #

# Import libarys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import config
import os

# Set Variables
listOfBool = ["", "True", "False"]
restoreToDefault = False

# Define functions
def restoreToDefaults():
    global restoreToDefault
    global window
    restoreToDefault = messagebox.askyesno("xACARS","Are you sure you want to restore to defaults?")
    if restoreToDefault == True:
        os.remove("settings.ini")
        messagebox.showinfo("xACARS","Restored defaults. Please restart xACARS.")
        print('test')
        window.quit()
    else:
        messagebox.showinfo("xACARS","Canceled restore of defaults.")
        restoreToDefault = False

def drawWindow(x):
    global restoreToDefault
    global window
    global listOfBool
    global restoreToDefault
    # Set Variables through tkinter
    window = tk.Tk()
    window.iconbitmap('Favicon.ico')

    fsuipc = tk.StringVar(window)
    fsuipc.set(str(config.useFSUIPC))

    darkMode = tk.StringVar(window)
    darkMode.set(str(config.darkMode))

    checkUpdate = tk.StringVar(window)
    checkUpdate.set(str(config.checkUpdate))

    getPreRel = tk.StringVar(window)
    getPreRel.set(str(config.getPreRel))

    startupMessage = tk.StringVar(window)
    startupMessage.set(str(config.loginMessage))

    # Draw window
    window.title('xACARS Settings')
    tk.Label(window, text='Settings', font="Arial").grid(row=0, columnspan=1, sticky="w") 
    tk.Label(window, text='Changes require restarting the program.').grid(row=1, columnspan=1, sticky="w")
    ttk.Separator(window, orient=tk.HORIZONTAL).grid(row=2, columnspan=4, sticky="we")

    tk.Label(window, text='Use FSUIPC/XPUIPC: ').grid(row=3, column=0, sticky="e")
    ttk.OptionMenu(window, fsuipc, *listOfBool).grid(row=3, column=1, sticky="we")
    tk.Label(window, text='Turn this off if you want an external program to write to the files in the input folder.').grid(row=3, column=3, sticky="w")

    tk.Label(window, text='Dark Mode: ').grid(row=4, column=0, sticky="e")
    ttk.OptionMenu(window, darkMode, *listOfBool).grid(row=4, column=1, sticky="we")
    tk.Label(window, text='This will enable dark mode, in the future.').grid(row=4, column=3, sticky="w")

    tk.Label(window, text='Check for updates on startup: ').grid(row=5, column=0, sticky="e")
    ttk.OptionMenu(window, checkUpdate, *listOfBool).grid(row=5, column=1, sticky="we")
    tk.Label(window, text='Turn this off if you want to manually check for updates.').grid(row=5, column=3, sticky="w")

    tk.Label(window, text='Download pre-release versions: ').grid(row=6, column=0, sticky="e")
    ttk.OptionMenu(window, getPreRel, *listOfBool).grid(row=6, column=1, sticky="we")
    tk.Label(window, text='This may be unstable.').grid(row=6, column=3, sticky="w")

    tk.Label(window, text='Startup Login Message: ').grid(row=7, column=0, sticky="e")
    ttk.OptionMenu(window, startupMessage, *listOfBool).grid(row=7, column=1, sticky="we")
    tk.Label(window, text='Disables the startup message that tells you how to login.').grid(row=7, column=3, sticky="w")

    ttk.Button(window, text='Restore to defaults', command=restoreToDefaults).grid(row=8, columnspan=4, sticky="we")
    ttk.Button(window, text='Save & Exit', command=window.quit).grid(row=9, columnspan=4, sticky="we")
    window.mainloop()

    # Post exit script - saves file
    window.destroy()
    
    if restoreToDefault == False:
        file = open("settings.ini", 'w')
        file.write("[DEFAULT]\n")
        file.write("fsuipc = " + fsuipc.get() + "\n")
        file.write("darkMode = " + darkMode.get() + "\n")
        file.write("checkForUpdatesOnStart = " + checkUpdate.get() + "\n")
        file.write("getPreReleaseVersions = " + getPreRel.get() + "\n")
        file.write("loginMessageEnabled = " + startupMessage.get())
        file.close()

    return