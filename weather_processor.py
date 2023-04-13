"""This is the main program use console """
from scrape_weather import WeatherScraper
from dbcm import DBCM
from db_operations import DBOperations
from plot_operations import PlotOperations
from datetime import datetime
from html.parser import HTMLParser
import urllib.request
import warnings

class WeatherProcessor:
    """This class is to launch and manage all the other tasks."""

    def __init__(self):
        """Get the latest date in the database."""
        with DBCM('weather.sqlite') as cursor:
            execute_str = '''SELECT * FROM weather
                             ORDER BY sample_date DESC
                             LIMIT 1'''
            cursor.execute(execute_str)
            row = cursor.fetchall()
        self.newest_date = row[0][1]
        self.db_date = row[0][1].split("-")

    def generate_data_urls(self):
        """Generate all the URLs for the weather data."""
        data_urls = []
        start_year = int(self.db_date[0])
        end_year = datetime.now().year
        end_month = datetime.now().month
        end_day = 31

        for i, year in enumerate(range(start_year, end_year + 1)):
            if year == datetime.now().year:
                for month in range(1, datetime.now().month + 1):
                    url = f'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear={start_year}&EndYear={end_year}&Day={end_day}&Year={year}&Month={month}#'
                    data_urls.append(url)
            else:
                for month in range(1, 13):
                    url = f'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear={start_year}&EndYear={end_year}&Day={end_day}&Year={year}&Month={month}#'
                    data_urls.append(url)
        return data_urls

    def update_db(self):
        """Update database to most recent day of year"""
        data_url_list = self.generate_data_urls()
        weather = {}
        for url in data_url_list:
            print('Scraping data from:', url)
            myparser = WeatherScraper()
            with urllib.request.urlopen(url) as response:
                html = str(response.read())
            myparser.feed(html)
            weather.update(myparser.temps_data)
        db = DBOperations()
        db.update_database(weather)

    @staticmethod
    def db_selection():
        """This is to create selection for update or download fullset"""
        print('Please select from:\n(1) download a full set of weather data\n(2) update it')

        try:
            x = int(input())
            if x == 1:
                full_set = DBOperations()
                full_set.create_database()
            elif x == 2:
                test = WeatherProcessor()
                print(f"Most recent date in database is {test.newest_date}")
                print("Updating database to today's date...")
                test.update_db()
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
            test.create_plot(test.weather_data)
        except (ValueError, IndexError):
            print("Invalid input. Please enter two years separated by a comma.")

if __name__ == '__main__':
    warnings.filterwarnings("ignore", "(?s).*MATPLOTLIBDATA.*", category=UserWarning)
    try:
        WeatherProcessor.db_selection()
        WeatherProcessor.plot_selection()
    except Exception as e:
        print(f"An error occurred: {e}")