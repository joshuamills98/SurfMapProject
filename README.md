(https://user-images.githubusercontent.com/57185163/116960698-86dbba00-ace4-11eb-9649-2af52a5ccfdd.png)
In this projected I used Python and C++ to build a physical surf map displayed using an arduino as shown below.
The idea behind this project was to have a physical map that would constantly update based on live wind and surf conditions to tell me which surf spots are working as well as display current conditions. The video below gives a demonstration.

Files:

arduino_serial.py - Calls all the conditions from the web and live wind readins and sends it to the arduino via serial communication

SurfMapFinal.ino - All the functionality of the arduino is written here from servo motors to show wind direction to the shift register operating 16 LEDs and the LCD display.

DEMO: 

Unfortunately this was the only video I got to show of it fully functioning as I had to leave in a rush, but it should show it well enough

[![Watch the video](https://user-images.githubusercontent.com/57185163/116960698-86dbba00-ace4-11eb-9649-2af52a5ccfdd.png)(https://user-images.githubusercontent.com/57185163/116960499-e38aa500-ace3-11eb-94bc-6d17385ae811.mp4)]

