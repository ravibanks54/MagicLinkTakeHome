from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Temperature:
    station_id: str
    date: Decimal
    degrees_c: Decimal
