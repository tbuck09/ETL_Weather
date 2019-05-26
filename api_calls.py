#####
# Import Dependencies
#####

# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
import os
import datetime

# Import API key
from api_keys import api_key

# Incorporated citipy to determine city based on latitude and longitude
from citipy import citipy


#####
# Generate cities list
#####

# Output File (CSV)
# output_data_file = "output_data/cities.csv"

# Range of latitudes and longitudes
lat_range = (-90, 90)
lng_range = (-180, 180)

# List for holding lat_lngs and cities
lat_lngs = []
cities = []

# Create a set of random lat and lng combinations
lats = np.random.uniform(low=-90.000, high=90.000, size=200)
lngs = np.random.uniform(low=-180.000, high=180.000, size=200)
lat_lngs = zip(lats, lngs)

# Identify nearest city for each lat, lng combination
for lat_lng in lat_lngs:
    city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name
    
    # If the city is unique, then add it to a our cities list
    if city not in cities:
        cities.append(city)

# Print the city count to confirm sufficient count
len(cities)


#####
# Perform API Calls
# * Perform a weather check on each city using a series of successive API calls.
# * Include a print log of each city as it'sbeing processed (with the city number and city name).
#####

#Initialize DataFrame
city_weather_df= pd.DataFrame({
    "City": cities,
    "Cloudiness": "",
    "Country": "",
    "Date": "",
    "Humidity": "",
    "Lat": "",
    "Lng": "",
    "Max Temp": "",
    "Wind Speed": ""
})

#Set index to "City" column
city_weather_df.set_index("City", inplace= True)

#Set variables for URL and API Key
base_url= "https://api.openweathermap.org/data/2.5/weather?q="
appid= api_key

#Initialize Set Number
set_no= 1
#Gather number of sets necessary to run all iterations without exceeding OWM's requests per minute for free accounts
#The int() function rounds the float down to the nearest integer; + 1 has the effect of rounding up.  
all_sets= int(len(cities)/60) + 1

#Begin the outer loop, iterating each set
for i in range(0,all_sets):
#Reset Record Number to 1 at the start of the set
    record_no= 1
#Increment start in intervals of 60, beginning with 0
    start= i*60
#Increment end in intervals of 60, beginning with 60 (this number is excluded in the df.iloc split)
    end= start + 60

#Begin inner loop, iterating each record
    for city, row in city_weather_df.iloc[start:end,:].iterrows():

#Save the result of the request into a variable
        response= requests.get(f"{base_url}{city}&appid={appid}")

#If the Status Code is 200 (presumed successful)...
        if response.status_code == 200:
#...gather information from the response and save it to the DataFrame for the current row.
            row["Cloudiness"]= response.json()["clouds"]["all"]
            row["Country"]= response.json()["sys"]["country"]
            row["Date"]= response.json()["dt"]
            row["Humidity"]= response.json()["main"]["humidity"]
            row["Lat"]= response.json()["coord"]["lat"]
            row["Lng"]= response.json()["coord"]["lon"]
            row["Max Temp"]= response.json()["main"]["temp_max"]
            row["Wind Speed"]= response.json()["wind"]["speed"]
#Print success record
            print(f"Processing Record {record_no} of Set {set_no} | {city.title()}")
#Move to the next Record Number
            record_no= record_no + 1

#If the Status Code was not 200 (presumed unsuccessful)...
        else:
#Note the failure
            print(f"{city.title()} **not** found. Skipping...")

#Move to the next Set Number
    set_no= set_no + 1
#Run time.sleep() on all sets, excluding the last.
    while set_no <= all_sets:
        time.sleep(60)
        break

#Present the DataFrame
city_weather_df.head()

#Remove failures from the DataFrame (all rows are empty; "Cloudiness" was selected arbitrarily as this is the first column)
city_weather_df_no_na= city_weather_df.loc[city_weather_df["Cloudiness"] != ""]


#####
# Convert Raw Data to DataFrame
# * Export the city data into a .csv.
# * Display the DataFrame
#####

#I wanted to save multiple graphs for comparison
#Get local datetime
now= datetime.datetime.now()
#Format datetime for use in the Titles of the graphs
now_figtitle= now.strftime("%m/%d/%y")
#Format datetime for use when naming the csv and png files
now_savefig= now.strftime("%d%b%Y_%H%M").upper()

#Overwrite any csv that may be there...
city_weather_df_no_na.to_csv(f"resources/City_Weather.csv")

#...but save it to a unique ID for comparison as well.
#Save the cleaned DataFrame to a csv
city_weather_df_no_na.to_csv(f"resources/City_Weather_{now_savefig}.csv")
#Resave the cleaned csv to replace the original DataFrame (not necessary, but this variable name looks better in the analysis)
city_weather_df= pd.read_csv(f"resources/City_Weather_{now_savefig}.csv")
#Present the DataFrame
city_weather_df.head()


#####
#####
# Plotting the Data
# * Use proper labeling of the plots using plot titles (including date of analysis) and axes labels.
# * Save the plotted figures as .pngs.
#####
#####


#####
# Latitude vs. Temperature Plot
#####

#Plot the data
plt.scatter(
    city_weather_df["Lat"],
#Convert from Kelvins to Fahrenheit
    (city_weather_df["Max Temp"]- 273.15) * 9/5 + 32,
    edgecolors="k",
)

#Add plot elements
plt.title(f"City Latitude vs. Max Temperature ({now_figtitle})")
plt.xlabel("Latitude")
plt.ylabel("Max Temperature (F)")
plt.grid()

#Save the figure (ddMONyyyy_hhmm)
plt.savefig(f"images/MaxTemp_{now_savefig}")


#####
# Latitude vs. Humidity Plot
#####
#Plot the data
plt.scatter(
    city_weather_df["Lat"],
    city_weather_df["Humidity"],
    edgecolors="k",
)

#Add plot elements
plt.title(f"City Latitude vs. Humidity ({now_figtitle})")
plt.xlabel("Latitude")
plt.ylabel("Humidity (%)")
plt.grid()

#Save the figure (ddMONyyyy_hhmm)
plt.savefig(f"images/Humidity_{now_savefig}")


#####
# Latitude vs. Cloudiness Plot
#####

#Plot the data
plt.scatter(
    city_weather_df["Lat"],
    city_weather_df["Cloudiness"],
    edgecolors="k",
)

#Add plot elements
plt.title(f"City Latitude vs. Cloudiness ({now_figtitle})")
plt.xlabel("Latitude")
plt.ylabel("Cloudiness (%)")
plt.grid()

#Save the figure (ddMONyyyy_hhmm)
plt.savefig(f"images/Cloudiness_{now_savefig}")


#####
# Latitude vs. Wind Speed Plot
#####

#Plot the data
plt.scatter(
    city_weather_df["Lat"],
    city_weather_df["Wind Speed"],
    edgecolors="k",
)

#Add plot elements
plt.title(f"City Latitude vs. Wind Speed ({now_figtitle})")
plt.xlabel("Latitude")
plt.ylabel("Wind Speed (mph)")
plt.grid()

#Save the figure (ddMONyyyy_hhmm)
plt.savefig(f"images/WindSpeed_{now_savefig}")