#include <LiquidCrystal.h>
#include <Servo.h>
#include <Stepper.h>

// initialize the library with the numbers of the interface pins
//rs- green, enable - orange, d4 -yellow, d5-white, d6- brown, d7-grey
LiquidCrystal lcd(A0, A1, A5, A3, A4, A2);
Servo swellServo; // instantiate servo motor


//Pin connected to ST_CP of 74HC595 yellow
int latchPin = 12;
//Pin connected to SH_CP of 74HC595 blue
int clockPin = 9;
////Pin connected to DS of 74HC595 white 
int dataPin = 13;

String inString= ""; 
String spotOnString = "";
String tideString = "";
String tempString = "";
String swellString = "";
String windString = "";
char input; 
signed int spotOn;
int swellPos = 0;    // variable to store the servo position
int swellDirection = 0; //vaiable to store the swell direction (in degrees)
const int stepsPerRevolution = 1800;  // change this to fit the number of steps per revolution
const int rolePerMinute = 15;         // Adjustable range of 28BYJ-48 stepper is 0~17 rpm
int integer;

Stepper myStepper(stepsPerRevolution, 2, 3, 5, 6);
void setup() {
  // put your setup code here, to run once:
  pinMode(A5, OUTPUT);
  pinMode(A4, OUTPUT);
  pinMode(A3, OUTPUT);
  pinMode(A2, OUTPUT);
  pinMode(A1, OUTPUT);
  pinMode(latchPin, OUTPUT);//Set up 74hc595 pins
  pinMode(dataPin, OUTPUT);  
  pinMode(clockPin, OUTPUT);
  swellServo.attach(11); // pwm driver for swellDirection servo
  
  Serial.begin(9600);
  spotOn = 65535;
  updateShiftRegister();
  lcd.begin(16,2);
  lcd.clear();
  myStepper.setSpeed(rolePerMinute);
}

void loop() {
  // put your main code here, to run repeatedly:
  while (Serial.available() > 0) {
    int input = Serial.read();
      // convert the incoming byte to a char and add it to the string:
    if (input != '\n')  {
      inString += (char)input ;
    }
    if (input == '\n'){ //The code will need to see a new line in oreder to finish
      delay(300);
      myStepper.step(-integer); //Set wind back to beginning
      windString = "";
      //Python will send through a string of format '-xxx..._yyy...+zzz...$www...&
      for (int i = inString.indexOf('-')+1; i<inString.indexOf('_'); i++){
        spotOnString.concat(inString[i]);
      }
      for (int i = inString.indexOf('_')+1; i<inString.indexOf('+'); i++){
        tideString.concat(inString[i]);
      }
      for (int i = inString.indexOf('+')+1; i<inString.indexOf('$'); i++){
        tempString.concat(inString[i]);
      }
      for (int i = inString.indexOf('$')+1; i<inString.indexOf('&'); i++){
        swellString.concat(inString[i]);
      }
      for (int i = inString.indexOf('&')+1; i<inString.indexOf('^'); i++){
        windString.concat(inString[i]);
      }
      spotOn = spotOnString.toInt(); //best to set this to a long for when more spots are needed
      updateShiftRegister();
      swellDirection = swellString.toInt(); 
      delay(100);
      swellServo.write(swellDirection);
//      delay(300);
//      int integer = windString.toInt()*5;
//      myStepper.step(integer);
      lcd.print(tempString);
      lcd.setCursor(0,1);
      lcd.print(tideString); 
      //Reset Strings
      spotOnString = "";
      tideString = "";
      tempString = "";
      windString = "";
      swellString = "";
      //Update Register

      }

  }
    }

void updateShiftRegister()
{
   digitalWrite(latchPin, LOW);
   shiftOut(dataPin, clockPin, LSBFIRST, (spotOn));
   shiftOut(dataPin, clockPin, LSBFIRST, (spotOn >> 8));
   // shift out highbyte
   // shift out highbyte
   digitalWrite(latchPin, HIGH);
}
