"""Data read/write and manipulation functions."""
from datetime import datetime, timedelta
import sys
from typing import Any
import database_common

ALLOWED_EXTENSIONS: set[str] = {'png', 'jpg', 'jpeg'}

@database_common.connection_handler
def get_latest_questions(cursor) -> list[dict[str, str]]:
    """Show latest questions in home page"""
    query: str = """
        SELECT *
        FROM question
        ORDER BY submission_time DESC
        LIMIT 5"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_sorted_questions(cursor, sort_by='date',
            order='descending') -> list[dict[str, str]]:
    """Sort given data by specific header."""
    translate: dict[str, str] = {'date': 'submission_time',
                                'title': 'title',
                                'message': 'message',
                                'views': 'view_number',
                                'votes': 'vote_number',
                                'comments': 'comments',
                                'descending': 'DESC',
                                'ascending': 'ASC'}
    query: str = f"""
        SELECT *
        FROM question
        ORDER BY {translate[sort_by]} {translate[order]}
        """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_answers_for_question(cursor, question_id) -> list[dict[str, str]]:
    """Get all answers for a question."""
    query: str = """
        SELECT *
        FROM answer
        WHERE question_id = %(qid)s"""
    cursor.execute(query, {'qid': question_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_comments_for_question(cursor, question_id) -> list[dict[str, str]]:
    """Get all comments for a question."""
    query: str = """
        SELECT *
        FROM comment
        WHERE question_id = %(qid)s"""
    cursor.execute(query, {'qid': question_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_comments_for_answer(cursor, answer_id) -> list[dict[str, str]]:
    """Get all comments for a answer."""
    query: str = """
        SELECT *
        FROM comment
        WHERE answer_id = %(aid)s"""
    cursor.execute(query, {'aid': answer_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_question_by_id(cursor, question_id) -> list[dict[str, str]]:
    """Get specific question by its ID."""
    query: str = """
        SELECT *
        FROM question
        WHERE id=%(id)s"""
    cursor.execute(query, {'id': question_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_answer_by_id(cursor, answer_id) -> list[dict[str, str]]:
    """Get specific question by its ID."""
    query: str = """
        SELECT *
        FROM answer
        WHERE id=%(id)s"""
    cursor.execute(query, {'id': answer_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_comment_by_id(cursor, comment_id) -> list[dict[str, str]]:
    """Get specific question by its ID."""
    query: str = """
        SELECT *
        FROM comment
        WHERE id=%(id)s"""
    cursor.execute(query, {'id': comment_id})
    return cursor.fetchall()


@database_common.connection_handler
def add_question_to_database(cursor, title, message, image_path) -> None:
    """Save user question into database."""
    query: str = """
        INSERT INTO question (submission_time, view_number, vote_number, title, message, image) 
        VALUES (%s, %s, %s, %s, %s, %s)"""
    cursor.execute(query, [time_now(), 0, 0, title, message, image_path])


@database_common.connection_handler
def add_answer_to_database(cursor, question_id, message, image) -> None:
    """Save user answer into database."""
    query: str = """
        INSERT INTO answer (submission_time, vote_number, question_id, message, image)
        VALUES (%s, %s, %s, %s, %s)"""
    cursor.execute(query, [time_now(), 0, question_id, message, image])


@database_common.connection_handler
def add_comment_to_question(cursor, question_id, message) -> None:
    """Save user answer into database."""
    query: str = """
        INSERT INTO comment (submission_time, question_id, message, edited_count)
        VALUES (%s, %s, %s, %s)"""
    cursor.execute(query, [time_now(), question_id, message, 0])


@database_common.connection_handler
def add_comment_to_answer(cursor, answer_id, message) -> None:
    """Save user answer into database."""
    query: str = """
        INSERT INTO comment (submission_time, answer_id, message, edited_count)
        VALUES (%s, %s, %s, %s)"""
    cursor.execute(query, [time_now(), answer_id, message, 0])


@database_common.connection_handler
def edit_comment(cursor, comment_id, message) -> None:
    """Save user answer into database."""
    query: str = """
        UPDATE comment
        SET message = %(message)s
        SET edited_count = edited_count + 1
        WHERE id = %(id)s"""
    cursor.execute(query, {'message': message, 'id': comment_id})


@database_common.connection_handler
def edit_answer(cursor, question_id, message, image) -> None:
    """Save user answer into database."""
    query: str = """
        UPDATE answer
        SET message = %(message)s, image = %(image)s
        WHERE id = %(id)s"""
    cursor.execute(query, {'message': message, 'id': question_id,
                            'image': image})


@database_common.connection_handler
def vote_question_up(cursor, question_id) -> None:
    """Add points to a question."""
    query: str = """
        UPDATE question
        SET vote_number = vote_number + 1
        WHERE id=%(id)s"""
    cursor.execute(query, {'id': question_id})


@database_common.connection_handler
def vote_question_down(cursor, question_id) -> None:
    """Remove points from a question."""
    query: str = """
        UPDATE question
        SET vote_number = vote_number - 1
        WHERE id=%(id)s"""
    cursor.execute(query, {'id': question_id})


@database_common.connection_handler
def vote_answer_up(cursor, answer_id) -> None:
    """Add points to a question."""
    query: str = """
        UPDATE answer
        SET vote_number = vote_number + 1
        WHERE id=%(id)s"""
    cursor.execute(query, {'id': answer_id})


@database_common.connection_handler
def vote_answer_down(cursor, answer_id) -> None:
    """Remove points from a question."""
    query: str = """
        UPDATE answer
        SET vote_number = vote_number - 1
        WHERE id=%(id)s"""
    cursor.execute(query, {'id': answer_id})


@database_common.connection_handler
def delete_question(cursor, question_id) -> None:
    """Delete question from database."""
    query_answer: str = """
        DELETE FROM answer
        WHERE question_id = %(id)s"""
    query_question: str = """
        DELETE FROM question
        WHERE id = %(id)s"""
    cursor.execute(query_answer, {'id': question_id})
    cursor.execute(query_question, {'id': question_id})


@database_common.connection_handler
def delete_answer(cursor, answer_id) -> None:
    """Delete answer from database."""
    query: str = """
        DELETE FROM answer
        WHERE id = %(id)s"""
    cursor.execute(query, {'id': answer_id})


@database_common.connection_handler
def delete_comment(cursor, comment_id) -> None:
    """Delete comment from database."""
    query: str = """
        DELETE FROM comment
        WHERE id = %(id)s"""
    cursor.execute(query, {'id': comment_id})


@database_common.connection_handler
def edit_question(cursor, question_id, title, message, image_path) -> None:
    """Save edits to a question."""
    query: str = """
        UPDATE question
        SET title = %(title)s, message = %(message)s, image = %(image_path)s
        WHERE id = %(id)s"""
    cursor.execute(query, {'title' : title,
                            'message': message,
                            'id': question_id,
                            'image_path': image_path})


@database_common.connection_handler
def increase_question_view_count(cursor, question_id) -> None:
    """Increase question view counter."""
    query: str = """
        UPDATE question
        SET view_number = view_number + 1
        WHERE id = %(id)s"""
    cursor.execute(query, {'id': question_id})


@database_common.connection_handler
def extract_sql_answer_count(cursor) -> dict[str, int]:
    """Get comment count for each question."""
    query: str = """
        SELECT q.id AS question_id, COUNT(a.id) AS comments
        FROM question AS q
        LEFT JOIN answer AS a ON q.id = a.question_id
        GROUP BY q.id"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def search_for_question(cursor, phrase) -> list[dict[str, str]]:
    """Show latest questions in home page"""
    query: str = """
        SELECT q.id, q.title, q.message, q.image, t.name AS tag_name
        FROM question AS q
        LEFT JOIN question_tag AS qt ON q.id = qt.question_id
        LEFT JOIN tag as t ON qt.tag_id = t.id
        WHERE q.title ILIKE %(phrase)s OR t.name LIKE %(phrase)s
        ORDER BY q.submission_time DESC
        LIMIT 10"""
    like_pattern = '%{}%'.format(phrase)
    cursor.execute(query, {'phrase': like_pattern})
    return cursor.fetchall()


def get_answer_count() -> dict[str, str]:
    """Extract SQL data into key: value pairs.
    With ID as key and comment count as value."""
    # pylint: disable=no-value-for-parameter
    sql_count_data: Any = extract_sql_answer_count()
    comment_count_dict: dict[str, str] = {}
    for row in sql_count_data:
        comment_count_dict.update({str(row['question_id']):
                                    str(row['comments'])})
    return comment_count_dict


def get_answer_comments(answer_ids: list[int]) -> list[dict[str, str]]:
    """Get all comments for answers in a question."""
    comments: list[dict[str, str]] = []
    for aid in answer_ids:
        # pylint: disable=no-value-for-parameter
        comments.append(get_comments_for_answer(answer_id = aid))
    print(comments, file=sys.stderr)
    return comments


def time_now() -> datetime:
    """Get time of question posting."""
    current_time: datetime  = datetime.now().replace(microsecond=0)
    return current_time


def how_much_time_passed(date: datetime) -> str:
    """Calculate how much time has passed since date."""
    current_time: datetime = time_now()
    time_then: datetime = date
    delta: timedelta = current_time - time_then
    if delta.days >= 365:
        years: int = delta.days // 365
        return f'{years} {"year" if years == 1 else "years"} ago'
    if delta.days >= 30:
        months: int = delta.days // 30
        return f'{months} {"month" if months == 1 else "months"} ago'
    if delta.days > 0:
        return f'{delta.days} days ago'
    if delta.seconds >= 3600:
        return f'{delta.seconds // 3600} hours ago'
    if delta.seconds >= 60:
        return f'{delta.seconds // 60} minutes ago'
    return f'{delta.seconds} seconds ago'


def allowed_file(filename) -> bool:
    """Check if uploaded file has allowed extension"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
