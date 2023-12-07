import climate_data
import cpi_data
import crime_data
import hospice_data


def main():
    load_data()
    show_menu()

    climate_score = climate_data.climate_get_score()
    crime_score = crime_data.crime_get_score()
    cpi_score = cpi_data.cpi_get_score()
    hospice_score = hospice_data.hospice_get_score()
    print(climate_score)
    print(crime_score)
    print(cpi_score)
    print(hospice_score)

# TODO
def load_data():
    return

# TODO
# Show Graph for Temperature
# Show Scores for Crime
# Show Scores for Hospice
# Show Scores for CPI
# Show Overall Comparison
# Quit

def show_menu():
    return

if __name__ == "__main__":
    main()
