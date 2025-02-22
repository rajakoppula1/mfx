# Project Documentation

## Index
1. `database.py` - Manages database connections, table creation, and data retrieval.
2. `distance_calculator.py` - Calculates the distance between two locations using latitude and longitude.
3. `user_data.py` - (Planned) Allows users to add custom values and categories to ZIP codes.
4. `main.py` - (Planned) Main controller to integrate modules and manage user interaction.

## distance_calculator.py Module

### Purpose
The `distance_calculator.py` module calculates the distance between two ZIP code locations using the Haversine formula. This formula is accurate for calculating distances over the earth’s surface, making it suitable for your app.

### Code Explanation
- **Function `calculate_distance(coord1, coord2)`**: This function takes in two coordinates (latitude, longitude) as tuples.
- **Haversine Formula**: It converts coordinates from degrees to radians, then uses the Haversine formula to compute the great-circle distance in kilometers.
- **Return Value**: The distance in kilometers between the two points.
## conversion.py Module

### Purpose
The `conversion.py` module provides a simple function to convert distances from kilometers to miles.

### Functionality
- **Function `km_to_miles(km)`**: Takes a distance in kilometers and converts it to miles using the conversion factor (1 km ≈ 0.621371 miles).

This module can be used alongside the `distance_calculator.py` to easily switch between kilometers and miles when displaying distances.

This module is designed to keep the distance logic separate from database or user interface code, making it reusable for other applications if needed.
