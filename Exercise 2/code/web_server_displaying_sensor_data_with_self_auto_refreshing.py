import socket
import network
import time
import machine
import dht

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

SSID = "Taher"
PASSWORD = "50904426"
wlan.connect(SSID, PASSWORD)

# Wait for the connection to be established
while not wlan.isconnected():
    time.sleep(1)

# Print the IP address of the Pico W
ip_address = wlan.ifconfig()[0]
print("IP Address:", ip_address)

# Measure sensor data
sensor = dht.DHT22(machine.Pin(2))

def generate_html(temperature, humidity):
    # Generate HTML content (without HTTP headers)
    html = f"""\
    <!DOCTYPE html>
    <html>
    <head>
        <title>Raspberry Pi Pico Web Server</title>
        <meta http-equiv="refresh" content="2">
    </head>
    <body>
        <h1>Sensing values</h1>
        <h3>Humidity: {humidity}%</h3>
        <h3>Temperature (C): {temperature}</h3>
    </body>
    </html>
    """
    return html

# Web server setup
def handle_client(client):
    try:
        request = client.recv(1024)  # Receive HTTP request
        print("Request:", request)

        # Read the DHT22 sensor
        sensor.measure()
        temperature = sensor.temperature()  # Get temperature
        humidity = sensor.humidity()  # Get humidity

        # Generate the HTTP response
        response = "HTTP/1.1 200 OK\r\n" \
                   "Content-Type: text/html\r\n" \
                   "Connection: close\r\n\r\n"  # HTTP headers
        response += generate_html(temperature, humidity)  # Append HTML body

        client.sendall(response)  # Send the complete HTTP response
    except Exception as e:
        print("Error:", e)
    finally:
        client.close()  # Ensure the connection is closed

# Start the server
addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
server = socket.socket()
server.bind(addr)
server.listen(1)  # Listen for incoming connections
print("Server running on", addr)

while True:
    client, addr = server.accept()
    print("Client connected from:", addr)
    handle_client(client)

