from decimal import Decimal
from unittest import TestCase

from accessors.TemperatureInMemoryClient import TemperatureInMemoryClient
from models.DateRange import DateRange
from models.Temperature import Temperature


class TestTemperatureInMemoryClient(TestCase):

    def setUp(self):
        data = {'68':
                [Temperature('68', Decimal('2020.01'), Decimal('1.123')),
                 Temperature('68', Decimal('2020.02'), Decimal('2.0')),
                 Temperature('68', Decimal('2021.90'), Decimal('-5.0')),
                 Temperature('68', Decimal('2021.99'), Decimal('10.0'))
                 ],
                '999':
                [Temperature('999', Decimal('2021.11'), Decimal('5.0')),
                 Temperature('999', Decimal('2022.11'), Decimal('5.1'))],
                '1000':
                [Temperature('1000', Decimal('2000.03'), Decimal('1.123'))]}
        self.client = TemperatureInMemoryClient(data)

    def test_list_stations(self):
        stations = self.client.list_stations()
        expected_stations = ['68', '999', '1000']
        self.assertEqual(expected_stations, stations)

    def test_get_temperatures_by_station(self):
        temperatures = self.client.get_temperatures_by_station('999')
        expected_temperatures = \
            [Temperature('999', Decimal('2021.11'), Decimal('5.0')),
             Temperature('999', Decimal('2022.11'), Decimal('5.1'))]
        self.assertEqual(expected_temperatures, temperatures)

    def test_get_temperatures_by_station_with_date_range(self):
        temperatures = self.client.get_temperatures_by_station('68', DateRange('2020.00', '2021.00'))
        expected_temperatures = \
            [Temperature('68', Decimal('2020.01'), Decimal('1.123')),
             Temperature('68', Decimal('2020.02'), Decimal('2.0'))]
        self.assertEqual(expected_temperatures, temperatures)

    def test_get_temperatures_by_station_outside_of_date_range(self):
        temperatures = self.client.get_temperatures_by_station('68', DateRange('2019.00', '2020.00'))
        self.assertTrue(len(temperatures) == 0)


class TestTemperatureInMemoryClientEmptyData(TestCase):

    def test_list_stations_returns_empty_list(self):
        self.client = TemperatureInMemoryClient({})
        stations = self.client.list_stations()
        self.assertTrue(len(stations) == 0)

    def test_get_temperatures_by_station_returns_empty_list(self):
        self.client = TemperatureInMemoryClient({'68': []})
        self.assertTrue(len(self.client.get_temperatures_by_station('68')) == 0)
