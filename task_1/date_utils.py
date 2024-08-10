from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta


def get_end_of_month(dtime: datetime, add_months: int) -> datetime:
    """
    Возвращает последний день месяца для заданной даты и времени c учетом добавления/вычитания месяцев.
    В случае если add_months < 0, возвращается первый день месяца

    Args:
        dtime (datetime): Дата и время, вычисления границ месяца.
        add_months (int, optional): Количество месяцев, которые нужно добавить/вычесть к дате. Значение по умолчанию - 0.

    Returns:
        datetime: дата с нужным месяцем
    """
    if add_months >= 0:
        add_months += 1

    # переход у первому дню следующего месяца от нужного
    last_day_month = dtime.replace(
        day=1, hour=23, minute=59, second=59, microsecond=0
    ) + relativedelta(months=add_months)

    if add_months >= 0:
        # получение нужного месяца
        last_day_month -= timedelta(days=1)

    return last_day_month


def get_current_dtime(): return datetime.today()
