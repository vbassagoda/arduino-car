// WiFi library
//#include <WiFiS3.h>
#include "secrets.h"
WiFiUDP udp;

// connection to flask backend
int PORT = 12345;
char myPacket[255];
int dataLen;
String direction;
String response;

// Motor directions
#define IN1_PIN 5   // left forward
#define IN2_PIN 4   // left backward
#define IN3_PIN 3   // right forward
#define IN4_PIN 2   // right backward


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

  // Set direction pins to output for both motor   
  pinMode(IN1_PIN, OUTPUT);   
  pinMode(IN2_PIN, OUTPUT);   
  pinMode(IN3_PIN, OUTPUT);   
  pinMode(IN4_PIN, OUTPUT);
}

void loop() {
  delay(100); // wait before checking for new packets
  moveMotors(LOW, LOW, LOW, LOW);   // Both motors stop
  delay(200); // wait for motors to stop
  if (udp.parsePacket()) {
    // read direction provided by user
    dataLen = udp.available();
    udp.read(myPacket,255);
    myPacket[dataLen]=0;
    direction=String(myPacket);
    direction.trim();
    Serial.println("Received direction: "+direction);

    // move motors based on direction
    if (direction == "F") {
      moveMotors(HIGH, LOW, HIGH, LOW);  // Both motors forward
    } else if (direction == "R") {
      moveMotors(HIGH, LOW, LOW, LOW);  // Both motors forward
    } else if (direction == "L") {
      moveMotors(LOW, LOW, HIGH, LOW);  // Both motors forward
    }
    delay(100);

    // send response to flask backend
    response ="Here is your "+direction+" direction";  
    udp.beginPacket(udp.remoteIP(), udp.remotePort());
    udp.print(response);
    udp.endPacket();
    Serial.println("SENT: "+response);
  }
}

void moveMotors(int dir1, int dir2, int dir3, int dir4) {
  // Motor A
  digitalWrite(IN1_PIN, dir1);
  digitalWrite(IN2_PIN, dir2);
  // Motor B  
  digitalWrite(IN3_PIN, dir3);
  digitalWrite(IN4_PIN, dir4);
}