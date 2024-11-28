import machine
import dht
import time

# Initialize the sensor on GP2 (Pin 4)
sensor = dht.DHT22(machine.Pin(2))

while True:
    try:
        sensor.measure()  # Trigger the sensor
        temperature = sensor.temperature()  # Get temperature
        humidity = sensor.humidity()  # Get humidity
        print(f"Temperature: {temperature:.1f}°C")
        print(f"Humidity: {humidity:.1f}%")
    except OSError as e:
        print("Sensor error:", e)

    time.sleep(1)  # Wait 2 seconds (DHT22 sampling interval)
