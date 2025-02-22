from distance_calculator import calculate_distance
from conversion import km_to_miles
from radius_search import find_zip_codes_within_radius
from database import connect_db, get_coordinates

def main():
    conn = connect_db('/Users/rajasimhakoppula/Documents/mfx/App/PRAG/data/spatial_analysis.db')
    
    action = input("Choose an action: 'distance' to measure distance or 'radius' to find nearby ZIP codes: ").strip().lower()
    
    if action == "distance":
        zip1 = input("Enter the first ZIP code: ").strip()
        zip2 = input("Enter the second ZIP code: ").strip()
        coord1 = get_coordinates(zip1, conn)
        coord2 = get_coordinates(zip2, conn)
        if coord1 and coord2:
            distance_km = calculate_distance(coord1, coord2)
            unit = input("Would you like the distance in kilometers (km) or miles (mi)? ").strip().lower()
            distance = km_to_miles(distance_km) if unit == "mi" else distance_km
            print(f"Distance between ZIP codes: {distance:.2f} {unit}")
        else:
            print("One or both ZIP codes not found.")
    
    elif action == "radius":
        center_zip = input("Enter the center ZIP code: ").strip()
        radius_unit = input("Enter the radius unit (km for kilometers or mi for miles): ").strip().lower()
        radius = float(input(f"Enter the radius in {radius_unit}: "))
        
        # Convert miles to kilometers if needed
        if radius_unit == "mi":
            radius = radius / 0.621371  # Convert miles to kilometers
        
        zip_codes = find_zip_codes_within_radius(center_zip, radius, conn)
        result_unit = "miles" if radius_unit == "mi" else "kilometers"
        
        print(f"ZIP codes within {radius:.2f} {result_unit} of {center_zip}: {zip_codes}" if zip_codes else f"No ZIP codes found within the specified {result_unit}.")
    
    conn.close()

if __name__ == "__main__":
    main()
