from machine import Pin, UART

import utime

gps = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
buff = bytearray(255)


def toFloat(s):
    try:
        f = float(s)
        return f
    except:
        return None


def toTime(s):
    if (len(s) < 6):
        return None
    return s[0:2] + ":" + s[2:4] + ":" + s[4:6]


def toDate(s):
    if (len(s) < 6):
        return None
    return '20' + s[0:2] + '/' + s[2:4] + '/' + s[4:6]


def toDegree(raw, flag):
    rawFloat = toFloat(raw)
    if (rawFloat == None):
        return None
    
    degPart = int(rawFloat/100) 
    minPart = rawFloat - float(degPart*100) 
    
    degValue = float(degPart + minPart/60.0)
    if (flag == 'W' or flag == 'S'):
        degValue = (-1.0) * degValue
    
    return degValue


def printGPSData(d):
    if (d['longitude']):
        print("======================================")
        print("    Longitude  : {:.6f}".format(d['longitude']))
    if (d['latitude']): 
        print("    Latitude   : {:.6f}".format(d['latitude']))
    if (d['altitude']):
        print("    Altitude   : {:.1f}".format(d['altitude']) + " m")
    if (d['hdop']):
        print("    HDOP       : {:.1f}".format(d['hdop']))
    if (d['satellites']):
        print("    Satellites : {:.0f}".format(d['satellites']))
    if (d['gpstime']):
        print("    GPS time   : " + d['gpstime'])
    if (d['speed']):
        print("    Speed      : {:.1f}".format(d['speed']) + " knots")
    if (d['course']):
        print("    Course     : {:.1f}".format(d['course']) + " deg")
    if (d['timestamp']):
        print("    Date/time  : " + d['timestamp'])
    if (d['longitude']):
        print("--------------------------------------")


def parseGPS(sentence):
    gpsData = {
        "latitude": None,
        "longitude": None,
        "satellites": None,
        "gpstime": None,
        "speed": None,
        "course": None,
        "timestamp": None,
        "hdop": None,
        "altitude": None        
    }
    
    parts = sentence.split(',')
   
    if (parts[0] == "b'$GPGGA" and len(parts) == 15):
        if(parts[1] and parts[2] and parts[3] and parts[4] and parts[5] and parts[6] and parts[7]):
            gpsData['latitude'] = toDegree(parts[2], parts[3])
            gpsData['longitude'] = toDegree(parts[4], parts[5])
            gpsData['altitude'] = toFloat(parts[9])
            gpsData['satellites'] = toFloat(parts[7])
            gpsData['hdop'] = toFloat(parts[8])
            gpsData['gpstime'] = toTime(parts[1])
    
    elif (parts[0] == "b'$GPRMC" and len(parts) == 13):
        if (parts[1] and parts[2] and parts[3] and parts[4] and parts[5] and parts[6]):
            if (parts[2] == 'A'):
                gpsData['latitude'] = toDegree(parts[3], parts[4])
                gpsData['longitude'] = toDegree(parts[5], parts[6])
                gpsData['speed'] = toFloat(parts[7])
                gpsData['course'] = toFloat(parts[8])
                date = toDate(parts[9])
                time = toTime(parts[1])
                if (time and date):
                    gpsData['timestamp'] = '20' + date + ' ' + time
                else:
                    gpsData['timestamp'] = None
                    
    if (gpsData['longitude'] and gpsData['latitude']):
        return gpsData
    else:
        return None


while True:
    buff = str(gps.readline())
    #print(buff)
    data = parseGPS(buff)
    if (data):
        printGPSData(data)
    
    utime.sleep(0.2)
