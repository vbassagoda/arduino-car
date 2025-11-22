#include <WiFiS3.h>
#include "secrets.h"
WiFiUDP udp;
int PORT = 12345;
char myPacket[255];
int dataLen;
String color;
String response;
void setup() {
  Serial.begin(9600);
  Serial.print("Connecting to ");
  Serial.println(SSID);
  WiFi.begin(SSID, PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");
  Serial.println(WiFi.localIP());
  udp.begin(PORT);
  Serial.print("UDP Server started on port ");
  Serial.print(PORT);
  // put your setup code here, to run once:
}

void loop() {
  // put your main code here, to run repeatedly:
  if (udp.parsePacket()) {
    dataLen = udp.available();
    Serial.println(dataLen);
    udp.read(myPacket,255);
    Serial.println(myPacket);
    myPacket[dataLen]=0;
    Serial.println(myPacket);
    color=String(myPacket);
    color.trim();
    Serial.println("Received color: "+color);
    response ="Here is your "+color+" Marble";  
    udp.beginPacket(udp.remoteIP(), udp.remotePort());
    udp.print(response);
    udp.endPacket();
    Serial.println("SENT: "+response);
  }
}