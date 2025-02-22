import pandas as pd
import os

# Load the original file
input_file = "/Users/rajasimhakoppula/Downloads/Zip Codes by DMA.xlsx"
output_folder = "/Users/rajasimhakoppula/Documents/mfx/App/TBC/DatafleX_Output"
output_file = os.path.join(output_folder, "processed_zip_code_data.xlsx")

# Create the output directory if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Read the Excel file into a DataFrame
df = pd.read_excel(input_file)

# Format ZIP_CODE with leading zeros
df['ZIP_CODE'] = df['ZIP_CODE'].apply(lambda x: f"{int(x):05d}")

# Define a function to get the mode of a series, safely
def safe_mode(series):
    if not series.empty:
        mode = series.mode()
        if not mode.empty:
            return mode[0]
    return None

# Group by ZIP_CODE and aggregate the data
grouped = df.groupby('ZIP_CODE').agg({
    'STATE_NAME': lambda x: safe_mode(x),
    'COUNTY_NAME': lambda x: safe_mode(x),
    'DMA_NAME': lambda x: safe_mode(x),
    'No. of Vehicles': 'sum'
}).reset_index()

# Save the processed data to a new Excel file
grouped.to_excel(output_file, index=False)
