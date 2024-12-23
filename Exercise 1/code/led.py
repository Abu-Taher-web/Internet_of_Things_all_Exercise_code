from machine import Pin
import time

led = Pin(13, Pin.OUT)  # Onboard LED is connected to GPIO 25

led.on()

