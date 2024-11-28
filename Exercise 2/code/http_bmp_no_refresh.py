from machine import Pin
from bmp280 import BMP280
import network
import socket
import time
import json
import config

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

# set up socket and listen on port 80
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)  # Listen for incoming connections

print('[INFO] Listening on', addr)

# html with js for AJAX updates
def generate_html():
    html = """\
    HTTP/1.1 200 OK
    Content-Type: text/html

    <!DOCTYPE html>
    <html>
      <head>
        <title>Raspberry Pi Pico Web Server</title>
        <script>
          function fetchData() {
              fetch('/data')
              .then(response => response.json())
              .then(data => {
                  document.getElementById("press").textContent = data.pressure;
                  document.getElementById("temp").textContent = data.temperature;
              })
              .catch(error => console.error('ERROR fetching data:', error));
          }
          setInterval(fetchData, 1000); // Fetch every 1s
        </script>
      </head>
      <body>
          <h1>Sensing values</h1>
          <h3>Pressure (Pa): <span id="press">Loading...</span></h3>
          <h3>Temperature (C): <span id="temp">Loading...</span></h3>
      </body>
    </html>
    """
    return str(html)

# define I2C connection and BMP
i2c = machine.I2C(id=1, sda=Pin(14), scl=Pin(15)) # id=channel
bmp = BMP280(i2c)

# accept connections + send HTTP response
while True:
    cl, addr = s.accept()
    print('[INFO] Client connected from', addr)
    
    # receive request
    request = cl.recv(1024).decode('utf-8')
    print('[INFO] Request:', request)
    
    if 'GET / ' in request:
        # gen default html with loading value
        response = generate_html()
    elif 'GET /data' in request:
        # gen default html with read/updated value
        data = {
            "pressure": bmp.pressure,
            "temperature": bmp.temperature
        }
        response = "HTTP/1.1 200 OK\nContent-Type: application/json\n\n" + json.dumps(data)
    else:
        response = "HTTP/1.1 404 Not Found\n\nERROR"

    # send the response to the client
    cl.send(response)
    
    # close connection
    cl.close()
