"""This is the main program use console """
from scrape_weather import WeatherScraper
from db_operations import DBOperations
from plot_operations import PlotOperations
from datetime import datetime
from html.parser import HTMLParser
import urllib.request
import warnings

class WeatherProcessor:
    """This class is to launch and manage all the other tasks."""

    def __init__(self):
        self.db = DBOperations('weather.sqlite')
        self.scraper = WeatherScraper()
        self.latest_date = self.db.fetch_data_latest()
        self.today = datetime.now().date()

    def update_db(self):
        """Updates the database to the most recent data."""
        current_month = int(self.today.__str__().split("-")[1])
        current_year = int(self.today.__str__().split("-")[0])
        while self.latest_date[:-3] != str(current_year) + "-" + str(current_month).zfill(2):
            self.scraper.scrape_month_weather_temp_data(current_year, current_month)
            current_month -= 1
            if current_month == 0:
                current_year -= 1
                current_month = 12
        self.db.save_data(self.scraper.weather)
    
    def download_full_set_data(self):
        """Downloads the full set of weather data."""
        self.scraper.scrape_to_earliest_month_weather()
        self.db.save_data(self.scraper.weather)

    def db_selection(self):
        """This is to create selection for update or download fullset"""
        print('Please select from:\n(1) download a full set of weather data\n(2) update it')

        try:
            x = int(input())
            if x == 1:
                print("Downloading full set of weather data...")
                self.download_full_set_data()
            elif x == 2:
                print(f"Most recent date in database is {self.latest_date[1]}")
                print(f"Updating database to today's date, {self.today}...")
                self.update_db()
                print("Database update succeeded.")
            else:
                print("Invalid input. Please enter 1 or 2.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    @staticmethod
    def plot_selection():
        """This method is to create weather plot"""
        print('Please enter year range of interest (from year, to year, e.g. 2000,2017)')
        try:
            x = input().split(",")
            from_year, to_year = int(x[0]), int(x[1])
            test = PlotOperations(from_year, to_year)
            test.create_weather_data()

            print('Please enter the year and month to plot (e.g. 2022,3 for March 2022)')
            year, month = input().split(",")
            test.create_plot(test.weather_data)
            test.create_day_plot(int(year), int(month))
        except (ValueError, IndexError):
            print("Invalid input. Please enter two years separated by a comma.")

if __name__ == '__main__':
    warnings.filterwarnings("ignore", "(?s).*MATPLOTLIBDATA.*", category=UserWarning)
    test = WeatherProcessor()
    test.db_selection()
    test.plot_selection()