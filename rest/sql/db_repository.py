from rest.sql.db_connection import DBConnection


db_name = 'shoppify-db'
db_user = 'postgres'
db_password = 'mleko'
db_host = 'localhost'


def get_db_connection() -> DBConnection:
    return DBConnection(db_name, db_user, db_password, db_host)
