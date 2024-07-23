import pandas as pd

# Path to the local CSV file
file_path = '/home/swieyeinthesky/bluehillproject/data/blue_hill.csv'

# Read the CSV file into a DataFrame
blue_hill_data = pd.read_csv(file_path)

# Ensure the 'Date' column is of datetime type
blue_hill_data['Date'] = pd.to_datetime(blue_hill_data['Date'])

# Extract Month-Day from the Date column
blue_hill_data['Month-Day'] = blue_hill_data['Date'].dt.strftime('%m-%d')

# Group by Month-Day and calculate mean and standard deviation for PRCP, TMAX, and TMIN
mean_values = blue_hill_data.groupby('Month-Day')[['PRCP', 'TMAX', 'TMIN']].mean().reset_index()
std_dev_values = blue_hill_data.groupby('Month-Day')[['PRCP', 'TMAX', 'TMIN']].std().reset_index()

# Merge the mean and standard deviation DataFrames
summary_stats = pd.merge(mean_values, std_dev_values, on='Month-Day', suffixes=('_mean', '_std'))

# Display the results
print(summary_stats)

# Save the results to a CSV file
summary_stats.to_csv('/home/swieyeinthesky/bluehillproject/data/summary_stats_by_day.csv', index=False)
