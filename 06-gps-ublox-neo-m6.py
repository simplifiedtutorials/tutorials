from machine import Pin, UART

import utime

gpsModule = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

buff = bytearray(255)

TIMEOUT = False
FIX_STATUS = False

sentence = ""
latitude = ""
longitude = ""
satellites = ""
GPStime = ""
speed = ""
course = ""
timestamp = ""
horaccuracy = ""
altitude = ""

def getGPS(gpsModule):
    
    global FIX_STATUS, TIMEOUT, latitude, longitude, satellites, GPStime, speed, course, altitude, horaccuracy, timestamp, sentence
    
    timeout = utime.time() + 20 
    while True:
        gpsModule.readline()
        buff = str(gpsModule.readline())
        print(buff)
       
        parts = buff.split(',')
       
        if (parts[0] == "b'$GPGGA" and len(parts) == 15):
            sentence = "GGA"
            if(parts[1] and parts[2] and parts[3] and parts[4] and parts[5] and parts[6] and parts[7]):
                #print(buff)
                
                latitude = convertToDegree(parts[2], parts[3])
                longitude = convertToDegree(parts[4], parts[5])
                altitude = parts[9]
                satellites = parts[7]
                horaccuracy = parts[8]
                
                GPStime = parts[1][0:2] + ":" + parts[1][2:4] + ":" + parts[1][4:6]
                FIX_STATUS = True
                break
        
        if (parts[0] == "b'$GPRMC" and len(parts) == 13):
            sentence = "RMC"
            if (parts[1] and parts[2] and parts[3] and parts[4] and parts[5] and parts[6]):
                if (parts[2] == 'A'):
                    latitude = convertToDegree(parts[3], parts[4])
                    longitude = convertToDegree(parts[5], parts[6])
                    speed = parts[7]
                    course = parts[8]
                    date = '20' + parts[9][0:2] + '/' + parts[9][2:4] + '/' + parts[9][4:6] 
                    time = parts[1][0:2] + ":" + parts[1][2:4] + ":" + parts[1][4:6]
                    timestamp = date + ' ' + time
                    FIX_STATUS = True
                    break
                    
                
        if (utime.time() > timeout):
            TIMEOUT = True
            break
        utime.sleep_ms(500)
        
        
def convertToDegree(raw, flag):
    rawFloat = float(raw)
    
    degPart = int(rawFloat/100) 
    minPart = rawFloat - float(degPart*100) 
    
    degValue = float(degPart + minPart/60.0)
    if (flag == 'W' or flag == 'S'):
        degValue = (-1.0) * degValue
    
    return degValue
    
    
while True:
    
    getGPS(gpsModule)

    if(FIX_STATUS == True):
        if (sentence == "GGA"):
            print("----------------------")
            print("$GPGGA data")
            print("Longitude: {:.6f}".format(longitude))
            print("Latitude: {:.6f}".format(latitude))
            print("Altitude: " + altitude + " m")
            print("HDOP: " + horaccuracy)
            print("No. of satellites: " + str(int(satellites)))
            print("Time: " + GPStime)
            print("----------------------")
        elif (sentence == "RMC"):
            print("----------------------")
            print("$GPRMC Data")
            print("Longitude: {:.6f}".format(longitude))
            print("Latitude: {:.6f}".format(latitude))
            if (speed != ""):
                print("Speed: {:.1f} knots".format(float(speed)))
            if (course != ""):
                print("Course: {:.1f} deg".format(float(course)))
            print("Date/time: " + timestamp)
            print("----------------------")
            
        FIX_STATUS = False
        
    if(TIMEOUT == True):
        print("No GPS data is found.")
        TIMEOUT = False

