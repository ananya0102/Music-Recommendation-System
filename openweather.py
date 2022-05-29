import json
import requests
import streamlit as st
from os import environ
import json

#API key for openweathermap API
api_key=st.secrets['api_key']

url='https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

def getweather(city):
    result = requests.get(url.format(city, api_key))     
    if result:
        json = result.json()
        x=json["weather"]
        #we have to obtain the weather id in order to classify weather into 4 categories
        weather_id=x[0]["id"]
        weather_id=weather_id//100
        return weather_id
    else:
        print("error in search !")