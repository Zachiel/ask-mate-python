"""Data read/write and manipulation functions."""
import csv
from datetime import datetime, timedelta
from typing import Any

HEADERS_QUESTION: list[str] = ['id', 'submission_time', 'view_number',
                    'vote_number', 'title', 'message', 'image']
HEADERS_ANSWER: list[str] = ['id', 'submission_time', 'vote_number',
                            'question_id', 'message', 'image']

def get_data_from_file(filename: str) -> list[Any]:
    """Read data from file into list of dictionaries."""
    with open(filename, 'r', encoding='UTF-8') as data:
        data_list = []
        reader = csv.DictReader(data)
        for item in reader:
            data_list.append(item)
        return data_list


def write_data_to_file(filename: str, data_dict: list[dict[str, str]]) -> None:
    """Write dictionaries to file."""


def sorter(data_dict: list[dict[str, str]], sort_by='submission_time',
           descending=True) -> list[dict[str, str]]:
    """Sort given data by specific header."""


def convert_date(unix_date: int) -> str:
    """Convert unix date into human format."""
    epoch_time = datetime.datetime.strftime(datetime.datetime.fromtimestamp(unix_date), '%d/%m/%Y, %H:%M:%S')
    print(epoch_time)
    return 'ok'


def generate_id() -> str:
    """Generate new id."""
