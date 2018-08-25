#include <Servo.h>

// Servo variables
Servo myservo;
int control_pin = 6;
int standard_pos = 0;

// Connection variable
int incoming;

// Printing variable
int flag = 0;

// is_transaction variable
bool received_transaction = false;


// Ultra sonic pins
const int trigPin = 9;
const int echoPin = 10;
// Ultra sonic variables
long duration;
int distance;


void setup() {
  myservo.attach(control_pin); // Attach Servo to pin
  myservo.write(standard_pos); // Set starting position
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  Serial.begin(9600);
}

void loop() { 
    // Clears the trigPin
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    // Sets the trigPin on HIGH state for 10 micro seconds
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    // Reads the echoPin, returns the sound wave travel time in microseconds
    duration = pulseIn(echoPin, HIGH);
    distance = duration*0.034/2; // Calculating the distance (in cm)
    //Serial.println(distance);
  if (Serial.available() > 0) {
    incoming = Serial.read(); // read Serial input
    flag = 0;    
    //detectInput();
    //handlePinOutputs();
  }
  if (distance < 25) {
        //Serial.print("Distance: ");
        Serial.print(1); // Send 1 to PC serial port
        if(flag == 0){
          //Serial.println("Car detected!");
          flag=1;
        }
    }

    if (incoming == 'O') {
       if(flag == 0){
          //Serial.println("Barrier: moving");
          flag=1;
        }

        // OPENING
        for(pos = 0; pos<=90; pos++) {    // goes from 0 degrees to 90 degrees                             
          myservo.write(pos);              // move to each position within range with short delay 
          delay(100);   
        }  
        delay(10000); // wait after opening to let car pass
        // CLOSING
        for(pos = 90; pos>=0; pos--) {    // goes from 90 degrees to 0 degrees                                
          myservo.write(pos);              // move to each position within range with short delay
          delay(100);   
        }  
        myservo.write(standard_pos);              // move servo back to starting position, wait for next car
        delay(10000); // wait there
        }
    // if no opening signal was sent
    else {
        myservo.write(standard_pos);              // tell servo to go to position in variable 'pos' 
        if(flag == 0){
          //Serial.println("Barrier: not moving");
          flag=1;
        }
    }
}
