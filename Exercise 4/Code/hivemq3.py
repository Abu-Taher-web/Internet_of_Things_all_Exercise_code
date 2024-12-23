from machine import Pin, I2C
from bmp280 import BMP280
import network
import time
import simple
from simple import MQTTClient
import ssl
import config
import dht

# Setup LED
led = Pin("LED", Pin.OUT)  # GPIO 13 as output pin for LED

# Setup Wi-Fi
ssid = config.ssid
password = config.pwd

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

wlan.connect(ssid, password)

connection_timeout = 10
while connection_timeout > 0:
    if wlan.status() == 3:  # Connected
        break
    connection_timeout -= 1
    print('Waiting for Wi-Fi connection...')
    time.sleep(1)

# Check if connection successful
if wlan.status() != 3:
    raise RuntimeError('[ERROR] Failed to establish a network connection')
else:
    print('[INFO] CONNECTED!')
    network_info = wlan.ifconfig()
    print('[INFO] IP address:', network_info[0])

# Define I2C connection and BMP
dht_sensor = dht.DHT22(machine.Pin(2))  # id=channel
i2c = machine.I2C(id=1, sda=Pin(14), scl=Pin(15))  # id=channel
bmp = BMP280(i2c)

# Callback function for both topics
def on_message(topic, msg):
    print(f"Received message: {msg} on topic: {topic}")
    if topic == b"picow/control":
        if msg == b"ON":  # Turn LED ON
            led.value(1)
            print("LED ON (control topic)")
        elif msg == b"OFF":  # Turn LED OFF
            led.value(0)
            print("LED OFF (control topic)")
    elif topic == b"anomaly/detection":
        if msg == b"Anomaly detected!":  # Turn LED ON (Anomaly detected)
            led.on()
            print("LED ON (anomaly detected)")
        elif msg == b"Normal data.":  # Turn LED OFF (Normal data)
            led.off()
            print("LED OFF (normal data)")

# Config SSL connection
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.verify_mode = ssl.CERT_NONE  # Disable certificate verification

# MQTT client connect
client = MQTTClient(client_id=b'tumi_picow', server=config.MQTT_BROKER, port=config.MQTT_PORT,
                    user=config.MQTT_USER, password=config.MQTT_PWD, ssl=context)

# Set the callback function before subscribing
client.set_callback(on_message)

# Connect to the broker
client.connect()

# Subscribe to both topics after setting the callback
#client.subscribe(b"picow/control")  # Topic for LED control
client.subscribe(b"anomaly/detection")  # Topic for anomaly detection

# Publish function
def publish(mqtt_client, topic, value):
    mqtt_client.publish(topic, value)
    print("[INFO][PUB] Published {} to {} topic".format(value, topic))

# Main loop
while True:
    dht_sensor.measure()  # Take a new measurement
    temperature1 = dht_sensor.temperature()  # Get temperature
    humidity1 = dht_sensor.humidity()
    temperature2 = bmp.temperature
    pressure2 = bmp.pressure

    # Publish sensor data to MQTT topics
    publish(client, 'room1/temperature1', str(temperature1))
    publish(client, 'room1/humidity1', str(humidity1)) 
    publish(client, 'room2/temperature2', str(temperature2))
    publish(client, 'room2/pressure2', str(pressure2))

    # Check for incoming messages and handle them accordingly
    client.check_msg()

    # Wait for 3 seconds
    time.sleep(1)
