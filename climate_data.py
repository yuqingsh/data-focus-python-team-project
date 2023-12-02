import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_climate_data():
    # URL of the webpage
    # Pittsburgh, Miami, New York City, Philadelphia, Tampa, Orlando and Irvine
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
    df = pd.DataFrame(
        columns=["city", "state", "month", "high", "low", "precipitation"]
    )
    raws = []
    for i in range(len(cities)):
        data, raw = scrape_one_city(cities[i], states[i])
        raws.append(raw)
        for j in range(12):
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
    df.to_csv("output.csv", index=False)
    with open("raw.txt", "w") as file:
        for raw in raws:
            file.write(raw)

    return df


def scrape_one_city(city, state):
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


def climate_get_score():
    df = get_climate_data()
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


def main():
    climate_get_score()


if __name__ == "__main__":
    main()
