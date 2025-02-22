import pandas as pd
from geopy.distance import geodesic
import numpy as np
import os
import shutil

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# File path to the original Excel file (source file location)
original_file_path = '/Users/rajasimhakoppula/Downloads/NTW DCs.xlsx'

# Define the new location for the source file in the same folder as the script
source_file_path = os.path.join(script_dir, 'NTW DCs.xlsx')

# Copy the source Excel file to the script's directory
shutil.copy(original_file_path, source_file_path)

# Load the ZIP Codes and NTW DC tabs into DataFrames from the copied file
zip_codes_df = pd.read_excel(source_file_path, sheet_name='ZIP Codes')
dc_df = pd.read_excel(source_file_path, sheet_name='NTW DC')

# Define required columns for validation
required_columns_zip = ['ZIP_CODE', 'Lat', 'Lon']
required_columns_dc = ['NTW - SAP Location', 'Market Name', 'City', 'State', 'Zip']

# Validate required columns
for col in required_columns_zip:
    if col not in zip_codes_df.columns:
        raise ValueError(f"Missing required column '{col}' in ZIP Codes sheet.")
for col in required_columns_dc:
    if col not in dc_df.columns:
        raise ValueError(f"Missing required column '{col}' in NTW DC sheet.")

# Merge NTW DC DataFrame with ZIP Codes to get latitude and longitude for each DC
dc_merged_df = pd.merge(dc_df, zip_codes_df, left_on='Zip', right_on='ZIP_CODE', how='left')

# Function to calculate distance between two points
def calculate_distance(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).miles

# Function to create a bounding box
from geopy.distance import distance
def create_bounding_box(lat, lon, radius):
    north = distance(miles=radius).destination((lat, lon), 0)[0]
    south = distance(miles=radius).destination((lat, lon), 180)[0]
    east = distance(miles=radius).destination((lat, lon), 90)[1]
    west = distance(miles=radius).destination((lat, lon), 270)[1]
    return south, north, west, east

# Initialize a list to store results
results = []

# Iterate over each distribution center (DC)
for _, dc in dc_merged_df.iterrows():
    dc_lat = dc['Lat']
    dc_lon = dc['Lon']
    
    if pd.notnull(dc_lat) and pd.notnull(dc_lon):
        min_lat, max_lat, min_lon, max_lon = create_bounding_box(dc_lat, dc_lon, 100)
        filtered_zip_codes = zip_codes_df[
            (zip_codes_df['Lat'] >= min_lat) & 
            (zip_codes_df['Lat'] <= max_lat) & 
            (zip_codes_df['Lon'] >= min_lon) & 
            (zip_codes_df['Lon'] <= max_lon)
        ].copy()  # Use .copy() to avoid SettingWithCopyWarning
        
        # Calculate precise distances and filter within 100 miles
        filtered_zip_codes.loc[:, 'Distance'] = filtered_zip_codes.apply(
            lambda row: calculate_distance(dc_lat, dc_lon, row['Lat'], row['Lon']) 
            if pd.notnull(row['Lat']) and pd.notnull(row['Lon']) else np.nan, axis=1
        )
        within_radius = filtered_zip_codes[filtered_zip_codes['Distance'] <= 100]
        
        for _, zip_code in within_radius.iterrows():
            results.append({
                'DC (NTW-SAP Location)': dc['NTW - SAP Location'],
                'DMA Name (Market Name)': dc['Market Name'],
                'City': dc['City'],
                'State': dc['State'],
                'Zip': dc['Zip'],
                'ZIP Code within 100 miles': zip_code['ZIP_CODE'],
                'Distance (Miles)': zip_code['Distance']
            })

# Convert results into a DataFrame
results_df = pd.DataFrame(results)

# Define the output file path based on the script's directory
output_file_path = os.path.join(script_dir, 'ZIP_Codes_within_100_miles.xlsx')

# Save the results to an Excel file with an extra sheet for file details
with pd.ExcelWriter(output_file_path) as writer:
    results_df.to_excel(writer, index=False, sheet_name='Results')
    
    # Adding a new sheet with information about the source file
    file_info = pd.DataFrame({
        'Details': [
            'Source file name: NTW DCs.xlsx',
            'Location: Same directory as the script',
            'Used sheets: ZIP Codes and NTW DC',
            'Purpose: To provide ZIP codes and DC details for distance calculation'
        ]
    })
    file_info.to_excel(writer, index=False, sheet_name='File Info')