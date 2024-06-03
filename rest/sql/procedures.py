from typing import Set

import psycopg2

from rest.common.exceptions.sql_exception import SqlException

# Database connection parameters
dbname = 'shoppify-db'
dbuser = 'postgres'
dbpassword = 'mleko'
dbhost = 'localhost'



custom_error_letters: Set[str] = {'U'}

def add_user(username: str, email: str, password: str) -> None:
    # Connect to your postgres DB
    conn = psycopg2.connect(dbname=dbname, user=dbuser, password=dbpassword, host=dbhost)

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Example function call
    try:
        cur.callproc('add_user', [username, email, password])

        # Retrieve the result
        result = cur.fetchone()
        print(result)

        conn.commit()

    except psycopg2.Error as e:
        if e.pgcode[0] not in custom_error_letters:
            raise e
        raise SqlException(e.pgerror)
    finally:
        # Clean up: close cursor and connection
        cur.close()
        conn.close()
