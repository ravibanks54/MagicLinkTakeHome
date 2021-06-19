from abc import ABC, abstractmethod
from typing import List, Optional

from models.DateRange import DateRange
from models.Temperature import Temperature


class TemperatureClient(ABC):

    @abstractmethod
    def list_stations(self) -> List[str]:
        pass

    @abstractmethod
    def get_temperatures_by_station(self, station_id: str, window: Optional[DateRange] = None) -> List[Temperature]:
        pass
