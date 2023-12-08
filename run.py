import climate_data
import cpi_data
import crime_data
import hospice_data
import pandas as pd


# global vars
climate_df = None
cpi_df = None
crime_dict = None
hospice_df = None

def main():
    preload_all_data()
    interact_user()


def show_menu():
    print('''
    Please select from this menu:

    1)  Plot graph for Temperature
    2)  Display Scores for Crime data(from 1 - 7)
    3)  Display Scores for Inflation data(from 1- 7)
    4)  Display Scores for Hospice data(from 1- 7)
    5)  Display Overall Comparison
    Q)  Quit from this program
    ''')


def change_dict_to_df(input_dict):
    city_list = []
    score_list = []
    for key, value in input_dict.items():
        city_list.append(key.upper())
        score_list.append(value)

    return pd.DataFrame({"City": city_list, "Score": score_list})


def show_single_score(input_category):
    if input_category == '2':
        crime_score = crime_data.crime_get_score(crime_dict)
        print(change_dict_to_df(crime_score))
    elif input_category == '3':
        cpi_score = cpi_data.cpi_get_score(cpi_df)
        print(change_dict_to_df(cpi_score))
    else:
        hospice_score = hospice_data.hospice_get_score(hospice_df)
        print(change_dict_to_df(hospice_score))


def show_overall_score():
    hospice_score = hospice_data.hospice_get_score(hospice_df)
    record_value = hospice_score['NEW YORK']
    del hospice_score['NEW YORK']
    hospice_score['NEW-YORK'] = record_value
    climate_score = climate_data.climate_get_score(climate_df)
    cpi_score = cpi_data.cpi_get_score(cpi_df)
    crime_score = crime_data.crime_get_score(crime_dict)
    score_list = [climate_score, crime_score, cpi_score,
                  hospice_score]
    city_list = ['PITTSBURGH', 'MIAMI', 'NEW-YORK', 'PHILADELPHIA', 'TAMPA', 'ORLANDO', 'IRVINE']
    total_score = {}

    for city in city_list:
        total_score[city] = 0

    for score in score_list:
        for key, value in score.items():
            total_score[key.upper()] = total_score[key.upper()] + value

    ans_df = change_dict_to_df(total_score)
    ans_df = ans_df.sort_values(by='Score', ascending=False)

    print(ans_df)

def preload_all_data():
    # preload data to save time for user interaction
    global climate_df
    global cpi_df
    global crime_dict
    global hospice_df
    print("Starting the app...")
    print("Loading climate data...")
    climate_df = climate_data.preload_climate_data()
    print("Loading CPI data...")
    cpi_df = cpi_data.preload_cpi_data()
    print("Loading crime data...")
    crime_dict = crime_data.preload_crime_data()
    print("Loading hospice data...")
    hospice_df = hospice_data.preload_hospice_data()
    print("All data loaded.")


def interact_user():
    user_input = ''
    while user_input != 'Q' and user_input != 'q':
        show_menu()
        user_input = input('    Your choice: ').strip()
        if user_input == '2' or user_input == '3' or user_input == '4':
            show_single_score(user_input)
        elif user_input == '5':
            show_overall_score()
        elif user_input == '1':
            climate_data.plot_graph()
        else:
            pass


if __name__ == "__main__":
    main()
