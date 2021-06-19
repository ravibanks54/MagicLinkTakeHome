from unittest import TestCase

from models.DateRange import DateRange


class TestDateRange(TestCase):
    def test_constructor_success(self):
        DateRange('2020.01', '2020.02')

    def test_constructor_invalid_arguments(self):
        self.assertRaises(AssertionError, lambda: DateRange('2020.02', '2020.01'))

