from machine import Pin
import time

led = Pin(25, Pin.OUT)   
red_led = Pin(15, Pin.OUT) 

while True:
  led.value(1)            
    red_led.value(0)
  time.sleep(1)
  led.value(0)    
    red_led.value(1)
  time.sleep(1)
  