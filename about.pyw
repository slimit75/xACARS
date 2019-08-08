# ----------------------------------------- #
# about.py                                  #
# Speed_Limit75                             #
#                                           #
# This file powers the about screen.        #
# ----------------------------------------- #

# Import variables
import tkinter as tk
from tkinter import ttk
import config

# Draw window
window = tk.Tk()
window.iconbitmap('Favicon.ico')
window.title('xACARS - About')
tk.Label(window, text="xACARS " + config.version, font="Arial").grid(row=0, column=0)
tk.Label(window, text="xACARS was developed by Speed_Limit75.").grid(row=1, column=0)
ttk.Separator(window, orient=tk.HORIZONTAL).grid(row=2, column=0, sticky="we")
tk.Label(window, text="This program is currently a beta, so you should expect broken things.").grid(row=3, column=0, sticky="w")
tk.Label(window, text="xACARS is powered by FSUIPC/XPUIPC to gather data from the simulator.").grid(row=4, column=0, sticky="w")
tk.Label(window, text="It is written in python, and its graphical interface is powered by").grid(row=5, column=0, sticky="w")
tk.Label(window, text="tkinter. It will have a graphical overhaul before release.").grid(row=6, column=0, sticky="w")
window.mainloop()