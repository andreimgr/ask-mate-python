import database_common
import bcrypt
from psycopg2 import sql
from psycopg2.extras import RealDictCursor


def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')


@database_common.connection_handler
def register_user(cursor: RealDictCursor, username: str, password: str) -> list:
    query = f"""
        INSERT INTO users (username, password, created_on)
        VALUES ('{username}', '{password}', '{CURRENT_TIME}')"""
    cursor.execute(query)

