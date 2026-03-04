const int trigPin = 10;  
const int echoPin = 11; 

float duration, distance;  

void setup() {
  // put your setup code here, to run once:
	pinMode(trigPin, OUTPUT);
	pinMode(echoPin, INPUT);
	Serial.begin(115200);
	
	// Wait for serial port to connect (useful for some boards)
	while (!Serial) {
		; // wait for serial port to connect
	}
	
	Serial.println("Ultrasonic Sensor Ready");
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(trigPin, LOW);
	
  delayMicroseconds(2);
	digitalWrite(trigPin, HIGH);
	delayMicroseconds(10);

	digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);  

  distance = (duration * 0.0343) / 2;

  Serial.print("Distance: "); 
	Serial.println(distance);
	delay(100);
}
