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
        Fetches all data from the database.
        """
        try:
            with DBCM(self.db_name) as cursor:
                sql_select_all = """SELECT * FROM WeatherData;"""
                cursor.execute(sql_select_all)
                fetch_weather = cursor.fetchall()
            return fetch_weather
        except Exception as e:
            print("*** Error fetching data:", e)

    def fetch_data_years(self, start_year: int, end_year: int) -> dict:
        """
        Fetches data for the specified years from the database and returns it as a dict.
        """
        try:
            weather_data = dict()
            with DBCM(self.db_name) as cursor:
                for month in range(1, 13):
                    monthly_list = []
                    for year in range(start_year, end_year + 1):
                        cursor.execute(
                            "SELECT avg_temp FROM WeatherData WHERE sample_date LIKE ?",
                            ('%{}-{:02d}%'.format(year, month),))
                        rows = cursor.fetchall()
                        monthly_list.extend(float(row[0]) for row in rows if row[0])
                    weather_data[month] = monthly_list
                return weather_data
        except Exception as e:  
            print("*** Error fetching data:", e)
    
    def fetch_data_month(self, year: int, month: int) -> list:
        """
        Fetches data for the specified month from the database and returns a list.
        """
        monthly_list = []
        year = str(year)
        with DBCM(self.db_name) as cursor:
            cursor.execute(
                "SELECT avg_temp FROM WeatherData WHERE sample_date LIKE ?",
                ('%{}%'.format(year + '-' + str(month).zfill(2)),))
            rows = cursor.fetchall()
            for row in rows:
                if '{}'.format(row[0]) != '':
                    monthly_list.append(float('{}'.format(row[0])))
        return monthly_list
    
    def fetch_data_latest(self) -> str:
        """Get the latest date in the database."""
        with DBCM(self.db_name) as cursor:
            cursor.execute(
                """SELECT * FROM WeatherData ORDER BY sample_date DESC LIMIT 1""")
            row = cursor.fetchall()
        return row[0][1]
    
    def save_data(self, data_source: dict):
        """
        Saves new data to the database.
        """
        new_weather_data = []
        for sample_date, data in data_source.items():
            new_sample = [sample_date]
            for stat, value in data.items():
                try:
                    float(value)
                    new_sample.append(value)
                except:
                    new_sample.append('')
            new_weather_data.append(tuple(new_sample))
        try:
            with DBCM(self.db_name) as cursor:
                sql_save_data = """INSERT OR IGNORE INTO WeatherData (sample_date, max_temp, min_temp, avg_temp) VALUES (?,?,?,?);"""
                for date_data in new_weather_data:
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
            print("*** Error purging database.", e)


            
if __name__ == '__main__':
    # Initialize DBOperations object.
    mydb = DBOperations('weather.sqlite')
    # Initialize database table.
    mydb.initialize_db()

    # Initialize WeatherScraper object.
    my_scraper = WeatherScraper()
    # Specify to scrape weather from October, 2022 for testing update_db.
    my_scraper.scrape_to_earliest_month_weather(2022, 10)

    # Save scraped data to database.
    mydb.save_data(my_scraper.weather)
    print("*** save_data result: ", mydb.fetch_data())

    # Delete data from database.
    # mydb.purge_data()
    # print("*** purge_data result: ", mydb.fetch_data())