from machine import Pin
import time

led = Pin("LED", Pin.OUT)  # Configure the onboard LED pin

while True:
    led.on()               # Turn the LED on
    time.sleep(0.5)        # Wait for 0.5 seconds
    led.off()              # Turn the LED off
    time.sleep(0.5)
    # Wait for 0.5 seconds
