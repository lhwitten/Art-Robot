// Parses through g-code received through serial communication, and converts to motor commands

// Include needed libraries for stepper motors
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
#include <ezButton.h>
#include <Servo.h>

// Create the motor shield object
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 

// Create pointers for x motor and y motor
Adafruit_StepperMotor *xMotor = AFMS.getStepper(200, 2);
Adafruit_StepperMotor *yMotor = AFMS.getStepper(200, 1);

// Create servo object to lift and lower pens
Servo servo;
// Declare the Servo pin 
int servoPin = 9; 

// Create limit switch button objects
ezButton xLimit(2);  // create ezButton object that attach to pin 2
ezButton yLimit(3);

// Set up
String message; // stores the current message
float px, py;      // x and y locations
float penState = 0; // pen position: 0 = both up, 1 = left pen up, 2 = right pen up

void setup() {
  // put your setup code here, to run once:
  Serial.begin(57600); // starts communication
  // help(); // displays helpful information

  AFMS.begin(); // stepper motor setup
  xMotor -> setSpeed(10); // motor speed
  yMotor -> setSpeed(10);

  servo.attach(servoPin); // where servo is attached
  servo.write(90); // making start position of servo at 90 degrees so it is able to rotate in 2 directions

  xLimit.setDebounceTime(50); // set debounce time to 50 milliseconds
  yLimit.setDebounceTime(50); // set debounce time to 50 milliseconds

  message = "";
  px = 0;
  py = 0;
  // setHome(); // make sure pens are at (0,0)
}

void help() {
  // display helpful info

  Serial.print(F("Art Robot "));
  Serial.println(F("Commands:"));
  Serial.println(F("G0 [X(steps)] [Y(steps)] [Z(whether pen is lifted)]; - linear move FAST"));
  Serial.println(F("G1 [X(steps)] [Y(steps)] [Z(whether pen is lifted)]; - linear move"));
}

void setHome() {
  // bring the pen to the home position (0,0)

  int xstate = xLimit.getState();
  int ystate = yLimit.getState();

  // setting x home
  while (true) {
    xLimit.loop();
    if (xstate == LOW){
      Serial.println("x limit touched");
      break;
    }
    Serial.println("The X limit switch: UNTOUCHED");
    if (xLimit.isPressed()) {
      break;
    }
    xstate = xLimit.getState();
    xMotor -> step(1,BACKWARD,SINGLE);
  }
  Serial.println("The X limit switch: TOUCHED");

  // setting y home
  while (true) {
    yLimit.loop();
    if (ystate== LOW) {
      break;
    }
    Serial.println("The Y limit switch: UNTOUCHED");
    if (yLimit.isPressed()) {
      break;
    }
    ystate = yLimit.getState();
    yMotor -> step(1,BACKWARD,SINGLE);
  }
  Serial.println("The Y limit switch: TOUCHED");

  // changing coordinates to (0,0)
  px = 0;
  py = 0;
}

float parseMessage(char code,float val) {
  // Look for character /code/ in the message and read the float that immediately follows it.
  // arguments:
  //  code - character to look for
  //  val - return value if code is not found
  // return: the value found.  If nothing found, val is returned.

  int idx = message.indexOf(code);
  Serial.println(code);
  if (idx != -1) {
    int space = message.indexOf(" ", idx);
    return (message.substring(idx+1, space)).toFloat();
  }

  return val;  // end reached, nothing found, return default val
}

void where() {
  // print current position
  Serial.print("X");
  Serial.println(px);

  Serial.print("Y");
  Serial.println(py);
} 

void processCommand() {
  // Read the message and find any recognized commands

  // look for commands that start with 'G'
  int cmd=parseMessage('G',-1);
  switch(cmd) {
  case 0: // move in a line
  case 1: // move in a line
    line( parseMessage('X',px),
    parseMessage('Y',py), parseMessage('Z', penState));
    break;
  default: break;
  }

  // if the string has no G commands it will get here and the Arduino will ignore it
}

void line(float newx,float newy, float penCmd) {
  // Uses Bresenham's line algorithm to move both motors and lifts or lowers pens
  // Arguments:
  //  newx - new x position
  //  newy - new y position
  //  penCmd - new pen position

  long dx=newx-px; // distance to move (difference between current x and new x)
  long dy=newy-py;
  int dirx=dx > 0?FORWARD:BACKWARD; // direction to move
  int diry=dy > 0?FORWARD:BACKWARD;
  dx=abs(dx); // absolute delta
  dy=abs(dy);

// lift or lower pen as needed
if (penState != penCmd) {
  if (penCmd == 0) {
    servo.write(90);
    penState = 0;
  }
  if (penCmd == 1) {
    servo.write(105);
    penState = 1;
  }
  if (penCmd == 2) {
    servo.write(75);
    penState = 2;
  }
}

  // variable to keep track of how much motors should move
  long over=0;

  if(dx > dy) {
    for(long i=0;i < dx;++i) {
      xMotor -> step(1,dirx,SINGLE);
      over+=dy;
      if(over>=dx) {
        over-=dx;
        yMotor -> step(1,diry,SINGLE);
      }
    }
  } else {
    for(long i=0;i < dy;++i) { 
      yMotor -> step(1,diry,SINGLE);
      over+=dx; 
      if(over>=dy) { 
        over-=dy;
        xMotor -> step(1,dirx,SINGLE); 
      }
    }
  }
  px = newx;
  py = newy;
  return;
}

void loop() {
  // put your main code here, to run repeatedly:


  // listen for commands
  if( Serial.available() > 0 ) { // if something is available
    Serial.println("message received!!");
    char c = Serial.read(); // read it

    // put the character in a string to store
    message += c;

    // if we got a return character (;) the message is done
    if ((c == ';') && (message.length() > 0)) {      
      Serial.println(message);
      processCommand(); // do what the command told you to
      // Serial.print("x,y");
      // Serial.println(px,py);
      message = "";
      Serial.print(F("> ")); // tell python code to send next command
    }
  }
}