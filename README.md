In this projected I used Python and C++ to build a physical surf map displayed using an arduino as shown below.
The idea behind this project was to have a physical map that would constantly update based on live wind and surf conditions to tell me which surf spots are working as well as display current conditions. The video below gives a demonstration.

Files:

arduino_serial.py - Calls all the conditions from the web and live wind readins and sends it to the arduino via serial communication

SurfMapFinal.ino - All the functionality of the arduino is written here from servo motors to show wind direction to the shift register operating 16 LEDs and the LCD display.