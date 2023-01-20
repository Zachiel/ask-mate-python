"""Data read/write and manipulation functions."""
import csv
from datetime import datetime, timedelta
from typing import Any
import string
import random
import psycopg2
import database_common

HEADERS_QUESTION: list[str] = ['id', 'submission_time', 'view_number',
                    'vote_number', 'title', 'message', 'image']
HEADERS_ANSWER: list[str] = ['id', 'submission_time', 'vote_number',
                            'question_id', 'message', 'image']
QUESTION_PATH = 'sample_data/question.csv'

ANSWER_PATH = 'sample_data/answer.csv'

@database_common.connection_handler
def get_questions(cursor):
    query = """
        SELECT *
        FROM question"""
    cursor.execute(query)
    desc = cursor.description
    column_names = [col[0] for col in desc]
    question_sql = [dict(zip(column_names, row)) for row in cursor.fetchall()]
    return (question_sql)

@database_common.connection_handler
def get_answers(cursor):
    query = """
        SELECT *
        FROM answer"""
    cursor.execute(query)
    desc = cursor.description
    column_names = [col[0] for col in desc]
    answer_sql = [dict(zip(column_names, row)) for row in cursor.fetchall()]
    return (answer_sql)

def get_question_by_id(question_ids):
    questions = get_questions()
    for question in questions:
        if question['question_id'] == int(question_ids):
            return question



def add_data_to_file(mode, question_id='', message='', title=''):
    if mode == 'answer':
        new_answer = {}
        new_answer['id'] = generate_id()
        new_answer['submission_time'] = time_now()
        new_answer['vote_number'] = '0'
        new_answer['question_id'] = question_id
        new_answer['message'] = message
        
        write_data_to_file(HEADERS_ANSWER,
                            ANSWER_PATH,
                            new_answer)
        
    elif mode == 'question':
        new_question = {}
        new_question['id'] = generate_id()
        new_question['submission_time'] = time_now()
        new_question['view_number'] = '0'
        new_question['vote_number'] = '0'
        new_question['title'] = title
        new_question['message'] = message
        write_data_to_file(HEADERS_QUESTION,
                                        QUESTION_PATH,
                                        new_question)
    else:
        print('Wrong mode!')

        
def voting_questions(question_id, mode):
    questions = get_data_from_file(QUESTION_PATH)
    
    for question in questions:
        if question['id'] == question_id:
            num = int(question['vote_number'])
            if mode == 'up':
                num += 1
            elif mode == 'down':
                num -= 1
            else:
                print('Wrong mode!')

            question['vote_number'] = str(num)
            delete_question_from_file_by_id('sample_data/question.csv', question_id)
            write_data_to_file(HEADERS_QUESTION, QUESTION_PATH, question)
            break
        

def get_data_from_file(filename: str) -> list[Any]:
    """Read data from file into list of dictionaries."""
    with open(filename, 'r', encoding='UTF-8') as data:
        data_list = []
        reader = csv.DictReader(data)
        for item in reader:
            data_list.append(item)
        return data_list



def delete_question_from_file_by_id(filename: str, id):
    lines = []
    with open(filename, 'r') as readFile:
        reader = csv.DictReader(readFile, fieldnames=HEADERS_QUESTION)
        for row in reader:
            lines.append(row)
            if row['id'] == id:
                lines.remove(row)
    with open(filename, 'w') as writeFile:
        writer = csv.DictWriter(writeFile, fieldnames=HEADERS_QUESTION)
        writer.writerows(lines)
                

def delete_answers_for_question_id(filename: str, question_id):
    lines = []
    with open(filename, 'r') as readFile:
        reader = csv.DictReader(readFile, fieldnames=HEADERS_ANSWER)
        for row in reader:
            lines.append(row)
            if row['question_id'] == question_id:
                lines.remove(row)
    with open(filename, 'w') as writeFile:
        writer = csv.DictWriter(writeFile, fieldnames=HEADERS_ANSWER)
        writer.writerows(lines)


def delete_specific_answer(answer_id, filename=ANSWER_PATH):
    lines = []
    with open(filename, 'r') as readFile:
        reader = csv.DictReader(readFile, fieldnames=HEADERS_ANSWER)
        for row in reader:
            if row['id'] != answer_id:
                lines.append(row)
    with open(filename, 'w') as writeFile:
        writer = csv.DictWriter(writeFile, fieldnames=HEADERS_ANSWER)
        writer.writerows(lines)



def write_data_to_file(headers, filename: str, data_dict: dict[str, str]):
    """Write dictionaries to file."""
    with open(filename, 'a+', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writerow(data_dict)


def generate_id():
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    alphabet = list(string.ascii_lowercase)
    data = get_data_from_file(QUESTION_PATH)
    ids = []
    for question in data:
        ids.append(question['id'])
    id = random.choice(numbers) + random.choice(numbers) +random.choice(alphabet)
    if id in ids:
        generate_id()
    else:
        return id

def count_comments() -> dict[str, int]:
    """Get comment count for each question."""
    comments_count = {}
    questions = get_data_from_file(QUESTION_PATH)
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

#print(count_comments())
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

def time_now():
    time_now  = datetime.now()
    time_now = int(round(datetime.timestamp(time_now), 0))
    return time_now


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
    days_1 = time_list[0].split(' ')
    days = int(days_1[0])
    if (days // 365) > 0:
        return f'{days // 365} years ago'
    return f'{days} days ago'

