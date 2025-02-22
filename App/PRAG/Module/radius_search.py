from distance_calculator import calculate_distance
from database import get_coordinates

def find_zip_codes_within_radius(center_zip, radius, conn):
    """
    Find all ZIP codes within a given radius (in kilometers) from a center ZIP code.
    
    Parameters:
    center_zip (str): The ZIP code from which to measure the radius.
    radius (float): The radius in kilometers.
    conn: SQLite database connection object.
    
    Returns:
    list: A list of ZIP codes within the specified radius.
    """
    center_coords = get_coordinates(center_zip, conn)
    if not center_coords:
        print("Center ZIP code not found.")
        return []

    cursor = conn.cursor()
    cursor.execute("SELECT zip_code, lat, long FROM Locations")
    zip_codes_within_radius = []

    for zip_code, lat, lng in cursor.fetchall():
        distance = calculate_distance(center_coords, (lat, lng))
        if distance <= radius:
            zip_codes_within_radius.append(zip_code)

    return zip_codes_within_radius
