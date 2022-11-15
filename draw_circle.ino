#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 

//// Select which 'port' 1 for M1, M2, 2 for M3 or M4
//// y motor m1,m2
//Adafruit_StepperMotor *myMotorY = AFMS.getStepper(200, 1);
//
//// x motor m3,m4
//Adafruit_StepperMotor *myMotorX = AFMS.getStepper(200, 2);


Adafruit_StepperMotor *xMotor = AFMS.getStepper(200, 2);
Adafruit_StepperMotor *yMotor = AFMS.getStepper(200, 1);

void setup() {
  // put your setup code here, to run once:
AFMS.begin();
xMotor -> setSpeed(10);
yMotor -> setSpeed(10);
}

void loop() {
  // put your main code here, to run repeatedly:
  
//  
//  xMotor -> step(1000,FORWARD,SINGLE);
//  yMotor -> step(20,FORWARD,SINGLE);
//  
//  xMotor -> release();
//  delay(10000);

//  {
//   xMotor -> step(3,FORWARD,SINGLE);
//   yMotor -> step(1,FORWARD,SINGLE);
//  } 

int radius = 50;
int pi = 3.14;
int x = radius;
int y = 0 ;
float angle_delta = 0.1;

for (float angle = 0.0; angle < 2.0*pi ; angle += angle_delta)
{
  int xx = radius * cos(angle) ;
  int yy = radius * sin(angle) ;
  while (xx != x || yy != y)
  {
    if (xx > x)
    {
      xMotor -> step(1, FORWARD, SINGLE) ;
      x += 1 ;
    }
    else if (xx < x)
    {
      xMotor -> step(1, BACKWARD, SINGLE) ;
      x -= 1 ;
    }
    if (yy > y)
    {
      yMotor -> step(1, FORWARD, SINGLE) ;
      y += 1 ;
    }
    else if (yy < y)
    {
      yMotor -> step(1, BACKWARD, SINGLE) ;
      y -= 1 ;
    }
  }
//  delay(10);
}
}
