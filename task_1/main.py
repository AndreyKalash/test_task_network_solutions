import warnings

from cli import get_args
from parsers import records_from_string
from record_operations import get_expiring_records


def main() -> None:
    # получаем аргументы
    args = get_args()

    records_str = args.records
    with_print = args.with_print
    include_dates = args.include_dates
    add_months = args.add_months

    # предупреждение
    if include_dates and not with_print:
        warnings.warn(
            "Dates will not be included in the output since 'with_print' is not enabled."
        )

    records = records_from_string(records_str)
    req_records = get_expiring_records(records, add_months, with_print, include_dates)
    return req_records

if __name__ == "__main__":
    main()
