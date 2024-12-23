## Exercise 4

### Learning Outcome
Students will learn to configure Node-RED for data integration and utilize databases like InfluxDB and MongoDB for efficient data storage and management in IoT systems.

### Tasks to Do
- **Setup Node-RED** to connect data received from the MQTT server to a database.
- Utilize databases (InfluxDB) to store data from the server.
- Implement output control.

### Node-RED
Node-RED is a programming tool used for wiring together hardware devices, APIs, and online services through flow-based programming. It is highly effective for IoT-based projects. In this exercise, we will:
1. Acquire data published on the MQTT cloud server using Node-RED.
2. Store the data into an InfluxDB instance on a local machine.

<img src="https://github.com/Abu-Taher-web/Internet_of_Things_all_Exercise_code/blob/main/Exercise%204/Images/node-red.png" alt="Node-RED Flow Example" />


## Implementation Steps

### Setup Node-RED for Connecting Data from MQTT Server to InfluxDB

1. **Install Node-RED**:
   - Ensure Node.js is installed on your system. Verify using:
     ```bash
     node -v
     ```
   - Open the command prompt as an administrator and run:
     ```bash
     npm install -g --unsafe-perm node-red
     ```
   - Start Node-RED:
     ```bash
     node-red
     ```
   - Open the Node-RED dashboard in your browser (usually at [http://localhost:1880](http://localhost:1880)).

2. **Install Required Packages**:
   - Navigate to the menu (top-right corner) > **Manage Palette** > **Install** tab.
   - Install the required package for InfluxDB using:
     ```bash
     npm install node-red-contrib-influxdb
     ```

### InfluxDB Installation on Local Machine

1. **Download and Install InfluxDB**:
   - Follow instructions on the official [InfluxDB site](https://www.influxdata.com/) to download the required .rar file.
   - Extract the files to `C:\Program Files\InfluxData\` using:
     ```powershell
     Expand-Archive -Path "E:\Downloads\influxdb2-2.7.10-windows.zip" -DestinationPath "C:\Program Files\InfluxData\" -Force
     ```
   - Navigate to the directory and run:
     ```bash
     .\influxd.exe
     ```

2. **Access and Configure InfluxDB**:
   - Open [http://127.0.0.1:8086/](http://127.0.0.1:8086/) in your browser.
   - Complete the initial setup, create a bucket for collecting data, and save the API token. 
   - If the setup page does not appear:
     - Go to **Load Data** > **Buckets** to create a bucket (e.g., "Oulu").
     - Navigate to **API Tokens** and create an all-access token.

### Implementation in Node-RED

1. **Configure MQTT Input**:
   - Drag an MQTT input node onto the workspace.
   - Configure it with the following:
     - **Server settings**: Add details for your HiveMQ Cloud server.
     - **Topic**: Set the topic where sensor data is published.

2. **Setup Function Node to Process Data**:
   - Drag a function node onto the workspace and connect it to the MQTT input node.
   - Use the following JavaScript code to format the incoming data:
    ## Function Node Code Example

In this part, we process the incoming MQTT messages and map them to the correct fields and measurements for InfluxDB. Here's the JavaScript code used in the Node-RED function node:

```javascript
let newMsg = {}; // Initialize a new message object

// Ensure msg.topic exists
if (!msg.topic) {
    node.error("Topic is undefined. Check MQTT configuration.");
    return null; // Stop processing this message
}

// Map topics to field names and measurement names for InfluxDB
let topicMapping = {
    "room1/temperature1": { measurement: "room1", field: "Temperature" },
    "room1/humidity": { measurement: "room1", field: "Humidity" },
    "room2/temperature": { measurement: "room2", field: "Temperature" },
    "room2/humidity": { measurement: "room2", field: "Humidity" }
};

// Extract topic and payload
let topic = msg.topic;
let payloadValue = parseFloat(msg.payload); // Convert payload to float

// Check if topic exists in the mapping
if (topic in topicMapping) {
    let mapped = topicMapping[topic];
    
    // Prepare the new payload structure for InfluxDB
    newMsg.payload = {
        measurement: mapped.measurement, // Measurement name (e.g., room1, room2)
        fields: { 
            [mapped.field]: payloadValue // Dynamic field based on topic (e.g., Temperature, Humidity)
        },
        "Temperature1": payloadValue,
        tags: { location: mapped.measurement }, // Optional: Add tags if necessary (e.g., location)
        timestamp: new Date().toISOString() // Optional: Use the current timestamp
    };
} else {
    // Handle unexpected topics
    node.error(`Unhandled topic: ${topic}`);
    return null; // Stop processing this message
}

// Return the processed message
return newMsg;
```
   - Use a debug node to monitor the published data.

3. **Connect to InfluxDB**:
   - Drag an InfluxDB output node onto the canvas.
   - Configure the node with:
     - **Server settings**: Provide the InfluxDB URL, token, and bucket details.
     - **Measurement**: Specify the measurement name (e.g., "Temp").

4. **Visualize Data in InfluxDB**:
   - Go to **Data Explorer** in InfluxDB.
   - Select the bucket and measurement to view the graph of incoming measurements.

<img src="https://github.com/Abu-Taher-web/Internet_of_Things_all_Exercise_code/blob/main/Exercise%204/Images/influxdb.png" alt="Node-RED Flow Example" />


## Controlling the Output on Raspberry Pi Pico W

### Implementation Diagram
1. **Inject Node**: Used to periodically trigger data retrieval.

2. **Data In Node**: Fetches the latest temperature data from the database using an InfluxDB input node. It queries the InfluxDB bucket to retrieve the most recent measurement.

3. **Function Node**: Processes the temperature data and determines whether the output should be "ON" or "OFF" based on a predefined threshold.

4. **Control Node**: Publishes the "ON"/"OFF" message to a specific topic (e.g., `picow/Control`) via an MQTT output node, which is then used to control the Raspberry Pi Pico W.

5. **Debug Nodes**: Added at multiple stages to monitor the processed data and ensure accurate values are being transmitted.

6. **Microcontroller Action**: The Raspberry Pi Pico W subscribes to the `picow/Control` topic and takes appropriate action (e.g., turning an LED on or off) based on the received control signals.

### Final Testing
- Verify that control signals from Node-RED are correctly received and acted upon by the Raspberry Pi Pico W.
- Ensure the system responds accurately to changing data values, meeting the specified threshold conditions.

<img src="https://github.com/Abu-Taher-web/Internet_of_Things_all_Exercise_code/blob/main/Exercise%204/Images/grafana.png" alt="Node-RED Flow Example" />
