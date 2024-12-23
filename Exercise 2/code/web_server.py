import socket
import wifi_connection
from wifi_connection import connect_wifi

# Replace with your Wi-Fi credentials
SSID = "Taher"
PASSWORD = "50904426"

# Connect to Wi-Fi
ip_address = connect_wifi(SSID, PASSWORD)
print("IP Address:", ip_address)

# Web server setup
def handle_client(client):
    request = client.recv(1024)  # Receive HTTP request
    print("Request:", request)

    # HTTP response
    response = """\
HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
    <head>
        <title>Pico W Server</title>
    </head>
    <body>
        <h1>Hello, World!</h1>
        <p>This is a web server running on Raspberry Pi Pico W.</p>
    </body>
</html>
"""
    client.send(response)  # Send HTTP response
    client.close()  # Close connection

# Start the server
addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
server = socket.socket()
server.bind(addr)
server.listen(1)
print("Server running on", addr)

while True:
    client, addr = server.accept()
    print("Client connected from:", addr)
    handle_client(client)
