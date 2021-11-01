import database_common
import bcrypt
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

CURRENT_TIME = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@database_common.connection_handler
def register_user(cursor: RealDictCursor, username: str, password: str) -> list:
    query = f"""
        INSERT INTO users (username, password, created_on)
        VALUES ('{username}', '{password}', '{CURRENT_TIME}')"""
    cursor.execute(query)

@database_common.connection_handler
def check_login(cursor: RealDictCursor, username: str, password: str) -> list:
    wrong_username = f"User {username} not found!"
    wrong_password = "Wrong password!"

    query = f"""SELECT username 
                FROM users
                WHERE username = '{username}'"""

    cursor.execute(query)

    try:
        fetch_username = dict(cursor.fetchone())
    except TypeError:
        return wrong_username
        
    if fetch_username is None:
        return wrong_username
    else:
        query = f"""SELECT password
                    FROM users
                    WHERE username = '{username}'"""
 
        cursor.execute(query)
        fetch_password = dict(cursor.fetchone())

        hashed_user_password = fetch_password["password"].encode('utf-8')
        check_hash = bcrypt.checkpw(password.encode("utf-8"), hashed_user_password)

        if check_hash is False:
            return wrong_password
        return check_hash

