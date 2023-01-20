import psycopg2
import psycopg2.extras


def get_connection_string():
    # /TODO: Hide sensitive data
    return ("dbname=cc_ask_mate user=cc_ask_mate password=test123")


def open_database():
    try:
        connection_string = get_connection_string()
        connection = psycopg2.connect(connection_string)
        connection.autocommit = True
    except psycopg2.DatabaseError as exception:
        print('Database connection problem')
        raise exception
    return connection


def connection_handler(function):
    def wrapper(*args, **kwargs):
        connection = open_database()
        # we set the cursor_factory parameter to return with a RealDictCursor cursor (cursor which provide dictionaries)
        cur = connection.cursor()
        ret_value = function(cur, *args, **kwargs)
        connection.commit()
        cur.close()
        connection.close()
        return ret_value
    return wrapper
