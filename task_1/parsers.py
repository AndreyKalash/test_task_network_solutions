import json
from datetime import datetime
from typing import List

from config import DATE_FORMAT
from models import Record


def records_from_string(json_string: str) -> List[Record]:
    """
    Преобразует JSON-строку в список записей.

    Args:
        json_string (str): JSON-строка, представляющая список записей.

    Returns:
        List[Record]: Список записей, полученных из JSON-строки.

    Raises:
        ValueError:
            - Если строка не соответствует синтаксису JSON.
            - Если для поля в записи передается неверный тип данных
        TypeError:
            - Если строка не соответствует формату List[].
            - Если в записи присутсвуют лишние поля
        KeyError: Если в записи отсутсвует нужное поле.
    """
    try:
        data = json.loads(json_string.replace("'", '"'))
    except json.JSONDecodeError as ex:
        raise ValueError(
            f"The string does not match the JSON syntax. {ex.msg}: line {ex.lineno} column {ex.colno} - {ex.pos}"
        )

    if not isinstance(data, list):
        raise TypeError("The string does not match to the 'List[]' format")

    records = []
    for i, item in enumerate(data, 1):
        try:
            begin = item["begin"]
            if begin == '0000-00-00 00:00:00':
                begin = '0001-01-01 00:00:00'
            end = item["end"]
            item["begin"] = datetime.strptime(begin, DATE_FORMAT)
            item["end"] = datetime.strptime(end, DATE_FORMAT)
            record = Record(**item)
        except KeyError as e:
            raise KeyError(f"Missing required field in record {i}: {str(e)}")
        except ValueError as e:
            raise ValueError(f"Error in record {i}: {str(e)}")
        except TypeError as e:
            raise TypeError(f"Error in record {i}: {str(e)}")
        records.append(record)

    return records
