import database_common
import data_handler
from psycopg2 import sql
from psycopg2.extras import RealDictCursor


@database_common.connection_handler
def display_users (cursor: RealDictCursor) -> list:
    query = """SELECT 
                users.id AS user_id, 
                users.username AS username, 
                users.created_on AS user_registration_time,
                COUNT(question.user_id) AS user_asked_questions_counter,
                COUNT(answer.user_id) AS user_answers_counter
                FROM users
                JOIN question
                ON users.id = question.user_id
                JOIN answer
                ON users.id = answer.user_id
                GROUP BY users.id"""

    cursor.execute(query)
    fetch = cursor.fetchall()

    user_list = []

    for user in fetch:
        user_list.append(dict(user))

    return user_list

