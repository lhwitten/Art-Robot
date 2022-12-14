// test servo motor lift / lower pen
// Include the Servo library 
#include <Servo.h> 
// Declare the Servo pin 
int servoPin = 9; 
// Create a servo object 
Servo Servo1; 
int initial_pos = 90;
int step = 20;
void setup() { 
  Serial.begin(9600);
   // We need to attach the servo to the used pin number 
   Servo1.attach(servoPin); 
   Servo1.write(initial_pos);
}
void loop(){ 
   // Make servo go to 100 degrees (right pen lowered)
   Servo1.write(initial_pos + step); 
   delay(1000); 
   
   // Make servo go to 90 degrees 
   Servo1.write(initial_pos); 
   delay(5000); 
   
   // Make servo go to 80 degrees 
   Servo1.write(initial_pos - step); 
   delay(1000); 
   
   // Make servo go to 90 degrees 
   Servo1.write(initial_pos); 
   delay(1000); 
}
