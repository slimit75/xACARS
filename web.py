# ----------------------------------------- #
# web.py                                    #
# Speed_Limit75                             #
#                                           #
# This file is a libary that makes API      #
# requests to the Virtual Airline take up   #
# less space in the code, and also return   #
# an error should there be one.             #
# ----------------------------------------- #

# Import libarys
import requests
import webbrowser
import config

# Define functions
def get(website): # GET request, returns text should there be any
    try:
        data = requests.get(website, headers={"Content-type":"application/json", "X-API-Key":config.APIKey})
        return data.text
    except Exception as e:
        return str(e)

def getRaw(website): # GET request, returns reqest as an object
    try:
        data = requests.get(website, headers={"Content-type":"application/json", "X-API-Key":config.APIKey})
        return data
    except Exception as e:
        return str(e)

def post(website, datax): # POST request, returns http response as an object
    try:
        response = requests.post(website, data = datax, headers={"Content-type":"application/json", "X-API-Key":config.APIKey})
        return response
    except Exception as e:
        return str(e)

def isLatestVersion():
    data = requests.get('https://raw.githubusercontent.com/3dash/xACARS/update-system/updates.json').json()
    return (config.getPreRel == True and str(data["latestBeta"]) == config.version) or str(data["latestStable"]) == config.version

def delete(x): # For future use
    return

def openWiki():
    webbrowser.open_new_tab("https://github.com/3dash/xACARS/wiki")