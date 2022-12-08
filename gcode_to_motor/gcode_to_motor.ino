/**
 * Parses through g-code received through serial port
 **/

//------------------------------------------------------------------------------
//SETUP
//------------------------------------------------------------------------------
// include needed libraries for stepper motors
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

// limit switches
ezButton xLimit(2);  // create ezButton object that attach to pin 2
ezButton yLimit(3);


// Set up
#define BAUD (57600) // How fast Arduino is talking
#define MAX_MES (64) // Longest message Arduino can store


char buffer[MAX_MES]; // where we store message until we get a ';'
int sofar; // how much is in the buffer
float px, py;      // location
char mode_abs=1;   // absolute mode MIGHT WANT TO GET RID OF THIS
float penState = 0; // pen position: 0 = both up, 1 = left pen up, 2 = right pen up

void setup() {
  // put your setup code here, to run once:
  Serial.begin(BAUD); // starts communication
  help(); // displays helpful information
  ready();

  AFMS.begin(); // motor setup
  xMotor -> setSpeed(10);
  yMotor -> setSpeed(10);

  servo.attach(9); // where servo is attached

  xLimit.setDebounceTime(50); // set debounce time to 50 milliseconds
  yLimit.setDebounceTime(50); // set debounce time to 50 milliseconds

  setHome(); // make sure pens are at (0,0)
}

/**
 * display helpful information
 */
void help() {
  Serial.print(F("Art Robot "));
  Serial.println(F("Commands:"));
  Serial.println(F("G0 [X(steps)] [Y(steps)] [Z(whether pen is lifted)]; - linear move FAST"));
  Serial.println(F("G1 [X(steps)] [Y(steps)] [Z(whether pen is lifted)]; - linear move"));
  Serial.println(F("G04 P[seconds]; - delay"));
  Serial.println(F("G92 [X(steps)] [Y(steps)]; - change logical position"));
  Serial.println(F("M18; - disable motors"));
  Serial.println(F("M100; - this help message"));
  Serial.println(F("M114; - report position and feedrate"));
}

/**
 * prepares the input buffer to receive a new message and 
 * tells the serial connected device it is ready for more
 */
void ready() {
  sofar=0; // clear input buffer
  Serial.print(F("> ")); // signal ready to receive input
}

//------------------------------------------------------------------------------
// METHODS
//------------------------------------------------------------------------------

/** Bring the pen to the home position (0,0)
 */
void setHome() {

  int xstate = xLimit.getState();
  int ystate = yLimit.getState();

  // setting x home
  while (true) {
    xLimit.loop();
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
    Serial.println("The Y limit switch: UNTOUCHED");
    if (yLimit.isPressed()) {
      break;
    }
    ystate = yLimit.getState();
    yMotor -> step(1,BACKWARD,SINGLE);
  }
  Serial.println("The Y limit switch: TOUCHED");

  // changing coordinates to (0,0)
  position(0,0);
}

 
/**
 * Look for character /code/ in the buffer and read the float that immediately follows it.
 * arguments:
 *  code - character to look for
 *  val - return value if code is not found
 * return: the value found.  If nothing found, val is returned.
 **/
float parseNumber(char code,float val) {
  char *ptr=buffer;  // start at the beginning of buffer
  while((long)ptr > 1 && (*ptr) && (long)ptr < (long)buffer+sofar) {  // scan through to end
    if(*ptr==code) {  // if you find code on your walk,
      return atof(ptr+1);  // convert the digits that follow into a float and return it
    }
    ptr=strchr(ptr,' ')+1;  // take a step from here to the letter after the next space
  }
  return val;  // end reached, nothing found, return default val
}

/**
 * delay for the appropriate number of microseconds
 * argument:
 *  ms - how many milliseconds to wait
 */
void pause(long ms) {
  delay(ms/1000);
  delayMicroseconds(ms%1000);  // delayMicroseconds doesn't work for values > ~16k
}

/**
 * Set the logical position
 * arguments: 
 *  npx - new position x
 *  npy - new position y
 */
void position(float npx,float npy) {
  // check where it is??
  px=npx;
  py=npy;
}

/**
 * write a string followed by a float to the serial line.  Convenient for debugging.
 * @input code the string.
 * @input val the float.
 */
void output(const char *code,float val) {
  Serial.print(code);
  Serial.println(val);
}

/**
 * print the current position
 */
void where() {
  output("X",px);
  output("Y",py);
} 

/**
 * Read the input buffer and find any recognized commands. One G or M command per line.
 */
void processCommand() {
  // look for commands that start with 'G'
  int cmd=parseNumber('G',-1);
  switch(cmd) {
  case 0: // move in a line
  case 1: // move in a line
    line( parseNumber('X',(mode_abs?px:0)) + (mode_abs?0:px),
    parseNumber('Y',(mode_abs?py:0)) + (mode_abs?0:py), parseNumber('Z', penState)); // LOOK OVER THIS AGAIN
    break;
  case 4: pause(parseNumber('P',0)*1000); break; // wait a while
  case 92: // set logical position
    position( parseNumber('X',0),
    parseNumber('Y',0) );
    break;
  default: break;
  }

  // look for commands that start with 'M'
  cmd=parseNumber('M',-1);
  switch(cmd) {
  case 18: // turns off power to steppers (releases the grip)
    xMotor -> release();
    yMotor -> release();
    break;
  case 100: help(); break;
  case 114: where(); break; // prints px, py, and mode.
  default: break;
  }

  // if the string has no G or M commands it will get here and the Arduino will ignore it
}

/**
 * Uses Bresenham's line algorithm to move both motors
 * Arguments:
 *  newx - destination x position
 *  newy - destination y position
 **/
void line(float newx,float newy, float penCmd) {
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
    servo.write(100);
    penState = 1;
  }
  if (penCmd == 2) {
    servo.write(80);
    penState = 2;
  }
}

// variables for iterating
  long i;
  long over=0;

  if(dx > dy) {
    for(i=0;i < dx;++i) {
      xMotor -> step(1,dirx,SINGLE);
      over+=dy;
      if(over>=dx) {
        over-=dx;
        yMotor -> step(1,diry,SINGLE);
      }
      // test limits and/or e-stop here
    }
  } else {
    for(i=0;i < dy;++i) { 
      yMotor -> step(1,diry,SINGLE);
      over+=dx; 
      if(over>=dy) { 
        over-=dy;
        xMotor -> step(1,dirx,SINGLE); 
      }
      // test limits and/or e-stop here } }
    }
    position(newx, newy);
    return;
  }
}


//------------------------------------------------------------------------------
// MAIN LOOP
//------------------------------------------------------------------------------
void loop() {
  // put your main code here, to run repeatedly:

  
  // listen for commands
  if( Serial.available() ) { // if something is available
    char c = Serial.read(); // read it
    Serial.println(c); // print what you received (for debugging)
//    Serial.println(sofar);

    // store the byte as long as there's room in the buffer
    // if the buffer is full some data might get lost
    if(sofar < MAX_MES) buffer[sofar++]=c;
    // if we got a return character (\n) the message is done
    if(c=='\n') {
      Serial.print(F("\r\n")); // optional: send back a return for debugging

      // strings must end with a \0.
      buffer[sofar]=0;
      processCommand(); // do what the command told you to
      ready();
    }
  }
}
