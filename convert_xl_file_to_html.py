import pandas as pd
from datetime import datetime
import os

def read_low_prices(file_path):
    # Read Excel file using openpyxl engine
    df_low = pd.read_excel(file_path, engine='openpyxl')
    return df_low

def convert_to_html(df, file_name):
    html = df.to_html(index=False)
    with open(file_name, 'w') as file:
        file.write(html)
    print(f"HTML file saved to {file_name}")

if __name__ == "__main__":
    # Define file paths
    excel_file_path = 'flight_tickets_data/flights_low_2024-09-08.xlsx'  # Update with the actual path
    html_file_path = 'low_prices_table.html'
    
    # Read and convert data
    df_low = read_low_prices(excel_file_path)
    convert_to_html(df_low, html_file_path)
