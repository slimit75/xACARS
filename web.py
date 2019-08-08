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

def post(x): # For future use
    return

def delete(x): # For future use
    return 