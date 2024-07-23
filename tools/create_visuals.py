import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import StringIO

# Fetch the CSV file from the URL
url = 'https://raw.githubusercontent.com/HaydenWStone/bluehillproject/main/data/summary_stats_by_day.csv'
response = requests.get(url)
response.raise_for_status()  # Check that the request was successful

# Read the CSV content
csv_content = StringIO(response.text)
data = pd.read_csv(csv_content)

# Convert 'Month-Day' to datetime, coerce errors to NaT
data['Date'] = pd.to_datetime(data['Month-Day'], format='%m-%d', errors='coerce')

# Drop rows with NaT in 'Date'
data = data.dropna(subset=['Date'])

# Sort by date
data = data.sort_values('Date')

# Plot TMAX_mean and TMIN_mean
plt.figure(figsize=(12, 6))
plt.plot(data['Date'], data['TMAX_mean'], label='TMAX_mean', color='red')
plt.plot(data['Date'], data['TMIN_mean'], label='TMIN_mean', color='blue')
plt.fill_between(data['Date'], data['TMAX_mean'], data['TMIN_mean'], color='gray', alpha=0.1)
plt.title('Daily Mean Low and High Temperatures at Blue Hill (1893 - Present)')
plt.xlabel('Date')
plt.ylabel('Temperature (°F)')
plt.legend()

# Set x-axis major ticks to monthly intervals
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(30))
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b'))

plt.grid(True)

# Save the plot as an image
plt.savefig('/home/swieyeinthesky/bluehillproject/data/visuals/calendar_day_mean_temps.png')

plt.show()
