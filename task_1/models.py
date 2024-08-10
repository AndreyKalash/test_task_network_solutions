from dataclasses import dataclass
from datetime import datetime


@dataclass
class Record:
    begin: datetime
    end: datetime
    record_id: int
    name: str

    def __post_init__(self):
        if not isinstance(self.begin, datetime):
            raise ValueError("'begin' must be a datetime object")
        if not isinstance(self.end, datetime):
            raise ValueError("'end' must be a datetime object")
        if not isinstance(self.record_id, int):
            raise ValueError("'record_id' must be an integer")
        if not isinstance(self.name, str):
            raise ValueError("'name' must be a string")
