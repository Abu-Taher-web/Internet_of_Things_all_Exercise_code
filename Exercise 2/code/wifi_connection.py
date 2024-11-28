import network
import time

def connect_wifi(SSID, PASSWORD):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    # Wait for connection
    print("Connecting to Wi-Fi...")
    while not wlan.isconnected():
        time.sleep(1)

    print("Connected!")
    return wlan.ifconfig()[0]  # Return IP address
