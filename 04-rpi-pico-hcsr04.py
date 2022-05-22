from machine import Pin, I2C
import utime
from pico_i2c_lcd import I2cLcd

# Internal led init
led = Pin(25, Pin.OUT)
led.high()

# LCD section ------------------------------------
I2C_ADDR     = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16
i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1))
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)


def lcdPrint(col, row, s):
    lcd.move_to(col, row)
    lcd.putstr(s)
    
def lcdClear():
    lcd.clear()

# HC-SR04 section --------------------------------
trigger = Pin(14, Pin.OUT)
echo = Pin(15, Pin.IN)

# Distance function
def calcDistance():
    trigger.low()
    utime.sleep_us(2)

    trigger.high()
    utime.sleep_us(10)
    trigger.low()

    while echo.value() == 0:
       signaloff = utime.ticks_us()

    while echo.value() == 1:
       signalon = utime.ticks_us()

    timepassed = signalon - signaloff
    distance = (timepassed * 0.0343) / 2

    if (distance < 0.1) or (distance > 450):
        distance = None
        
    return distance

# Main program -----------------------------------
def main():
    lcdPrint(0, 0, "Hello ...")
    lcdPrint(0, 1, "Simple Tutorials")
    utime.sleep(2)

    lcdClear()
    lcdPrint(0, 0, "I'm counting...")

    while True:
        led.toggle()
        d = calcDistance()
        if (d):
            print ("Distance : {:.1f} cm".format(d))
            lcdPrint(0, 1, "                ")
            lcdPrint(0, 1, "d = {:.1f} cm".format(d))
        utime.sleep(1)


if __name__ == "__main__":
    main()
