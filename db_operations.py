"""This module contains operations for the database. """
from dbcm import DBCM
from scrape_weather import WeatherScraper

class DBOperations:
    """
    The DBOperations class represents the operations of the database.
    """
    # *** Create tables, Insert data, Query data ***
    def fetch_data(): 
        """"""
        print()
    
    def save_data():
        print()

    def initialize_db(path: str):
        """Creates a table if one does not exists."""
        try: 
            with DBCM(path) as cursor:
                SQL_INITIALIZE_DB = """create table if not exists WeatherData
                (id integer primary key autoincrement not null,
                    sample_date text not null UNIQUE,
                    location text not null UNIQUE,
                    min_temp real not null,
                    max_temp real not null,
                    avg_temp real not null); """
                cursor.execute(SQL_INITIALIZE_DB)
        except Exception as e:
            print("*** Error creating table:", e)
            # sample_date -> text, unique in combination with location
            # location -> text, unique in combination with sample_date

    def purge_data():
        print()

DBOperations.initialize_db('weather.sqlite')