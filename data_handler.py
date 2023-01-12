"""Data read/write and manipulation functions."""
import csv
from datetime import datetime, timedelta
from typing import Any

HEADERS_QUESTION: list[str] = ['id', 'submission_time', 'view_number',
                    'vote_number', 'title', 'message', 'image']
HEADERS_ANSWER: list[str] = ['id', 'submission_time', 'vote_number',
                            'question_id', 'message', 'image']
QUESTION_PATH = 'sample_data/question.csv'
ANSWER_PATH = 'sample_data/answer.csv'

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


def count_comments() -> dict[str, int]:
    """Get comment count for each question."""
    comments_count = {}
    questions = get_data_from_file('sample_data/question.csv')
    answers = get_data_from_file('sample_data/answer.csv')
    for question in questions:
        for key, value in question.items():
            if key == 'id':
                comments_count.update({value: 0})
    for answer in answers:
        for key, value in answer.items():
            if key == 'question_id':
                comments_count[value] += 1
    return comments_count


def sorter(data_dict: list[dict[str, str]], sort_by='date',
           direction='descending') -> list[dict[str, str]]:
    """Sort given data by specific header."""
    order_translate: dict[str, str] = {'date': 'submission_time',
                    'title': 'title', 'message': 'message',
                    'views': 'view_number', 'votes': 'vote_number',
                    'comments': 'comments'}
    if sort_by in ['date', 'views', 'votes']:
        ordered = sorted(data_dict,
                        key=lambda k: int(k[order_translate[sort_by]]),
                        reverse=direction == 'descending')
        return ordered
    if sort_by != 'comments':
        ordered = sorted(data_dict,
                        key=lambda k: k[order_translate[sort_by]],
                        reverse=direction == 'descending')
        return ordered
    comments: dict[str, int] = count_comments()
    comments = sorted(comments.items(), key=lambda k: k[1],
                    reverse=direction == 'descending')
    ordered_set: set[dict[str, str]] = set()
    for key in comments.keys():
        for item in data_dict:
            if key == item['id']:
                ordered_set.add(item)
    for item in data_dict:
        if item not in ordered_set:
            ordered_set.add(item)
    return list(ordered_set)


def how_much_time_passed(unix_date: int) -> str:
    """Calculate how much time has passed since date."""
    time_now: datetime = datetime.now()
    time_then: datetime = datetime.fromtimestamp(int(unix_date))
    delta: timedelta = time_now - time_then
    delta: timedelta = delta - timedelta(microseconds=delta.microseconds)
    time_list: list[str] = str(delta).split(',')
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


