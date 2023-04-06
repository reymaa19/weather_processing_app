"""This module contains database operations. """
import sqlite3
from scrape_weather import WeatherScraper

class DBOperations:
    """
    The DBOperations class represents the operations of the database.
    """

    # *** Create database, Create tables, Insert data, Query data ***

    conn = sqlite3.connect("weather.sqlite")
    print("Opened the database successfully.")