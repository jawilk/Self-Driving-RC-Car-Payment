#include <AFMotor.h>
//#include <SoftwareSerial.h>

// Motor pins
AF_DCMotor motor_forward_backward(1);
AF_DCMotor motor_left_right(2);

// Motor speed variables; adjust according to own motor type/battery strength
int speed_forward_backward = 130;
int speed_left_right = 145;

// Ultra sonic pins
const int trigPin = 9;
const int echoPin = 10;
// Ultra sonic variables
long duration;
int distance;

// Serial communication variables
char incoming;

// Printing logic variable
int flag = 0;


void setup() {
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  Serial.begin(9600);
}

void loop() {
   // Clears the trigPin
   digitalWrite(trigPin, LOW);
   delayMicroseconds(2);
   digitalWrite(trigPin, HIGH);
   delayMicroseconds(10); // Sets the trigPin on HIGH state for 10 micro seconds
   digitalWrite(trigPin, LOW);

   duration = pulseIn(echoPin, HIGH); // Reads the echoPin, returns the sound wave travel time in microseconds
   distance = duration*0.034/2; // Calculating the distance (in cm)
   
   if(Serial.available() > 0){ // Read incoming serial(bluetooth) connection
      incoming = Serial.read();     
      Serial.print("Received: "); 
      Serial.println(incoming);
      flag = 0; // Set printing flag to 0
   }
   /***************************Speed*****************************/
   if (incoming == '0') {
      speed_forward_backward = 100;
      speed_left_right = 110;
      if(flag == 0){
          Serial.print("Motor: ");
          Serial.println(speed_forward_backward);
          flag=1;
    }}
   else if (incoming == '1') {
      speed_forward_backward = 120;
      speed_left_right = 130;
      if(flag == 0){
          Serial.print("Motor: ");
          Serial.println(speed_forward_backward);
          flag=1;
    }
    }
   else if (incoming == '2') {
      speed_forward_backward = 150;
      speed_left_right = 165;
      if(flag == 0){
          Serial.print("Motor: ");
          Serial.println(speed_forward_backward);
          flag=1;
    }
    }
    else if (incoming == '3') {
      speed_forward_backward = 175;
      speed_left_right = 185;
      if(flag == 0){
          Serial.print("Motor: ");
          Serial.println(speed_forward_backward);
          flag=1;
    }
    }
    else if (incoming == '4') {
      speed_forward_backward = 200;
      speed_left_right = 215;
      if(flag == 0){
          Serial.print("Motor: ");
          Serial.println(speed_forward_backward);
          flag=1;
    }
    }
    else if (incoming == '5') {
      speed_forward_backward = 225;
      speed_left_right = 235;
      if(flag == 0){
          Serial.print("Motor: ");
          Serial.println(speed_forward_backward);
          flag=1;
    }
    }
    else if (incoming == '6') {
      speed_forward_backward = 255;
      speed_left_right = 255;
      if(flag == 0){
          Serial.print("Motor: ");
          Serial.println(speed_forward_backward);
          flag=1;
     }
    }
  /***********************Forward****************************/
  //If incoming equals 'W', car will move forward !!(if ultra sonic distance > 15)!! 
    if (incoming == 'W') {
      if (distance > 15) {
        motor_left_right.setSpeed(0);
        motor_forward_backward.run(FORWARD);
        motor_forward_backward.setSpeed(speed_forward_backward);
        if(flag == 0){
          Serial.println("Motor: forward");
          flag=1;
          }
      }
      else {
        Serial.print("Distance: ");
        Serial.println(distance);
        motor_forward_backward.setSpeed(0);
        motor_left_right.setSpeed(0);
        if(flag == 0){
          Serial.println("Motor: stop");
          flag=1;
          }
      }
   }
  /**********************Forward Left************************/
  //If incoming equals 'Q', car will go forward left !!(if ultra sonic distance > 15)!!
    else if (incoming == 'Q') {
      if (distance > 15) {
        motor_left_right.run(FORWARD);
        motor_left_right.setSpeed(255);
        motor_forward_backward.run(FORWARD);
        motor_forward_backward.setSpeed(speed_left_right);
        if(flag == 0){
          Serial.println("Motor: forward left");
          flag=1;
    }}
     else {
        Serial.print("Distance: ");
        Serial.println(distance);
        motor_forward_backward.setSpeed(0);
        motor_left_right.setSpeed(0);
        if(flag == 0){
          Serial.println("Motor: stop");
          flag=1;
        }
    }
   }
  /**********************Forward Right************************/
  //If incoming equals 'E', car will go forward right !!(if ultra sonic distance > 15)!!
    else if (incoming == 'E') {
      if (distance > 15) {
        motor_left_right.run(BACKWARD);
        motor_left_right.setSpeed(255);
        motor_forward_backward.run(FORWARD);
        motor_forward_backward.setSpeed(speed_left_right);
        
        if(flag == 0){
          Serial.println("Motor: forward right");
          flag=1;
    }}
    else {
        Serial.print("Distance: ");
        Serial.println(distance);
        motor_forward_backward.setSpeed(0);
        motor_left_right.setSpeed(0);
        if(flag == 0){
          Serial.println("Motor: stop");
          flag=1;
        }
    }    
   }
  /***********************Backward****************************/
  //If s is equal with letter 'B', car will go backward
    else if (incoming == 'T') {
        motor_left_right.setSpeed(0);
        motor_forward_backward.run(BACKWARD);
        motor_forward_backward.setSpeed(speed_forward_backward);
        if(flag == 0){
          Serial.println("Motor: backward");
          flag=1;
        }
    }
  /**********************Backward Left************************/
  //If incoming equals 'R', car will go backward left
    else if (incoming == 'R') {
        motor_left_right.run(FORWARD);
        motor_left_right.setSpeed(255);
        motor_forward_backward.run(BACKWARD);
        motor_forward_backward.setSpeed(speed_left_right);
        if(flag == 0){
          Serial.println("Motor: backward left");
          flag=1;
        }
   }
  /**********************Backward Right************************/
  //If incoming equals 'F', car will go backward right
    else if (incoming == 'F') {
        motor_left_right.run(BACKWARD);
        motor_left_right.setSpeed(255);
        motor_forward_backward.run(BACKWARD);
        motor_forward_backward.setSpeed(speed_left_right);
        if(flag == 0){
          Serial.println("Motor: backward right");
          flag=1;
        }
    }
  /***************************Left*****************************/
  //If incoming equals 'J', wheels will turn left
    else if (incoming == 'J') {
        motor_forward_backward.setSpeed(0);
        motor_left_right.run(FORWARD);
        motor_left_right.setSpeed(255);
        if(flag == 0){
          Serial.println("Motor: left");
          flag=1;
        }
    }
  /***************************Right*****************************/
  //If incoming equals 'I', wheels will turn right
    else if (incoming == 'I') {
        motor_forward_backward.setSpeed(0);
        motor_left_right.run(BACKWARD);
        motor_left_right.setSpeed(255);
        if(flag == 0){
          Serial.println("Motor: right");
          flag=1;
        }
    }
  /************************Stop*****************************/
  //If incoming equals 'O', car will stop
    else if (incoming == 'O') {
        motor_forward_backward.setSpeed(0);
        motor_left_right.setSpeed(0);
        if(flag == 0){
          Serial.println("Motor: stop");
          flag=1;
        }
    }
}
