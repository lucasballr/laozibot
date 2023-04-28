from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
import sqlite3
import config

owm_api_key = config.OWM_API_KEY

def get_weather(loc):
    owm = OWM(owm_api_key)
    mgr = owm.weather_manager()

    # Search for current weather in London (Great Britain) and get details
    try:
        current = mgr.weather_at_place(loc)
        forecast = mgr.forecast_at_place(loc, "3h")
    except:
        return "There was an error obtaining weather information"

    tomorrow = timestamps.tomorrow()
    today = timestamps.next_three_hours()
    f_tomorrow = forecast.get_weather_at(tomorrow)
    f_today = forecast.get_weather_at(today)
    

    w = current.weather
    

    return """ Current weather: Weather: {}, Wind Speed: {}, Humidity: {}, Temperature: {}, Rain: {}, Heat Index: {}, Clouds: {}
Today's forecast: Weather: {}, Wind Speed: {}, Humidity: {}, Temperature: {}, Rain: {}, Heat Index: {}, Clouds: {}
Tomorrow's forecast: Weather: {}, Wind Speed: {}, Humidity: {}, Temperature: {}, Rain: {}, Heat Index: {}, Clouds: {}
""".format(w.detailed_status, w.wind()['speed'], w.humidity, w.temperature('fahrenheit'), w.rain, w.heat_index, w.clouds, f_today.detailed_status, f_today.wind()['speed'], f_today.humidity, f_today.temperature('fahrenheit'), f_today.rain, f_today.heat_index, f_today.clouds, f_tomorrow.detailed_status, f_tomorrow.wind()['speed'], f_tomorrow.humidity, f_tomorrow.temperature('fahrenheit'), f_tomorrow.rain, f_tomorrow.heat_index, f_tomorrow.clouds)       

# Add a new user to the database
def add_user(conn, name, location):
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (name, location) VALUES (?, ?)", (name, location))
        conn.commit()
        print("User added successfully!")
    except sqlite3.IntegrityError:
        print("User with that name already exists")

# Update a user's location
def update_location(conn, name, new_location):
    c = conn.cursor()
    c.execute("UPDATE users SET location = ? WHERE name = ?", (new_location, name))
    conn.commit()
    print("Location updated successfully!")

# Get a user's location
def get_location(conn, name):
    c = conn.cursor()
    c.execute("SELECT location FROM users WHERE name = ?", (name,))
    location = c.fetchone()
    if location:
        return location[0]
    else:
        return False

def get_user(conn, name):
    c = conn.cursor()
    c.execute("SELECT name FROM users WHERE name = ?", (name,))
    n = c.fetchone()
    if n:
        return True
    else:
        return False

