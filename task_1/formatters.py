from config import DATE_FORMAT_TEXT, RECORD_FORMAT_TEXT
from models import Record


def format_record(record: Record, include_dates: bool) -> str:
    """
    Форматирует запись в строку в зависимости от необходимости включения дат.

    Args:
        record (Record): Словарь, представляющий запись.
        include_dates (bool): Флаг, указывающий на необходимость добавления дат в форматированную строку.

    Returns:
        str: Форматированная строка записи.
    """
    # форматирование основной части записи
    output = RECORD_FORMAT_TEXT.format(record_id=record.record_id, name=record.name)
    # добавление форматирования дат, если это требуется
    if include_dates:
        output += DATE_FORMAT_TEXT.format(begin=record.begin, end=record.end)

    return output
