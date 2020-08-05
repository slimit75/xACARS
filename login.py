# ----------------------------------------- #
# login.pyw                                 #
# Speed_Limit75                             #
# Additional contributions by Henry Shires  #
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

List = config.List
websites = config.websites
savedAPIKeys = config.savedAPIKeys
usernames = config.usernames

def login(airline, username, key):
    try:
        getAirline = airline.get()
        getKey = key.get()
        getUsername = username.get()
        index = List.index(getAirline)

        config.changeVar("APIKey", getKey)
        config.changeVar("airline", getAirline)
        config.changeVar("website", websites[index])

        data = web.getRaw(config.website + '/api/user')

        if str(data) == "<Response [200]>":
            data = json.loads(data.text)
            data = data["data"]["name"]
            if getUsername == data:
                return True
            else:
                tk.messagebox.showerror(
                    "xACARS Error", "Invalid API Key or API Key does not match username.")
        elif str(data) == "<Response [401]>":
            tk.messagebox.showerror(
                "xACARS Error", "Invalid API Key or API Key does not match username.")
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
                    "xACARS Error", "HTML Error: " + data)
            else:
                tk.messagebox.showerror(
                    "xACARS Error", "Error when logging in: " + str(data))
        return False
    except Exception as e:
        tk.messagebox.showerror("xACARS Error", e)
        return False

def register(airline, username, website, key):
    return
