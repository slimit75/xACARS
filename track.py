# ----------------------------------------- #
# track.pyw                                 #
# Speed_Limit75                             #
#                                           #
# This file is the bridge between xACARS    #
# and the flight simulator. This is the     #
# only file to use the pyuipc (UIPC API)    #
# libary.                                   #
# ----------------------------------------- #

# Import libarys
import pyuipc
import math
import os

# Opens connection to FSUIPC/XPUIPC, and returns if it was successful.
def beginTrack():
    try:
        pyuipc.open(0)
        return True
    except pyuipc.FSUIPCException as e:
        return "UIPC Connection Error: " + str(e.errorCode)
    except Exception as e:
        return "ERROR: " + str(e)

def endTrack():  # Closes connection to FSUIPC/XPUIPC.
    pyuipc.close()

def posUpdate():  # Update input folder with latest data from FSUIPC/XPUIPC.
    lat = pyuipc.read([(0x6010, "f")])
    lat = float(lat[0])

    long = pyuipc.read([(0x6018, "f")])
    long = float(long[0])

    hdg = pyuipc.read([(0x6040, "f")])
    hdg = float(hdg[0])
    hdg = hdg*180/math.pi

    vs = pyuipc.read([(0x0842, "h")])
    vs = float(vs[0])
    vs = vs * -3.28084

    alt = pyuipc.read([(0x6020, "f")])
    alt = float(alt[0])
    alt = alt*3.28084

    gs = pyuipc.read([(0x6030, "f")])
    gs = float(gs[0])
    gs = gs*3600/1852

    return lat, long, hdg, vs, alt, gs