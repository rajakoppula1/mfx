import pandas as pd
from geopy.distance import geodesic

# Load the Excel file
file_path = '/Users/rajasimhakoppula/Downloads/Zip Tracker.xlsx'  # Your file path
zip_codes_data = pd.read_excel(file_path, sheet_name='ZIP Codes')
data_tab = pd.read_excel(file_path, sheet_name='Data')
opportunities_data = pd.read_excel(file_path, sheet_name='list')

# Print the headers to debug
print(opportunities_data.columns)

# Extract relevant columns from the opportunities data
opportunities_data = opportunities_data[['Business Name', 'Adress', 'Zip Code', 'Lat', 'long']].rename(columns={'long': 'Lon'})

# Initialize results list
results = []

# Process each opportunity
for _, opportunity in opportunities_data.iterrows():
    opp_dc_lat_lon = (opportunity["Lat"], opportunity["Lon"])
    consumer_tire_potential = 0
    current_plt_units = 0

    # Calculate distance to each US Zip
    for _, row in zip_codes_data.iterrows():
        us_zip_lat_lon = (row["Lat"], row["Lon"])
        distance = geodesic(opp_dc_lat_lon, us_zip_lat_lon).miles

        if distance <= 110:  # Only consider US Zips within 110 miles
            consumer_tire_potential += row['Annual PLT Potential'] if pd.notnull(row['Annual PLT Potential']) else 0
            current_plt_units += row['FY 23 NTW PLT Units'] if pd.notnull(row['FY 23 NTW PLT Units']) else 0

            # Append result for this US Zip
            results.append({
                "Business Name": opportunity["Business Name"],
                "Address": opportunity["Adress"],
                "Opportunity DC": opportunity["Zip Code"],
                "US Zip": row["ZIP_CODE"],
                "Distance (miles)": distance,
                "Consumer Tire Potential within 110 Miles": consumer_tire_potential,
                "Current PLT Market Share": (current_plt_units / consumer_tire_potential) if consumer_tire_potential else 0,
                "Potential Market Share": consumer_tire_potential * 0.2,
                "DMA": ""  # Add DMA information if available
            })

# Convert the results into a DataFrame
results_df = pd.DataFrame(results)

# Save the results to a new Excel file
output_file_path = '/Users/rajasimhakoppula/Downloads/Tire_Market_Potential_Analysis_Results.xlsx'  # Specify your desired output path
results_df.to_excel(output_file_path, index=False, sheet_name="Analysis Results")

print("Analysis complete! Results saved to:", output_file_path)
