from machine import I2C
import utime
from pico_i2c_lcd import I2cLcd

# LCD I2C stuff
I2C_ADDR     = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1))
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# First display
lcd.putstr("Hello ...\nSimple Tutorials")
utime.sleep(2)
lcd.clear()
lcd.putstr("I'm counting...")

# The loop
i = 0
while True:
    lcd.move_to (0, 1)
    lcd.putstr("                ")

    i += 1
    lcd.move_to (0, 1)
    lcd.putstr(str(i % 20))

    utime.sleep(1)
