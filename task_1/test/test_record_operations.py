import unittest
from datetime import datetime
from unittest.mock import patch

from config import DATE_FORMAT_TEXT, RECORD_FORMAT_TEXT
from date_utils import get_current_dtime
from formatters import format_record
from models import Record
from record_operations import get_expiring_records


class TestGetExpiringRecords(unittest.TestCase):

    @patch("formatters.format_record")
    @patch("builtins.print")
    @patch("date_utils.datetime")
    def test_get_expiring_records(
        self, mock_get_current_dtime, mock_print, mock_format_record, 
    ):
        """Возврат записей. Вывод в консоль записей с датами и без"""

        mocked_today = datetime(2024, 8, 1)
        mock_get_current_dtime.today.return_value = mocked_today
        self.assertEqual(get_current_dtime(), datetime(2024, 8, 1, 0, 0, 0))

        # тестовые данные
        records = [
            Record(
                begin=datetime(2024, 6, 1),
                end=datetime(2024, 7, 15),
                record_id=1,
                name="Record 1",
            ),
            Record(
                begin=datetime(2024, 7, 1),
                end=datetime(2024, 8, 10),
                record_id=2,
                name="Record 2",
            ),
            Record(
                begin=datetime(2024, 8, 1),
                end=datetime(2024, 8, 31),
                record_id=3,
                name="Record 3",
            ),
        ]

        # записи, которые должны быть возвращены
        expected_records = [
            Record(
                begin=datetime(2024, 7, 1),
                end=datetime(2024, 8, 10),
                record_id=2,
                name="Record 2",
            ),
            Record(
                begin=datetime(2024, 8, 1),
                end=datetime(2024, 8, 31),
                record_id=3,
                name="Record 3",
            ),
        ]

        # фиксированные форматированык записи
        mock_format_record.side_effect = lambda record, include_dates: (
            f"Record ID: {record.record_id}, Name: {record.name}, Begin: {record.begin}, End: {record.end}"
            if include_dates
            else f"Record ID: {record.record_id}, Name: {record.name}"
        )

        # запуск тестируемой функции
        result_1 = get_expiring_records(
            records, add_months=0, with_print=True, include_dates=True
        )
        result_2 = get_expiring_records(
            records, add_months=0, with_print=True, include_dates=False
        )

        self.assertEqual(result_1, expected_records)
        self.assertEqual(result_2, expected_records)

        expected_output_1 = [
            f"Record ID: 2, Name: Record 2, Begin: {datetime(2024, 7, 1)}, End: {datetime(2024, 8, 10)}",
            f"Record ID: 3, Name: Record 3, Begin: {datetime(2024, 8, 1)}, End: {datetime(2024, 8, 31)}",
        ]

        expected_output_2 = [
            "Record ID: 2, Name: Record 2",
            "Record ID: 3, Name: Record 3",
        ]

        for output in expected_output_1:
            mock_print.assert_any_call(output)

        for output in expected_output_2:
            mock_print.assert_any_call(output)

        self.assertEqual(
            mock_print.call_count, len(expected_output_1) + len(expected_output_2)
        )

    @patch("date_utils.get_end_of_month")
    def test_no_expiring_records(self, mock_get_end_of_month):
        mock_get_end_of_month.return_value = datetime(2024, 8, 31, 23, 59, 59)

        # записи, которые не истекают в текущем месяце
        records = [
            Record(
                begin=datetime(2024, 1, 1),
                end=datetime(2024, 2, 1),
                record_id=1,
                name="Record 1",
            ),
            Record(
                begin=datetime(2024, 3, 1),
                end=datetime(2024, 4, 1),
                record_id=2,
                name="Record 2",
            ),
        ]

        result = get_expiring_records(records, add_months=0)

        self.assertEqual(result, [])

    @patch("date_utils.get_end_of_month")
    def test_expiring_records_with_negative_months(self, mock_get_end_of_month):
        """Записи истекшие в прошлом месяце"""

        mock_get_end_of_month.return_value = datetime(2024, 8, 9, 23, 59, 59)

        # тестовые записи
        records = [
            Record(
                begin=datetime(2024, 4, 15),
                end=datetime(2024, 7, 15),
                record_id=1,
                name="Record 1",
            ),
            Record(
                begin=datetime(2024, 7, 1),
                end=datetime(2024, 8, 15),
                record_id=2,
                name="Record 2",
            ),
        ]

        result = get_expiring_records(records, add_months=-2)

        # ожидаемая запись
        expected_records = [
            Record(
                begin=datetime(2024, 4, 15),
                end=datetime(2024, 7, 15),
                record_id=1,
                name="Record 1",
            )
        ]
        self.assertEqual(result, expected_records)


if __name__ == "__main__":
    unittest.main()
