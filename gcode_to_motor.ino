// recieves g-code from pi, sends over "ok" messages to pi
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 

Adafruit_StepperMotor *xMotor = AFMS.getStepper(200, 2);
Adafruit_StepperMotor *yMotor = AFMS.getStepper(200, 1);

#define BAUD (57600) // How fast is Arduino talking
#define MAX_MES (64) // Longest message Arduino can store


char buffer[MAX_MES]; // where we store message until we get a ';'
int sofar; // how much is in the buffer
float px, py;      // location
char mode_abs=1;   // absolute mode?

/**
 * Look for character /code/ in the buffer and read the float that immediately follows it.
 * @return the value found.  If nothing is found, /val/ is returned.
 * @input code the character to look for.
 * @input val the return value if /code/ is not found.
 **/
float parseNumber(char code,float val) {
  char *ptr=buffer;  // start at the beginning of buffer
  while((long)ptr > 1 && (*ptr) && (long)ptr < (long)buffer+sofar) {  // walk to the end
    if(*ptr==code) {  // if you find code on your walk,
      return atof(ptr+1);  // convert the digits that follow into a float and return it
    }
    ptr=strchr(ptr,' ')+1;  // take a step from here to the letter after the next space
  }
  return val;  // end reached, nothing found, return default val.
}

/**
 * delay for the appropriate number of microseconds
 * @input ms how many milliseconds to wait
 */
void pause(long ms) {
  delay(ms/1000);
  delayMicroseconds(ms%1000);  // delayMicroseconds doesn't work for values > ~16k.
}

/**
 * Set the logical position
 * @input npx new position x
 * @input npy new position y
 */
void position(float npx,float npy) {
  // here is a good place to add sanity tests
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
 * print the current position, feedrate, and absolute mode.
 */
void where() {
  output("X",px);
  output("Y",py);
  Serial.println(mode_abs?"ABS":"REL");
} 

void setup() {
  // put your setup code here, to run once:
  Serial.begin(BAUD); // open coms
  help(); // ??
  ready();

  AFMS.begin();
  xMotor -> setSpeed(10);
  yMotor -> setSpeed(10);
}

/**
 * display helpful information
 */
void help() {
  Serial.print(F("Art Robot "));
  Serial.println(F("Commands:"));
  Serial.println(F("G00 [X(steps)] [Y(steps)] [F(feedrate)]; - linear move"));
  Serial.println(F("G01 [X(steps)] [Y(steps)] [F(feedrate)]; - linear move"));
  Serial.println(F("G04 P[seconds]; - delay"));
  Serial.println(F("G90; - absolute mode"));
  Serial.println(F("G91; - relative mode"));
  Serial.println(F("G92 [X(steps)] [Y(steps)]; - change logical position"));
  Serial.println(F("M18; - disable motors"));
  Serial.println(F("M100; - this help message"));
  Serial.println(F("M114; - report position and feedrate"));
}

/**
 * prepares the input buffer to receive a new message and 
 * tells the serial connected device it is ready for more.
 */
void ready() {
  sofar=0; // clear input buffer
  Serial.print(F("> ")); // signal ready to receive input
}

// main loop ?? :0
void loop() {
  // put your main code here, to run repeatedly:
  
  // listen for commands
  if( Serial.available() ) { // if something is available
    char c = Serial.read(); // get it
    Serial.print(c); // optional: repeat back what I got for debugging

    // store the byte as long as there's room in the buffer.
    // if the buffer is full some data might get lost
    if(sofar < MAX_MES) buffer[sofar++]=c;
    // if we got a return character (\n) the message is done.
    if(c=='\n') {
      Serial.print(F("\r\n")); // optional: send back a return for debugging

      // strings must end with a \0.
      buffer[sofar]=0;
      processCommand(); // do something with the command
      ready();
    }
  }
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
//    set_feedrate(parsenumber('F',fr));
    line( parseNumber('X',(mode_abs?px:0)) + (mode_abs?0:px),
    parseNumber('Y',(mode_abs?py:0)) + (mode_abs?0:py) );
    break;
  case 4: pause(parseNumber('P',0)*1000); break; // wait a while
  case 90: mode_abs=1; break; // absolute mode
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
  case 114: where(); break; // prints px, py, fr, and mode.
  default: break;
  }

  // if the string has no G or M commands it will get here and the Arduino will silently ignore it
}

/**
 * Uses Bresenham's line algorithm to move both motors
 * @input newx the destination x position
 * @input newy the destination y position
 * This code is from David Forrest https://github.com/MarginallyClever/GcodeCNCDemo/blob/master/GcodeCNCDemo2Axis/GcodeCNCDemo2Axis.ino
 **/
void line(float newx,float newy) {
  long dx=newx-px; // distance to move (difference between current x and new x)
  long dy=newy-py;
  int dirx=dx > 0?FORWARD:BACKWARD; // direction to move
  int diry=dy > 0?FORWARD:BACKWARD;
  dx=abs(dx); // absolute delta
  dy=abs(dy);

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
      // update the logical position. We don't just = newx because 
      // px + dx * dirx == newx could be false by a tiny margin and we don't want rounding errors. px+= dx*dirx; py+= dy*diry; } /** * delay for the appropriate number of microseconds * @input ms how many milliseconds to wait */ void pause(long ms) { delay(ms/1000); delayMicroseconds(ms%1000); // delayMicroseconds doesn't work for values > ~16k. } /** * Set the feedrate (speed motors will move) * @input nfr the new speed in steps/second */ void set_feedrate(float nfr) { if(fr==nfr) return; // same as last time? quit now. if(nfr > MAX_FEEDRATE || nfr < MIN_FEEDRATE) { 
      // don't allow crazy feed rates
    }
    return;
  }
}
