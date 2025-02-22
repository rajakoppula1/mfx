import math

def calculate_distance(coord1, coord2):
    """
    Calculate the Haversine distance between two points on the earth (specified in decimal degrees).
    
    Parameters:
    coord1 (tuple): A tuple (latitude, longitude) for the first location.
    coord2 (tuple): A tuple (latitude, longitude) for the second location.
    
    Returns:
    float: The distance between the two points in kilometers.
    """
    
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371  # Radius of Earth in kilometers

    # Convert latitude and longitude from degrees to radians
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    # Haversine formula
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # Distance in kilometers
