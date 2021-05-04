import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import serial 
import time
#Extract Wind direction
w = requests.get("https://wind.willyweather.com.au/nsw/south-coast/moruya-airport.html")
windText = w.text
windDirection = re.findall(r'<strong>(.+)</strong>',windText)[0]

#Extract Swell Direction and height
s = requests.get("https://magicseaweed.com/Broulee-Surf-Report/1046/")
swellText = s.text
swellDirection = re.findall(r'Primary Swell - (\w{1,3})', swellText)[0]

#Extract Tide height
t = requests.get("https://www.tidetime.org/australia-pacific/australia/broulee.htm").text
tidetime = float(re.findall(r'(\d+) hrs',t)[0]) #first one is High tide, second one is Low tide
if ((tidetime>=10) or (tidetime<2)):
    tide = 'High'
elif ((tidetime<10 and tidetime>=8) or (tidetime<4 and tidetime>=2)):
    tide ='Mid'
else:
    tide = 'Low'
    
#Extract Sea Temp
St=requests.get("https://www.surf-forecast.com/breaks/Moruya-Rivermouth/seatemp") 
seaTemp= float(re.findall(r'sea temperature is <span class="temp">(\d{1,2}\.*\d)<', St.text)[0])

#Ideal Conditions Dictionary
idealSwells = {
    "South Broulee" : ['NE','ENE','S','SSE','SE'],
    "Moruya Wall" : ['E','SE','ESE'],
    "Congo" : ['E','ENE','NE','SSE','SE','ESE'],
    "Meringo" : ['SE','ESE','E','ENE'],
    "South Bingi" : ['NE','ENE','E','ESE','SE','SSE','S'],
    "Plantation" : ['NE','ENE','E'],
    "Blackfellows" : ['E','ESE','SE','SSE'],
    "Jemisons" : ['S','SSE','SE','ESE','E','ENE','NE']
}

idealWinds = {
    "South Broulee" : ['W','WNW','NW','NNW','N','NNE','NE'],
    "Moruya Wall" : ['W','WSW','SW','SSW','S','SSE','SE'],
    "Congo" : ['W','WNW','NW','NNW'],
    "Meringo" : ['WNW','W','WSW','SW','SSW','S','SSE'],
    "South Bingi" : ['W','WNW','NW','NNW','N','NNE','NE'],
    "Plantation" : ['WSW','W','WNW','NW'],
    "Blackfellows" : ['W','WSW','SW','SSW','S','SSE'],
    "Jemisons" : ['W','WNW','NW','NNW']
}

idealTides = {
    "South Broulee" : ['Low','Mid'],
    "Moruya Wall" : ['Low','Mid','High'],
    "Congo" : ['Low','Mid'],
    "Meringo" : ['High'],
    "South Bingi" : ['Low','Mid'],
    "Plantation" : ['Low','Mid','High'],
    "Blackfellows" : ['Low','Mid'],
    "Jemisons" : ['Low','Mid','High']
}
#Search in Dictionary
tideWorking  = np.zeros(len(idealTides))
swellWorking = np.zeros(len(idealTides))
windWorking =  np.zeros(len(idealTides))
i=0
for location, tides in idealTides.items():
    if tide in idealTides[location]:
        tideWorking[i]=1
    i=i+1

i=0
for location, winds in idealWinds.items():
    if windDirection in idealWinds[location]:
        windWorking[i]=1
    i=i+1

i=0
for location, swell in idealSwells.items():
    if swellDirection in idealSwells[location]:
        swellWorking[i]=1
    i=i+1

#Find the and result of all conditions
result = np.zeros(len(tideWorking))
for i in range(0, len(tideWorking)):
        result[i] = tideWorking[i] and swellWorking[i] and windWorking[i]
#convert to string
result= [int(x) for x in result.tolist()]
resultint = str(int(''.join(str(i) for i in result), 2)) + '\n' #concat newline for arduino 
# with serial.Serial('COM3', 9600) as ser:
#     time.sleep(2)
#     ser.write(resultint.encode())
    
#     ser.close()

print(seaTemp)
print(tide)
print(windDirection)
print(swellDirection)
print(idealSwells.keys())

