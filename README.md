Atlas Scientific Dissolved Oxygen (DO) Sensor Integration
This repository contains code for interfacing with the Atlas Scientific Dissolved Oxygen (DO) sensor using an Arduino Nano and a Raspberry Pi (Mycodo platform) via RS485 communication. Both the Arduino and Mycodo code request data from the sensor and handle the response, extracting and logging the DO values.

Arduino Code

Description
The Arduino code communicates with the Atlas Scientific DO sensor using the SoftwareSerial library. It sends a request for the dissolved oxygen value, processes the response, and prints the value to the serial monitor.

Features
Utilizes SoftwareSerial for serial communication with the DO sensor.
Sends the r command to request the DO value from the sensor.
Parses the response and extracts the numeric DO value.

Setup
RX pin of the DO sensor connected to D12 (Arduino Nano).
TX pin of the DO sensor connected to D11 (Arduino Nano).
Ensure the baud rate for both the serial monitor and sensor communication is set to 9600.

Usage
Upload the provided code to your Arduino Nano, open the Serial Monitor, and observe the dissolved oxygen values being printed every 3 seconds.

Mycodo Python Code (Raspberry Pi)
Description
The Python code is designed to be integrated into the Mycodo platform to read dissolved oxygen values from the Atlas Scientific DO sensor via RS485 communication. It uses the RPi.GPIO and pySerial libraries for GPIO and serial control.

Features
Sends an r command to the DO sensor to request data via RS485.
Handles RS485 direction control using GPIO pin 4.
Extracts the DO value and logs it into the Mycodo database.

Setup
Connect the RS485 module to GPIO4 on the Raspberry Pi for direction control.
Ensure RPi.GPIO and pySerial libraries are installed in the Mycodo environment.
Use the provided Mycodo input template to integrate and store the DO values.

Usage
Add the Python code as a custom input in Mycodo, configure the necessary channels and units, and start receiving real-time dissolved oxygen data.

License
MIT License
