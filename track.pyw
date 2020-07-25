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

# Define functions


# Opens connection to FSUIPC/XPUIPC, and returns if it was successful.
def beginTrack():
    try:
        pyuipc.open(0)
        return "UIPC Connection Successful!"
    except pyuipc.FSUIPCException as e:
        return "UIPC Connection Error: " + str(e.errorCode)
    except Exception as e:
        return "ERROR: " + str(e)


def endTrack():  # Closes connection to FSUIPC/XPUIPC.
    pyuipc.close()


# Write data to a text file in the input folder. Creates file if there is none, and if there is one it overwrites it.
def writeData(x, y):
    file = open(str(os.getenv('APPDATA')) + '/xACARS/input/' + x + '.txt', 'w')
    file.write(str(y))
    file.close()


def posUpdate():  # Update input folder with latest data from FSUIPC/XPUIPC.
    lat = pyuipc.read([(0x6010, "f")])
    lat = float(lat[0])
    writeData('lat', lat)
    long = pyuipc.read([(0x6018, "f")])
    long = float(long[0])
    writeData('lon', long)
    # hdg = pyuipc.read([(0x6038, "f")]) True Heading
    hdg = pyuipc.read([(0x6040, "f")])  # Magnetic Heading
    hdg = float(hdg[0])
    hdg = hdg*180/math.pi
    writeData('heading', hdg)
    vs = pyuipc.read([(0x0842, "h")])
    vs = float(vs[0])
    vs = vs * -3.28084
    writeData('vs', vs)
    alt = pyuipc.read([(0x6020, "f")])
    alt = float(alt[0])
    alt = alt*3.28084
    writeData('altitude', alt)
    gs = pyuipc.read([(0x6030, "f")])
    gs = float(gs[0])
    gs = gs*3600/1852
    writeData('gs', gs)
    # GS, ALT
