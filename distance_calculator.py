from geopy.distance import geodesic

# Starting Coordinates
start_coords = (28.028943, -81.969788)

# Coordinates for each city in the list
cities_coords = {
    "Atlanta": (33.7490, -84.3880),
    "Baltimore": (39.2904, -76.6122),
    "Boston": (42.3601, -71.0589),
    "Charleston": (32.7765, -79.9311),
    "Charlotte": (35.2271, -80.8431),
    "Chicago": (41.8781, -87.6298),
    "Cincinnati": (39.1031, -84.5120),
    "Cleveland": (41.4993, -81.6944),
    "Columbus": (39.9612, -82.9988),
    "Dallas": (32.7767, -96.7970),
    "Denver": (39.7392, -104.9903),
    "Detroit": (42.3314, -83.0458),
    "El Paso": (31.7619, -106.4850),
    "Houston": (29.7604, -95.3698),
    "Jacksonville": (30.3322, -81.6557),
    "Kansas City": (39.0997, -94.5786),
    "Long Beach": (33.7701, -118.1937),
    "Louisville": (38.2527, -85.7585),
    "Memphis": (35.1495, -90.0490),
    "Miami": (25.7617, -80.1918),
    "Minneapolis": (44.9778, -93.2650),
    "Mobile": (30.6954, -88.0399),
    "Nashville": (36.1627, -86.7816),
    "New Orleans": (29.9511, -90.0715),
    "New York": (40.7128, -74.0060),
    "Norfolk": (36.8508, -76.2859),
    "Oakland": (37.8044, -122.2711),
    "Omaha": (41.2565, -95.9345),
    "Phoenix": (33.4484, -112.0740),
    "Portland": (45.5152, -122.6784),
    "Salt Lake City": (40.7608, -111.8910),
    "Savannah": (32.0809, -81.0912),
    "Tacoma": (47.2529, -122.4443),
    "St. Louis": (38.6270, -90.1994),
    "Tampa": (27.9506, -82.4572),
}

# Calculate the distance from Pewaukee to each city
distances = {city: geodesic(start_coords, coords).miles for city, coords in cities_coords.items()}

# Sort the cities by distance
sorted_cities = sorted(distances.items(), key=lambda item: item[1])

# Get the top 5 closest cities
top_5_closest = sorted_cities[:5]

# Print the top 5 closest cities and their distances
for city, distance in top_5_closest:
    print(f"{city}: {distance:.2f} miles")