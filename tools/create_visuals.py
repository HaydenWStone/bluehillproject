import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import StringIO
import numpy as np
from scipy.stats import linregress

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




# Plot PRCP_mean
plt.figure(figsize=(12, 6))
plt.plot(data['Date'], data['PRCP_mean'], label='PRCP_mean', color='green')
plt.title('Daily Mean Precipitation at Blue Hill (1893 - Present)')
plt.xlabel('Date')
plt.ylabel('Precipitation (Inches)')
plt.legend()

# Set x-axis major ticks to monthly intervals
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(30))
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b'))

plt.grid(True)

# Save the plot as an image
plt.savefig('/home/swieyeinthesky/bluehillproject/data/visuals/calendar_day_mean_precip.png')

plt.show()




# Plot TMAX_std
plt.figure(figsize=(12, 6))
plt.plot(data['Date'], data['TMAX_std'], label='TMAX_std', color='red')
plt.title('Standard Deviations of Daily High Temps at Blue Hill (1893 - Present)')
plt.xlabel('Date')
plt.ylabel('Temperature (°F)')
plt.legend()

# Set x-axis major ticks to monthly intervals
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(30))
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b'))

plt.grid(True)

# Save the plot as an image
plt.savefig('/home/swieyeinthesky/bluehillproject/data/visuals/calendar_day_hightemp_stds.png')

plt.show()






# Step 1: Load the data
url = 'https://raw.githubusercontent.com/HaydenWStone/bluehillproject/main/data/blue_hill.csv'
response = requests.get(url)
data = StringIO(response.text)
df = pd.read_csv(data)

# Step 2: Clean and preprocess the data
df['Date'] = pd.to_datetime(df['Date'])  # Ensure the date is in datetime format
df = df[['Date', 'TMAX']]  # Keep only relevant columns
df = df.dropna()  # Drop missing values

# Step 3: Exclude data from the current year
current_year = pd.to_datetime('today').year
df = df[df['Date'].dt.year < current_year]  # Filter out entries from the current year

# Step 4: Extract year for each date
df['Year'] = df['Date'].dt.year

# Step 5: Calculate the average TMAX for each year
annual_avg_tmax = df.groupby('Year')['TMAX'].mean().reset_index()

# Step 6: Apply a rolling average to smooth the data
annual_avg_tmax['TMAX_smoothed'] = annual_avg_tmax['TMAX'].rolling(window=10, min_periods=1).mean()

# Step 7: Calculate the trend line using linear regression
slope, intercept, r_value, p_value, std_err = linregress(annual_avg_tmax['Year'], annual_avg_tmax['TMAX'])
trend_line = intercept + slope * annual_avg_tmax['Year']

# Step 8: Plot the annual averages, smoothed trend, and trend line
plt.figure(figsize=(14, 8))
plt.plot(annual_avg_tmax['Year'], annual_avg_tmax['TMAX'], marker='o', linestyle='-', color='lightgrey', label='Annual Avg TMAX')
plt.plot(annual_avg_tmax['Year'], annual_avg_tmax['TMAX_smoothed'], color='blue', linewidth=2.5, label='Smoothed Trend')
plt.plot(annual_avg_tmax['Year'], trend_line, color='red', linestyle='--', linewidth=2, label=f'Trend Line (Slope: {slope:.4f})')

plt.xlabel('Year')
plt.ylabel('Average High Temperature (TMAX)')
plt.title('Trend of Mean Daily High Temps 1893 - Present')
plt.legend()
plt.grid(True)
plt.savefig('/home/swieyeinthesky/bluehillproject/data/visuals/year_trend_high_temps.png')
plt.show()







