import psycopg2
import psycopg2.extras
import data_handler
import database_common
import datetime

conn = psycopg2.connect("dbname=cc_ask_mate user=cc_ask_mate password=test123")
cur = conn.cursor()
cur.execute("SELECT * FROM answer;")
desc = cur.description
column_names = [col[0] for col in desc]
answers_sql = [dict(zip(column_names, row))  
        for row in cur.fetchall()]
cur.execute("SELECT * FROM question;")
desc = cur.description
column_names = [col[0] for col in desc]
question_sql = [dict(zip(column_names, row))  
        for row in cur.fetchall()]
conn.close()

def time_now():
    time_now  = datetime.now()
    time_now = int(round(datetime.timestamp(time_now), 0))
    return time_now




# @database_common.connection_handler
def count_comments() -> dict[str, int]:
    """Get comment count for each question."""
    comments_count = {}
    questions = data_handler.get_questions()
    answers = data_handler.get_answers()
    for question in questions:
        for key, value in question.items():
            if key == 'question_id':
                comments_count.update({value: 0})
    for answer in answers:
        for key, value in answer.items():
            if key == 'question_id':
                comments_count[value] += 1
    return comments_count



print(count_comments())