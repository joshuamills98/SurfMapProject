import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import serial 
import time

#This code will extract wind, swell and tide conditions from different websites and output a byte-encoded string to send to the arduino

#Extract Wind Direction Narooma

#This class will allow conversion between Compass direction and compass bearing
class CompassDict(dict):
    def __getitem__(self, item):
        if not isinstance(item, range): 
            for key in self:
                if item in key:
                    return self[key]
            raise KeyError(item)
        else:
            return super().__getitem__(item) # or super(RangeDict, self) for Python 2
            
    def reverse(self, direction): 
        if direction == 'N':
            return 0
        else:
            return np.mean(list(Compass.keys())[list(Compass.values()).index(direction)])
                

#Instantiate compass object
Compass = CompassDict({range(0,12): 'N', range(12,34): 'NNE', range(34,57): 'NE', 
                        range(57,79):'ENE', range(79,102):'E', range(102,124):'ESE', range(124,147):'SE',
                        range(147,169):'SSE', range(169,192):'S', range(192,214):'SSW', range(214,237):'SW',
                        range(237,259):'WSW',range(259,282):'W',range(282,304):'WNW',
                        range(304,327):'NW',range(327,349):'NNW',range(349,360):'N'})

# wNar = requests.get('http://www.findu.com/cgi-bin/wxpage.cgi?last=24&call=CW8505').text #This is broken
# windDirectionNarooma = Compass[int(re.findall(r'Wind from  (\d+) degrees', wNar)[0])]
# windSpeedNarooma = round(float(re.findall(r' @ (\d+\.?\d+) MPH',wNar)[0])/1.151)

#Extract Wind direction and Speed Moruya
w = requests.get("https://wind.willyweather.com.au/nsw/south-coast/moruya-airport.html")
windText = w.text
windDirectionMoruya = re.findall(r' (.+)</strong>',windText)[0]
windSpeedMoruya = round(float(re.findall(r' +(\d+\.*\d*)km/h',windText)[0])/1.852)
windCompassDirectionMoruya = int(Compass.reverse(windDirectionMoruya))

#Extract Swell Direction and height from Broulee swell data
s = requests.get("https://magicseaweed.com/Broulee-Surf-Report/1046/")
swellText = s.text
swellDirection = re.findall(r'Primary Swell - (\w{1,3})', swellText)[0]
swellPeriod = float(re.findall(r'\"period\":(\d+),',swellText)[0])
swellHeight =(float(re.findall(r'\"minBreakingHeight\":(\d+),', swellText)[0])+float(re.findall(r'\"maxBreakingHeight\":(\d+),', swellText)[0]))/2 # Take average of max and min heights
swellCompassDir = int(Compass.reverse(swellDirection))
if (swellCompassDir>180): #Convert comass direction to match with servo (which can only output 180 degrees of rotation)
    swellCompassDir = 0 
else:
    swellCompassDir = 180-swellCompassDir

#Extract Tide height and direction 
t = requests.get("https://www.tidetime.org/australia-pacific/australia/broulee.htm").text
tidetime = float(re.findall(r'(\d+) hrs',t)[0]) #Extract time until next high tide
if (tidetime>=10):
    tide = 'High'
    Dir = 'D'
elif (tidetime<2):
    tide = 'High'
    Dir = 'R'
elif ((tidetime<10 and tidetime>=8)): 
    tide ='Mid'
    Dir = 'D'
elif ((tidetime<4 and tidetime>=2)): #have 2-4 hours i=until high tide therefore rising
    tide = 'Mid'
    Dir = 'R'
elif ((tidetime<6 and tidetime>=4)):
    tide = 'Low'
    Dir = 'R'
else:
    tide = 'Low'
    Dir = 'D'
    
#Extract Sea Temp
St=requests.get("https://www.surf-forecast.com/breaks/Moruya-Rivermouth/seatemp") 
seaTemp= float(re.findall(r'sea temperature is <span class="temp">(\d{1,2}\.*\d)<', St.text)[0])

#Ideal Conditions Dictionary - create a dictionary for each spot that lists its favored conditions
idealSwells = {
    "South Broulee" : ['NE','ENE','S','SSE','SE'],
    "Moruya Wall" : ['E','SE','ESE'],
    "Congo" : ['E','ENE','NE','SSE','SE','ESE'],
    "Meringo" : ['SE','ESE','E','ENE'],
    "South Bingi" : ['NE','ENE','E','ESE','SE','SSE','S'],
    "Plantation" : ['NE','ENE','E'],
    "Blackfellows" : ['E','ESE','SE','SSE'],
    "Jemisons" : ['S','SSE','SE','ESE','E','ENE','NE'],
    "Dalmeny" : ['NE','ENE','S','E','SSE','SE'],
    "Yabbara" : ['NE','ENE','E'],
    "Kianga" : ['E','ESE','SE','SSE','S'],
    "Carters" : ['E','ESE','SE','SSE'],
    "Narooma Bar" : ['E','ESE','SE','SSE'],
    "Handkerchiefs" : ['NE','ENE','E','ESE','SE','SSE','S'],
    "Fullers" : ['NE','ENE','E','ESE','SE','SSE','S'],
    "Corunna" : [],
    # "Seconds" : ['Mid','High'],
    # "1080" : [],
    # "Tilba Point" : [],
    # "Wallaga Lake" : ['S','SSE','SE',],
    # "Camel Rock" : [],
    # "Horseshoe Bay" : ['Low','Mid']
    # "Bear Beach" : ['S','SSE','SE']
}

idealWindsMoruya = {
    "South Broulee" : ['W','WNW','NW','NNW','N','NNE','NE'],
    "Moruya Wall" : ['W','WSW','SW','SSW','S','SSE','SE'],
    "Congo" : ['W','WNW','NW','NNW'],
    "Meringo" : ['WNW','W','WSW','SW','SSW','S','SSE'],
    "South Bingi" : ['W','WNW','NW','NNW','N','NNE','NE'],
    "Plantation" : ['WSW','W','WNW','NW'],
    "Blackfellows" : ['W','WSW','SW','SSW','S','SSE'],
    "Jemisons" : ['W','WNW','NW'],
    "Dalmeny" : ['WNW','W','WSW','SW','SSW','S','SSE','SE'],
    "Yabbara" : ['W','WNW','NW','NNW','N','NNE','NE'],
    "Kianga" : ['W','WNW','WSW','SW','SSW'],
    "Carters" : ['W','WNW','WSW','SW','SSW','S'],
    "Narooma Bar" : ['WNW','W','WSW','SW','SSW','S','SSE','SE','ESE'],
    "Handkerchiefs" : ['W','WNW','NW','NNW'],
    "Fullers" : ['W','WNW','NW','NNW','N','NNE'],
    "Corunna" : ['W','WNW','WSW','SW','SSW','NW','NNW','N'],
}

# idealWindsNarooma = {
# "Dalmeny" : ['WNW','W','WSW','SW','SSW','S','SSE','SE'],
# "Yabbara" : ['W','WNW','NW','NNW','N','NNE','NE'],
# "Kianga" : ['W','WNW','WSW','SW','SSW'],
# "Carters" : ['W','WNW','WSW','SW','SSW','S'],
# "Narooma Bar" : [],
# "Handkerchiefs" : [],
# "Fullers" : [],
# "Corunna" : [],
# "Seconds" : [],
# "1080" : [],
# "Tilba Point" : [],
# "Wallaga Lake" : ['S','SSE','SE','],
# "Camel Rock" : ['SW','WSW','W','WNW','NW','NNW','N'],
# "Horseshoe Bay" : ['W','WSW','SW','SSW','S','SSE','SE']
# }

#Ideal Tides is subject to change as sand banks develop 
idealTides = {
    "South Broulee" : ['Low','Mid'],
    "Moruya Wall" : ['Low','Mid','High'],
    "Congo" : ['Low','Mid'],
    "Meringo" : ['High'],
    "South Bingi" : ['Low','Mid','High'],
    "Plantation" : ['Low','Mid','High'],
    "Blackfellows" : ['Low','Mid'],
    "Jemisons" : ['Low','Mid','High'],
    "Dalmeny" : ['Low'],
    "Yabbara" : ['Low','Mid','High'],
    "Kianga" : ['Low','Mid','High'],
    "Carters" : ['Low'],
    "Narooma Bar" : ['Low','Mid'],
    "Handkerchiefs" : ['Low','Mid','High'],
    "Fullers" : ['Low','Mid','High'],
    "Corunna" : ['Low','Mid','High'],
    # "Seconds" : ['Mid','High'],
    # "1080" : ['Low','Mid'],
    # "Tilba Point" : ['Low','Mid','High'],
    # "Wallaga Lake" : ['Mid','High'],
    # "Camel Rock" : ['Low','Mid','High'],
    # "Horseshoe Bay" : ['Low','Mid']
    # "Bear Beach" : ['Mid','High']
}
#Search through dictionaries to return locations that work in given conditions
tideWorking  = np.zeros(len(idealTides))
swellWorking = np.zeros(len(idealTides))
windWorking =  np.zeros(len(idealTides))
i=0
for location, tides in idealTides.items():
    if tide in idealTides[location]:
        tideWorking[i]=1
    i=i+1

i=0
for location, winds in idealWindsMoruya.items():
    if windDirectionMoruya in idealWindsMoruya[location]:
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
#Read the C input commands 
resultint = '-' + str(int(''.join(str(i) for i in result), 2)) + '_' + tide + ' ' + Dir + ' ' + str(windDirectionMoruya) + ' @ ' + str(windSpeedMoruya) + 'kts' + '+' + str(seaTemp) + 'C ' + str(swellHeight) + 'ft @' + str(round(swellPeriod)) + 's' + '$' + str(swellCompassDir) + '&' + str(windCompassDirectionMoruya) + '^'+'\n'#concat newline for arduino
    
with serial.Serial('COM3', 9600) as ser: #Send trough encoded data to Arduino on serial COM 3
    time.sleep(2)
    ser.write(resultint.encode())   

    ser.close()
    
# working = []   #Output the keys of the working locations
# for i in range(len(idealTides)):
    # if result[i]:
        # working.append(list(idealTides.keys())[i]) 

    
print("Seatemp = ", seaTemp, "Deg C")
print("Tide = ", tide)
print("Moruya Wind Direction = " ,windDirectionMoruya," at ", windSpeedMoruya, "kts")
# print("Narooma Wind Direction = " , windDirectionNarooma," at ", windSpeedNarooma, "kts")
print('Swell : ', swellDirection,',',' swellHeight :', swellHeight, 'ft @ ', swellPeriod, ' s')
