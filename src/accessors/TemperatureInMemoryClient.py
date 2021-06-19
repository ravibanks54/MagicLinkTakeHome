import typing
from bisect import bisect_left, bisect_right
from decimal import Decimal
from typing import List, Optional

from interfaces.TemperatureClient import TemperatureClient
from models.DateRange import DateRange
from models.Temperature import Temperature


class TemperatureInMemoryClient(TemperatureClient):
    # station_id is dict key. List of temperature data is sorted ascending by date
    station_temperature_dict: typing.Dict[str, List[Temperature]] = {}

    def __init__(self, initial_data: typing.Dict[str, List[Temperature]]):
        self.station_temperature_dict = initial_data

    def list_stations(self) -> List[str]:
        return list(self.station_temperature_dict.keys())

    def get_temperatures_by_station(self, station_id: str, window: Optional[DateRange] = None) \
            -> Optional[List[Temperature]]:

        temperature_list = self.station_temperature_dict.get(station_id)

        if window:
            return self._filter_list(temperature_list, window)
        else:
            return temperature_list

    @staticmethod
    def _filter_list(temperature_list: List[Temperature], window: DateRange) -> List[Temperature]:

        if len(temperature_list) == 0:
            return temperature_list

        dates = [temperature.date for temperature in temperature_list]
        # Filter dates using binary search since dates in list are sorted.
        start_index = bisect_left(dates, Decimal(window.start_date))
        end_index = bisect_right(dates, Decimal(window.end_date), start_index)

        return temperature_list[start_index:end_index]

