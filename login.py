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
import configparser
import web
import json

def login(airline, username, key):
    try:

        getAirline = airline.get()
        getKey = key.get()
        getUsername = username.get()
        index = config.List.index(getAirline)

        config.changeVar("APIKey", getKey)
        config.changeVar("airline", getAirline)
        config.changeVar("website", config.websites[index])

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

def register(airline, website, username, apiKey):
    getAirline = airline.get()
    getKey = apiKey.get()
    getUsername = username.get()
    getWebsite = website.get()

    index = 0
    while index < len(config.List):
        index += 1

    accounts = configparser.ConfigParser()
    accounts[str(index + 1)] = {'name': getAirline, 'url': getWebsite, 'apikey': getKey, 'username': getUsername}

    with open('airlines.ini', 'a') as configfile:
        configfile.write("\n\n")
        accounts.write(configfile)

def edit(airline, website, username, apiKey):
    getAirline = airline.get()
    getKey = apiKey.get()
    getUsername = username.get()
    getWebsite = website.get()
    index = config.List.index(airline)
    
    airlineFile = configparser.ConfigParser()

    if apiKey == "":
        if username == "":
            airlineFile[str(index + 1)] = {'name': getAirline, 'url': getWebsite}
        else:
            airlineFile[str(index + 1)] = {'name': getAirline, 'url': getWebsite, 'username': getUsername}
    else:
        if username == "":
            airlineFile[str(index + 1)] = {'name': getAirline, 'url': getWebsite, 'apikey': getKey}
        else:
            airlineFile[str(index + 1)] = {'name': getAirline, 'url': getWebsite, 'apikey': getKey, 'username': getUsername}

    file = open('airlines.ini', 'r')
    data = file.read()
    file.close()

    data1 = data.split("[" + str(index + 1) + "]")
    data2 = data1[1].split("[" + str(index + 2) + "]")

    with open('airlines.ini', 'w') as configfile:
        configfile.write(data1[0])
        airlineFile.write(configfile)

        if not index + 2 == len(config.List):
            configfile.write("[" + str(index + 2) + "]")
            configfile.write(data2[1])
        configfile.close()

def delete(airline):
    airline = airline.get()

    index = config.List.index(airline)
    
    airlineFile = configparser.ConfigParser()

    file = open('airlines.ini', 'r')
    data = file.read()
    file.close()

    print(str(index + 1))
    data1 = data.split("[" + str(index) + "]")
    print(data1[0])

    try:
        data2 = data1[1].split("[" + str(index + 1) + "]")
        print(data2[1])
    except Exception as e:
        tk.messagebox.showerror("xACARS Error", e)
        data2 = ["", ""]

    with open('airlines.ini', 'w') as configfile:
        configfile.write(data1[0])
        #config.write(configfile)

        if not data2[1] == "":
            configfile.write("[" + str(index) + "]")
            configfile.write(data2[1])
        configfile.close()
        airlineFile.write(configfile)
