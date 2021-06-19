from unittest import TestCase

from accessors.TemperatureInMemoryClient import TemperatureInMemoryClient
from components.TemperatureAnalyzer import TemperatureAnalyzer
from utils import csv_loader


class TestTemperatureAnalyzer(TestCase):

    def setUp(self):
        client = TemperatureInMemoryClient(csv_loader.load_temperature_data('tests/data/test.csv'))
        self.analyzer = TemperatureAnalyzer(client)

    def test_get_lowest_temperature(self):
        station_date_pair = self.analyzer.get_lowest_temperature()
        self.assertIsNotNone(station_date_pair)
        station, date = station_date_pair
        expected_station = '68'
        expected_date = '2000.542'
        self.assertEqual(expected_station, station)
        self.assertEqual(expected_date, date)

    def test_get_largest_temperature_fluctuation(self):
        station_id = self.analyzer.get_largest_temperature_fluctuation()
        expected_station_id = '68'
        self.assertEqual(expected_station_id, station_id)

    def test_get_largest_temperature_fluctuation_over_range(self):
        station_id = self.analyzer.get_largest_temperature_fluctuation_over_range('0.0', '3020.0')
        expected_station_id = '68'
        self.assertEqual(expected_station_id, station_id)

    def test_get_largest_temperature_fluctuation_over_range_inclusive(self):
        station_id = self.analyzer.get_largest_temperature_fluctuation_over_range('2000.375', '2004.125')
        expected_station_id = '68'
        self.assertEqual(expected_station_id, station_id)

    def test_get_largest_temperature_fluctuation_outside_range(self):
        station_id = self.analyzer.get_largest_temperature_fluctuation_over_range('0.0', '1.0')
        self.assertIsNone(station_id)



class TestTemperatureAnalyzerEmptyData(TestCase):

    def setUp(self):
        client = TemperatureInMemoryClient(csv_loader.load_temperature_data('tests/data/empty.csv'))
        self.analyzer = TemperatureAnalyzer(client)

    def test_get_lowest_temperature_returns_none(self):
        station_date_pair = self.analyzer.get_lowest_temperature()
        self.assertIsNone(station_date_pair)

    def test_get_largest_temperature_fluctuation_returns_none(self):
        station_id = self.analyzer.get_largest_temperature_fluctuation()
        self.assertIsNone(station_id)

    def test_get_largest_temperature_fluctuation_over_range_returns_none(self):
        station_id = self.analyzer.get_largest_temperature_fluctuation_over_range('', '')
        self.assertIsNone(station_id)

