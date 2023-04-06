"""This module contains operations for the database."""
from dbcm import DBCM
from scrape_weather import WeatherScraper

class DBOperations:
    """
    The DBOperations class represents the operations of the database.
    """
    def __init__(self, path: str):
        """Initializes the database path name."""
        self.db_name = path

    def fetch_data(self) -> list: 
        """
        Fetches requested data from the database for plotting.
        """
        try:
            with DBCM(self.db_name) as cursor:
                sql_select_all = """SELECT * FROM WeatherData;"""
                cursor.execute(sql_select_all)
                fetch_weather = cursor.fetchall()
            return fetch_weather
        except Exception as e:
            print("*** Error fetching data:", e)
    
    def save_data(self, data_source: dict):
        """
        Saves new data to the database.
        """
        new_weather_data = []
        for sample_date, data in data_source.items():
            new_sample = [sample_date]
            for stat, value in data.items():
                new_sample.append(value)
            new_weather_data.append(tuple(new_sample))
        try:
            with DBCM(self.db_name) as cursor:
                sql_save_data = """INSERT OR IGNORE INTO WeatherData (sample_date, max_temp, min_temp, avg_temp) VALUES (?,?,?,?);"""
                for date_data in new_weather_data:
                    print(date_data)
                    cursor.execute(sql_save_data, date_data)
        except Exception as e:
            print("*** Error inserting data.", e)

    def initialize_db(self):
        """
        Creates a table if one does not exists.
        """
        try: 
            with DBCM(self.db_name) as cursor:
                SQL_INITIALIZE_DB = """CREATE TABLE IF NOT EXISTS WeatherData 
    (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    sample_date TEXT NOT NULL, 
    location TEXT NOT NULL default %s,
    min_temp REAL NOT NULL,
    max_temp REAL NOT NULL,
    avg_temp REAL NOT NULL,
    UNIQUE(sample_date, location));""" % "'Winnipeg, Manitoba'"
                cursor.execute(SQL_INITIALIZE_DB)
        except Exception as e:
            print("*** Error creating table:", e)

    def purge_data(self):
        """
        Deletes all the data inside the database.
        """
        try:
            print('Purging all data in the database... ')
            with DBCM(self.db_name) as cursor:
                sql_purge_data_1 = """DELETE FROM WeatherData;"""
                sql_purge_data_2 = """DELETE FROM sqlite_sequence WHERE NAME = 'WeatherData';"""
                cursor.execute(sql_purge_data_1)
                cursor.execute(sql_purge_data_2)
        except Exception as e:
            self.logger.error(e)

if __name__ == '__main__':
    mydb = DBOperations('weather.sqlite')
    mydb.initialize_db()

    my_scraper = WeatherScraper()
    my_scraper.scrape_month_weather_temp_data(2023, 3)

    mydb.save_data(my_scraper.weather)

    print(mydb.fetch_data())

    mydb.purge_data()
    print(mydb.fetch_data())
    test = '1'
    print(test.isnumeric())