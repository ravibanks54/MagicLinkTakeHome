from unittest import TestCase

from utils import csv_loader


class TestCsvLoader(TestCase):
    def test_load_temperature(self):
        csv_loader.load_temperature_data('tests/data/test.csv')

    def test_load_temperature_empty(self):
        temperatures = csv_loader.load_temperature_data('tests/data/empty.csv')
        self.assertTrue(len(temperatures) == 0)
