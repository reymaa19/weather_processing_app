import calendar
import matplotlib.pyplot as plt
from db_operations import DBOperations

class PlotOperations:
    def __init__(self, start_year=1996, end_year=2023):
        """Set up default years."""
        self.start_year = start_year
        self.end_year = end_year
        self.weather_data = {}
        self.month = 0
        self.my_db = DBOperations('weather.sqlite')

    def create_weather_data(self):
        """Read data from the database."""
        self.weather_data = self.my_db.fetch_data_years(self.start_year, self.end_year)

    def create_plot(self, data):
        """Create a plot with a range of years."""
        fig, ax = plt.subplots()
        ax.boxplot(data.values())
        ax.set_xticklabels(data.keys())
        ax.set(xlabel='Month', ylabel='Temperature (Celsius)',
               title=f"Monthly Temperature Distribution for: {self.start_year} to {self.end_year}")
        plt.show()

    def create_day_plot(self, year, month):
        """Create a monthly plot."""
        monthly_list = self.my_db.fetch_data_month(year, month)

        plt.plot(monthly_list)
        plt.xlabel('Day')
        plt.ylabel('Temperature (Celsius)')
        plt.title('Daily Temperature Distribution for: ' +
                  str(year) + ' ' + calendar.month_name[month])
        plt.show()


if __name__ == '__main__':
    print('Please enter the year and month to plot (e.g. 2020,3 for March 2020)')
    year, month = input().split(",")

    test = PlotOperations(2000, 2023)
    test.create_weather_data()
    test.create_plot(test.weather_data)
    test.create_day_plot(int(year), int(month))
