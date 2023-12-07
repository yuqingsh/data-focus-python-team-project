import requests
import pandas as pd


def main():
    hospice_score = hospice_get_score()
    print(hospice_score)


def download_csv(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

        with open(save_path, 'wb') as file:
            file.write(response.content)

    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")


def load_csv_to_dataframe(file_path):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        return df

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except pd.errors.EmptyDataError:
        print(f"Error: File '{file_path}' is empty.")
    except pd.errors.ParserError as pe:
        print(f"Error parsing CSV: {pe}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def clean_hospice_data(df):
    # Define the key-value pairs
    target_cities = [('PITTSBURGH', 'PA'), ('MIAMI', 'FL'), ('NEW YORK', 'NY'),
                     ('PHILADELPHIA', 'PA'), ('TAMPA', 'FL'), ('ORLANDO', 'FL'), ('IRVINE', 'CA')]

    # Filter the DataFrame based on key-value pairs
    filtered_df = df[(df['citytown'].isin([key for key, value in target_cities])) &
                     (df['state'].isin([value for key, value in target_cities]))]
    filtered_df = filtered_df[filtered_df['score'] != 'Not Available']
    filtered_df['score'] = filtered_df['score'].astype('float')
    return filtered_df


def calculate_hospice_score(filtered_df):
    hospice_score = filtered_df[['citytown', 'state', 'score']].groupby(['citytown', 'state']).mean().reset_index()
    hospice_score = hospice_score.sort_values(by='score', ascending=True)
    hospice_score['ranking'] = range(1, len(hospice_score) + 1)
    return hospice_score


def hospice_get_score():
    hospice_url = ('https://data.cms.gov/provider-data/api/1/pdc/query/252m-zfp9/0/download?'
                   'conditions%5B0%5D%5Bproperty'
                   '%5D=measure_name&conditions%5B0%5D%5Boperator%5D=%3D&conditions%'
                   '5B0%5D%5Bvalue%5D=Hospice%20Care%20Index%'
                   '20Overall%20Score&properties=1-2-3-4-5-6-7-8-9-10-11-12-13-14-15&format=csv')
    save_path = './hospice_raw.csv'
    download_csv(hospice_url, save_path)
    raw_df = load_csv_to_dataframe(save_path)
    filtered_df = clean_hospice_data(raw_df)
    hospice_score = calculate_hospice_score(filtered_df)

    city_list = hospice_score['citytown']
    max_score = 7
    ans = {}
    for city in city_list:
        ans[city] = max_score
        max_score -= 1

    return ans


if __name__ == "__main__":
    main()
