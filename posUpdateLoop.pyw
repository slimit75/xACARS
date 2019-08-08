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

# Set variables
stop = False

# Define functions
def loop():
    while True:
        try:
            track.posUpdate()
        except Exception as e:
            pass

        time.sleep(5)

        if stop == True:
            break

def startLoop():
    global thread
    thread = threading.Thread(target=loop)
    thread.start()

def stopLoop():
    global thread
    global stop
    stop = True