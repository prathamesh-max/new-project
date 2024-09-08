import pandas as pd

# Read the Excel file
df = pd.read_excel('flight_tickets_data/flights_low_2024-09-08.xlsx')

# Convert DataFrame to HTML
html_table = df.to_html(index=False)

# Save HTML table to a file
with open('"E:\OneDrive\Desktop\gitinfo\username.github.io"/low_prices_table.html', 'w') as f:
    f.write(html_table)
