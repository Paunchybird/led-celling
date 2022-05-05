#!/usr/bin/env python

import json
import requests
import time
from rgbmatrix import graphics
from samplebase import SampleBase
from PIL import Image

class Weather(SampleBase):
    def __init__(self, *args, **kwargs):
        super(Weather, self).__init__(*args, **kwargs)
    
    def run(self):
        while True:
            self.job()
            time.sleep(10)
            
    def drawimage(self,path, x, y):
        image = Image.open(path).convert('RGB')
        image.load()
        self.matrix.SetImage(image, x, y)

    def job(self):
        matrix = self.matrix.CreateFrameCanvas()
        # Enter Location code found at: http://bulk.openweathermap.org/sample/city.list.json.gz
        location = '6359395' 

        # Include app id generated when you make you account at: http://openweathermap.org/api
        appid = '6d7153de1e09360852d7576b14eafa31'
        # Clear matrix
        matrix.Clear()

        # Pull fresh weather data
        try:
            response = requests.get('http://api.openweathermap.org/data/2.5/weather?id='+location+'&mode=json&cnt=10&appid='+appid)

            data = json.loads(response.text)
          
            main = data['main']

            #Get Current Conditions
            temp = main['temp']
            temp = ((temp-273.15))
            temp = int(round(temp))

            weather = data['weather']
            weather = weather[0]
            icon = weather['icon']

            Conditions = weather['id']

            #Draw weather icon
            cond = ''
            if Conditions == 900:
                cond = 'tornado'
                
            elif Conditions == 901 or Conditions == 902:
                cond = 'hurricane'

            elif Conditions == 906 or Conditions == 611 or Conditions == 612:
                cond = 'hail'
              
            elif Conditions == 600 or Conditions == 601 or Conditions == 602:
                cond = 'snow'
                
            else: 
                self.drawimage('/opt/led-matrix/weathericons/' + icon + '.png', 9, 1)
            
            if cond:
               self.drawimage('/opt/led-matrix/weathericons/' + cond + '.png', 9, 1)     

            #Draw temperature
            TempComponents = str(temp) + "ºC"
            TempLength = len(TempComponents)

            # Sets Temperature Color
            if temp <= 20:
                TempColor = graphics.Color(0, 0, 255)
            elif temp > 30:
                TempColor = graphics.Color(255, 0, 0)
            else:
                TempColor = graphics.Color(255, 255, 255)
            
            self.font= graphics.Font()
            self.font.LoadFont("/opt/led-matrix/fonts/" + "6x13" + ".bdf")
            
            graphics.DrawText(self.matrix, self.font, TempLength, 30, TempColor,
                              TempComponents)

            print('Current Temp: '+str(temp)+' Icon Code: '+str(icon))

        except requests.exceptions.RequestException as e:
            self.drawimage('/opt/led-matrix/weathericons/' + 'error' + '.png',9,1)

if __name__ == "__main__":
    weather = Weather()
    if (not weather.process()):
        weather.print_help()


