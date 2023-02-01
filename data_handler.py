"""Data read/write and manipulation functions."""
from datetime import datetime, timedelta
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
def get_tag_for_question(cursor, question_id):
    query: str = """
        SELECT *
        FROM question_tag
        WHERE question_id = %(qid)s"""
    cursor.execute(query, {'qid': question_id})

    data = cursor.fetchall()
    if data == []:
        return 'None'
    else:
        id = str(data[0]['tag_id'])
        query: str = """
            SELECT *
            FROM tag
            WHERE id = %(id)s"""
        cursor.execute(query, {'id': id})
        tag = cursor.fetchall()[0]['name']
        return tag

@database_common.connection_handler
def add_tag_to_database(cursor, tag_name):
    """Save new tag into database."""
    query: str = """
    INSERT INTO tag (name)
    VALUES (%s)"""
    cursor.execute(query, [tag_name])


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
def get_question_by_id(cursor, question_id) -> list[dict[str, str]]:
    """Get specific question by its ID."""
    query: str = """
        SELECT *
        FROM question
        WHERE id=%(id)s"""
    cursor.execute(query, {'id': question_id})
    return cursor.fetchall()

@database_common.connection_handler
def get_question_id_from_title(cursor, title) -> list[dict[str, str]]:
    """Get specific question ID by its title."""
    query: str = """
        SELECT id
        FROM question
        WHERE title=%(title)s"""
    cursor.execute(query, {'title': title})
    id = cursor.fetchall()[0]['id']
    return id

@database_common.connection_handler
def get_tags(cursor):
    """get all tags from base"""
    query: str = """
    SELECT *
    FROM tag"""
    cursor.execute(query)
    return cursor.fetchall()



@database_common.connection_handler
def add_question_to_database(cursor, title, message, image_path) -> None:
    """Save user question into database."""
    query: str = """
        INSERT INTO question (submission_time, view_number, vote_number, title,
                                message, image) 
        VALUES (%s, %s, %s, %s, %s, %s)"""
    cursor.execute(query, [time_now(), 0, 0, title, message, image_path])


@database_common.connection_handler
def get_tag_id(cursor, name):
    """taking tag id basing on its name"""
    query: str = """
    SELECT id
    FROM tag
    WHERE name = %(name)s"""
    cursor.execute(query, {'name': name})
    id = cursor.fetchall()[0]['id']
    return id


@database_common.connection_handler
def get_tagged_questions(cursor, given_tag) -> list[dict[str, str]]:
    """Show questions with specific tag in home page"""

    query: str = """
        SELECT question_id
        FROM question_tag
        WHERE tag_id = %(given_tag)s """
    cursor.execute(query, {'given_tag': given_tag})
    data = cursor.fetchall()
    questions_with_given_tag = []
    for info in data:
        questions_with_given_tag.append(str(info['question_id']))

    query_2: str = """
        SELECT *
        FROM question
        WHERE id IN %(questions_with_given_tag)s
        """
    cursor.execute(query_2, {'questions_with_given_tag': questions_with_given_tag})
    return cursor.fetchall()



#print(get_tagged_questions(1))

@database_common.connection_handler
def add_tag(cursor, question_id, tag):  
    """add question tag to database"""
    tag_id = get_tag_id(tag)
    query: str ="""
        INSERT INTO question_tag (question_id, tag_id)
        VALUES (%s, %s)"""
    cursor.execute(query, [question_id, tag_id])


@database_common.connection_handler
def add_answer_to_database(cursor, question_id, message) -> None:
    """Save user answer into database."""
    query: str = """
    INSERT INTO answer (submission_time, vote_number, question_id, message)
    VALUES (%s, %s, %s, %s)"""
    cursor.execute(query, [time_now(), 0, question_id, message])


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
    query_tag: str = """
        DELETE FROM question_tag
        WHERE question_id = %(id)s"""
    query_question: str = """
        DELETE FROM question
        WHERE id = %(id)s"""
    cursor.execute(query_answer, {'id': question_id})
    cursor.execute(query_tag, {'id': question_id})
    cursor.execute(query_question, {'id': question_id})
    


@database_common.connection_handler
def delete_answer(cursor, answer_id) -> None:
    """Delete answer from database."""
    query: str = """
        DELETE FROM answer
        WHERE id = %(id)s"""
    cursor.execute(query, {'id': answer_id})


@database_common.connection_handler
def edit_question(cursor, question_id, title, message, image_path, tag) -> None:
    """Save edits to a question."""
    tag_id = get_tag_id(tag)
    query: str = """
        UPDATE question
        SET title = %(title)s, message = %(message)s, image = %(image_path)s
        WHERE id = %(id)s"""
    query_tag: str = """
        UPDATE question_tag
        SET tag_id = %(tag_id)s
        WHERE question_id = %(question_id)s"""
    cursor.execute(query, {'title' : title,
                            'message': message,
                            'id': question_id,
                            'image_path': image_path})
    cursor.execute(query_tag, {'question_id': question_id,
                                'tag_id': tag_id})


@database_common.connection_handler
def increase_view_count(cursor, question_id) -> None:
    """Increase question view counter."""
    query: str = """
        UPDATE question
        SET view_number = view_number + 1
        WHERE id = %(id)s"""
    cursor.execute(query, {'id': question_id})


@database_common.connection_handler
def extract_sql_comment_count(cursor) -> dict[str, int]:
    """Get comment count for each question."""
    query: str = """
        SELECT q.id AS question_id, COUNT(a.id) AS comments
        FROM question AS q
        LEFT JOIN answer AS a ON q.id = a.question_id
        GROUP BY q.id"""
    cursor.execute(query)
    return cursor.fetchall()


def get_comment_count() -> dict[str, str]:
    """Extract SQL data into key: value pairs.
    With ID as key and comment count as value."""
    # pylint: disable=no-value-for-parameter
    sql_count_data: Any = extract_sql_comment_count()
    comment_count_dict: dict[str, str] = {}
    for row in sql_count_data:
        comment_count_dict.update({str(row['question_id']):
                                    str(row['comments'])})
    return comment_count_dict


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
