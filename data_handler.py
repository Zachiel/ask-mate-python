"""Data read/write and manipulation functions."""
from datetime import datetime, timedelta
import sys
from typing import Any
import bcrypt
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
                                'votes': 'votes_up',
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
def get_tag_id(cursor, name):
    """taking tag id basing on its name"""
    query: str = """
    SELECT id
    FROM tag
    WHERE name = %(name)s"""
    cursor.execute(query, {'name': name})
    tag_id = cursor.fetchall()[0]['id']
    return tag_id


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
def get_question_id_from_title(cursor, title) -> list[dict[str, str]]:
    """Get specific question ID by its title."""
    query: str = """
        SELECT id
        FROM question
        WHERE title=%(title)s"""
    cursor.execute(query, {'title': title})
    question_id = cursor.fetchall()[0]['id']
    return question_id


@database_common.connection_handler
def add_question_to_database(cursor, user_id, title, message, image_path) -> None:
    """Save user question into database."""
    query: str = """
        INSERT INTO question (submission_time, view_number, votes_up, votes_down, title, message, image) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    query2: str = """
        INSERT INTO question_user (question_id, user_id)
        VALUES ((
            SELECT MAX(id)
            FROM question), %s)"""
    cursor.execute(query, [time_now(), 0, 0, 0, title, message, image_path])
    cursor.execute(query2, [user_id['id']])


@database_common.connection_handler
def add_answer_to_database(cursor, user_id, question_id, message, image) -> None:
    """Save user answer into database."""
    query: str = """
        INSERT INTO answer (submission_time, votes_up, votes_down, question_id, message, image, accepted, edited_count)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    query2: str = """
        INSERT INTO answer_user (answer_id, user_id)
        VALUES ((
            SELECT MAX(id)
            FROM answer), %s)"""
    cursor.execute(query, [time_now(), 0, 0, question_id, message, image, False, 0])
    cursor.execute(query2, [user_id['id']])



@database_common.connection_handler
def add_comment_to_question(cursor, user_id, question_id, message) -> None:
    """Save user answer into database."""
    query: str = """
        INSERT INTO comment (submission_time, question_id, message, edited_count)
        VALUES (%s, %s, %s, %s)"""
    query2: str = """
        INSERT INTO comment_user (comment_id, user_id)
        VALUES ((
            SELECT MAX(id)
            FROM comment), %s)"""
    cursor.execute(query, [time_now(), question_id, message, 0])
    cursor.execute(query2, [user_id['id']])


@database_common.connection_handler
def add_comment_to_answer(cursor, user_id, answer_id, message) -> None:
    """Save user answer into database."""
    query: str = """
        INSERT INTO comment (submission_time, answer_id, message, edited_count)
        VALUES (%s, %s, %s, %s)"""
    query2: str = """
        INSERT INTO comment_user (comment_id, user_id)
        VALUES ((
            SELECT MAX(id)
            FROM comment), %s)"""
    cursor.execute(query, [time_now(), answer_id, message, 0])
    cursor.execute(query2, [user_id['id']])


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
def edit_answer(cursor, question_id, message) -> None:
    """Save user answer into database."""
    query: str = """
        UPDATE answer
        SET message = %(message)s
        WHERE id = %(id)s"""
    cursor.execute(query, {'message': message, 'id': question_id})


@database_common.connection_handler
def vote_question_up(cursor, question_id) -> None:
    """Add points to a question."""
    query: str = """
        UPDATE question
        SET votes_up = votes_up + 1
        WHERE id=%(id)s"""
    cursor.execute(query, {'id': question_id})


@database_common.connection_handler
def vote_question_down(cursor, question_id) -> None:
    """Remove points from a question."""
    query: str = """
        UPDATE question
        SET votes_down = votes_down + 1
        WHERE id=%(id)s"""
    cursor.execute(query, {'id': question_id})


@database_common.connection_handler
def vote_answer_up(cursor, answer_id) -> None:
    """Add points to a question."""
    query: str = """
        UPDATE answer
        SET votes_up = votes_up + 1
        WHERE id=%(id)s"""
    cursor.execute(query, {'id': answer_id})


@database_common.connection_handler
def vote_answer_down(cursor, answer_id) -> None:
    """Remove points from a question."""
    query: str = """
        UPDATE answer
        SET votes_down = votes_down + 1
        WHERE id=%(id)s"""
    cursor.execute(query, {'id': answer_id})


@database_common.connection_handler
def delete_question(cursor, question_id) -> None:
    """Delete question from database."""
    answers = get_answers_for_question(question_id)
    answer_ids = [answer['id'] for answer in answers] if answers else []
    question_comments = get_comments_for_question(question_id)
    question_comment_ids = [comment['id'] for comment in question_comments] if question_comments else []
    answer_comments = []
    for aid in answer_ids:
        answer_comments.extend(get_comments_for_answer(aid))
    answer_comment_ids = [comment['id'] for comment in answer_comments]
    delete_comment_user_constraints: str = """
    DELETE FROM comment_user
    WHERE comment_id = %(id)s"""
    delete_answer_user_constraints: str = """
    DELETE FROM answer_user
    WHERE answer_id = %(id)s"""
    delete_question_user_constraints: str = """
    DELETE FROM question_user
    WHERE question_id = %(id)s"""
    delete_question_tag_constraints: str = """
    DELETE FROM question_tag
    WHERE question_id = %(id)s"""
    delete_question_comment: str = """
    DELETE FROM comment
    WHERE question_id = %(id)s"""
    delete_answer_comment: str = """
    DELETE FROM comment
    WHERE answer_id = %(id)s"""
    delete_answer_query: str = """
    DELETE FROM answer
    WHERE question_id = %(id)s"""
    delete_question_query: str = """
    DELETE FROM question
    WHERE id = %(id)s"""
    for cid in answer_comment_ids:
        cursor.execute(delete_comment_user_constraints, {'id': cid})
    for aid in answer_ids:
        cursor.execute(delete_answer_comment, {'id': aid})
        cursor.execute(delete_answer_user_constraints, {'id': aid})
    for cid in question_comment_ids:
        cursor.execute(delete_comment_user_constraints, {'id': cid})
    cursor.execute(delete_question_comment, {'id': question_id})
    cursor.execute(delete_answer_query, {'id': question_id})
    cursor.execute(delete_question_user_constraints, {'id': question_id})
    cursor.execute(delete_question_tag_constraints, {'id': question_id})
    cursor.execute(delete_question_query, {'id': question_id})


@database_common.connection_handler
def delete_answer(cursor, answer_id) -> None:
    """Delete answer from database."""
    query_answer: str = """
        DELETE FROM answer
        WHERE id = %(id)s"""
    query_answer_user: str = """
        DELETE FROM answer_user
        WHERE answer_id = %(id)s"""
    query_comment: str = """
        DELETE FROM comment
        WHERE answer_id = %(id)s"""
    query_comment_user: str = """
        DELETE FROM comment_user
        WHERE comment_id = %(id)s"""
    comment_ids = get_comment_ids_by_answer_id(answer_id)
    for comment_id in comment_ids:
        cursor.execute(query_comment_user, {'id': comment_id['id']})
    cursor.execute(query_comment, {'id': answer_id})
    cursor.execute(query_answer_user, {'id': answer_id})
    cursor.execute(query_answer, {'id': answer_id})


@database_common.connection_handler
def get_comment_ids_by_answer_id(cursor, answer_id):
    query: str = """
        SELECT id FROM comment
        WHERE answer_id = %(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchall()


@database_common.connection_handler
def delete_comment(cursor, comment_id) -> None:
    """Delete comment from database."""
    query1: str = """
        DELETE FROM comment_user
        WHERE comment_id = %(id)s"""
    query: str = """
        DELETE FROM comment
        WHERE id = %(id)s"""
    cursor.execute(query1, {'id': comment_id})
    cursor.execute(query, {'id': comment_id})


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
def increase_question_view_count(cursor, question_id) -> None:
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

@database_common.connection_handler
def check_exisiting_username(cursor, username):
    query: str = """
        SELECT * FROM accounts WHERE username = %(username)s"""
    cursor.execute(query, {'username': username})
    account = cursor.fetchone()
    if account:
        return True
    else:
        return False


@database_common.connection_handler
def check_exisiting_email(cursor, email):
    query: str = """
        SELECT * FROM accounts WHERE email = %(email)s"""
    cursor.execute(query, {'email': email})
    account = cursor.fetchone()
    if account:
        return True
    else:
        return False


@database_common.connection_handler
def register_new_user(cursor, username, password, email, fname, lname, registrationDate):
    query: str = """
    INSERT INTO accounts (username, password, email, fname, lname, registrationDate)
    VALUES (%s, %s, %s, %s, %s, %s)"""
    cursor.execute(query, (username, password, email, fname, lname, registrationDate, ))


@database_common.connection_handler
def search_for_question(cursor, phrase) -> list[dict[str, str]]:
    """Show latest questions in home page"""
    query: str = """
        SELECT q.id, q.title, q.message, q.image, t.name AS tag_name
        FROM question AS q
        LEFT JOIN question_tag AS qt ON q.id = qt.question_id
        LEFT JOIN tag as t ON qt.tag_id = t.id
        WHERE q.title ILIKE %(phrase)s OR t.name ILIKE %(phrase)s
        ORDER BY q.submission_time DESC
        LIMIT 5"""
    like_pattern = '%{}%'.format(phrase)
    cursor.execute(query, {'phrase': like_pattern})
    return cursor.fetchall()


def get_answer_count() -> dict[str, str]:
    """With ID as key and comment count as value."""
    # pylint: disable=no-value-for-parameter
    sql_count_data: Any = extract_sql_comment_count()
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
        tag_id = str(data[0]['tag_id'])
        query: str = """
            SELECT *
            FROM tag
            WHERE id = %(id)s"""
        cursor.execute(query, {'id': tag_id})
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
def get_tags(cursor):
    """get all tags from base"""
    query: str = """
    SELECT *
    FROM tag"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_tagged_questions(cursor, given_tag) -> list[dict[str, str]]:
    """Show questions with specific tag in home page"""
    tag_id = get_tag_id(given_tag)
    query_on: str = """
        SELECT q.submission_time, q.id, q.title, q.message, q.image, qt.question_id AS question_tag, qt.tag_id, t.name
        FROM question AS q
        LEFT JOIN question_tag AS qt ON q.id = qt.question_id
        LEFT JOIN tag as t ON qt.tag_id = t.id
        WHERE t.id = %(tag_id)s
        ORDER BY q.submission_time DESC"""
    cursor.execute(query_on, {'tag_id': tag_id})
    return cursor.fetchall()


@database_common.connection_handler
def add_tag(cursor, question_id, tag):
    """add question tag to database"""
    if tag:
        tag_id = get_tag_id(tag)
        query: str ="""
            INSERT INTO question_tag (question_id, tag_id)
            VALUES (%s, %s)"""
        cursor.execute(query, [question_id, tag_id])


def hash_password(password):
    to_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(to_bytes, salt)
    hashed = hashed.decode('utf-8')
    return hashed

@database_common.connection_handler
def check_login_password(cursor, username, password):
    query: str = """
        SELECT password FROM accounts
        WHERE username = %s"""
    cursor.execute(query, (username, ))
    db_hashed_password = cursor.fetchone()
    return bcrypt.checkpw(password.encode('utf-8'),
                            db_hashed_password['password'].encode('utf-8'))


@database_common.connection_handler
def get_all_users(cursor):
    """Get all registered users."""
    query: str = """
        SELECT id, username, registrationdate
        FROM accounts"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_user_by_id(cursor, user_id):
    """Get specific user."""
    query: str = """
        SELECT a.id, a.username, a.email, a.fname, a.lname, a.registrationdate,
            (SELECT
                COUNT(qu.user_id)
                FROM question_user AS qu
                WHERE qu.user_id = %(id)s) AS questions,
            (SELECT
                COUNT(au.user_id)
                FROM answer_user AS au
                WHERE au.user_id = %(id)s) AS answers,
            (SELECT
                COUNT(cu.user_id)
                FROM comment_user AS cu
                WHERE cu.user_id = %(id)s) AS comments
        FROM accounts AS a
        LEFT JOIN question_user AS qu ON a.id = qu.user_id
        LEFT JOIN answer_user AS au ON a.id = au.user_id
        LEFT JOIN comment_user AS cu ON a.id = cu.user_id
        WHERE id = %(id)s
        GROUP BY a.id"""
    cursor.execute(query, {'id': user_id})
    return cursor.fetchone()


@database_common.connection_handler
def accept_answer_by_id(cursor, id):
    query: str = """
    UPDATE answer
    SET accepted = True
    WHERE id = %(id)s"""
    cursor.execute(query, {'id': id})


@database_common.connection_handler
def decline_answer_by_id(cursor, id):
    query: str = """
    UPDATE answer
    SET accepted = False
    WHERE id = %(id)s"""
    cursor.execute(query, {'id': id})


@database_common.connection_handler
def decline_answers_by_question_id(cursor, question_id):
    query: str = """
    UPDATE answer
    SET accepted = False
    WHERE question_id = %(question_id)s
    AND accepted = True"""
    cursor.execute(query, {'question_id': question_id})
    

@database_common.connection_handler
def get_user_id_by_username(cursor, username):
    query: str = """
    SELECT id FROM accounts
    WHERE username = %(username)s"""
    cursor.execute(query, {'username': username['username']})
    return cursor.fetchone()


@database_common.connection_handler
def get_question_ids_of_user_id(cursor, user_id):
    query: str = """
    SELECT question_id FROM question_user
    WHERE user_id = %(user_id)s"""
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchall()


def check_if_question_of_user(question_id, question_ids_of_current_user):
    question_of_user: bool = False
    for element in question_ids_of_current_user:
        if question_id == str(element['question_id']):
            question_of_user = True
            break
    return question_of_user

@database_common.connection_handler
def get_user_reputation(cursor, user_id):
    """Calculate reputation of a specific user."""
    query: str = """
        SELECT 
            SUM((SELECT SUM(q.votes_up) 
                    FROM question_user AS qu
                    LEFT JOIN question AS q ON q.id = qu.question_id
                    WHERE qu.user_id = %(id)s) * 5
                + -(SELECT SUM(q.votes_down) 
                    FROM question_user AS qu
                    LEFT JOIN question AS q ON q.id = qu.question_id
                    WHERE qu.user_id = %(id)s) * 2) AS q_rep,
            SUM((SELECT SUM(a.votes_up) 
                    FROM answer_user AS au
                    LEFT JOIN answer AS a ON a.id = au.answer_id
                    WHERE au.user_id = %(id)s) * 10
                + -(SELECT SUM(a.votes_down) 
                    FROM answer_user AS au
                    LEFT JOIN answer AS a ON a.id = au.answer_id
                    WHERE au.user_id = %(id)s) * 2) AS a_rep,
            (SELECT SUM(CASE
                            WHEN a.accepted = TRUE
                            THEN 15
                            ELSE 0
                        END)
                    FROM answer_user AS au
                    LEFT JOIN answer AS a ON a.id = au.answer_id
                    WHERE au.user_id = %(id)s ) AS a_acc_rep
        FROM accounts AS acc
        WHERE acc.id = %(id)s
        GROUP BY acc.id"""
    cursor.execute(query, {'id': user_id})
    return cursor.fetchone()


def get_all_user_stats():
    """Get all user question/answer/comment statistics."""
    users_ids = [user['id'] for user in get_all_users()]
    users_data = []
    for user_id in users_ids:
        users_data.append(get_user_by_id(user_id))
    return users_data


@database_common.connection_handler
def check_credentials(cursor, login: str, password: str):
    """Verify user login credentials."""
    query: str = """
        SELECT password
        FROM accounts
        WHERE username = %(login)s"""
    cursor.execute(query, {'login': login})
    user = cursor.fetchone()
    return bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8'))


@database_common.connection_handler
def get_id_by_username(cursor, username):
    """Get user id through their username."""
    query: str = """
        SELECT id, username
        FROM accounts
        WHERE username = %(username)s"""
    cursor.execute(query, {'username': username})
    return cursor.fetchone()
