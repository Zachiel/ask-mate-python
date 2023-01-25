"""Database connection functions."""
# pylint: disable=line-too-long, unused-import
import os
import sys
import psycopg2
import psycopg2.extras

def get_connection_string():
    """Secure connection to the database."""
    user_name = os.environ.get('PSQL_USER_NAME')
    password = os.environ.get('PSQL_PASSWORD')
    host = os.environ.get('PSQL_HOST')
    database_name = os.environ.get('PSQL_DB_NAME')
    env_variables_defined = (user_name and password and
                                        host and database_name)
    if env_variables_defined:
        return f'postgresql://{user_name}:{password}@{host}/{database_name}'
    raise KeyError('Some necessary environment variable(s) are not defined')


def open_database():
    """Accessing database records."""
    try:
        connection_string = get_connection_string()
        connection = psycopg2.connect(connection_string)
        connection.autocommit = True
    except psycopg2.DatabaseError as exception:
        print('Database connection problem')
        raise exception
    return connection


def connection_handler(function):
    """Extract specific records requested by function."""
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
