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
    observation = mgr.weather_at_place(loc)
    w = observation.weather

    return (
        "Weather: {}".format(w.detailed_status),         # 'clouds'
        "Wind Speed: {}".format(w.wind()['speed']),                  # {'speed': 4.6, 'deg': 330}
        "Humidity: {}".format(w.humidity),                # 87
        "Temperature: {}".format(w.temperature('fahrenheit')),  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
        "Rain: {}".format(w.rain),                    # {}
        "Heat Index: {}".format(w.heat_index),              # None
        "Clouds: {}".format(w.clouds)                  # 75
        )

# Add a new user to the database
def add_user(conn, name, location):
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (name, location) VALUES (?, ?)", (name, location))
        conn.commit()
        print("User added successfully!")
    except sqlite3.IntegrityError:
        print("User with that email already exists")

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


