import pandas as pd
from datetime import datetime
from meteostat import Point, Daily

import os
BASE_PATH = ""

GEOLOCATIONS = os.path.join(BASE_PATH,"airports_geolocation.csv")
geo_df = pd.read_csv(GEOLOCATIONS)
 
start = datetime(2023, 1, 1)
end = datetime(2023, 1, 1, 23, 59) 

weather_list = []

for i, row in geo_df.iterrows():
    code = row["IATA_CODE"]
    lat = row["LATITUDE"]
    lon = row["LONGITUDE"]

    location = Point(lat, lon)

    data = Daily(location, start, end)
    df = data.fetch()
    df["IATA_CODE"] = code

    weather_list.append(df)

weather_all = pd.concat(weather_list)
print(weather_all.shape)

output_path = "../data/weather_by_airport.csv"
weather_all.to_csv(output_path)
print("Saved weather_by_airport.csv")
