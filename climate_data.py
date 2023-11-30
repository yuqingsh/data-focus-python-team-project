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
    data = []
    data.append([])
    data.append([])
    data.append([])
    for table in tables:
        rows = table.find_all("tr")
        for i in range(1, 4):
            row = rows[i]
            cells = row.find_all("td")
            for cell in cells:
                data[i - 1].append(cell.text.strip())
    return data, response.text

def main():
    get_climate_data()

if __name__ == "__main__":
    main()
