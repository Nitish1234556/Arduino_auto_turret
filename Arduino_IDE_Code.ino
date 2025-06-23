#include <Servo.h>

// Define pin numbers
const int laserPin = 10;     // Pin for laser control
const int servoXPin = 9;     // Pin for horizontal (X-axis ) servo
const int servoYPin = 11;    // Pin for vertical (Y-axis) servo

// Create servo objects for X and Y axes
Servo servoX;
Servo servoY;

void setup() {
    Serial.begin(9600);               // Initialize serial communication
    servoX.attach(servoXPin);         // Attach horizontal servo to pin 9
    servoY.attach(servoYPin);         // Attach vertical servo to pin 11
    pinMode(laserPin, OUTPUT);        // Set laser pin as output
    digitalWrite(laserPin, LOW);      // Ensure laser is off initially
}

void loop() {
    if (Serial.available() > 0) {
        String input = Serial.readStringUntil('\n'); // Read incoming data
        Serial.println("Received: " + input);        // Debug print

        int commaIndex = input.indexOf(',');
        if (commaIndex > 0) {
            int centerX = input.substring(0, commaIndex).toInt(); // Parse X coordinate
            int centerY = input.substring(commaIndex + 1).toInt(); // Parse Y coordinate

            // Check for the command to turn off the laser
            if (centerX == 0 && centerY == 0) {
                // Turn off the laser
                digitalWrite(laserPin, LOW);
                Serial.println("Laser OFF");  // Debug print
            } else {
                // Map the X coordinate (0 to 1200) to servo angles (0 to 120 degrees)
                int posX = map(centerX, 0, 1300, 0, 120);  

                // Map the Y coordinate (0 to 700) to servo angles (160 to 85 degrees)
                int posY = map(centerY, 0, 700, 130, 60);

                // Move servos to the new positions
                servoX.write(posX);
                servoY.write(posY);

                // Turn on the laser
                digitalWrite(laserPin, HIGH);
                Serial.println("Laser ON");  // Debug print

                // Use a non-blocking timer for the 1-second delay
                unsigned long startTime = millis();  // Record the start time
                while (millis() - startTime < 1000) {
                    // Keep the laser on for 1 second without blocking other operations
                }

                // Turn off the laser after 1 second
                digitalWrite(laserPin, LOW);
                Serial.println("Laser OFF");  // Debug print
            }
        }
    }
}