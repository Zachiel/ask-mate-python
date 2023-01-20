# Creates a decorator to handle the database connection/cursor opening/closing.
# Creates the cursor with RealDictCursor, thus it returns real dictionaries, where the column names are the keys.
import os

import psycopg2
import psycopg2.extras






def get_connection_string():
    # setup connection string
    # to do this, please define these environment variables first
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
        cur.close()
        connection.close()
        return ret_value

    return wrapper
