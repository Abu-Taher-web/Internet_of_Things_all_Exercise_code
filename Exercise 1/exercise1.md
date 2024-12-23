# 📂  Exercise 1: Initial Setup

## 📖 Learning Outcome
To get familiar with Raspberry Pi Pico W and MicroPython by completing the following tasks:
- Setting up MicroPython on Raspberry Pi Pico W.
- Blinking the onboard LED with a timer delay.
- Exploring communication interfaces (e.g., testing BMP280 sensor with I2C).
- I used DHT22 for this exercise. BMP280 will be used letter

---

## 🛠️ Tasks to Complete
1. **Setup MicroPython on Raspberry Pi Pico W**:
   - Download and install MicroPython firmware.
   - Install and configure the Thonny IDE.
2. **Blink the Onboard LED**:
   - Write and upload a MicroPython script to blink the LED.
3. **Familiarize with Communication Interfaces**:
   - Test the BME280 sensor using the I2C interface.

---

## Implementation Steps

### 1. Setup MicroPython on Raspberry Pi Pico W
#### Download MicroPython Firmware
1. Visit the official [MicroPython website](https://micropython.org) and download the latest `.uf2` file for the Raspberry Pi Pico W.
2. Connect the Raspberry Pi Pico W to your computer while holding down the **BOOTSEL** button.
3. Release the **BOOTSEL** button after connecting. The Pico should appear as a USB drive on your computer.
4. Drag and drop the downloaded `.uf2` file onto the Pico's USB drive. The Pico will reboot automatically.

#### Install Thonny IDE
1. Download and install the [Thonny IDE](https://thonny.org) from its official website.
2. Open Thonny and navigate to `Tools > Options > Interpreter`.
3. Select **MicroPython (Raspberry Pi Pico)** as the interpreter.
4. Set the correct port (use the auto-detect port option if available).

<img src="Exercise 1/pin configuration/dht22_pin_configuration.png" width="500" />

---

### 2. Blink the Onboard LED with a Timer Delay
1. Write a MicroPython script in Thonny to blink the onboard LED:
   ```python
   import machine
   import time

   led = machine.Pin("LED", machine.Pin.OUT)
   while True:
       led.toggle()
       time.sleep(1)  # Adjust the delay as needed

### 3. Read Data from the DHT22 sensor
You can refer to the script for reading data from the DHT22 sensor [here]('Exercise 1/code/dht22_sensor_reading.py').

### ⚙️ Tools and Technologies
1. MicroPython
2. Thonny IDE
3. Raspberry Pi Pico W
4. DHT22 Sensor
