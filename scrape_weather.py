import calendar
import urllib.request
import logging

from html.parser import HTMLParser
from datetime import date, datetime

class WeatherScraper(HTMLParser):
    #WeatherScraper scrapes the weather data, filter and package them for database input later.
    def __init__(self):
        HTMLParser.__init__(self)
        self.weather = {}
        self.data = ''
        self.reading_temp_flag = False
        self.date_list = []
        self.stop_scraping = False
        self.logger = logging.getLogger()

    def handle_starttag(self, tag, attrs):
        #Condition for starting tag scarping.
        try:
            if tag == 'abbr':
                if attrs[0][1]:  # <abbr title="May 1, 2018">
                    try:
                        current_date = attrs[0][1]
                        self.date_list.append(datetime.strptime(current_date, '%B %d, %Y').strftime('%Y-%m-%d'))
                    except ValueError:
                        return None

            if tag == 'td':
                self.reading_temp_flag = True
        except Exception as e:
            print("<Error>:", e)

    def handle_data(self, data: str):
        #Condition for scraping the useful data.
        try:
            if self.reading_temp_flag:
                if data not in ['LegendM', 'LegendE', ' ', 'LegendT', 'LegendCarer', 'E']:
                    self.data += data.strip() + ','
        except Exception as e:
            print("<Error>:", e)

    def handle_endtag(self, tag):
        #Condition for ending tag scarping.
        try:
            if tag == 'td':
                self.reading_temp_flag = False
        except Exception as e:
            print("<Error>:", e)

    def start_scraping(self, url: str, year: int) -> None:
        #Scraping a specific year temperature data.
        try:
            print('Start scraping from website: ' + url)
            for i in range(1, 13):
                self.scrape_month_weather_temp_data(year, i)
        except Exception as e:
            print("<Error>:", e)

    def scrape_to_earliest_month_weather(self, year: int = datetime.today().year,
                                             month: int = datetime.today().month) -> None:
        #Automatically detect when no more weather data is available for scraping.
        try:
            while not self.stop_scraping:
                self.scrape_month_weather_temp_data(year, month)
                month -= 1
                if month == 0:
                    year -= 1
                    month = 12
        except Exception as e:
            print("<Error>:", e)

    def scrape_month_weather_temp_data(self, year: int, month: int) -> dict:
        #Scraping a month temperature data on the website page.
        try:
            print('Scraping data for year: {0}, month: {1}...'.format(year, month))
            days_of_current_month = calendar.monthrange(year, month)[1]
            # Get raw info from HTML parse
            url = ("http://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=" + str(year)
                   + "&Day=1&Year=" + str(year)
                   + "&Month=" + str(month) + "#")

            new_scraper = WeatherScraper()
            with urllib.request.urlopen(url) as response:
                html = str(response.read())
            new_scraper.feed(html)
            
            # If the date_list in the website already be scraped, then we will stop the scrapper.
            if new_scraper.date_list != [] and new_scraper.date_list in self.date_list:
                self.stop_scraping = True
                print('There is no data for year: {0}, month: {1}.'.format(year, month))
                return {}

            result = new_scraper.data.split(',')

            # Convert raw info to weather list.
            # From the website, each row has 11 column, and the last 4 lines are useless(sum, avg, xtrm, summary).
            columns = 11
            if date.today().year == year and date.today().month == month:
                rows = date.today().day
            else:
                rows = days_of_current_month
            result_grouping = [result[i:i + columns] for i in range(0, rows * columns, columns)]
            daily_temps_list = []
            for item in result_grouping:
                if len(item) >= 3:
                    # '' only happened in yesterday and today, others are 'M'
                    if item[0] != '' and item[1] != '' and item[2] != '':
                        my_dict = {"Max": str(item[0]), "Min": str(item[1]), "Mean": str(item[2])}
                        daily_temps_list.append(my_dict)

            # Zip weather list items with the date
            month_dict = dict(zip(new_scraper.date_list, daily_temps_list))
            self.date_list.append(new_scraper.date_list)
            self.weather.update(month_dict)

            return month_dict
        
        except Exception as e:
            print("<Error>:", e)

if __name__ == '__main__':
    my_scraper = WeatherScraper()
    my_scraper.scrape_to_earliest_month_weather(2023, 3)
    print(my_scraper.weather)