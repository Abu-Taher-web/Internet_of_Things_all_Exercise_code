import socket
import network
import time
import machine
import dht
import json  # Import the json module to handle JSON responses

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

# Initialize the sensor
sensor = dht.DHT22(machine.Pin(2))

# Function to generate the HTML page
def generate_html():
    html = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>Raspberry Pi Pico Web Server</title>
            <script>
              function fetchData() {{
                  fetch('/data')  // Fetch data from /data endpoint
                  .then(response => response.json())  // Parse the JSON response
                  .then(data => {{
                      document.getElementById("hum").textContent = data.humidity;
                      document.getElementById("temp").textContent = data.temperature;
                  }})
                  .catch(error => console.error('ERROR fetching data:', error));
              }}
              setInterval(fetchData, 1000); // Fetch every 1 second
            </script>
        </head>
        <body>
            <h1>Sensing values</h1>
            <h3>Humidity: <span id="hum">Loading...</span></h3>
            <h3>Temperature (C): <span id="temp">Loading...</span></h3>
        </body>
    </html>
    """
    return html

# Function to handle incoming client requests
def handle_client(client):
    try:
        request = client.recv(1024)  # Receive HTTP request
        print("Request:", request)

        # Parse the HTTP request (simple approach)
        request_path = str(request).split(" ")[1]  # Get the requested path
        
        # If the path is /data, send JSON response with sensor data
        if request_path == "/data":
            sensor.measure()  # Trigger the sensor reading
            temperature = sensor.temperature()  # Get temperature
            humidity = sensor.humidity()  # Get humidity
            data = {"temperature": temperature, "humidity": humidity}
            response = json.dumps(data)  # Convert data to JSON
            client.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n" + response)
        else:
            # Otherwise, serve the HTML page
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
            response += generate_html()  # HTML content
            client.sendall(response)  # Send the HTML response

    except Exception as e:
        print("Error:", e)
    finally:
        client.close()  # Ensure the connection is closed

# Start the server
addr = socket.getaddrinfo("0.0.0.0", 8080)[0][-1]
server = socket.socket()
server.bind(addr)
server.listen(1)  # Listen for incoming connections
print("Server running on", addr)

# Main loop to handle incoming connections
while True:
    client, addr = server.accept()
    print("Client connected from:", addr)
    handle_client(client)

