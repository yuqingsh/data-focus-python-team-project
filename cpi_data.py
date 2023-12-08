import requests
import pandas as pd

cities = ['Pittsburgh', 'Miami', 'New-York', 'Philadelphia', 'Tampa', 'Orlando', 'Irvine']
series_ids = ['CUUSA321SA0', 'CUURA320SEHA', 'CUURA101SA0', 'CUURA102SA0', 'CUURA422SA0', 'CUURA316SA0', 'CUURA421SA0']


def get_data(series_id, city_name, result_df):
    # Specify the API endpoint and parameters
    api_url = "https://api.stlouisfed.org/fred/series/observations"
    api_key = "fa792f5d75d3b3daa222f49e37ac9191"
    file_type = "json"

    # Construct the full API URL
    full_url = f"{api_url}?series_id={series_id}&api_key={api_key}&file_type={file_type}"

    # Make the API request
    response = requests.get(full_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON data
        json_data = response.json()

        # Extract 'data' and 'value' pairs
        observations = json_data['observations']
        data_value_pairs = [{'city': city_name, 'date': obs['date'], 'value': obs['value']} for obs in observations]

        # Create a DataFrame from the data and value pairs
        df = pd.DataFrame(data_value_pairs)
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        df = df.dropna(subset=['value'])
        df = df.replace({0: pd.NA}).dropna()
        df = df.replace({'.': pd.NA}).dropna()

        result_df = pd.concat([result_df, df], ignore_index=True)
        return result_df
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code} - {response.text}")

def preload_cpi_data():
    result_df = pd.DataFrame()

    for i in range(7):
        result_df = get_data(series_ids[i], cities[i], result_df)
    return result_df


def get_cpi_data(cpi_df):
    mean_df = cpi_df.drop(columns=['date']).groupby('city')['value'].mean().reset_index()
    mean_df = mean_df.rename(columns={'value': 'average'})

    # result_df.to_csv('output_file.csv', index=False)
    # mean_df.to_csv('mean_output_file.csv', index=False)

    mean_df.sort_values(by='average', inplace=True)
    city_list = mean_df['city'].tolist()

    return city_list


def cpi_get_score(cpi_df):
    city_list = get_cpi_data(cpi_df)
    ans = {}
    max_score = 7
    for city in city_list:
        ans[city] = max_score
        max_score -= 1

    return ans


def main():
    cpi_get_score()


if __name__ == "__main__":
    main()
