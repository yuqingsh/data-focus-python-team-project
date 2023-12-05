import climate_data
import cpi_data
import crime_data
import hospice_data


def main():
    climate_score = climate_data.climate_get_score()
    crime_score = crime_data.crime_get_score()
    cpi_score = cpi_data.cpi_get_score()
    hospice_score = hospice_data.hospice_get_score()


if __name__ == "__main__":
    main()
