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



@database_common.connection_handler
def get_data(cursor, data_type: str, sort_by='date',
           order='DESC') -> list[dict[str, str]]:
    """Sort given data by specific header."""
    sort_by_translate: dict[str, str] = {'date': 'submission_time',
                    'title': 'title', 'message': 'message',
                    'views': 'view_number', 'votes': 'vote_number',
                    'comments': 'comments'}
    query = """
    SELECT *
    FROM {}
    ORDER BY {} {}""".format(data_type, sort_by_translate[sort_by], order)
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
    questions = get_data('question')
    for question in questions:
        if question['id'] == int(question_ids):
            return question



@database_common.connection_handler
def add_data_to_file(cursor, mode, question_id='', message='', title=''):
    if mode == 'answer':
        cursor.execute('INSERT INTO answer (submission_time, vote_number, question_id, message) VALUES  (%s, %s, %s, %s)',
        (time_now(), 0, question_id, message))
        database_common.open_database().commit()
       
    elif mode == 'question':
        cursor.execute("INSERT INTO question (submission_time, view_number, vote_number, title, message) VALUES  (%s, %s, %s, %s, %s)",
        (time_now(), 0, 0,title,message))
        database_common.open_database().commit()

    else:
        print('Wrong mode!')

@database_common.connection_handler
def voting_questions(cursor, question_id, mode):
    if mode == 'up':
        cursor.execute("UPDATE question SET vote_number = vote_number + 1 WHERE id=%(id)s", {'id': question_id})
    elif mode == 'down':
        cursor.execute("UPDATE question SET vote_number = vote_number - 1 WHERE id=%(id)s", {'id': question_id})
    else:
        print('Wrong mode!')
    

@database_common.connection_handler
def delete_data(cursor, mode, aid='', given_question_id=''):
    if mode == 'question':
        cursor.execute("DELETE FROM question WHERE id = %(question_id)s",
                        {'question_id': given_question_id})
        cursor.execute("DELETE FROM answer WHERE question_id = %(question_id)s",
                        {'question_id': given_question_id})
    elif mode == 'answer':
        cursor.execute("DELETE FROM answer WHERE id = %(answer_id)s",
                        {'answer_id': aid})

    else:
        print('Wrong mode!')
 

def count_comments() -> dict[str, int]:
    """Get comment count for each question."""
    comments_count = {}
    questions = get_data('question')
    answers = get_data('answer')
    for question in questions:
        for key, value in question.items():
            if key == 'id':
                comments_count.update({value: 0})
    for answer in answers:
        for key, value in answer.items():
            if key == 'question_id':
                
                comments_count[value] += 1
    return comments_count

@database_common.connection_handler
def sorter(cursor, data_type: str, sort_by='date',
           order='DESC') -> list[dict[str, str]]:
    """Sort given data by specific header."""
    query = """
    SELECT *
    FROM %(data_type)s
    ORDER BY %(sort_by)s %(order)s"""
    cursor.execute(query, {'data_type': data_type, 'sort_by': sort_by, 'order': order})
    return cursor.fetchall()

def time_now():
    current_time  = datetime.now()
    current_time_wo_ms = current_time - timedelta(microseconds=current_time.microsecond)
    return current_time_wo_ms


def how_much_time_passed(date: datetime) -> str:
    """Calculate how much time has passed since date."""
    current_time: datetime = time_now()
    time_then: datetime = date
    delta: timedelta = current_time - time_then
    if delta.days >= 365:
        return f'{delta.days // 365} years ago'
    if delta.days > 0:
        return f'{delta.days} days ago'
    if delta.seconds >= 3600:
        return f'{delta.seconds // 3600} hours ago'
    if delta.seconds >= 60:
        return f'{delta.seconds // 60} minutes ago'
    return f'{delta.seconds} seconds ago'
