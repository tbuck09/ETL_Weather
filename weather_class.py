# City,Cloudiness,Country,Date,Humidity,Lat,Lng,Max Temp,Wind Speed
class Weather:
    """A Weather Class for entering rows into weather.db"""
    def __init__(self,city,cloudiness,country,date,humidity,lat,lng,max_temp,wind_speed):
        self.city= city
        self.cloudiness= cloudiness
        self.country= country
        self.date= date
        self.humidity= humidity
        self.lat= lat
        self.lng= lng
        self.max_temp= max_temp
        self.wind_speed= wind_speed