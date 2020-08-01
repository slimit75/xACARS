# ----------------------------------------- #
# login.pyw                                 #
# Speed_Limit75                             #
#                                           #
# As the name suggests, this file manages   #
# logging into the virtual airline.         #
# ----------------------------------------- #

# Import libarys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import config
import web
import json
import listAirlines

List = config.list
websites = config.websites
savedAPIKeys = config.savedAPIKeys
usernames = config.usernames

def login(airline, username, key):
    try:
        global airline
        global key
        global username
        global List
        global websites
        global savedAPIKeys

        airline.set("None")

    except Exception:
        listAirlines.reload()
    return


def terminate():
    global airline
    global key
    global username

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
            tk.messagebox.showerror(
                "xACARS Critical Error", "Error: Invalid API Key or API Key does not match username.")
            return
    elif str(data) == "<Response [401]>":
        tk.messagebox.showerror(
            "xACARS Critical Error", "Invalid API Key or API Key does not match username.")
    else:
        data1 = str(data)
        if data1.startswith("<Response [") == True:
            data = str(data)
            data.split("[")
            data1 = data[11]
            data2 = data[12]
            data3 = data[13]
            data = data1 + data2 + data3
            tk.messagebox.showerror(
                "xACARS Critical Error", "HTML Error: " + data)
        else:
            tk.messagebox.showerror(
                "xACARS Critical Error", "Error when logging in: " + str(data))
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
