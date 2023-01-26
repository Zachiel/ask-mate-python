"""Database connection functions."""
import os
import sys
from typing import Union, Callable, Any
import psycopg2.extras as extras
import psycopg2

def get_connection_string() -> str:
    """Secure connection to the database."""
    user_name: Union[str, None] = os.environ.get('PSQL_USER_NAME')
    password: Union[str, None] = os.environ.get('PSQL_PASSWORD')
    host: Union[str, None] = os.environ.get('PSQL_HOST')
    database_name: Union[str, None] = os.environ.get('PSQL_DB_NAME')
    env_variables_defined: Union[str, None] = (user_name and password and
                                                host and database_name)
    if env_variables_defined:
        return f'postgresql://{user_name}:{password}@{host}/{database_name}'
    raise KeyError('Some necessary environment variable(s) are not defined')


def open_database():
    """Accessing database records."""
    try:
        connection_string: str = get_connection_string()
        connection = psycopg2.connect(connection_string)
        connection.autocommit = True
    except psycopg2.DatabaseError as exception:
        print('Database connection problem')
        raise exception
    return connection


def connection_handler(function) -> Callable:
    """Extract specific records requested by function."""
    def wrapper(*args, **kwargs) -> Any:
        with open_database() as connection:
            with connection.cursor() as cursor:
                cursor = connection.cursor(cursor_factory=extras.RealDictCursor)
                return_value: Any = function(cursor, *args, **kwargs)
        print(return_value, file=sys.stderr)
        return return_value
    return wrapper
