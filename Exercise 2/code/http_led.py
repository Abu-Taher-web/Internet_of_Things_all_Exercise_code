from machine import Pin
import network
import socket
import time
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


# define LED
led = Pin("LED", Pin.OUT)

# generate html
def generate_html(status):
    html = f"""\
    HTTP/1.1 200 OK
    Content-Type: text/html

    <!DOCTYPE html>
    <html>
      <head><title>Raspberry Pi Pico Web Server</title></head>
      <body>
          <h1>TOGGLE LED</h1>
          <h2>LED is now {status}</h2>
          <p><a href='/toggle'><button style="background-color: #ed9418; padding: 20px; font-size:20px">Toggle</button></a></p>
      </body>
    </html>
    """
    return str(html)

# accept connections + send HTTP response
while True:
    cl, addr = s.accept()
    print('[INFO] Client connected from', addr)
    
    # receive request
    request = cl.recv(1024)
    print('[INFO] Request:', request)
    
    # get led status
    led_status = led.value() # 0=OFF/1=ON
    
    
    if "toggle" in str(request):
        if led_status: # ON
            led.off()
            led_status = 0
        else:
            led.on()
            led_status = 1
    status_char = "OFF" if led_status == 0 else "ON"
    
    response = generate_html(status_char)
    
    # send the response to the client
    cl.send(response)
    
    # close connection
    cl.close()  

