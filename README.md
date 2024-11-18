# weather_processing_app

A Python GUI application that scrapes and visualizes historical weather data from [Environment Canada's climate data portal](https://climate.weather.gc.ca/historical_data/search_historic_data_e.html) for Winnipeg weather station. The application retrieves daily temperature records dating back to 1840 and provides tools for data analysis and visualization.

## Features
- Scrapes historical temperature data from Environment Canada's climate database
- Stores data in a local SQLite database using a context manager pattern
- Creates interactive visualizations with matplotlib:
  - Monthly temperature distribution plots
  - Historical temperature trend analysis
  - Daily temperature comparisons
- Modular architecture with separate components for:
  - Web scraping (scrape_weather.py)
  - Database operations (db_operations.py)
  - Data visualization (plot_operations.py)
  - GUI interface (weather_gui.py)

## Project Structure
- `weather_gui.py`: Main GUI application
- `weather_processor.py`: Core data processing logic
- `scrape_weather.py`: Web scraping functionality
- `db_operations.py`: Database interaction layer
- `plot_operations.py`: Data visualization
- `dbcm.py`: Database context manager

## Requirements
- Python 3.10 or higher
- wxPython >= 4.1.0
- matplotlib >= 3.5.0
- sqlite3 (built into Python)
- requests >= 2.26.0 (for web scraping)

## Installation

### From Source
1. Clone the repository
2. Create and activate a virtual environment:
```sh
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```
3. Install dependencies: 
```sh
pip install wxPython>=4.1.0 matplotlib>=3.5.0 requests>=2.26.0
```
4. Run the application:
```sh
python weather_gui.py
```

### Pre-built Binary
1. Download the latest WeatherScraperApp installer
2. Run the installer and follow the prompts
3. Launch via desktop shortcut or start menu

## Usage
1. **Fetch Data**:
   - Click "Scrape Data" to download historical weather data
   - Choose between full historical download or updates only

2. **Visualize Data**:
   - Generate monthly temperature distribution plots
   - View historical temperature trends
   - Compare daily temperatures across years

3. **Database Management**:
   - Data automatically saved to SQLite database
   - Updates merge with existing records
   - Built-in database integrity checks
