from dataclasses import dataclass
from decimal import Decimal


@dataclass
class DateRange:
    start_date: str
    end_date: str

    def __post_init__(self):
        assert Decimal(self.end_date) >= Decimal(self.start_date)
