import argparse


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-records", "-r", required=True, type=str, help="JSON string with records"
    )
    parser.add_argument(
        "-with_print", "-p", action="store_true", help="Flag to print records"
    )
    parser.add_argument(
        "-include_dates",
        "-d",
        action="store_true",
        help="Flag to include dates in output",
    )
    parser.add_argument(
        "-add_months", "-m", default=0, type=int, help="How many months to add"
    )

    return parser.parse_args()
