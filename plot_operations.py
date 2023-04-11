"""This module is to create different plots """
from dbcm import DBCM
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import calendar


class PlotOperations():
    def __init__(self, start_year=1996, end_year=2023):
        """Set up default years"""
        self.start_year = start_year
        self.end_year = end_year
        self.weather_data = dict()
        self.month = 0

    def create_weather_data(self):
        """Read data from the database"""
        with DBCM('weather.sqlite') as cursor:
            for month in range(1, 13):
                monthly_list = []
                for year in range(self.start_year, self.end_year + 1):
                    cursor.execute(
                        "SELECT avg_temp FROM WeatherData WHERE sample_date LIKE ?",
                        ('%{}-{:02d}%'.format(year, month),))
                    rows = cursor.fetchall()
                    monthly_list.extend(float(row[0]) for row in rows if row[0])
                self.weather_data[month] = monthly_list


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
    test.create_day_plot(2013, 5)