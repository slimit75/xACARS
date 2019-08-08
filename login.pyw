# ----------------------------------------- #
# login.pyw                                 #
# Speed_Limit75                             #
#                                           #
# As the name suggests, this file manages   #
# logging into the virtual airline.         #
# ----------------------------------------- #

# Import libarys
import tkinter as tk
from tkinter import messagebox
import config
import web
import json
import listAirlines

# Define functions
List = config.list
websites = config.websites
savedAPIKeys = config.savedAPIKeys
usernames = config.usernames

# Define functions
def login():
    try:
        global airline
        global key
        global username
        global window
        global List
        global websites
        global savedAPIKeys
    
        List = config.list
        websites = config.websites
        savedAPIKeys = config.savedAPIKeys

        window = tk.Tk()
        window.iconbitmap('Favicon.ico')
        key = tk.StringVar(window)
        airline = tk.StringVar(window)
        username = tk.StringVar(window)
        airline.set("None")

        window.title('xACARS ' + config.version)
        tk.Label(window, text='Airline: ').grid(row=0, column=0)
        tk.OptionMenu(window, airline, *List).grid(row=0, column=1)
        tk.Label(window, text='Username: ').grid(row=1, column=0)
        tk.Entry(window, textvariable=username).grid(row=1, column=1)
        tk.Label(window, text='API Key: ').grid(row=2, column=0)
        tk.Entry(window, textvariable=key, text=key).grid(row=2, column=1)
        tk.Button(window, text="Autofill", command=autofill).grid(row=2, column=2)
        tk.Button(window, text="Autofill", command=autofillUsername).grid(row=1, column=2)
        tk.Button(window, text='Log In', command=terminate).grid(row=3, columnspan=3, sticky="we")
        window.mainloop()
        window.destroy()
    except Exception:
        listAirlines.reload()
    return

def terminate():
    global airline
    global key
    global username
    global window

    airline2 = airline.get()
    key2 = key.get()
    username2 = username.get()
    a = List.index(airline2)

    config.changeVar("APIKey", key2)
    config.changeVar("airline", airline2)
    config.changeVar("website", websites[a])

    data = web.getRaw(config.website + '/api/user')

    if str(data) == "<Response [200]>":
        data = json.loads(data.text)
        data = data["data"]["name"]
        if username2 == data:
            window.quit()
        else:
            tk.messagebox.showerror("xACARS Critical Error", "Error: Invalid API Key, or API Key does not match username.")
            return
    elif str(data) == "<Response [401]>":
        tk.messagebox.showerror("xACARS Critical Error", "Error: Invalid API Key, or API Key does not match username.")
    else:
        data1 = str(data)
        if data1.startswith("<Response [") == True:
            data = str(data)
            data.split("[")
            data1 = data[11]
            data2 = data[12]
            data3 = data[13]
            data = data1 + data2 + data3
            tk.messagebox.showerror("xACARS Critical Error", "HTML Error: " + data)
        else:
            tk.messagebox.showerror("xACARS Critical Error", "Error when logging in: " + str(data))
        return

def autofill():
    global airline
    global key
    global savedAPIKeys
    a = List.index(airline.get())
    key.set(savedAPIKeys[a])
    return

def autofillUsername():
    global airline
    global usernames
    global username
    a = List.index(airline.get())
    username.set(usernames[a])
    return