import climate_data
import cpi_data
import crime_data
import hospice_data
import pandas as pd


def main():
    show_overall_score()


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
        crime_score = crime_data.crime_get_score()
        print(change_dict_to_df(crime_score))
    elif input_category == '3':
        cpi_score = cpi_data.cpi_get_score()
        print(change_dict_to_df(cpi_score))
    else:
        hospice_score = hospice_data.hospice_get_score()
        print(hospice_score)


def show_overall_score():
    score_list = [climate_data.climate_get_score(), crime_data.crime_get_score(), cpi_data.cpi_get_score(),
                  hospice_data.hospice_get_score()]
    city_list = ['PITTSBURGH', 'MIAMI', 'NEW YORK', 'PHILADELPHIA', 'TAMPA', 'ORLANDO', 'IRVINE']
    total_score = {}

    for city in city_list:
        total_score[city] = 0

    for score in score_list:
        print(score)
        for key, value in score:
            print(key + ":" + value)
            total_score[key.upper()] = total_score[key.upper()] + value

    ans_df = change_dict_to_df(total_score)
    ans_df = ans_df.sort_values(by='Score', ascending=False)

    print(ans_df)


def interact_user():
    user_input = ''
    while user_input != 'Q' and user_input != 'q':
        show_menu()
        user_input = input('    Your choice: ').strip()
        if user_input == '2' or user_input == '3' or user_input == '4':
            show_single_score(user_input)
        elif user_input == '5':
            show_overall_score()
        else:
            pass


if __name__ == "__main__":
    main()
