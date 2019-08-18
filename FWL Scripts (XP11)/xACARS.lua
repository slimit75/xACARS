function joinPath(x, y)
    return x .. "\\" .. y
end

fileLoc = os.getenv('APPDATA')
fileLoc = joinPath(fileLoc, 'xACARS')
logMsg(fileLoc)

function writeData(x, y)
    file = joinPath(fileLoc, 'input')
    file = joinPath(file, x .. '.txt')

    f = io.open(file, "w")
    io.output(f)
    io.write(tostring(y))
    io.close(f)
end

function refresh()
    writeData('lat', get("sim/flightmodel/position/latitude"))
    writeData('lon', get("sim/flightmodel/position/longitude"))
    writeData('heading', get("sim/cockpit2/gauges/indicators/compass_heading_deg_mag"))
    writeData('vs', get("sim/cockpit2/gauges/indicators/vvi_fpm_pilot"))
    writeData('altitude', get("sim/cockpit2/gauges/indicators/altitude_ft_pilot"))
    gs = get("sim/flightmodel/position/groundspeed")
    gs = gs * 1.94384
    writeData('gs', gs)
end

do_often("refresh()")