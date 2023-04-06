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

    # *** Create tables, Insert data, Query data ***

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
        new_weather_data = [] # CREATE NEW LIST
        for sample_date, data in data_source.items(): # FOR EVERY KEY AND VALUE IN DICTIONARY
            new_sample = [sample_date] # sample = ['2023-05-05']
            for stat, value in data.items(): # FOR EVERY MEAN, MIN, OR AVERAGE AND ITS VALUE
                new_sample.append(value) # ADD IT TO THE NEW ROW `['2023-05-05', '1.3', '0.3', '1']`
            new_weather_data.append(tuple(new_sample)) # ADD NEW SAMPLE TO LIST OF TUPLES `[('2023-05-05', '1.3', '0.3', '1'), (...), (...)]`
        try:
            with DBCM(self.db_name) as cursor:
                sql_save_data = """INSERT OR IGNORE INTO WeatherData (sample_date, max_temp, min_temp, avg_temp) VALUES (?,?,?,?);"""
                # SOMETHING WRONG HERE
                for date_data in new_weather_data:
                    cursor.execute(sql_save_data, date_data)
                # SUPPOSED TO COMMIT AFTER EXITING `with` STATEMENT
                # !!! LOCATION IS NOT BEING RECORDED !!!
        except Exception as e:
            print("*** Error inserting data.", e)





    def initialize_db(self):
        """
        Creates a table if one does not exists.
        """
        try: 
            with DBCM(self.db_name) as cursor:
                SQL_INITIALIZE_DB = """CREATE TABLE IF NOT EXISTS WeatherData
                (id integer primary key autoincrement not null,
                    sample_date text not null UNIQUE,
                    location text not null UNIQUE,
                    min_temp real not null,
                    max_temp real not null,
                    avg_temp real not null); """
                cursor.execute(SQL_INITIALIZE_DB)
        except Exception as e:
            print("*** Error creating table:", e)

    def purge_data():
        print()

if __name__ == '__main__':
    mydb = DBOperations('weather.sqlite')
    mydb.initialize_db()

    my_scraper = WeatherScraper()
    my_scraper.scrape_month_weather_temp_data(2023, 3)
    print(my_scraper.weather)
    mydb.save_data(my_scraper.weather) # SAVING NO DATA (save_data not executing properly)
    print(mydb.fetch_data())