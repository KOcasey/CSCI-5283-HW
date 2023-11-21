## Using API to get data
# # make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import pandas as pd
from pathlib import Path
from sodapy import Socrata
from datetime import datetime

def extract_data(target_dir, date, start_date):
    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    client = Socrata("data.austintexas.gov", None)

    # Example authenticated client (needed for non-public datasets):
    # client = Socrata(data.austintexas.gov,
    #                  MyAppToken,
    #                  username="user@example.com",
    #                  password="AFakePassword")

    # First 2000 results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    results = client.get("9t4d-g238", limit=200000) # use limit= to specify rows

    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)
    # filter to only include today's data
    # if it's not the first time loading data only select data from current date
    if str(date) != start_date:
        results_df['datetime'] = pd.to_datetime(results_df['datetime'])
        results_df = results_df[results_df['datetime'].dt.strftime('%Y-%m-%d') == str(date)]

    Path(target_dir).mkdir(parents=True, exist_ok=True)
    results_df.to_csv(target_dir + f'/outcomes_{date}.csv', index=False)