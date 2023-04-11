"""This module is to create different plots """
from dbcm import DBCM
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import calendar
from db_operations import DBOperations


class PlotOperations():
    def __init__(self, start_year=1996, end_year=2023):
        """Set up default years"""
        self.start_year = start_year
        self.end_year = end_year
        self.weather_data = dict()
        self.month = 0
        self.my_db = DBOperations('weather.sqlite')

    def create_weather_data(self):
        """Read data from the database"""
        self.weather_data = self.my_db.fetch_data(self.start_year, self.end_year, self.weather_data)
        
    def create_plot(self, data):
        """This method creates a plot with a range of years"""
        fig, ax = plt.subplots()
        ax.boxplot(data.values())
        ax.set_xticklabels(data.keys())
        ax.set(xlabel='Month', ylabel='Temperature (Celsius)',
            title=f"Monthly Temperature Distribution for: {self.start_year} to {self.end_year}")
        plt.show()


    def create_day_plot(self, year, month):
        """This method create a monthly plot"""
        monthly_list = []
        year = str(year)
        with DBCM('weather.sqlite') as cursor:
            cursor.execute(
                "SELECT avg_temp FROM WeatherData WHERE sample_date LIKE ?",
                ('%{}%'.format(year + '-' + str(month).zfill(2)),))
            rows = cursor.fetchall()
            for row in rows:
                if '{}'.format(row[0]) != '':
                    monthly_list.append(float('{}'.format(row[0])))

        plt.plot(monthly_list)
        plt.xlabel('Day')
        plt.ylabel('Temperature (Celsius)')
        plt.title('Daily Temperature Distribution for : ' +
                  str(year) + ' ' + calendar.month_name[month])
        plt.show()


if __name__ == '__main__':
    test = PlotOperations(2000, 2023)
    test.create_weather_data()
    test.create_plot(test.weather_data)
    test.create_day_plot(2020, 3)