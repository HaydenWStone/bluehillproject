import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import StringIO
import numpy as np
from scipy.stats import linregress

# Function to fetch and read CSV data from a URL
def fetch_csv_data(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure we notice bad responses
    csv_content = StringIO(response.text)
    return pd.read_csv(csv_content)

# Fetch and prepare the summary stats data
url_summary = 'https://raw.githubusercontent.com/HaydenWStone/bluehillproject/main/data/summary_stats_by_day.csv'
summary_data = fetch_csv_data(url_summary)

# Convert 'Month-Day' to datetime, coerce errors to NaT
summary_data['Date'] = pd.to_datetime(summary_data['Month-Day'], format='%m-%d', errors='coerce')

# Drop rows with NaT in 'Date'
summary_data = summary_data.dropna(subset=['Date'])

# Sort by date
summary_data = summary_data.sort_values('Date')

# Plot TMAX_mean and TMIN_mean
plt.figure(figsize=(12, 6))
plt.plot(summary_data['Date'], summary_data['TMAX_mean'], label='TMAX_mean', color='red')
plt.plot(summary_data['Date'], summary_data['TMIN_mean'], label='TMIN_mean', color='blue')
plt.fill_between(summary_data['Date'], summary_data['TMAX_mean'], summary_data['TMIN_mean'], color='gray', alpha=0.1)
plt.title('Daily Mean Low and High Temperatures at Blue Hill (1893 - Present)')
plt.xlabel('Date')
plt.ylabel('Temperature (°F)')
plt.legend()
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(30))
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b'))
plt.grid(True)
plt.savefig('/home/swieyeinthesky/bluehillproject/data/visuals/calendar_day_mean_temps.png')
plt.show()

# Plot PRCP_mean
plt.figure(figsize=(12, 6))
plt.plot(summary_data['Date'], summary_data['PRCP_mean'], label='PRCP_mean', color='green')
plt.title('Daily Mean Precipitation at Blue Hill (1893 - Present)')
plt.xlabel('Date')
plt.ylabel('Precipitation (Inches)')
plt.legend()
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(30))
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b'))
plt.grid(True)
plt.savefig('/home/swieyeinthesky/bluehillproject/data/visuals/calendar_day_mean_precip.png')
plt.show()

# Plot TMAX_std
plt.figure(figsize=(12, 6))
plt.plot(summary_data['Date'], summary_data['TMAX_std'], label='TMAX_std', color='red')
plt.title('Standard Deviations of Daily High Temps at Blue Hill (1893 - Present)')
plt.xlabel('Date')
plt.ylabel('Temperature (°F)')
plt.legend()
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(30))
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b'))
plt.grid(True)
plt.savefig('/home/swieyeinthesky/bluehillproject/data/visuals/calendar_day_hightemp_stds.png')
plt.show()

# Plot PRCP_odds
plt.figure(figsize=(12, 6))
plt.plot(summary_data['Date'], summary_data['PRCP_odds'], label='PRCP_odds', color='purple')
plt.title('Probability of Precipitation at Blue Hill (1893 - Present)')
plt.xlabel('Date')
plt.ylabel('Probability of Precipitation')
plt.legend()
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(30))
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b'))
plt.grid(True)
plt.savefig('/home/swieyeinthesky/bluehillproject/data/visuals/calendar_day_prcp_odds.png')
plt.show()

# Fetch and prepare the detailed Blue Hill data
url_detail = 'https://raw.githubusercontent.com/HaydenWStone/bluehillproject/main/data/blue_hill.csv'
detailed_data = fetch_csv_data(url_detail)

# Clean and preprocess the data
detailed_data['Date'] = pd.to_datetime(detailed_data['Date'])
detailed_data = detailed_data[['Date', 'TMAX']].dropna()
current_year = pd.to_datetime('today').year
detailed_data = detailed_data[detailed_data['Date'].dt.year < current_year]
detailed_data['Year'] = detailed_data['Date'].dt.year

# Calculate the average TMAX for each year
annual_avg_tmax = detailed_data.groupby('Year')['TMAX'].mean().reset_index()

# Apply a rolling average to smooth the data
annual_avg_tmax['TMAX_smoothed'] = annual_avg_tmax['TMAX'].rolling(window=10, min_periods=1).mean()

# Calculate the trend line using linear regression
slope, intercept, r_value, p_value, std_err = linregress(annual_avg_tmax['Year'], annual_avg_tmax['TMAX'])
trend_line = intercept + slope * annual_avg_tmax['Year']

# Plot the annual averages, smoothed trend, and trend line
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
