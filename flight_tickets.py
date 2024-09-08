import requests
import pandas as pd
from datetime import datetime
import os

# Replace with your actual API key and endpoint details
API_KEY = 'a89c6e0e55mshe980c0b00597e2bp1cb818jsn270f55a52ed3'
API_HOST = 'sky-scanner3.p.rapidapi.com'  # Replace with the actual host provided by RapidAPI
URL = 'https://sky-scanner3.p.rapidapi.com/flights/search-one-way'  # Replace with the actual endpoint

def get_flight_data():
    headers = {
        "x-rapidapi-key": "a89c6e0e55mshe980c0b00597e2bp1cb818jsn270f55a52ed3",
	"x-rapidapi-host": "sky-scanner3.p.rapidapi.com"
    }
    
    params = {
        "departDate": "2024-10-31",  # Start date for searching flights
        #"date_to": "2024-10-31",  # End date for searching flights
        "currency": "USD",  # Currency for flight prices
        "fromEntityId": "BOM",  # BOM (Mumbai)
        "toEntityId": "FRA"  # FRA (Frankfurt)
    }
    
    try:
        response = requests.get(URL, headers=headers, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        
        if not data.get('status'):
            errors = data.get('errors', {})
            for key, value in errors.items():
                print(f"Error with {key}: {value}")
            print(f"Message: {data.get('message')}")
            return
        
        # Extracting flight data
        flight_quotes = data.get('data', {}).get('flightQuotes', [])
        if flight_quotes:
            # Normalize the data into a DataFrame
            flight_list = []
            for flight in flight_quotes:
                flight_info = flight.get('content', {})
                flight_list.append({
                    'Price': flight_info.get('price'),
                    'Departure Date': flight_info.get('outboundLeg', {}).get('localDepartureDateLabel'),
                    'Direct': flight_info.get('direct')
                })
                
            df = pd.DataFrame(flight_list)
            save_to_excel(df)
        else:
            print("No flights found.")
            
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def save_to_excel(df):
    folder_path = 'flight_data'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    date_today = datetime.now().strftime('%Y-%m-%d')
    file_name = f"{folder_path}/flights_{date_today}.xlsx"
    
    df.to_excel(file_name, index=False)
    print(f"Flight data saved to {file_name}")

if __name__ == "__main__":
    get_flight_data()
