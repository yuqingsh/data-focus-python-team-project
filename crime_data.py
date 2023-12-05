import requests
import json
import numpy as np

CITIES = [
    "pittsburgh",
    "miami",
    "new-york",
    "philadelphia",
    "tampa",
    "orlando",
    "irvine",
]

CITIES_STATES = {
    "pittsburgh": "PA",
    "miami": "FL",
    "new-york": "NY",
    "philadelphia": "PA",
    "tampa": "FL",
    "orlando": "FL",
    "irvine": "CA",
}

BASE_URL = "https://api.usa.gov/crime/fbi/cde/arrest/state/"


def fetch_data_one_city(city, secrety_key="rME1GBOinfksPYZEfhQkrQf7ElQjuaJa3UZX2qWe"):
    state = CITIES_STATES[city]
    url = BASE_URL + state + "/property_crime"
    params = {
        'from': 2019,
        'to': 2023,
        'API_KEY': secrety_key
    }
    response = requests.get(url, params=params)
    data = json.loads(response.text)
    data_list = data["data"]
    crime_case_nums = []
    for item in data_list[1:]:
        crime_case_num = 0
        crime_case_num += int(item["Motor Vehicle Theft"])
        crime_case_num += int(item["Arson"])
        crime_case_num += int(item["Burglary"])
        crime_case_num += int(item["Embezzlement"])
        crime_case_num += int(item["Forgery and Counterfeiting"])
        crime_case_num += int(item["Larceny - Theft"])
        crime_case_num += int(item["Vandalism"])
        crime_case_num += int(item["Stolen Property: Buying, Receiving, Possessing"])
        crime_case_nums.append(crime_case_num)

    return np.mean(crime_case_nums)


def fetch_data():
    ret = {}
    for city in CITIES:
        ret[city] = fetch_data_one_city(city)
    return ret


def crime_get_score():
    data = fetch_data()
    values = list(data.values())
    values.sort()
    values_dict = {}
    max_score = 7

    for i in range(len(values)):
        if i == 0:
            values_dict[values[i]] = max_score
        else:
            if values[i - 1] < values[i]:
                max_score -= 1
            values_dict[values[i]] = max_score

    ans = {}
    for key, value in data.items():
        ans[key] = values_dict[value]

    return ans


def main():
    data = fetch_data()
    print(data)


if __name__ == "__main__":
    main()