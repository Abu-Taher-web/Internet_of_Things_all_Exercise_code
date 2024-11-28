from machine import Pin, I2C
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






def publish(mqtt_client, topic, value):
    mqtt_client.publish(topic, value)
    print("[INFO][PUB] Published {} to {} topic".format(value, topic))


while True:
    
    dht_sensor.measure()  # Take a new measurement
    temperature = dht_sensor.temperature()  # Get temperature
    humidity = dht_sensor.humidity()
    # publish as MQTT payload
    publish(client, 'tumi_picow/temp', str(temperature))
    publish(client, 'tumi_picow/humidity', str(humidity))
    publish(client, 'home/livingroom/temperature', str(temperature))
    publish(client, 'home/livingroom/humidity', str(humidity))

    # every 2s
    time.sleep_ms(2000)
    