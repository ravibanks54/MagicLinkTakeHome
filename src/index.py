from accessors.TemperatureInMemoryClient import TemperatureInMemoryClient
from components.TemperatureAnalyzer import TemperatureAnalyzer

from utils import csv_loader

if __name__ == '__main__':
    filepath = "data/prod.csv"
    initial_data = csv_loader.load_temperature_data(filepath)
    client = TemperatureInMemoryClient(initial_data)
    analyzer = TemperatureAnalyzer(client)
    station_id, date = analyzer.get_lowest_temperature()
    print(f"Lowest temperature reported at station: {station_id} on date: {date}.")
    largest_fluctuation_station_id = analyzer.get_largest_temperature_fluctuation()
    print(f"Largest temperature fluctuation reported at station: {largest_fluctuation_station_id}")
