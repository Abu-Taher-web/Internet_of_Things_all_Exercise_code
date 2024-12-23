from machine import Pin, I2C
from bmp280 import BMP280
import network
import time
import simple
from simple import MQTTClient
import ssl
import config
import dht


# setup wifi
ssid = config.ssid
password = config.pwd

# connect to wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

wlan.connect(ssid, password)

connection_timeout = 10
while connection_timeout > 0:
    if wlan.status() == 3: # connected
        break
    connection_timeout -= 1
    print('Waiting for Wi-Fi connection...')
    time.sleep(1)

# check if connection successful
if wlan.status() != 3: 
    raise RuntimeError('[ERROR] Failed to establish a network connection')
else: 
    print('[INFO] CONNECTED!')
    network_info = wlan.ifconfig()
    print('[INFO] IP address:', network_info[0])
 
 
# define I2C connection and BMP
dht_sensor = dht.DHT22(machine.Pin(2)) # id=channel
i2c = machine.I2C(id=1, sda=Pin(14), scl=Pin(15))  # id=channel
bmp = BMP280(i2c)

def on_message(topic, msg): 
    print(f"Received message: {msg} on topic: {topic}") 
    if msg == b"ON":  
        print("LED ON") 
    elif msg == b"OFF": 
        print("LED OFF") 
# config ssl connection w Transport Layer Security encryption (no cert)
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT) # TLS_CLIENT = connect as client not server/broker
context.verify_mode = ssl.CERT_NONE # CERT_NONE = not verify server/broker cert - CERT_REQUIRED: verify

# config ssl connection w Transport Layer Security encryption (cert required)
# context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
# context.verify_mode = ssl.CERT_REQUIRED
# context.load_verify_locations('ccertificate.pem') # Load the certificate from path

# mqtt client connect
client = MQTTClient(client_id=b'tumi_picow', server=config.MQTT_BROKER, port=config.MQTT_PORT,
                    user=config.MQTT_USER, password=config.MQTT_PWD, ssl=context)

client.connect()
client.set_callback(on_message) 
client.subscribe(b"picow/control") 





def publish(mqtt_client, topic, value):
    mqtt_client.publish(topic, value)
    print("[INFO][PUB] Published {} to {} topic".format(value, topic))


while True:
    
    dht_sensor.measure()  # Take a new measurement
    temperature1 = dht_sensor.temperature()  # Get temperature
    humidity1 = dht_sensor.humidity()
    temperature2 = bmp.temperature
    pressure2 = bmp.pressure
    # publish as MQTT payload
    publish(client, 'room1/temperature1', str(temperature1))
    publish(client, 'room1/humidity1', str(humidity1))
    publish(client, 'room2/temperature2', str(temperature2))
    publish(client, 'room2/pressure2', str(pressure2))
    client.check_msg()

    # every 2s
    time.sleep_ms(1000)
    