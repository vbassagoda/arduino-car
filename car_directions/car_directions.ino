// WiFi library
#include <WiFiS3.h>
#include "secrets.h"
WiFiUDP udp;

// connection to flask backend
int PORT = 12345;
char myPacket[255];
int dataLen;
String direction;
String response;

// Motor pins
#define ENA_PIN 9   // Left motor enable (PWM for speed)
#define ENB_PIN 3   // Right motor enable (PWM for speed)
#define IN1_PIN 7   // Left forward
#define IN2_PIN 6   // Left backward
#define IN3_PIN 5   // Right forward
#define IN4_PIN 4   // Right backward

int motorSpeed = 127;  // Default 50% speed (0-255)


void setup() {
  Serial.begin(9600);
  
  // connect to wifi
  WiFi.begin(SSID, PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
  }
  delay(1000); // wait for wifi connection
  Serial.println(WiFi.localIP()); // add ip address in app.py
  
  // start udp server
  udp.begin(PORT);
  Serial.print("UDP Server started on port ");
  Serial.print(PORT);

  // Set direction pins to output for both motors
  pinMode(IN1_PIN, OUTPUT);
  pinMode(IN2_PIN, OUTPUT);
  pinMode(IN3_PIN, OUTPUT);
  pinMode(IN4_PIN, OUTPUT);

  // Set enable pins to output (PWM for speed control)
  pinMode(ENA_PIN, OUTPUT);
  pinMode(ENB_PIN, OUTPUT);
}

void loop() {
  delay(100); // wait before checking for new packets
  if (udp.parsePacket()) {
    // read direction provided by user
    dataLen = udp.available();
    udp.read(myPacket,255);
    myPacket[dataLen]=0;
    direction=String(myPacket);
    direction.trim();
    Serial.println("Received packet: "+direction);

    // parse speed from packet (format: "F,75")
    int commaIndex = direction.indexOf(',');
    // Check if a comma was found (-1 means not found)
    if (commaIndex != -1) {
      // Extract the speed value after the comma and convert to integer (e.g., "F,75" -> 75)
      int speedPercent = direction.substring(commaIndex + 1).toInt();
      // Convert speed from 0-100% range to 0-255 PWM range for motor control
      motorSpeed = map(speedPercent, 0, 100, 0, 255);
      // Keep only the direction letter before the comma (e.g., "F,75" -> "F")
      direction = direction.substring(0, commaIndex);
    }
    Serial.println("Direction: "+direction+" Speed: "+String(motorSpeed));

    // set motor speed
    setSpeed(motorSpeed);

    // move motors based on direction
    if (direction == "B") {
      moveMotors(HIGH, LOW, HIGH, LOW);  // Both motors forward
    } else if (direction == "F") {
      moveMotors(LOW, HIGH, LOW, HIGH);  // Both motors backward
    } else if (direction == "R") {
      moveMotors(LOW, LOW, LOW, HIGH);  // Left motor forward, right motor stop (turn right)
    } else if (direction == "L") {
      moveMotors(LOW, HIGH, LOW, LOW);  // Right motor forward, left motor stop (turn left)
    } else {
      Serial.println("Unknown direction: " + direction);
    }
    delay(100); // wait for motors to move
    stopMotors();

    // send response to flask backend
    response ="Here is your "+direction+" direction at speed "+String(motorSpeed);
    udp.beginPacket(udp.remoteIP(), udp.remotePort());
    udp.print(response);
    udp.endPacket();
    Serial.println("SENT: "+response);
  }
  else {
    Serial.println("No packet received");
    stopMotors();
  }
}

void stopMotors() {
  setSpeed(0);
  moveMotors(LOW, LOW, LOW, LOW);
  delay(200); // wait for motors to stop
}

void moveMotors(int dir1, int dir2, int dir3, int dir4) {
  // Motor A (left)
  digitalWrite(IN1_PIN, dir1);
  digitalWrite(IN2_PIN, dir2);
  // Motor B (right)
  digitalWrite(IN3_PIN, dir3);
  digitalWrite(IN4_PIN, dir4);
}

void setSpeed(int speed) {
  analogWrite(ENA_PIN, speed);
  analogWrite(ENB_PIN, speed);
}