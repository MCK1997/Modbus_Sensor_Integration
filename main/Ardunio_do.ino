/*
   Arduino Code for Atlas Scientific Dissolved Oxygen (DO) Sensor
   This code communicates with the Atlas Scientific DO sensor using SoftwareSerial. 
   It requests DO readings and processes the response, extracting the numeric value.
   The data is then printed to the Serial Monitor.

   Pins:
   RX -> D12 (Arduino Nano)
   TX -> D11 (Arduino Nano)
*/

#include <SoftwareSerial.h>  // Include the SoftwareSerial library

#define rx 11  // RX pin (Arduino Nano D12)
#define tx 12  // TX pin (Arduino Nano D11)

SoftwareSerial myserial(rx, tx);  // Define SoftwareSerial for communication with the DO sensor

String sensorstring = "";  // String to hold the incoming data from the DO sensor
boolean sensor_string_complete = false;  // Flag to indicate if the full data string has been received

void setup() {
  Serial.begin(9600);  // Start the Serial Monitor at 9600 baud
  myserial.begin(9600);  // Start SoftwareSerial for the DO sensor at 9600 baud
  sensorstring.reserve(30);  // Reserve memory for incoming sensor data
  Serial.println("Atlas DO Sensor Test Started...");
}

void loop() {
  // Send the "r" command to request data from the sensor
  myserial.print("r\r");  // Send "r" command (read data)
  delay(1000);  // Delay for sensor to respond

  // Read data from the DO sensor
  while (myserial.available() > 0) {  // If data is available from the sensor
    char inchar = (char)myserial.read();  // Read the incoming character
    sensorstring += inchar;  // Append character to the sensorstring
    if (inchar == '\r') {  // If the incoming character is a carriage return
      sensor_string_complete = true;  // Mark that the full data string has been received
    }
  }

  // Process the sensor data once fully received
  if (sensor_string_complete) {
    // Check if the response contains "*OK" and extract only the value
    if (sensorstring.indexOf("*OK") == -1) {  // If "*OK" is not found, the string is just the sensor value
      Serial.println(sensorstring);  // Print the entire response to the Serial Monitor
    } else {
      String value = sensorstring.substring(0, sensorstring.indexOf("*OK"));  // Extract the value before "*OK"
      Serial.println(value);  // Print the extracted value to the Serial Monitor
    }
    sensorstring = "";  // Clear the sensorstring for the next reading
    sensor_string_complete = false;  // Reset the flag
  }

  delay(3000);  // Wait for 3 seconds before the next request
}
