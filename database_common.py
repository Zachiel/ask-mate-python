import sys
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
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        return_value = function(cursor, *args, **kwargs)
        converted_data = '' if return_value is None else [dict(row) for row in return_value]
        connection.commit()
        cursor.close()
        connection.close()
        # print to vscode console
        # print('=============================', file=sys.stderr)
        return converted_data
    return wrapper
