import pandas as pd
import requests
from io import StringIO

# URL to the remote CSV file on GitHub
file_url = 'https://raw.githubusercontent.com/HaydenWStone/bluehillproject/main/data/blue_hill.csv'

# Fetch the CSV file from the URL
response = requests.get(file_url)
response.raise_for_status()  # Ensure we notice bad responses

# Read the CSV file into a DataFrame
blue_hill_data = pd.read_csv(StringIO(response.text))

# Ensure the 'Date' column is of datetime type
blue_hill_data['Date'] = pd.to_datetime(blue_hill_data['Date'])

# Extract Month-Day from the Date column
blue_hill_data['Month-Day'] = blue_hill_data['Date'].dt.strftime('%m-%d')

# Group by Month-Day and calculate mean and standard deviation for PRCP, TMAX, and TMIN
mean_values = blue_hill_data.groupby('Month-Day')[['PRCP', 'TMAX', 'TMIN']].mean().reset_index()
std_dev_values = blue_hill_data.groupby('Month-Day')[['PRCP', 'TMAX', 'TMIN']].std().reset_index()

# Calculate the total number of days and number of days with PRCP > 0
total_days = blue_hill_data.groupby('Month-Day')['PRCP'].count().reset_index(name='total_days')
days_with_prcp = blue_hill_data[blue_hill_data['PRCP'] > 0].groupby('Month-Day')['PRCP'].count().reset_index(name='days_with_prcp')

# Merge the total days and days with PRCP > 0 into a single DataFrame
prcp_stats = pd.merge(total_days, days_with_prcp, on='Month-Day', how='left')
prcp_stats['days_with_prcp'] = prcp_stats['days_with_prcp'].fillna(0)  # Handle any NaNs from the merge

# Calculate the probability of days with PRCP > 0
prcp_stats['PRCP_odds'] = prcp_stats['days_with_prcp'] / prcp_stats['total_days']

# Merge the mean, standard deviation, and PRCP odds DataFrames
summary_stats = pd.merge(mean_values, std_dev_values, on='Month-Day', suffixes=('_mean', '_std'))
summary_stats = pd.merge(summary_stats, prcp_stats[['Month-Day', 'PRCP_odds']], on='Month-Day')

# Display the results
print(summary_stats)

# Save the results to a CSV file
summary_stats.to_csv('/home/swieyeinthesky/bluehillproject/data/summary_stats_by_day.csv', index=False)
