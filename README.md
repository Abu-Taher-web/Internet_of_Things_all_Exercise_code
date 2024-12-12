# IoT Home Automation Project

This repository contains four exercises that demonstrate the process of setting up an IoT pipeline using the **Raspberry Pi Pico W** and various IoT technologies.

## Folder Structure

### Exercise 1: Reading Sensor Data
This exercise demonstrates how to read data from sensors (such as a DHT22) using the **Raspberry Pi Pico W**. The data is collected and preprocessed for further use in the pipeline.

### Exercise 2: Setting up Raspberry Pi Pico W as Server
In this exercise, the **Raspberry Pi Pico W** is configured as a simple web server to serve the sensor data collected in Exercise 1. This allows remote access to the data via a browser or network.

### Exercise 3: Pico W -> HiveMQ Pipeline Implementation
This exercise extends the server setup from Exercise 2, integrating the **Raspberry Pi Pico W** with **HiveMQ** to publish sensor data. The data is sent through the MQTT protocol for reliable, real-time communication.

### Exercise 4: Pico W -> HiveMQ -> Node-RED -> InfluxDB Implementation
The final exercise completes the IoT pipeline by connecting **HiveMQ** to **Node-RED**, which processes the data and stores it in **InfluxDB**. This setup enables real-time data visualization and long-term storage for analysis.

## Technologies Used
- Raspberry Pi Pico W
- DHT22 Sensor (or any other sensor)
- HiveMQ (MQTT Broker)
- Node-RED
- InfluxDB

This project demonstrates the end-to-end process of building an IoT system from sensor data acquisition to real-time monitoring and storage.
