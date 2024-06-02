int smokeSensorPin = A0;  // Analog pin to which the smoke sensor is connected

void setup() {
  Serial.begin(9600);  // Initialize serial communication
}

void loop() {
  // Read the analog value from the smoke sensor
  int sensorValue = analogRead(smokeSensorPin);

  // Print the raw sensor value to the serial monitor
  Serial.print("Co2 Sensor Value: ");
  Serial.println(sensorValue);

  // Wait for a short time before reading again
  delay(1000);
}
