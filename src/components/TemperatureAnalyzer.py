from typing import Optional, Tuple

from interfaces.TemperatureClient import TemperatureClient
from models.DateRange import DateRange


class TemperatureAnalyzer:

    def __init__(self, client: TemperatureClient):
        self.client = client

    # A function that when called returns the `station_id`, and `date` pair that reported the
    # lowest temperature. If a tie occurs simply return one pair at random.
    def get_lowest_temperature(self) -> Optional[Tuple[str, str]]:
        stations = self.client.list_stations()
        min_temperature_c = float('inf')
        min_temperature = None
        for station in stations:
            temperature_list = self.client.get_temperatures_by_station(station)
            for temperature in temperature_list:
                temperature_c = temperature.degrees_c
                if temperature_c < min_temperature_c:
                    min_temperature_c = temperature_c
                    min_temperature = temperature
        if min_temperature:
            return min_temperature.station_id, str(min_temperature.date)
        else:
            return None

    # A function that returns the `station_id` that experienced the most amount of temperature
    # fluctuation across all dates that it reported temperatures for.
    def get_largest_temperature_fluctuation(self) -> Optional[str]:
        stations = self.client.list_stations()
        max_fluctuation = 0
        max_fluctuation_station_id = None
        for station in stations:
            cumulative_temperature_fluctuation = self._get_cumulative_temperature_fluctuation(station, window=None)
            if cumulative_temperature_fluctuation > max_fluctuation:
                max_fluctuation = cumulative_temperature_fluctuation
                max_fluctuation_station_id = station
        return max_fluctuation_station_id

    # A function that will return the `station_id` that experienced the most amount of temperature
    # fluctuation for any given range of dates.
    def get_largest_temperature_fluctuation_over_range(self, start_date: str, end_date: str) -> str:
        stations = self.client.list_stations()
        max_fluctuation = 0
        max_fluctuation_station_id = None
        for station in stations:
            window = DateRange(start_date, end_date)
            cumulative_temperature_fluctuation = self._get_cumulative_temperature_fluctuation(station, window)
            if cumulative_temperature_fluctuation > max_fluctuation:
                max_fluctuation = cumulative_temperature_fluctuation
                max_fluctuation_station_id = station
        return max_fluctuation_station_id

    def _get_cumulative_temperature_fluctuation(self, station: str, window: Optional[DateRange]):
        cumulative_temperature_fluctuation = 0

        temperature_list = self.client.get_temperatures_by_station(station, window)

        if len(temperature_list) > 1:
            for i in range(1, len(temperature_list) - 1):
                curr_temperature = temperature_list[i].degrees_c
                next_temperature = temperature_list[i + 1].degrees_c
                temperature_fluctuation = abs(curr_temperature - next_temperature)
                cumulative_temperature_fluctuation += temperature_fluctuation

        return cumulative_temperature_fluctuation
