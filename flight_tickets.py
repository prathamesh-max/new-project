import requests
import pandas as pd
from datetime import datetime
import os

# Replace with your actual API key and endpoint details
API_KEY = 'a89c6e0e55mshe980c0b00597e2bp1cb818jsn270f55a52ed3'
API_HOST = 'sky-scanner3.p.rapidapi.com'
URL = 'https://sky-scanner3.p.rapidapi.com/flights/cheapest-one-way'

def get_flight_data():
    headers = {
        "x-rapidapi-key": "a89c6e0e55mshe980c0b00597e2bp1cb818jsn270f55a52ed3",
	    "x-rapidapi-host": "sky-scanner3.p.rapidapi.com"
    }
    
    params = {
        "departDate": "2024-10-31",  # Start date for searching flights
        "currency": "EUR",           # Currency for flight prices
        "fromEntityId": "BOM",       # BOM (Mumbai)
        "toEntityId": "FRA"          # FRA (Frankfurt)
    }
    
    try:
        response = requests.get(URL, headers=headers, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()

        # Debugging: Print the API response
        print("API Response:", data)

        if not data.get('status'):
            errors = data.get('errors', {})
            for key, value in errors.items():
                print(f"Error with {key}: {value}")
            print(f"Message: {data.get('message')}")
            return
        
        # Extracting flight data
        flight_data = data.get('data', [])
        if isinstance(flight_data, list):  # Ensure 'data' is a list
            low_group_flights = []
            medium_group_flights = []
            high_group_flights = []
            
            for day in flight_data:
                if isinstance(day, dict):
                    date = day.get('day')  # Extract the date
                    group = day.get('group')  # Extract the group (low, medium, high)
                    price = day.get('price')  # Extract the price

                    # Categorize flights into low, medium, or high groups
                    if group == 'low':
                        low_group_flights.append({
                            'Date': date,
                            'Price': price
                        })
                    elif group == 'medium':
                        medium_group_flights.append({
                            'Date': date,
                            'Price': price
                        })
                    elif group == 'high':
                        high_group_flights.append({
                            'Date': date,
                            'Price': price
                        })

            # Debugging: Print the flight lists
            print("Low Group Flights:", low_group_flights)
            print("Medium Group Flights:", medium_group_flights)
            print("High Group Flights:", high_group_flights)

            # Save low, medium, and high group data to separate Excel files
            if low_group_flights:
                df_low = pd.DataFrame(low_group_flights)
                save_to_excel(df_low, 'low')
            if medium_group_flights:
                df_medium = pd.DataFrame(medium_group_flights)
                save_to_excel(df_medium, 'medium')
            if high_group_flights:
                df_high = pd.DataFrame(high_group_flights)
                save_to_excel(df_high, 'high')
        else:
            print("No valid flight data found.")
            
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def save_to_excel(df, group_type):
    folder_path = 'flight_tickets_data'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    date_today = datetime.now().strftime('%Y-%m-%d')
    file_name = f"{folder_path}/flights_{group_type}_{date_today}.xlsx"
    
    df.to_excel(file_name, index=False)
    print(f"Flight data for {group_type} group saved to {file_name}")

if __name__ == "__main__":
    get_flight_data()
