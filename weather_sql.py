import os

import sqlite3
from weather_class import Weather

weather_path= os.path.join("..","resources","City_Weather.csv")
weather_file= open(weather_path,"r")
weather_lines= weather_file.readlines()
weather_lines= [i.strip() for i in weather_lines]
weather_lines= weather_lines[1:len(weather_lines)]
weather_lines_csv= [i.split(",") for i in weather_lines]

list_of_weather= [
    Weather(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]) 
    for i in weather_lines_csv
    ]


conn= sqlite3.connect("weather.db")

c= conn.cursor()

c.execute("DROP TABLE IF EXISTS weather")

c.execute(
    """CREATE TABLE IF NOT EXISTS weather (
    city text,
    cloudiness integer,
    country text,
    date integer,
    humidity integer,
    lat real,
    lng real,
    max_temp real,
    wind_speed real
    )""")

for city_weather in list_of_weather:
    c.execute(
        """INSERT INTO weather VALUES 
            (:city,
                :cloudiness,
                :country,
                :date,
                :humidity,
                :lat,
                :lng,
                :max_temp,
                :wind_speed)""",
            {"city":city_weather.city,
                "cloudiness":city_weather.cloudiness,
                "country":city_weather.country,
                "date":city_weather.date,
                "humidity":city_weather.humidity,
                "lat":city_weather.lat,
                "lng":city_weather.lng,
                "max_temp":city_weather.max_temp,
                "wind_speed":city_weather.wind_speed})