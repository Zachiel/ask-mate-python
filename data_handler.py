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


def count_comments(questions: list[dict[str, str]],
                   answers: list[dict[str, str]]) -> dict[str, int]:
    """Get comment count for each question."""
    comments_count = {}
    for question in questions:
        for key, value in question.items():
            if key == 'id':
                comments_count.update({value: 0})
    for answer in answers:
        for key, value in answer.items():
            if key == 'question_id':
                comments_count[value] += 1
    return comments_count


def sorter(data_dict: list[dict[str, str]], sort_by='submission_time',
           descending=True) -> list[dict[str, str]]:
    """Sort given data by specific header."""


def how_much_time_passed(unix_date: int) -> str:
    """Calculate how much time has passed since date."""
    time_now = datetime.now()
    time_then = datetime.fromtimestamp(int(unix_date))
    delta = time_now - time_then
    delta = delta - timedelta(microseconds=delta.microseconds)
    time_list = str(delta).split(',')
    if len(time_list) == 1:
        hours, minutes, seconds = [int(time) for time in time_list[0].split(':')]
        if hours > 0:
            return f'{hours} hours ago'
        if minutes > 0:
            return f'{minutes} minutes ago'
        if seconds > 0:
            return f'{seconds} seconds ago'
    days = int(time_list[0].split(' ')[0])
    if (days // 365) > 0:
        return f'{days // 365} years ago'
    return f'{days} days ago'



def generate_id() -> str:
    """Generate new id."""
