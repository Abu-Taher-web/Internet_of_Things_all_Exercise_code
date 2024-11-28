import machine
from machine import Pin
import time
import socket
import wifi_connection1
from wifi_connection1 import connect_wifi

# Replace with your Wi-Fi credentials
SSID = "Taher"
PASSWORD = "50904426"

# Connect to Wi-Fi
ip_address = connect_wifi(SSID, PASSWORD)
print("IP Address:", ip_address)

# Setup GPIO for onboard LED control
led = Pin("LED", Pin.OUT)  # Onboard LED is connected to GPIO 25

# Web server setup
def handle_client(client):
    request = client.recv(1024)  # Receive HTTP request
    print("Request:", request)

    # Check for "GET /led/on" or "GET /led/off" to control onboard LED
    if b'GET /led/on' in request:
        led.on()  # Turn onboard LED on
    elif b'GET /led/off' in request:
        led.off()  # Turn onboard LED off

    # HTML content with button to control onboard LED
    response = """\
HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
    <head>
        <title>Pico W Server</title>
    </head>
    <body>
        <h1>Onboard LED Control</h1>
        <p>This is a web server running on Raspberry Pi Pico W.</p>
        <form method="GET" action="/led/on">
            <button type="submit">Turn LED On</button>
        </form>
        <form method="GET" action="/led/off">
            <button type="submit">Turn LED Off</button>
        </form>
    </body>
</html>
"""
    client.send(response)  # Send HTTP response
    client.close()  # Close connection

# Start the server
addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
server = socket.socket()
server.bind(addr)
server.listen(1)  # Only allow one client at a time
print("Server running on", addr)

while True:
    client, addr = server.accept()
    print("Client connected from:", addr)
    handle_client(client)
