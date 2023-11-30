import requests
import pandas as pd

# Specify the URL of the CSV file on the Airtable website
url = "https://airtable.com/appzVzSeINK1S3EVR/shroOenW19l1m3w0H/tblxearKzw8W7ViN8"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Use pandas to read the CSV data
    print(response.text)

    # Now 'df' contains the data from the CSV file, and you can manipulate or export it as needed
    # For example, you can export it to a local CSV file using the to_csv method:
    # df.to_csv('output.csv', index=False)
    print("CSV file exported successfully.")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")