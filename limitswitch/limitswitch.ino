// test limit switches
// #define xLimit 2
// //int yLimit = 3;

// void setup()
// {
//   Serial.begin(9600); 
//   pinMode(xLimit, INPUT);
// }

// void loop() {
 
//   if (digitalRead(xLimit) == HIGH)
//   {
//     Serial.println("Activated!");
//   }
 
//   else
//   {
//     Serial.println("Not activated.");
//   }
   
//   delay(100);
// }

#include <ezButton.h>

ezButton xLimit(2);  // create ezButton object that attach to pin 2;
ezButton yLimit(3);

void setup() {
  Serial.begin(57600);
  xLimit.setDebounceTime(50); // set debounce time to 50 milliseconds
  yLimit.setDebounceTime(50);
  setHome();
}

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
    // xMotor -> step(1,BACKWARD,SINGLE);
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
    // yMotor -> step(1,BACKWARD,SINGLE);
  }
  Serial.println("The Y limit switch: TOUCHED");

  // changing coordinates to (0,0)
  // px, py = 0,0
}

void loop() {
  // limitSwitch.loop(); // MUST call the loop() function first

  // if(limitSwitch.isPressed())
  //   Serial.println("The limit switch: UNTOUCHED -> TOUCHED");

  // if(limitSwitch.isReleased())
  //   Serial.println("The limit switch: TOUCHED -> UNTOUCHED");

  // int state = limitSwitch.getState();
  // if(state == HIGH)
  //   Serial.println("The limit switch: UNTOUCHED");
  // else
  //   Serial.println("The limit switch: TOUCHED");
}