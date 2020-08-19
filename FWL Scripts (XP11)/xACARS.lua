function joinPath(x, y)
    return x .. "\\" .. y
end

fileLoc = os.getenv('APPDATA')
fileLoc = joinPath(fileLoc, 'xACARS')

function writeData(x, y)
    file = joinPath(fileLoc, 'input')
    file = joinPath(file, x .. '.txt')
    
    f = io.open(file, "w")
    io.output(f)
    io.write(tostring(y))
    io.close(f)
end

function refresh()
    lat = LATITUDE
    writeData('lat', lat)
    lon = LONGITUDE
    writeData('lon', lon)
    hdg = get("sim/cockpit2/gauges/indicators/compass_heading_deg_mag")
    writeData('heading', hdg)
    vs = get("sim/cockpit2/gauges/indicators/vvi_fpm_pilot")
    vs = tostring(vs)
    if string.match(vs, "e") then
        vs = 0.0
    else
        vs = tonumber(vs)
        vs = vs * 1.94384
    end
    writeData("vs", vs)

    alt = get("sim/cockpit2/gauges/indicators/altitude_ft_pilot")
    writeData('altitude', alt)
    gs = get("sim/flightmodel/position/groundspeed")
    gs = tostring(gs)
    if string.match(gs, "e") then
        gs = 0.0
    else
        gs = tonumber(gs)
        gs = gs * 1.94384
    end
    
    writeData("gs", gs)
end

do_often("refresh()")