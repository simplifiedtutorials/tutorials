from machine import Pin, UART

import utime

gps = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
buff = bytearray(255)


def convertToDegree(raw, flag):
    try:
        rawFloat = float(raw)
    except:
        return None
    
    degPart = int(rawFloat/100) 
    minPart = rawFloat - float(degPart*100) 
    
    degValue = float(degPart + minPart/60.0)
    if (flag == 'W' or flag == 'S'):
        degValue = (-1.0) * degValue
    
    return degValue

def printGPSData(d):
    if (d['longitude']):
        print("===========================")
        print("    Longitude  : {:.6f}".format(d['longitude']))

    if (d['latitude']): 
        print("    Latitude   : {:.6f}".format(d['latitude']))
        
    if (d['altitude']):        
        print("    Altitude   : " + d['altitude'] + " m")
        
    if (d['hdop']):
        print("    HDOP       : " + d['hdop'])
        
    if (d['satellites']):
        print("    Satellites : " + str(int(d['satellites'])))
        
    if (d['gpstime']):
        print("    GPS time   : " + d['gpstime'])
        
    if (d['speed']):
        if (d['speed'] != ""):
            print("    Speed      : " + d['speed'] + " knots")
            
    if (d['course']):
        if (d['course'] != ""):
            print("    Course     : {:.1f} deg".format(float(d['course'])))
            
    if (d['timestamp']):
        print("    Date/time  : " + d['timestamp'])
    
    if (d['longitude']):
        print("---------------------------")


def parseGPS(strNMEA):
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
    
    parts = strNMEA.split(',')
   
    if (parts[0] == "b'$GPGGA" and len(parts) == 15):
        if(parts[1] and parts[2] and parts[3] and parts[4] and parts[5] and parts[6] and parts[7]):
            #print(buff)
            
            gpsData['latitude'] = convertToDegree(parts[2], parts[3])
            if (gpsData['latitude'] == None):
                return None
            gpsData['longitude'] = convertToDegree(parts[4], parts[5])
            if (gpsData['longitude'] == None):
                return None
            gpsData['altitude'] = parts[9]
            gpsData['satellites'] = parts[7]
            gpsData['hdop'] = parts[8]
            
            gpsData['gpstime'] = parts[1][0:2] + ":" + parts[1][2:4] + ":" + parts[1][4:6]
    
    elif (parts[0] == "b'$GPRMC" and len(parts) == 13):
        if (parts[1] and parts[2] and parts[3] and parts[4] and parts[5] and parts[6]):
            if (parts[2] == 'A'):
                gpsData['latitude'] = convertToDegree(parts[3], parts[4])
                if (gpsData['latitude'] == None):
                    return None
                gpsData['longitude'] = convertToDegree(parts[5], parts[6])
                if (gpsData['longitude'] == None):
                    return None
                gpsData['speed'] = parts[7]
                gpsData['course'] = parts[8]
                date = '20' + parts[9][0:2] + '/' + parts[9][2:4] + '/' + parts[9][4:6] 
                time = parts[1][0:2] + ":" + parts[1][2:4] + ":" + parts[1][4:6]
                gpsData['timestamp'] = date + ' ' + time
                    
    return gpsData


while True:
    buff = str(gps.readline())
    print(buff)
    data = parseGPS(buff)
    if (data):
        printGPSData(data)
    
    utime.sleep(0.5)
