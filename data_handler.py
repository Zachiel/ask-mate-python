"""Data read/write and manipulation functions."""
import sys
from datetime import datetime, timedelta
from psycopg2 import sql
import database_common


HEADERS_QUESTION: list[str] = ['id', 'submission_time', 'view_number',
                    'vote_number', 'title', 'message', 'image']
HEADERS_ANSWER: list[str] = ['id', 'submission_time', 'vote_number',
                            'question_id', 'message', 'image']


@database_common.connection_handler
def get_latest_questions(cursor) -> list[dict[str, str]]:
    """Show latest questions in home page"""
    query = """
    SELECT *
    FROM question
    ORDER BY submission_time DESC
    LIMIT 5"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_sorted_questions(cursor, data_type: str, sort_by='date',
           order='DESC') -> list[dict[str, str]]:
    """Sort given data by specific header."""
    translate: dict[str, str] = {'date': 'submission_time',
                                'title': 'title',
                                'message': 'message',
                                'views': 'view_number',
                                'votes': 'vote_number',
                                'comments': 'comments'}
    query = sql.SQL("""
    SELECT *
    FROM question
    ORDER BY %s %s
    """)
    cursor.execute(query, [translate[sort_by], order])
    return cursor.fetchall()


@database_common.connection_handler
def get_answers(cursor):
    query = """
        SELECT *
        FROM answer"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_question_by_id(cursor, question_ids):
    cursor.execute("""
        SELECT *
        FROM question
        WHERE id=%(id)s""", {'id': question_ids})
    return cursor.fetchall()
    

@database_common.connection_handler
def add_data_to_file(cursor, mode, question_id='', message='', title=''):
    if mode == 'answer':
        cursor.execute('INSERT INTO answer (submission_time, vote_number, question_id, message) VALUES  (%s, %s, %s, %s)',
        (time_now(), 0, question_id, message))       
    elif mode == 'question':
        cursor.execute("INSERT INTO question (submission_time, view_number, vote_number, title, message) VALUES  (%s, %s, %s, %s, %s)",
        (time_now(), 0, 0,title,message))
    else:
        print('Wrong mode!')


@database_common.connection_handler
def voting_questions(cursor, question_id, mode):
    if mode == 'up':
        cursor.execute("""UPDATE question
                        SET vote_number = vote_number + 1
                        WHERE id=%(id)s""", {'id': question_id})
    elif mode == 'down':
        cursor.execute("""UPDATE question
                        SET vote_number = vote_number - 1
                        WHERE id=%(id)s""", {'id': question_id})
    else:
        print('Wrong mode!')

        
@database_common.connection_handler
def voting_answer(cursor, answer_id, mode):
    if mode == 'up':
        cursor.execute("""UPDATE answer
                        SET vote_number = vote_number + 1
                        WHERE id=%(answer_id)s""", {'answer_id': answer_id})
    elif mode == 'down':
        cursor.execute("""UPDATE answer
                        SET vote_number = vote_number - 1
                        WHERE id=%(answer_id)s""", {'answer_id': answer_id})
    else:
        print('Wrong mode!', file=sys.stderr)


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


@database_common.connection_handler
def edit_question(cursor, mode, title, message, given_question_id=''):
    if mode == 'question':
        cursor.execute("UPDATE question SET title = %(new_title)s, message = %(new_message)s WHERE id = %(question_id)s",
                        {'new_title' : title,
                        'new_message': message,
                        'question_id': given_question_id})

    else:
        print('Wrong mode!')


def count_comments() -> dict[str, int]:
    """Get comment count for each question."""
    comments_count = {}
    questions = get_sorted_questions(data_type='question')
    answers = get_sorted_questions(data_type='answer')
    for question in questions:
        for key, value in question.items():
            if key == 'id':
                comments_count.update({value: 0})
    for answer in answers:
        for key, value in answer.items():
            if key == 'question_id':
                comments_count[value] += 1
    return comments_count


def time_now():
    current_time  = datetime.now()
    current_time_wo_ms = current_time - timedelta(
        microseconds=current_time.microsecond)
    return current_time_wo_ms


def how_much_time_passed(date: datetime) -> str:
    """Calculate how much time has passed since date."""
    current_time: datetime = time_now()
    time_then: datetime = date
    delta: timedelta = current_time - time_then
    if delta.days >= 365:
        years = delta.days // 365
        return f'{years} {"year" if years == 1 else "years"} ago'
    if delta.days >= 30:
        months = delta.days // 30
        return f'{months} {"month" if months == 1 else "months"} ago'
    if delta.days > 0:
        return f'{delta.days} days ago'
    if delta.seconds >= 3600:
        return f'{delta.seconds // 3600} hours ago'
    if delta.seconds >= 60:
        return f'{delta.seconds // 60} minutes ago'
    return f'{delta.seconds} seconds ago'
