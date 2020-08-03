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

List = config.list
websites = config.websites
savedAPIKeys = config.savedAPIKeys
usernames = config.usernames

def login(airline, username, key):
    try:
        airline.set("None")
        index = List.index(airline)

        config.changeVar("APIKey", key)
        config.changeVar("airline", airline)
        config.changeVar("website", websites[index])

        data = web.getRaw(config.website + '/api/user')

        if str(data) == "<Response [200]>":
            data = json.loads(data.text)
            data = data["data"]["name"]
            if username == data:
                # window.quit()
                print("Logged in")
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
    except Exception:
        listAirlines.reload()
    return
