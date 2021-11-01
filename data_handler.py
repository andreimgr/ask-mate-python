import database_common
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

@database_common.connection_handler
def register_user(cursor: RealDictCursor, username: str, password: str) -> list:
    query = f"""
        INSERT INTO users (username, password, created_on)
        VALUES ('{username}', '{password}', '{CURRENT_TIME}')"""
    cursor.execute(query)

