// test limit switches
#include <ezButton.h>

// limit switches
ezButton xLimit(2);  // create ezButton object that attach to pin 0
ezButton yLimit(3);  // pin 1
#define BAUD (57600) // How fast Arduino is talking

void setup() {
  // put your setup code here, to run once:
  Serial.begin(BAUD); // starts communication
  xLimit.setDebounceTime(50); // set debounce time to 50 milliseconds
  yLimit.setDebounceTime(50); // set debounce time to 50 milliseconds
//  xLimit.loop(); // MUST call the loop() function first
//  yLimit.loop(); // MUST call the loop() function first
}

void loop() {
  // put your main code here, to run repeatedly:
//  Serial.print(xLimit.isPressed());
//  Serial.print(yLimit.isPressed());


   xLimit.loop(); // MUST call the loop() function first

  if(xLimit.isPressed())
    Serial.println("The limit switch: UNTOUCHED -> TOUCHED");

  if(xLimit.isReleased())
    Serial.println("The limit switch: TOUCHED -> UNTOUCHED");

  int state = xLimit.getState();
  if(state == HIGH)
    Serial.println("The limit switch: UNTOUCHED");
  else
    Serial.println("The limit switch: TOUCHED");
}
