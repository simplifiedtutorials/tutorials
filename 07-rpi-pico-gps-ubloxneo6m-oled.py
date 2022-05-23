from machine import Pin, UART, I2C
from lib.ssd1306 import SSD1306_I2C

import utime

# GPS 
gps = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
buff = bytearray(255)

# OLED display
WIDTH = 128
HEIGHT = 64

i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=200000)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
oled.fill(0)
oled.text("Simplified Ttrls", 0, 4)
oled.show()


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
    return '20' + s[4:6] + '/' + s[2:4] + '/' + s[0:2]


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


def oledPrint4Rows(s1, s2, s3, s4):
    oled.fill(0)
    oled.text("Simplified Ttrls", 0, 4)
    oled.text(s1, 0, 20)
    oled.text(s2, 0, 32)
    oled.text(s3, 0, 44)
    oled.text(s4, 0, 56)
    oled.show()


def oledGPSData(d):
    if (d['longitude'] and d['latitude']):
        s1 = ""
        s2 = ""
        s3 = ""
        s4 = ""
        
        s1 = "X:{:.2f}".format(d['longitude']) + ",Y:{:.2f}".format(d['latitude'])
        if (d['altitude']):
            s2 = "Z:{:.1f}".format(d['altitude']) + " m"
            if (d['hdop'] and d['satellites']):
                s3 = "HD:{:.1f}".format(d['hdop']) + ", SAT:{:.0f}".format(d['satellites'])
            if (d['gpstime']):
                s4 = "T:" + d['gpstime']
        elif (d['speed']):
            s2 = "S:{:.1f}".format(d['speed']) + " knots"
            if (d['course']):
                s3 = "C:{:.1f}".format(d['course'])
            else:
                s3 = "C:unknown"
            if (d['timestamp']):
                s4 = "D:" + d['timestamp'][0:10]
        
        oledPrint4Rows(s1, s2, s3, s4)    
    else:
        oledPrint4Rows("", "", "No GPS data....", "")
    

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
                    gpsData['timestamp'] = date + ' ' + time
                else:
                    gpsData['timestamp'] = None
                    
    if (gpsData['longitude'] and gpsData['latitude']):
        return gpsData
    else:
        return None


while True:
    buff = str(gps.readline())
    if ((buff[0:8] == "b'$GPGGA") or (buff[0:8] == "b'$GPRMC")):
        print(buff)
        data = parseGPS(buff)
        if (data):
            printGPSData(data)
            oledGPSData(data)
    
    utime.sleep(0.2)
