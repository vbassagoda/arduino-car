// Motor Left
#define IN1_PIN 5   
#define IN2_PIN 4

// Motor Right
#define IN3_PIN 3
#define IN4_PIN 2

void setup() {
  // put your setup code here, to run once:
    Serial.begin(9600);   

	 // Set direction pins to output for both motor   
	 pinMode(IN1_PIN, OUTPUT);   
	 pinMode(IN2_PIN, OUTPUT);   
	 pinMode(IN3_PIN, OUTPUT);   
	 pinMode(IN4_PIN, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("Motors are stopped now");   
  
  delay(4000);
  Serial.println("Set direction FORWARD");
  moveMotors(HIGH, LOW, HIGH, LOW);  // Both motors forward
  delay(400);

  Serial.println("Turning motors off");
  moveMotors(LOW, LOW, LOW, LOW);   // Both motors stop

  delay(4000);
  Serial.println("Moving right");
  moveMotors(HIGH, LOW, LOW, LOW);
  delay(400);

  Serial.println("Turning motors off");
  moveMotors(LOW, LOW, LOW, LOW);

  delay(4000);
  Serial.println("Moving left");
  moveMotors(LOW, LOW, HIGH, LOW);
  delay(400);
  
  Serial.println("Turning motors off");
  moveMotors(LOW, LOW, LOW, LOW);
}

void moveMotors(int dir1, int dir2, int dir3, int dir4) {
  // Motor A
  digitalWrite(IN1_PIN, dir1);
  digitalWrite(IN2_PIN, dir2);
  // Motor B  
  digitalWrite(IN3_PIN, dir3);
  digitalWrite(IN4_PIN, dir4);
}


/*
void moveLeft(int dir1, int dir2) {
  // Motor A
  digitalWrite(IN1_PIN, dir1);
  digitalWrite(IN2_PIN, dir2);
  // Motor B  
  digitalWrite(IN3_PIN, dir2);
  digitalWrite(IN4_PIN, dir2);
}

void moveRight(int dir1, int dir2) {
  // Motor A
  digitalWrite(IN1_PIN, dir2);
  digitalWrite(IN2_PIN, dir2);
  // Motor B  
  digitalWrite(IN3_PIN, dir1);
  digitalWrite(IN4_PIN, dir2);
}
*/