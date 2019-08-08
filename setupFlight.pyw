# ----------------------------------------- #
# setupFlight.pyw                           #
# Speed_Limit75                             #
#                                           #
# Screen where you select a bid, and        #
# prefile. This will be removed and         #
# replaced in main.pyw in the near future.  #
# ----------------------------------------- #

# Import libarys
import tkinter as tk
from tkinter import ttk
import config
import web
import json

# Set variables
bid = ""
status = "selBid"
pirepId = ""

# Define functions
def refresh():
    global window
    global bidData
    global plannedFlightTime
    global flightLevel
    global plannedDistance
    global route
    global status

    if bid == "":
        getBid()
    else:
        window = tk.Tk()
        window.iconbitmap('Favicon.ico')
        window.title('xACARS - Flight')
        tk.Label(window, text='Flight Data', font="Arial").grid(row=0, columnspan=1, sticky="w")
        ttk.Separator(window, orient=tk.HORIZONTAL).grid(row=1, columnspan=4, sticky="we")
        if status == "prefile":
            plannedFlightTime = tk.StringVar(window)
            flightLevel = tk.StringVar(window)
            plannedDistance = tk.StringVar(window)
            route = tk.StringVar(window)
            tk.Label(window, text=bidData["flight"]["ident"]).grid(row=2, column=0, sticky="w")
            tk.Label(window, text=bidData["flight"]["dpt_airport_id"] + " - " + bidData["flight"]["arr_airport_id"]).grid(row=3, column=0, sticky="w")
            tk.Label(window, text="Planned Flight Time: ").grid(row=4, column=0, sticky="w")
            tk.Label(window, text="minutes").grid(row=4, column=3, sticky="w")
            tk.Entry(window, textvariable=plannedFlightTime).grid(row=4, column=1)
            tk.Label(window, text="Flight Level: FL").grid(row=5, column=0, sticky="w")
            tk.Entry(window, textvariable=flightLevel).grid(row=5, column=1)
            tk.Label(window, text="Planned Distance: ").grid(row=6, column=0, sticky="w")
            tk.Label(window, text="nm").grid(row=6, column=3, sticky="w")
            tk.Entry(window, textvariable=plannedDistance).grid(row=6, column=1)
            tk.Label(window, text="Route: ").grid(row=7, column=0, sticky="w")
            tk.Entry(window, textvariable=route).grid(row=7, column=1)
            tk.Button(window, text='Prefile', command=prefile).grid(row=8, columnspan=4, sticky="we")
        elif status == "AwiatingStart":
            tk.Label(window, text=bidData["flight"]["ident"]).grid(row=2, column=0, sticky="w")
            tk.Label(window, text=bidData["flight"]["dpt_airport_id"] + " - " + bidData["flight"]["arr_airport_id"]).grid(row=3, column=0, sticky="w")
            tk.Label(window, text="Planned Flight Time: " + str(plannedFlightTime) + "minutes").grid(row=4, column=0, sticky="w")
            tk.Label(window, text="Flight Level: FL" + str(flightLevel)).grid(row=5, column=0, sticky="w")
            tk.Label(window, text="Planned Distance: ").grid(row=6, column=0, sticky="w")
            tk.Label(window, text="nm").grid(row=6, column=3, sticky="w")
            tk.Entry(window, textvariable=plannedDistance, text=plannedDistance).grid(row=6, column=1)
            tk.Label(window, text="Route: " + str(route)).grid(row=7, column=0, sticky="w")
            tk.Button(window, text='Start Flight', command=prefile).grid(row=8, columnspan=4, sticky="we")
    window.mainloop()

def getBid():
    global bid
    global window
    global bidData
    global status
    import getBid
    bid = getBid.selBid
    bid = bid.get()

    data = bid.split(" ")
    data = data[0]

    bidData = web.get(config.website + '/api/user/bids')
    bidData = json.loads(bidData)["data"]
    a = 0
    for key in bidData:
        if key["flight"]["ident"] == data:
            break
        else:
            a = a + 1

    bidData = bidData[a]
    status = "prefile"
    refresh()
    
def prefile():
    global bidData
    global plannedFlightTime
    global flightLevel
    global plannedDistance
    global route
    global status
    global pirepId
    
    plannedFlightTime = plannedFlightTime.get()
    flightLevel = flightLevel.get()
    plannedDistance = plannedDistance.get()
    route = route.get()

    #plannedFlightTime = int(plannedFlightTime)
    #flightLevel = int(flightLevel)
    #plannedDistance = int(plannedDistance)

    data = '''{
    "airline_id": ''' + str(bidData["flight"]["airline"]["id"]) + ''',
    "aircraft_id": 1,
    "flight_number": ''' + str(bidData["flight"]["flight_number"]) + ''',
    "route_code": ''' + str(bidData["flight"]["flight_type"]) + ''',
    "route_leg": ''' + str(bidData["flight"]["route_leg"]) + ''',
    "dpt_airport_id": "''' + str(bidData["flight"]["dpt_airport_id"]) + ''',",
    "arr_airport_id": "''' + str(bidData["flight"]["arr_airport_id"]) + ''',",
    "level": ''' + str(flightLevel) + ''',
    "planned_distance": ''' + str(plannedDistance) + ''',
    "planned_flight_time": ''' + str(plannedFlightTime) + ''',
    "route": "''' + str(route) + '''",
    "source_name": "ACARS",
    "flight_type": ''' + str(bidData["flight"]["route_code"]) + ''',
}'''

    print(data)
    #a = requests.post(config.website + '/api/pireps/prefile', data)
    #print(a)
    #print(a.text)
    #pirepId = a.text

    status = "AwiatingStart"
    refresh()

refresh() # Support for files that import it expecting it to run.