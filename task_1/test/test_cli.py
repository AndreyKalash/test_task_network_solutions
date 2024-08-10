import unittest
from unittest.mock import patch

from cli import get_args


class TestGetArgs(unittest.TestCase):
    def test_get_args_with_all_arguments(self):
        """Все аргументы"""
        test_args = [
            "",
            "-r",
            '[{"record_id": 1, "name": "test", "begin": "2024-08-09 12:00:00", "end": "2024-08-09 12:30:00"}]',
            "-p",
            "-d",
            "-m",
            "2",
        ]
        with patch("sys.argv", test_args):
            args = get_args()
            self.assertEqual(
                args.records,
                '[{"record_id": 1, "name": "test", "begin": "2024-08-09 12:00:00", "end": "2024-08-09 12:30:00"}]',
            )
            self.assertTrue(args.with_print)
            self.assertTrue(args.include_dates)
            self.assertEqual(args.add_months, 2)

    def test_get_args_with_required_arguments(self):
        """Все требуемые аргументы"""
        test_args = [
            "",
            "-r",
            '[{"record_id": 1, "name": "test", "begin": "2024-08-09 12:00:00", "end": "2024-08-09 12:30:00"}]',
        ]
        with patch("sys.argv", test_args):
            args = get_args()
            self.assertEqual(
                args.records,
                '[{"record_id": 1, "name": "test", "begin": "2024-08-09 12:00:00", "end": "2024-08-09 12:30:00"}]',
            )
            self.assertFalse(args.with_print)
            self.assertFalse(args.include_dates)
            self.assertEqual(args.add_months, 0)

    def test_get_args_with_print_with_value(self):
        """with_print c значением"""
        test_args = [
            "",
            "-r",
            '[{"record_id": 1, "name": "test", "begin": "2024-08-09 12:00:00", "end": "2024-08-09 12:30:00"}]',
            "-p",
            "True",
        ]
        with patch("sys.argv", test_args):
            with self.assertRaises(SystemExit):
                get_args()

    def test_get_args_include_dates_with_value(self):
        """include_dates c значением"""
        test_args = [
            "",
            "-r",
            '[{"record_id": 1, "name": "test", "begin": "2024-08-09 12:00:00", "end": "2024-08-09 12:30:00"}]',
            "-d",
            "True",
        ]
        with patch("sys.argv", test_args):
            with self.assertRaises(SystemExit):
                get_args()

    def test_get_args_add_months_with_value(self):
        """add_months неверный тип данных"""
        test_args = [
            "",
            "-r",
            '[{"record_id": 1, "name": "test", "begin": "2024-08-09 12:00:00", "end": "2024-08-09 12:30:00"}]',
            "-m",
            "True",
        ]
        with patch("sys.argv", test_args):
            with self.assertRaises(SystemExit):
                get_args()

    def test_get_args_without_arguments(self):
        """Без требуемых аргументы"""
        test_args = [""]
        with patch("sys.argv", test_args):
            with self.assertRaises(SystemExit):
                get_args()


if __name__ == "__main__":
    unittest.main()
