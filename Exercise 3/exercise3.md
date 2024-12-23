# Exercise 3: Data Transmission via MQTT

### Learning Outcome:
To get familiar with Wireless Data Transmission via MQTT.

### Todo:
- Read BMP280 data via I2C Interface in real-time.
- Connect Raspberry Pi Pico with Wi-Fi.
- Get familiar with MQTT Server on HiveMQ.
- Publish the data to MQTT server.

## Implementation

### 1. Read BMP280 Sensor Data via I2C Interface in Real-time
- Refer to the work done in Exercise 1 for this step (code available in the Exercise 1 folder).

### 2. Connect Raspberry Pi Pico with Wi-Fi
- **Write Script to Connect to Wi-Fi**:  
  - Use the `network` module to connect the Pico to your Wi-Fi network.
  - Configure the SSID and password for your Wi-Fi network.

- **Run the Script**:  
  - Save and run the script on the Pico to test and verify the connection.
  - Ensure the Pico connects to the Wi-Fi network successfully by checking for an IP address assignment.

### 3. Create an MQTT Server
For creating an MQTT server to publish and subscribe to data via topics, we have multiple options available:
- Install Mosquitto MQTT Broker.
- Utilize MQTT test client on AWS IoT Core.
- Create an MQTT Cloud server on HiveMQ (Cloud provided by AWS).

**Steps to Create an MQTT Cloud Server on HiveMQ**:
1. **Create Your Account on HiveMQ**:  
   - Go to the HiveMQ website.  
   - Click on **Start Free > Sign up FREE NOW (HiveMQ Cloud)**.  
   - Complete the sign-up process.

2. **Log In to Your Account**:  
   - Access the dashboard after logging in.

3. **Create MQTT Cloud Server**:  
   - Click the **⊕** symbol near the "Clusters" section on the left panel.  
   - Choose the **Free** option.  
   - Once created, the server details will be displayed.  
   - **Cluster URL**: This is the URL you will use later in your code.  
   
   ![Cluster Details Placeholder](path/to/cluster-image.png)

4. **Define/Create Credentials for Access**:  
   - Go to the **Access Management** tab.  
   - Specify the username and password for your cluster.  
   - Choose "Publish and Subscribe" in the permissions.  
   - Click **Create Credential**.  

   ![Access Management Placeholder](path/to/access-management-image.png)
### 4. Publish the Data to MQTT Server

- **Install Required Libraries**:  
  - Install the following libraries on your Pico board for MQTT setup:  
    - `micropython-umqtt.robust`  
    - `micropython-umqtt.simple`  

  **NOTE**:  
  If you encounter issues installing these libraries with the latest version of MicroPython, try using version **v1.21.0 (2023-10-05)** `.uf2` firmware. The latest version may have bugs and is missing some libraries, such as `ussl` and `uzlib`.

- **Write Script to Publish Data**:  
  - Create an MQTT client using the credentials for your server/cluster (URL, port, username, password, and SSL configurations).
  - Use the `.connect()` function to connect to the MQTT Cloud server.
  - Publish the sensor data to a specific topic at regular intervals using `.publish(topic, value)`.

- **Verify Data Publishing**:  
  - Go to the **Web Client** tab.  
  - Connect to your HiveMQ Cloud Cluster using your credentials (username, password).  
  - Click **Subscribe**:  
    - Use `#` to subscribe to all topics.  
    - Alternatively, type the specific topic name you want to subscribe to.  
  - Observe the published messages displayed on the screen.  

   ![Data Publishing Placeholder](path/to/data-publishing-image.png)

---

### What's Next?

In the next exercise session, we will utilize **Node-RED** to connect different nodes and servers for receiving and transmitting data.  

Stay tuned!
