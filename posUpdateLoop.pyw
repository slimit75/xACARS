# ----------------------------------------- #
# posUpdateLoop.pyw                         #
# Speed_Limit75                             #
#                                           #
# This file runs a loop to refresh data in  #
# the input folder every 5 seconds,         #
# regardless if it can connect to FSUIPC or #
# XPUIPC.                                   #
# ----------------------------------------- #

# Import libarys
import time
import threading
import track
import json
import web
import config
import os

# Set variables
stop = False
pirepID = ""

# Define functions
def read(x):
    file = open(str(os.getenv('APPDATA')) + '/xACARS/input/' + x + '.txt', "r")
    toreturn = file.read()
    file.close()
    return toreturn

def loop():
    global pirepID
    while True:
        if config.useFSUIPC == True: track.beginTrack()
        try:
            if config.useFSUIPC == True: track.posUpdate()

            
            data = {
    "lat": float(read('lat')),
    "lon": float(read('lon')),
    "heading": float(read('heading')),
    "altitude": float(read('altitude')),
    "vs": float(read('vs')),
    "gs": float(read('gs'))
}
            data = {
    "positions": [data]
}
            data = json.dumps(data)
            data = web.post(config.website + '/api/pireps/' + pirepID + '/acars/position', data)
        except Exception as e:
            print(e)

        time.sleep(5)

        if stop == True:
            break

def startLoop(x):
    global thread
    global pirepID
    pirepID = x
    thread = threading.Thread(target=loop)
    thread.start()

def stopLoop():
    global thread
    global stop
    stop = True
    track.endTrack()