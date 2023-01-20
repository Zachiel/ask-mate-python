import psycopg2
import psycopg2.extras
import data_handler
import database_common

# dict_cur.execute("SELECT * FROM answer")
# rec = dict_cur.fetchall()
# dict_cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)



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


def zip_sql_to_dict(cursor):
        pass


# print(question_sql)
# print(data_handler.get_data_from_file(
#         'sample_data/answer.csv'))


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

get_questions()