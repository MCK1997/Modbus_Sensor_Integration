# Mycodo RS485 and pH Sensor Input
# This code is designed for integrating an RS485-based DO sensor with Mycodo. It communicates with the sensor via RS485, retrieves the pH value, and returns it for Mycodo's data logging. The code uses RPi.GPIO for GPIO control and pySerial for RS485 communication.

import serial
import time
import RPi.GPIO as GPIO
import copy
from mycodo.inputs.base_input import AbstractInput

# RS485 Direction Control Pin
RS485_DE_RE_PIN = 4

# Setup GPIO for RS485 communication
def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RS485_DE_RE_PIN, GPIO.OUT)
    GPIO.output(RS485_DE_RE_PIN, GPIO.LOW)  # Start in listening mode

# Function to manage serial communication with RS485
def data():
    setup_gpio()  # Set up the GPIO for RS485 communication
    
    # Initialize serial communication
    try:
        ser = serial.Serial(
            port='/dev/serial0',  # Use the correct serial port
            baudrate=9600,        # Adjust the baudrate for the RS485 communication
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
    except serial.SerialException as e:
        print(f"Failed to connect to serial port: {e}")
        return None

    # Function to send a request to the sensor
    def send_request(command):
        full_command = f'{command}\n'
        GPIO.output(RS485_DE_RE_PIN, GPIO.HIGH)  # Switch to transmit mode
        time.sleep(0.05)
        ser.write(full_command.encode('utf-8'))  # Send the command
        time.sleep(0.05)
        GPIO.output(RS485_DE_RE_PIN, GPIO.LOW)  # Switch back to listening mode

    # Function to receive the response from the sensor
    def receive_response():
        timeout = time.time() + 2  # 2-second timeout
        response = ''
        while True:
            if ser.in_waiting > 0:
                try:
                    data = ser.readline().decode('utf-8', errors='ignore').strip()
                    if data.isprintable():
                        return data
                except UnicodeDecodeError:
                    print("Received non-UTF-8 data, skipping...")
            if time.time() > timeout:
                print("Response timeout.")
                break
        return None

    # Send the command to the sensor
    send_request("r")  # 'r' command for requesting sensor data

    # Receive the response
    response = receive_response()
    ser.close()
    GPIO.cleanup()

    return response

# Mycodo Input Implementation
measurements_dict = {0: {"measurement": "ion_concentration", "unit": "pH"}}  # 'pH' as unit

INPUT_INFORMATION = {
    "input_name_unique": "Test_RS_PH_Sensor",
    "input_manufacturer": "Ceket_Development",
    "input_name": "CKT460",
    "input_library": "RPi.GPIO",
    "measurements_name": "Ion Concentration",
    "measurements_dict": measurements_dict,
    "url_manufacturer": "https://www.microchip.com/",
    "url_datasheet": "http://ww1.microchip.com/",
    "url_product_purchase": "https://www.adafruit.com/",
    "dependencies_module": [('pip-pypi', 'RPi.GPIO', 'RPi.GPIO')],
    "interfaces": ["I2C"],
    "options_enabled": ["period", "pre_output"],
    "options_disabled": ["interface"],
}


class InputModule(AbstractInput):
    def __init__(self, input_dev, testing=False):
        super(InputModule, self).__init__(input_dev, testing=testing, name=__name__)
        if not testing:
            self.initialize_input()

    def initialize_input(self):
        self.logger.debug("Initialization of RS485 Input completed.")

    def get_measurement(self):
        self.return_dict = copy.deepcopy(measurements_dict)
        try:
            # Fetch the sensor data using the 'data()' function
            response = data()
            if response:
                self.logger.debug(f"Received response: {response}")
                try:
                    # Only extract the numeric value, assuming no additional strings like "*OK"
                    response_value = float(response)
                    self.value_set(0, response_value)
                except ValueError:
                    self.logger.debug("Failed to convert the response to float.")
                    return None
            else:
                self.logger.debug("No valid response received.")
            return self.return_dict
        except Exception as msg:
            self.logger.exception(f"Input read failure: {msg}")
            return None
