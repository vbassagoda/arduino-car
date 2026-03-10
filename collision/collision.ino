// WiFi library
#include <WiFiS3.h>
#include "secrets.h"
WiFiUDP udp;

// connection to flask backend
int PORT_COLLISION = 12346;
char myPacketcollision[255];
String collision_response;

const int trigPin = 10;  
const int echoPin = 11; 

void setup() {
  // put your setup code here, to run once:
	pinMode(trigPin, OUTPUT);
	pinMode(echoPin, INPUT);
	Serial.begin(115200);
	
	// Wait for serial port to connect (useful for some boards)
	while (!Serial) {
		; // wait for serial port to connect
	}

  // connect to wifi
  WiFi.begin(SSID, PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
  }
  delay(1000); // wait for wifi connection
  Serial.println(WiFi.localIP()); // add ip address in app.py
  
  // start udp server
  udp.begin(PORT_COLLISION);
  Serial.print("UDP Server started on port ");
  Serial.print(PORT_COLLISION);
  Serial.println("Collision Sensor Ready");
}

float measureDistance() {
	float duration, distance;
	digitalWrite(trigPin, LOW);
	delayMicroseconds(2);
	digitalWrite(trigPin, HIGH);
	delayMicroseconds(10);
	digitalWrite(trigPin, LOW);
	duration = pulseIn(echoPin, HIGH);  
	distance = (duration * 0.0343) / 2;
	
	return distance;
}

void loop() {
	int packetSize = udp.parsePacket();
	if (packetSize) {
	  int len = udp.read(myPacketcollision, 254);
	  if (len > 0) {
		myPacketcollision[len] = '\0';
		String msg = String(myPacketcollision);
		if (msg == "ASK") {
		  float distance = measureDistance();
		  String response = String(distance);
		  udp.beginPacket(udp.remoteIP(), udp.remotePort());
		  udp.print(response);
		  udp.endPacket();
		  Serial.print("Distance: ");
		  Serial.println(distance);
		}
	  }
	}
	delay(10);
}

