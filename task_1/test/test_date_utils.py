import unittest
from datetime import datetime

from date_utils import get_end_of_month


class TestGetEndOfMonth(unittest.TestCase):

    def test_end_of_current_month(self):
        """Конец текущего месяца"""
        dtime = datetime(2024, 8, 9)  # 9 августа 2024 года
        expected = datetime(2024, 8, 31, 23, 59, 59)  # 31 августа 2024 года

        result = get_end_of_month(dtime, 0)
        self.assertEqual(result, expected)

    def test_end_of_next_month(self):
        """Конец следующего месяца"""
        dtime = datetime(2024, 8, 15, 14, 30)  # 15 августа 2024 года
        expected = datetime(2024, 9, 30, 23, 59, 59)  # 30 сентября 2024 года

        result = get_end_of_month(dtime, 1)
        self.assertEqual(result, expected)

    def test_end_of_previous_month(self):
        """Конец прошлого месяца"""
        dtime = datetime(2024, 8, 15, 14, 30)  # 15 августа 2024 года
        expected = datetime(2024, 7, 1, 23, 59, 59)  # 31 июля 2024 года

        result = get_end_of_month(dtime, -1)
        self.assertEqual(result, expected)

    def test_end_of_february_in_leap_year(self):
        """Конец февраля в високосном году месяца"""
        dtime = datetime(2024, 1, 15, 14, 30)  # 15 января 2024 года
        expected = datetime(
            2024, 2, 29, 23, 59, 59
        )  # 29 февраля 2024 года (високосный год)

        result = get_end_of_month(dtime, 1)
        self.assertEqual(result, expected)

    def test_end_of_february_in_non_leap_year(self):
        """Конец февраля не в високосном году месяца"""
        dtime = datetime(2023, 1, 15, 14, 30)  # 15 января 2023 года
        expected = datetime(
            2023, 2, 28, 23, 59, 59
        )  # 28 февраля 2023 года (не високосный год)

        result = get_end_of_month(dtime, 1)
        self.assertEqual(result, expected)
