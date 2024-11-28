import machine
from machine import Pin
from bme280 import BME280

i2c = machine.I2C(id=1, sda=Pin(14), scl=Pin(15)) #id=channel
bme = BME280(i2c=i2c)


while True:
    print(bme.values)
