from geopy.geocoders import OpenCage
from geopy.exc import GeocoderTimedOut

def get_lat_lon_from_zip(zip_code, api_key):
    geolocator = OpenCage(api_key)
    try:
        location = geolocator.geocode(zip_code)
        if location:
            return (location.latitude, location.longitude)
        else:
            return "Location not found"
    except GeocoderTimedOut:
        return "Geocoding service timed out"

# Example usage
api_key = 'ADD_API_KEY_HERE' # Replace with your OpenCage API key
zip_code = '33802 US' # Example ZIP code
coordinates = get_lat_lon_from_zip(zip_code, api_key)
print(f"Latitude and Longitude for ZIP code {zip_code}: {coordinates}")