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

import tkinter as tk
from tkinter import messagebox

# Set variables
stop = False
pirepID = ""

# Define functions
def loop():
    global pirepID
    while True:
        track.beginTrack()

        lat, lon, hdg, vs, alt, gs = track.posUpdate()
        try:
            exportdata = {"lat": lat,"lon": lon,"heading": hdg,"altitude": alt,"vs": vs,"gs": gs}
            exportdata = {"positions": [exportdata]}

            exportdata = json.dumps(exportdata)
            
            web.post(config.website + '/api/pireps/' + pirepID + '/acars/position', exportdata)
        except Exception as e:
            tk.messagebox.showerror("xACARS Error - Update Loop", e)

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