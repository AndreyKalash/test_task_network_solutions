from typing import List

from date_utils import get_end_of_month, get_current_dtime
from formatters import format_record
from models import Record


def get_expiring_records(
    records: List[Record],
    add_months: int = 0,
    with_print: bool = False,
    include_dates: bool = False,
) -> List[Record]:
    """
    Возвращает список записей, срок действия которых заканчивается в определенном месяце от текущей даты.

    Args:
        records (List[Record]): Список записей.
        add_months(int, optional): Количество добавляемых месяцев. Принимает отрицательные значения. По умолчанию - 0 (текущий месяц).
        with_print (bool, optional): Флаг для вывода записей. По умолчанию False.
        include_dates (bool, optional): Флаг для включения дат в вывод. По умолчанию False.

    Returns:
        List[Record]: Список записей, срок действия которых заканчивается в текущем месяце.
    """
    # получение текущей даты
    current_dtime = get_current_dtime()
    # последний день нужного месяца
    last_day = get_end_of_month(current_dtime, add_months)

    # список для записей, заканчивающихся в текущем месяце
    res_records = []

    # итерация по записям
    for record in records:
        # если дата окончания в нужном месяце - добавляем запись
        if min(current_dtime, last_day) < record.end <= max(current_dtime, last_day):
            res_records.append(record)
            # вывод записи в консоль
            if with_print:
                print(format_record(record, include_dates))

    return res_records
