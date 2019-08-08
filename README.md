# xACARS
ACARS system for phpVMS.

**There is a critical X-Plane only bug where only ground speed and vertical speed are being loaded by the XPUIPC bridge.**

## What does it require?
It requires:
- Python 3.7.4 32bit
- FSUIPC SDK for Python 3.7

- FSX, P3D, or X-Plane
- FSUIPC or XPUIPC

## Todo
- [x] Finish login system

- [ ] Pirep Handling

- - [x] Check & load bids

- - [x] Prefile Page

- - [ ] Start Flight Button

- - [ ] Position Updates

- - [ ] File Pirep Page

- - [ ] Make pages functional

- [ ] Bridge to Simulator

- - [x] FSUIPC/XPUIPC writes basic data

- - [ ] FSUIPC/XPUIPC writes all data needed

- [ ] Installer

- [ ] Update System

- [ ] Wiki

- [x] Settings

- [ ] Embedded Python

- [ ] Redo look of graphical interface, feature dark mode

### Future
- [ ] Linux Support

- [ ] Custom plugin for X-Plane 11 (for all systems)

- [ ] PIREP Event Updates

## What do all of the files do?
Here is a list of what they do:

```
about.pyw - Runs the "about" window
airlines.ini - Database of airlines
config.py - Handles reading the .ini files
enroute - Data for in-flight. 
getBid.pyw - Gets a bid
listAirlines.pyw - Lists airlines, and manages the creation and editing of them
login.pyw - Runs the login window
main.pyw - Runs the main window
setupFlight.pyw - Flight configuration menu, for prefiling.
track.pyw - Tracks the flight and updates its position.
web.py - Interfaces between the web and the program. Basically the requests module, except sends the headers without an extra field.
```
