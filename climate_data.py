import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def get_climate_data():
    """_summary_
    This function scrapes the climate data from the website and returns a dataframe.

    Args:
    Returns:
        df: a dataframe with columns: city, state, month, high, low, precipitation
    """

    # Cities and states to scrape
    cities = [
        "pittsburgh",
        "miami",
        "new-york",
        "philadelphia",
        "tampa",
        "orlando",
        "irvine",
    ]
    states = [
        "pennsylvania",
        "florida",
        "new-york",
        "pennsylvania",
        "florida",
        "florida",
        "california",
    ]

    # Create an empty dataframe
    df = pd.DataFrame(
        columns=["city", "state", "month", "high", "low", "precipitation"]
    )
    raws = []

    # Scrape the data for each city
    for i in range(len(cities)):
        data, raw = scrape_one_city(cities[i], states[i])
        raws.append(raw)
        # Add the data to the dataframe
        for j in range(12):
            # print(data[0][j], data[1][j], data[2][j])
            df = pd.concat(
                [
                    df,
                    pd.DataFrame(
                        [
                            [
                                cities[i],
                                states[i],
                                j + 1,
                                data[0][j],
                                data[1][j],
                                data[2][j],
                            ]
                        ],
                        columns=[
                            "city",
                            "state",
                            "month",
                            "high",
                            "low",
                            "precipitation",
                        ],
                    ),
                ],
                ignore_index=True,
            )
    # redirect the output to a csv file
    df.to_csv("output.csv", index=False)
    # redirect the raw html to a txt file
    with open("raw.txt", "w") as file:
        for raw in raws:
            file.write(raw)

    return df


def scrape_one_city(city, state):
    """ this function scrapes the climate data for one city and returns a dataframe and the raw html

    Args:
        city (_type_): the name of the city
        state (_type_): the name of the state

    Returns:
        data (dataframe): a dataframe with columns: city, state, month, high, low, precipitation
        response (string): the raw html
    """
    url = (
            "https://www.usclimatedata.com/climate/"
            + city
            + "/"
            + state
            + "/united-states/"
    )
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table_div = soup.find("div", {"class": "monthly_tables"})
    tables = table_div.find_all("table")
    data = [[], [], []]
    for table in tables:
        rows = table.find_all("tr")
        for i in range(1, 4):
            row = rows[i]
            cells = row.find_all("td")
            for cell in cells:
                data[i - 1].append(cell.text.strip())
    return data, response.text


def preload_climate_data():
    return get_climate_data()


def climate_get_score(df):
    """
    This function returns the score for each city
    :param df: the input cities climate dataframe
    :return: the score for each city
    """
    # df = get_climate_data()
    # Convert the 'high' and 'low' columns to numeric
    df['high'] = pd.to_numeric(df['high'])
    df['low'] = pd.to_numeric(df['low'])

    # Group by 'city' and calculate the average of 'high' and 'low'
    result = df.groupby('city').agg({'high': 'mean', 'low': 'mean'}).reset_index()
    result['tmp_diff'] = result['high'] - result['low']
    result.sort_values(by='tmp_diff', inplace=True)
    city_list = result['city'].tolist()

    ans = {}
    max_score = 7
    for city in city_list:
        ans[city] = max_score
        max_score -= 1

    return ans


def plot_graph():
    """
    This function plots the graph of the climate data
    :return: the plot
    """
    df = get_climate_data()
    df['high'] = pd.to_numeric(df['high'])
    df['low'] = pd.to_numeric(df['low'])
    df['month'] = pd.to_datetime(df['month'])

    cities = df['city'].unique()

    fig, axs = plt.subplots(3, 1, sharex=True, figsize=(10, 8))

    lines = []
    labels = []

    for city in cities:
        city_data = df[df['city'] == city]
        city_data['avg'] = (city_data['high'] + city_data['low']) / 2

        line1, = axs[0].plot(city_data['month'], city_data['avg'])
        line2, = axs[1].plot(city_data['month'], city_data['high'])
        line3, = axs[2].plot(city_data['month'], city_data['low'])

        lines.append(line1)
        labels.append(f'{city} Average')

    # Set titles for each subplot
    axs[0].set_title('Average Temperature')
    axs[1].set_title('High Temperature')
    axs[2].set_title('Low Temperature')

    # Set y labels for all subplots
    axs[0].set_ylabel('Temperature')
    axs[1].set_ylabel('Temperature')
    axs[2].set_ylabel('Temperature')

    # Set x label for the last subplot only
    axs[2].set_xlabel('Month')

    fig.legend(lines, labels, loc='upper right')

    plt.show()


def main():
    climate_get_score()


if __name__ == "__main__":
    main()
