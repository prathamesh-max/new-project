import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

def scrape_flight_data():
    # URL of the website you're scraping (update this with the actual site)
    url = "https://www.example.com/flights"
    
    # Fetch the website's content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Extract flight data (adjust based on actual HTML structure)
    flight_data = []
    flights = soup.find_all('div', class_='flight-info')  # Example tag and class
    
    for flight in flights:
        departure = flight.find('span', class_='departure').text
        arrival = flight.find('span', class_='arrival').text
        price = flight.find('span', class_='price').text
        date = flight.find('span', class_='date').text

        # Append data to the list
        flight_data.append({
            'Departure': departure,
            'Arrival': arrival,
            'Price': price,
            'Date': date
        })

    # Create a pandas DataFrame from the list
    df = pd.DataFrame(flight_data)

    # Save to an Excel file
    save_to_excel(df)

def save_to_excel(df):
    # Create directory if it doesn't exist
    folder_path = 'flight_data'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Save the file with the current date
    date_today = datetime.now().strftime('%Y-%m-%d')
    file_name = f"{folder_path}/flights_{date_today}.xlsx"
    
    # Save DataFrame to Excel file
    df.to_excel(file_name, index=False)
    print(f"Flight data saved to {file_name}")

if __name__ == "__main__":
    scrape_flight_data()
