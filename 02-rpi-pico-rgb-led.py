from machine import Pin
import time
import random

led = Pin(25, Pin.OUT)
led.value(1)

rled = Pin(18, Pin.OUT)
gled = Pin(19, Pin.OUT)
bled = Pin(20, Pin.OUT)

def leds_off():
    rled.value(1)
    gled.value(1)
    bled.value(1)

def led_on():
    leds_off()

    idx = random.randint(0,2)
    if idx == 0:
        the_led = rled
    elif idx == 1:
        the_led = gled
    else:
        the_led = bled
    

    the_led.value(0)
    time.sleep(random.randint(50,200) / 1000)


while True:
    led_on()
