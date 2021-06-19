import csv
import typing
from decimal import Decimal
from typing import List

from constants import DATE_FIELD, STATION_ID_FIELD, TEMPERATURE_C_FIELD
from models.Temperature import Temperature


def load_temperature_data(filepath: str) -> typing.Dict[str, List[Temperature]]:
    temperature_dict = {}
    with open(filepath, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            station_id = row[STATION_ID_FIELD]
            date = Decimal(row[DATE_FIELD])
            temperature_c = Decimal(row[TEMPERATURE_C_FIELD])
            if station_id in temperature_dict:
                temperature_dict[station_id].append(Temperature(station_id, date, temperature_c))
            else:
                temperature_dict[station_id] = [Temperature(station_id, date, temperature_c)]
    return temperature_dict
