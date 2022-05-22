from machine import Pin, I2C
from lib.ssd1306 import SSD1306_I2C
import utime
from lib.dht import DHT11

# turn internal led on
led = Pin(25, Pin.OUT)
led.low()

# OLED display
WIDTH = 128
HEIGHT = 64

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=200000)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

# 8x8 pixels each font
# up to 16 columns (font per row)
# 8 rows, offset for each row: 0, 8, 16, 24, 32, 40, 48, 56
# 5 rows, offset for each row: 4, 20, 32, 44, 56
# for 32 pixels height variant, row offset are: 0, 13, 25
oled.fill(0)
oled.text("Welcome!", 35, 4)
oled.text("Tutorials: Simp.", 0, 20)
oled.show()

utime.sleep(2)

sensor = DHT11(Pin(16, Pin.OUT, Pin.PULL_DOWN))

otime = utime.time()

while True:
    led.toggle()

    ntime = utime.time()
    if ((ntime - otime) > 120):
        oled.fill(0)
        oled.text("________________", 0, 8)
        oled.show()
        utime.sleep(1)
        otime = utime.time()
        
    temp = sensor.temperature
    humidity = sensor.humidity
    
    stemp = "Temp: {} C".format(temp)
    shum  = "Humidity: {:.0f}%".format(humidity)
    print(" Temperature: {}°C   Humidity: {:.0f}% ".format(temp, humidity))
    
    oled.fill(0)
    oled.text("Tutorials: Simp.", 0, 4)
    oled.text("DHT11 Data", 25, 24)
    oled.text(stemp, 15, 40)
    oled.text(shum, 15, 52)
    oled.show()
    
    utime.sleep(2)