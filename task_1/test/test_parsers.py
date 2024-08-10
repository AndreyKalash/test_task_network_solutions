import unittest
from datetime import datetime

from models import Record
from parsers import records_from_string


class TestRecordsFromString(unittest.TestCase):

    def test_valid_string(self):
        """Валидная json строка с списком записей"""
        json_str = """[{"begin": "2020-03-06 14:00:20", "end": "2021-12-03 23:59:50", "record_id": 2, "name": "RecordTwo"}]"""
        expected = [
            Record(
                begin=datetime(2020, 3, 6, 14, 0, 20),
                end=datetime(2021, 12, 3, 23, 59, 50),
                record_id=2,
                name="RecordTwo",
            )
        ]
        result = records_from_string(json_str)
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Record)
        self.assertEqual(result[0].record_id, 2)

        json_str = """[{"begin": "2020-03-06 14:00:20", "end": "2021-12-03 23:59:50", "record_id": 2, "name": "RecordTwo"}, {"begin": "2020-03-06 14:00:20", "end": "2021-12-03 23:59:50", "record_id": 3, "name": "RecordTwo"}]"""
        expected = [
            Record(
                begin=datetime(2020, 3, 6, 14, 0, 20),
                end=datetime(2021, 12, 3, 23, 59, 50),
                record_id=2,
                name="RecordTwo",
            ),
            Record(
                begin=datetime(2020, 3, 6, 14, 0, 20),
                end=datetime(2021, 12, 3, 23, 59, 50),
                record_id=3,
                name="RecordTwo",
            ),
        ]
        result = records_from_string(json_str)
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[1], Record)
        self.assertEqual(result[1].record_id, 3)

    def test_default_date_values(self):
        """Данные в датах по умолчанию"""
        json_str_1 = '[{"record_id": 2, "name": "RecordTwo", "begin": "0000-00-00 00:00:00", "end": "9999-12-31 23:59:59"}]'
        expected = [
            Record(
                begin=datetime(1, 1, 1),
                end=datetime(9999, 12, 31, 23, 59, 59),
                record_id=2,
                name="RecordTwo",
            )]
        results = records_from_string(json_str_1)
        self.assertEqual(expected, results)

    def test_invalid_json(self):
        """Невалидная json строка"""
        json_str_2 = '[{"invalid]'
        json_str_2 = """[{"begin": "2020-03-06 14:00:20", "end": "2021-12-03 23:59:50", "record_id": 2, "name": "RecordTwo"},]"""
        with self.assertRaises(ValueError):
            records_from_string('[{"invalid]')
            records_from_string(json_str_2)

    def test_not_list_json(self):
        """Невалидная json строка - не список"""
        with self.assertRaises(TypeError):
            records_from_string('{"key": "value"}')

    def test_invalid_date_format(self):
        """Невалидная json строка - неверный формат даты и времени в записи"""
        json_str_1 = '[{"record_id": 1, "name": "Test", "begin": "2023-01-01", "end": "2023-01-02"}]'
        json_str_2 = '[{"record_id": 1, "name": "Test", "begin": "2023.01.01 23-14-15", "end": "2023.01.02 23-14-15"}]'
        with self.assertRaises(ValueError):
            records_from_string(json_str_1)
            records_from_string(json_str_2)

    def test_invalid_date(self):
        """Невалидная json строка - неверная дата в записи"""
        json_str_1 = '[{"record_id": 1, "name": "Test", "begin": "2024-08-32 00:00:00", "end": "2024-08-32 00:00:00"}]'
        json_str_2 = '[{"record_id": 1, "name": "Test", "begin": "INVALID_DATE", "end": "INVALID_DATE"}]'
        with self.assertRaises(ValueError):
            records_from_string(json_str_1)
            records_from_string(json_str_2)

    def test_invalid_record_id_type(self):
        """Невалидная json строка - неверный тип данных поля 'record_id' в записи"""
        json_str = '[{"record_id": "not_an_integer", "name": "Test", "begin": "2023-01-01 00:00:00", "end": "2023-01-02 00:00:00"}]'
        with self.assertRaises(ValueError):
            records_from_string(json_str)

    def test_invalid_name_type(self):
        """Невалидная json строка - неверный тип данных поля 'name' в записи"""
        json_str = '[{"record_id": 1, "name": 123, "begin": "2023-01-01 00:00:00", "end": "2023-01-02 00:00:00"}]'
        with self.assertRaises(ValueError):
            records_from_string(json_str)

    def test_missing_field(self):
        """Невалидная json строка - отсутствие поля в записи"""
        json_str = '[{"record_id": 1, "name": "Test", "begin": "2023-01-01 00:00:00"}]'
        with self.assertRaises(KeyError):
            records_from_string(json_str)

    def test_extra_field(self):
        """Невалидная json строка - лишние поля в записи"""
        json_str = '[{"record_id": 1, "name": "Test", "begin": "2023-01-01 00:00:00", "end": "2023-01-01 00:00:00", "extra": "field"}]'
        with self.assertRaises(TypeError):
            records_from_string(json_str)

    def test_invalid_records(self):
        """Невалидная json строка - в списке не записи"""
        json_str = "[1, 2, 'asd']"
        with self.assertRaises(TypeError):
            records_from_string(json_str)


if __name__ == "__main__":
    unittest.main()
