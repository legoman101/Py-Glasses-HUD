import numpy as np
import cv2 #open cv (computre vision)
import os #to interact with the os
from pynput.keyboard import Key, Controller #to interact with the keyboard
import time #for telling the time
from datetime import datetime #for telling the date & time
from dotenv import load_dotenv #to interact with .env files
import requests 
import json #for interacting with .json files
from UliEngineering.EngineerIO import auto_print #for the kelvin to celcius conversions
from UliEngineering.Physics.Temperature import * #for the kelvin to celcius conversions
import geocoder #fotthe current location

#geocoder setup
myloc = geocoder.ip('me')
my_lat = str(myloc.lat)
my_lng = str(myloc.lng)

#dotenv setup
load_dotenv()

#typing setup
keyboard = Controller()

# Create a black image
black_img = np.zeros((512,512,3), np.uint8)

# definitions of text
current_day            = datetime.now().strftime("%A")
current_month          = datetime.now().strftime("%d")
current_year           = datetime.now().strftime("%Y")


def putText(position,text, scale):
    cv2.putText(output_image,
        text,  #the variable in the function (what to write)
        (position), #the position
        cv2.FONT_HERSHEY_SIMPLEX, #font
        scale, # font scale
        (255,255,255), #font colour
        2) #line type

def putTime():
    putText((10, 20), current_day, 0.5)
    putText((70, 20), current_month, 0.5)
    putText((100, 20), current_year, 0.5)
    putText((150, 20), str(datetime.now().strftime("%H:%M:%S")), 0.5)

def putWeather():
    putText((10, 50), Temperature, 0.5) # Puts the Temperature onto the frame
    putText((10, 70), Description, 0.5) # Puts the  weather Description onto the frame
    putText((10, 90), Humidity, 0.5) #Puts the Humidity onto the frame

def getweather_lat_long(latitude, longitude):
    api_key = os.getenv('openweathermapsapikey')
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&lat=" + latitude + "&lon=" + longitude
    response = requests.get(complete_url) 
    x = response.json()
    if x["cod"] != "404":
        y = x["main"] 
        current_temperature = y["temp"] 
        current_pressure = y["pressure"] 
        current_humidity = y["humidity"] 
        z = x["weather"] 
        weather_description = z[0]["description"]
        global Temperature
        global Description
        global Humidity
        Temp_Celsius = kelvin_to_celsius(current_temperature)
        Temp = round(Temp_Celsius, 0)#round Temp_Celsius to 0 decimal places
        Temperature = str(Temp) + ' Celsius'
        Description = str(weather_description)
        Humidity = str(current_humidity) + '% Humidity'

        return Temperature, Description, Humidity

    else: 
        error = "City Not Found"
        return error

video_capture = cv2.VideoCapture(0)

while True:
    if not video_capture.isOpened(): 
        print('Unable to load camera.')
        time.sleep(5)
        pass
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    output_image = frame

    #press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):# if 'q' pressed exit
        break 

    weather = getweather_lat_long(my_lat, my_lng)
    if weather == "City Not Found":
        print("City Not Found")
    else:
        putWeather()#puts the weather onto the frame
    putTime() #puts the time onto the frame
    
    #Display the image
    cv2.imshow("Text-Overlay-On-Video",output_image)
