import datetime
import time
from opensky_api import OpenSkyApi as osky

# Use your credentials to ensure authentication is attempted
api = osky()

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

