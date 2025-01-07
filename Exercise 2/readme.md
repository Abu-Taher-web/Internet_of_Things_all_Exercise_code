# Exercise 2: Wi-Fi and Wireless Data Transmission

### Learning Outcome:
To get familiar with wireless data transmission.

### Todo:
- Setup HTTP Web Server on Raspberry Pi Pico
- Interact with on-board LED via web interface
- Display real-time BMP values on web interface

## Implementation:

### 1. Setup HTTP Web Server on Pico W

**NOTE**:
- If you face issues connecting the Pico to Wi-Fi (at home or university), it may be due to router settings and configuration. 
- It is recommended to create a hotspot from your mobile and then connect your computer to the same Wi-Fi.

**Steps**:

1. **Connect Pico W to Wi-Fi**  
   - Import the necessary libraries: `network`, `socket`.
   - Define SSID (Wi-Fi name) and password.
   - Define WLAN with `network.WLAN(network.STA_IF)`.
   - Activate WLAN and connect with SSID and password.
   - Check the connection status with the `status()` function. If connected successfully, print the assigned IP for the Pico W.  
   (You can test the connection using ping or telnet commands.)

2. **Setup Socket and Listen**  
   - Define the address to make the socket listen on port 80 for all network interfaces (`0.0.0.0`).
   - Open socket, bind to the address, and start listening.

3. **Setup HTTP Web Server**  
   - Use a while loop to check for client connections.
   - Receive requests and send a response to the client.
   - Example response (HTML):

4. **Close Connection**

5. **Run and Test**  
   - Sample output on the webpage.
