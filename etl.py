
import json
import sqlite3
from datetime import datetime

# EXTRACT
with open("raw_data.json", "r") as file:
    raw_data = json.load(file)

weather = raw_data["data"]

print("Data extracted successfully")

# TRANSFORM
city = weather["city_name"]
temperature = weather["temp_kelvin"] - 273.15
humidity = int(weather["humidity"].replace("%", ""))
wind_speed = weather["wind"]["speed"]
wind_direction = weather["wind"]["direction"]

timestamp = datetime.fromtimestamp(
    raw_data["metadata"]["timestamp"]
)

print("\nTransformed Weather Data")
print("City:", city)
print("Temperature:", round(temperature, 2), "°C")
print("Humidity:", humidity, "%")
print("Wind Speed:", wind_speed)
print("Wind Direction:", wind_direction)

# LOAD
connection = sqlite3.connect("weather.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        temperature REAL,
        humidity INTEGER,
        wind_speed REAL,
        wind_direction TEXT,
        recorded_at TEXT
    )
""")

cursor.execute("""
    INSERT INTO weather
    (city, temperature, humidity, wind_speed,
     wind_direction, recorded_at)
    VALUES (?, ?, ?, ?, ?, ?)
""", (
    city,
    round(temperature, 2),
    humidity,
    wind_speed,
    wind_direction,
    timestamp.isoformat()
))

connection.commit()

print("\nData loaded successfully into SQLite!")

connection.close()
