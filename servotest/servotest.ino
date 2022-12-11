// test servo motor lift / lower pen
// Include the Servo library 
#include <Servo.h> 
// Declare the Servo pin 
int servoPin = 9; 
// Create a servo object 
Servo Servo1; 
void setup() { 
  Serial.begin(9600);
   // We need to attach the servo to the used pin number 
   Servo1.attach(servoPin); 
   Servo1.write(90);
}
void loop(){ 
   // Make servo go to 100 degrees (right pen lowered)
   Servo1.write(100); 
   delay(1000); 
   
   // Make servo go to 90 degrees 
   Servo1.write(90); 
   delay(5000); 
   
   // Make servo go to 80 degrees 
   Servo1.write(80); 
   delay(1000); 
   
   // Make servo go to 90 degrees 
   Servo1.write(90); 
   delay(1000); 
}
