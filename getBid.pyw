# ----------------------------------------- #
# getBid.pyw                                #
# Speed_Limit75                             #
#                                           #
# This file manages any bids made on the    #
# virtual airlines website. This window     #
# will be removed in the near future.       #
# ----------------------------------------- #

# Import libarys
import tkinter as tk
from tkinter import ttk
import config
import web
import json

# Set variables
list = config.list
websites = config.websites
savedAPIKeys = config.savedAPIKeys
bidList = []
selBid = ""

# Define Functions
def draw():
    global selBid
    window = tk.Tk()
    window.iconbitmap('Favicon.ico')
    selBid = tk.StringVar(window)
    window.title('xACARS - Bids')
    tk.Label(window, text='Bids', font="Arial").grid(row=0, columnspan=1, sticky="w") 
    ttk.Separator(window, orient=tk.HORIZONTAL).grid(row=1, columnspan=4, sticky="we")
    data = web.get(config.website + '/api/user/bids')
    ## Check for and list bids
    if data == '{"data":[]}':
        tk.Label(window, text="No bids! Place a bid on the airline website and restart xACARS!").grid(row=1, column=0)
    else:
        bids = json.loads(data)["data"]
        bidList.append(str(bids[0]["flight"]["ident"]) + " (" + str(bids[0]["flight"]["dpt_airport_id"]) + " - " + str(bids[0]["flight"]["arr_airport_id"]) + ")")
        for key in bids:
            bidList.append(str(key["flight"]["ident"]) + " (" + str(key["flight"]["dpt_airport_id"]) + " - " + str(key["flight"]["arr_airport_id"]) + ")")

        bidList.reverse()
    
        selBid.set(bidList[0])
        ttk.OptionMenu(window, selBid, *bidList).grid(row=2, column=0, sticky="we")
        ttk.Button(window, text='Select', command=window.quit).grid(row=2, column=1, sticky="we")

    window.mainloop()
    window.destroy()

    if data == '{"data":[]}':
        return "No bids"
    else:
        selBid = selBid.get()

        selBidText = selBid.split(" ")
        selBidText = selBidText[0]

        a = 0
        for key in bids:
            if key["flight"]["ident"] == selBidText:
                break
            else:
                a = a + 1
    
        return bids[a]