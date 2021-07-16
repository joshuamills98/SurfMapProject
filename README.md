## Surf Map Project
In this projected I used Python and C++ to build a physical surf map displayed using an arduino as shown below.
The idea behind this project was to have a physical map that would constantly update based on live wind and surf conditions to tell me which surf spots are working as well as display current conditions. The video below gives a demonstration.

# Files:

* **arduino_serial.py -** Calls all the conditions from the web and live wind readins and sends it to the arduino via serial communication
* **SurfMapFinal.ino -** All the functionality of the arduino is written here from servo motors to show wind direction to the shift register operating 16 LEDs and the LCD display.

# Demonstration: 

Unfortunately this was the only video I got to show of it fully functioning as I had to leave in a rush. The arrow shows the live swell direction taken from local buoys and the LEDs light up depending on whether the given location will have the right *tide*, *wind* and *swell direction* for it to be fun to surf (the spot is said to be "working" in surf lingo). An LCD displays other useful information such as *tide height*, *water temperature* and *swell height*. In the demonstration below the wind is blowing from the east and the swell is southerly, hence no spots are working and so no LEDs light up.

![SurfVidGif](https://user-images.githubusercontent.com/57185163/116961187-01590980-ace6-11eb-9022-1296fb13084f.gif)


