# region Importing libraries
import datetime
import time
from opensky_api import OpenSkyApi
import requests
import openpyxl as xl
# endregion

# region Importing sources
try:
    print("Importing sources...")
    fixes_Workbook = xl.load_workbook('fixes.xlsx')
    airports_Workbook = xl.load_workbook('airports.xlsx')
    print("Sources imported successfully.")
except Exception as e:
    print(f"Error importing sources: {e}")
    
fixes = fixes_Workbook.active
airports = airports_Workbook.active
# endregion
# region OpenSky API Setup
# Use your credentials to ensure authentication is attempted
print("Setting up OpenSky API connection...")
api = OpenSkyApi()

# region Time Conversion Functions

# Function to convert a specific date and time to a Unix timestamp (seconds since epoch)
def to_unix(year, month, day, hour, minute, second):
    # 1. Create a datetime object and explicitly set the timezone to UTC.
    dt = datetime.datetime(
        year, month, day, hour, minute, second, 
        tzinfo=datetime.timezone.utc 
    )
    # 2. Convert the UTC datetime object to a Unix timestamp (seconds).
    unix_time = int(dt.timestamp())
    return unix_time

def to_utc(unix_time):
    """
    Converts a Unix timestamp (seconds) to a timezone-aware UTC datetime object.
    This replaces the deprecated datetime.utcfromtimestamp().
    """
    # Use fromtimestamp() and explicitly set the timezone to UTC
    # datetime.UTC is an alias for datetime.timezone.utc available since Python 3.11
    return datetime.datetime.fromtimestamp(unix_time, tz=datetime.timezone.utc)
# endregion

# Setting the bounding box for the area of interest (Hungary)
min_lat, min_long, max_lat, max_long = 45.7, 16.0, 48.6, 22.9

active_flights = api.get_states(bbox=(min_lat, max_lat, min_long, max_long))
print(f"Number of active flights in the area: {len(active_flights.states)}")
# endregion
# region AviationStack setup & API call

# Loading the personal API key
import json
with open('aviationstack_key.json') as f:
    config = json.load(f)
    
AVSTACK_API_KEY = config['aviationstack_key']
BASE_URL = 'http://api.aviationstack.com/v1/flights'


def fetch_avData():
    arrival_flights = []
    departure_flights = []
    
    try:
        arrival_params = {
        'access_key': AVSTACK_API_KEY,
        # 'flight_date': f"{datetime.datetime.now().year}-{datetime.datetime.now().month}-{datetime.datetime.now().day}",
        'flight_status': 'landed',
        'arr_icao': 'LHBP',
        'limit': 20
        }
        departure_params = {
        'access_key': AVSTACK_API_KEY,
        # 'flight_date': f"{datetime.datetime.now().year}-{datetime.datetime.now().month}-{datetime.datetime.now().day}",
        'dep_icao': 'LHBP',
        'flight_status': 'landed',
        'limit': 20
        }
        
        departure_response = requests.get(BASE_URL, params=departure_params)
        departure_response.raise_for_status()  # Check for HTTP errors
        departure_data = departure_response.json()
            
        arrival_response = requests.get(BASE_URL, params=arrival_params)
        arrival_response.raise_for_status()  # Check for HTTP errors
        arrival_data = arrival_response.json()
            
        departures = departure_data.get('data', [])
        arrivals = arrival_data.get('data', [])
        
        for flight in departures:
            print(f"Flight {flight['flight']['iata']} is departing from Budapest Airport (LHBP)")
            
        for flight in arrivals:
            print(f"Flight {flight['flight']['iata']} is arriving at Budapest Airport (LHBP)")
            
    except (FileNotFoundError, KeyError, ValueError, RuntimeError, requests.exceptions.RequestException) as e:
        print(f"Error fetching AviationStack data: {e}")
    
    
    
    
if __name__ == "__main__":
    fetch_avData()
# endregion