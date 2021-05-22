# ----------------------------------------- #
# config.py                                 #
# Speed_Limit75                             #
#                                           #
# This file read all ini files and sets the #
# variables to reflect their settings. It   #
# also make sure all .ini files that are    #
# needed exist, somthing that used to be    #
# handled by its own file.                  #
# ----------------------------------------- #

# Import required libarys.
import configparser
import os
import tkinter as tk
from tkinter import messagebox

# Version
version = "v1.0.0-beta1"

# User Fields
airline = ""
website = ""
APIKey = ""
username = ""

# Airlines.ini fields
List = []
websites = []
savedAPIKeys = []
usernames = []

# Settings fields
checkUpdate = False
getPreRel = False

# Changes a variable
def changeVar(x, y):
    if x == "website":
        global website
        website = y
    elif x == "airline":
        global airline
        airline = y
    elif x == "APIKey":
        global APIKey
        y.replace(" ", "")
        y = y.strip()
        APIKey = y
    elif x == "rememberMe":
        global rememberMe
        rememberMe = y

# Converts a string to a boolean. Used by no external files
def stringToBool(x):
    if x == "true":
        return True
    elif x == "True":
        return True
    elif x == "false":
        return False
    elif x == "False":
        return False
    else:
        raise TypeError("Expected True, true, False, or false: not " + x)

# Reloads the list of airlines.
def reloadAirlines():
    global List
    global websites
    global savedAPIKeys
    global usernames

    config = configparser.ConfigParser()
    config.read("airlines.ini")
    configSections = config.sections()

    List = []
    websites = []
    savedAPIKeys = []
    usernames = []

    try:
        for key in configSections:
            List.append(config[key]['name'])
            websites.append(config[key]['URL'])
            savedAPIKeys.append(config[key]['apikey'])
            usernames.append(config[key]['username'])
    except Exception as e:
        tk.messagebox.showerror("xACARS Error", e)

def reloadSettings():
    global checkUpdate
    global getPreRel 

    # Read the config file and set variables
    config = configparser.ConfigParser() 
    config.read("settings.ini")

    # Change the "True/False" variables to a boolean
    checkUpdate = stringToBool(config["DEFAULT"]["checkForUpdatesOnStart"])
    getPreRel = stringToBool(config["DEFAULT"]["getPreReleaseVersions"])

def reloadIni():
    # Make sure all .ini files exist
    if os.path.exists('airlines.ini') == False:
        file = open("airlines.ini", 'w')
        file.write("[DEFAULT]\n")
        file.write("name=\n")
        file.write("url=\n")
        file.write("apikey=None Saved\n")
        file.write("rememberMe=False\n")

        file.close()

    if os.path.exists('settings.ini') == False:
        file = open("settings.ini", 'w')
        file.write("[DEFAULT]\n")
        file.write("checkForUpdatesOnStart = True\n")
        file.write("getPreReleaseVersions = False\n")
        file.close()

def rememberUser():
    global airline
    global website
    global APIKey
    global username

    config = configparser.ConfigParser()
    config.read("airlines.ini")
    configSections = config.sections()

    try:
        for key in configSections:
            if (stringToBool(config[key]["rememberMe"])):
                airline = config[key]['name']
                website = config[key]['URL']
                APIKey = config[key]['apikey']
                username = config[key]['username']
                return True
        return False

    except Exception as e:
        tk.messagebox.showerror("xACARS Error", e)
        return False

def forgetUsers():
    config = configparser.ConfigParser()
    config.read("airlines.ini")
    configSections = config.sections()

    try:
        for key in configSections:
            config[key]["rememberMe"] = "False"

        with open('airlines.ini', 'w') as configfile:
            config.write(configfile)

    except Exception as e:
        tk.messagebox.showerror("xACARS Error", e)
        return False

reloadIni()
reloadAirlines()
reloadSettings()