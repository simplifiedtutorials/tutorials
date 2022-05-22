from machine import Pin, I2C
from lib.ssd1306 import SSD1306_I2C
import utime

# turn internal led on
led = Pin(25, Pin.OUT)
led.low()

# OLED display
WIDTH = 128
HEIGHT = 32

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=200000)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

# 8x8 pixels each font
# up to 16 columns (font per row)
# 8 rows, offset for each row: 0, 8, 16, 24, 32, 40, 48, 56
# 5 rows, offset for each row: 4, 20, 32, 44, 56
# for 32 pixels height variant, row offset are: 0, 13, 25
oled.fill(0)
oled.text("Welcome!", 35, 0)
oled.text("Simplified Ttrls", 0, 13)
oled.text("3.ABCDEFGHIJKLM", 0, 25)
oled.show()

utime.sleep(5)


i = 0
while True:
    led.toggle()
    utime.sleep(1)

    i = i + 1
    print (str(i))
    
    oled.fill(0)
    oled.text("I'm counting", 5, 8)
    oled.text(str(i % 20), 55, 20)
    oled.show()
    
    utime.sleep(1)
