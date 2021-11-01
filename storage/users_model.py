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
    

@database_common.connection_handler
def get_id_for_user (cursor: RealDictCursor, username: str) -> list:
    query = f"""
        SELECT id
        FROM users
        WHERE username = '{username}'"""
    cursor.execute(query)
    fetch = dict(cursor.fetchone())

    user_id = fetch["id"]

    return user_id


@database_common.connection_handler
def get_username_by_question_id (cursor: RealDictCursor, question_id: int) -> list:
    query = f"""
        SELECT username
        FROM users
        JOIN question ON question.user_id = users.id
        WHERE question.id = {question_id}"""

    cursor.execute(query)
    fetch = dict(cursor.fetchone())

    username = fetch["username"]

    return username


@database_common.connection_handler
def get_username_by_answer_id (cursor: RealDictCursor, answer_id: int) -> list:
    query = f"""
        SELECT username
        FROM users
        JOIN answer on answer.user_id = users.id
        WHERE answer.id = {answer_id}"""

    cursor.execute(query)
    fetch = dict(cursor.fetchone())

    username = fetch["username"]

    return username


@database_common.connection_handler
def get_user_questions (cursor: RealDictCursor, user_id: int) -> list:
    query = f"""
        SELECT users.id AS user_id,
        question.title AS question_title,
        question.id AS question_id
        FROM users
        JOIN question ON users.id = question.user_id
        WHERE question.user_id = {user_id}"""

    cursor.execute(query)
    fetch = cursor.fetchall()

    user_questions = []

    for questions in fetch:
        user_questions.append(dict(questions))

    return user_questions


@database_common.connection_handler
def user_questions_count(cursor: RealDictCursor, user_id: int) -> list:
    query = f"""
        SELECT
        COUNT(question.user_id) as user_questions_counter
        FROM users
        LEFT JOIN question ON users.id = question.user_id
        WHERE users.id = {user_id}"""

    cursor.execute(query)
    fetch = cursor.fetchone()

    return fetch["user_questions_counter"]


@database_common.connection_handler
def user_answers_count(cursor: RealDictCursor, user_id: int) -> list:
    query = f"""
        SELECT
        COUNT(answer.user_id) as user_answers_counter
        FROM users
        LEFT JOIN answer ON users.id = answer.user_id
        WHERE users.id = {user_id}"""

    cursor.execute(query)
    fetch = cursor.fetchone()

    return fetch["user_answers_counter"]


@database_common.connection_handler
def get_user_answers (cursor: RealDictCursor, user_id: int) -> list:
    query = f"""
        SELECT users.id,
        answer.id AS answer_id,
        answer.message AS answer_message,
        COUNT(answer.user_id)
        FROM users
        JOIN answer ON users.id = answer.user_id
        WHERE answer.user_id = {user_id}
        GROUP BY users.id, answer.id, answer.message"""

    cursor.execute(query)
    fetch = cursor.fetchall()

    user_answers = []

    for answers in fetch:
        user_answers.append(dict(answers))

    return user_answers


@database_common.connection_handler
def get_user_info (cursor: RealDictCursor, user_id: int) -> list:
    query = f"""
        SELECT users.id,
        users.username AS username,
        users.created_on AS user_registration_date,
        COUNT(question.user_id) AS user_asked_questions_counter,
        COUNT(answer.user_id) AS user_answers_counter
        FROM users
        JOIN question ON users.id = question.user_id
        JOIN answer ON users.id = answer.user_id
        WHERE users.id = {user_id}
        GROUP BY users.id"""

    cursor.execute(query)
    fetch = dict(cursor.fetchone())

    return fetch

@database_common.connection_handler
def modifyReputation (cursor: RealDictCursor,user_id, repModifier) -> list:
    query = f"""
    UPDATE users
    SET reputation = reputation + {repModifier}
    WHERE
    id = {user_id};
    """
    cursor.execute(query)
    
    

