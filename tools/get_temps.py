import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import time
import os

def make_call(year):
    # Load environment variables from .env file
    load_dotenv()

    # Retrieve the token from environment variables
    token = os.getenv('NOAA_API_TOKEN')

    if not token:
        raise ValueError("NOAA API token is not set. Please set the environment variable 'NOAA_API_TOKEN'.")

    # Define the base URL and common parameters
    base_url = 'https://www.ncei.noaa.gov/cdo-web/api/v2/data'
    common_params = {
        'datasetid': 'GHCND',
        'stationid': 'GHCND:USC00190736',
        'datatypeid': 'TMAX,TMIN,PRCP',
        'units': 'standard',
        'limit': 1000
    }

    # Define headers
    headers = {'token': token}

    # File path
    file_path = "/home/swieyeinthesky/bluehillproject/data/blue_hill.csv"

    # Read the CSV file to find the last date entry
    try:
        data = pd.read_csv(file_path)
        if 'Date' in data.columns:
            data['Date'] = pd.to_datetime(data['Date'])
            last_date = data['Date'].max().date()
        else:
            print(f"'Date' column not found in the file.")
            last_date = None
    except Exception as e:
        print(f"Error reading the file: {e}")
        last_date = None

    # Define end_date as 2 days before today
    end_date = datetime.today().date() - timedelta(days=2)

    # Determine start_date
    if last_date:
        start_date = last_date + timedelta(days=1)
    else:
        start_date = None

    # Check if we need to make any requests
    if last_date and last_date >= end_date:
        print("No requests needed. The last date in the file is already up-to-date.")
        return
    elif not start_date or start_date > end_date:
        print("No valid start date found or start_date is beyond end_date. No requests needed.")
        return
    else:
        print(f"Requests needed from {start_date} to {end_date}.")

    # Function to fetch data for a given date range
    def fetch_data(start, end, datatype, retries=100):
        params = common_params.copy()
        params['startdate'] = start.strftime('%Y-%m-%d')
        params['enddate'] = end.strftime('%Y-%m-%d')
        params['datatypeid'] = datatype

        for attempt in range(retries):
            try:
                response = requests.get(base_url, headers=headers, params=params)
                response.raise_for_status()  # Raise an HTTPError for bad responses
                return response.json()['results']
            except requests.exceptions.HTTPError as e:
                print(f"HTTP error occurred: {e}")
                if response.status_code == 503:
                    print("Server unavailable, retrying...")
                    time.sleep(10)  # Wait for 10 seconds before retrying
                else:
                    break
            except requests.exceptions.RequestException as e:
                print(f"Request exception occurred: {e}")
                break
            except ValueError as e:
                print(f"Value error occurred: {e}")
                break
        return []

    # Collect data in chunks
    data = []
    current_start_date = start_date

    while current_start_date <= end_date:
        current_end_date = min(current_start_date + timedelta(days=365), end_date)
        data.extend(fetch_data(current_start_date, current_end_date, 'TMAX'))
        data.extend(fetch_data(current_start_date, current_end_date, 'TMIN'))
        data.extend(fetch_data(current_start_date, current_end_date, 'PRCP'))
        current_start_date = current_end_date + timedelta(days=1)

    # Convert the collected data to a DataFrame
    df = pd.DataFrame(data)

    # Pivot the DataFrame to have TMAX and TMIN in separate columns
    if not df.empty:
        df_pivot = df.pivot(index='date', columns='datatype', values='value').reset_index()

        # Rename columns for clarity
        df_pivot.columns = ['Date', 'PRCP', 'TMAX', 'TMIN']

        # Remove the substring "T00:00:00" from the date field
        df_pivot['Date'] = df_pivot['Date'].str.replace('T00:00:00', '')

        # Display the DataFrame
        print(df_pivot)

        # Remove blank lines by dropping rows where all elements are NaN
        df_pivot = df_pivot.dropna(how='all')

        # Check if the file exists
        if os.path.isfile(file_path):
            # Ensure the file ends with a newline before appending
            with open(file_path, 'a') as f:
                if os.stat(file_path).st_size > 0:
                    f.write('\n')
                df_pivot.to_csv(f, header=False, index=False)
        else:
            # If file doesn't exist, write data with the header
            df_pivot.to_csv(file_path, index=False, line_terminator='\n')
    else:
        print("No data fetched.")

make_call(datetime.now().year)
