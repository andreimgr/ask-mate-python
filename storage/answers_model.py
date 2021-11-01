import database_common
import data_handler
from psycopg2.extras import RealDictCursor

@database_common.connection_handler
def display_answers_by_question_id (cursor: RealDictCursor, question_id: int) -> list:
    query = f"""
        SELECT answer.id AS answer_id,
        answer.submission_time AS answer_submission_time,
        answer.message AS answer_message,
        answer.vote_number,
        users.username
        FROM answer
        JOIN users
        ON answer.user_id = users.id
        WHERE answer.question_id = {question_id}"""
        
    cursor.execute(query)
    fetch = cursor.fetchall()

    answers_by_question_id = []

    for row in fetch:
        answers_by_question_id.append(dict(row))

    return answers_by_question_id


@database_common.connection_handler
def display_answer_by_id (cursor: RealDictCursor, answer_id: str) -> list:
    query = f"""
        SELECT *
        FROM answer
        WHERE answer.id = {answer_id}"""
    cursor.execute(query)
    fetch = cursor.fetchall()

    answer_by_id = []

    for answer in fetch:
        answer_by_id.append(dict(answer))

    return answer_by_id


@database_common.connection_handler
def add_new_answer (cursor: RealDictCursor, question_id: int, new_answer: str, user_id: int) -> list:
    query = f"""
        INSERT INTO answer (submission_time, vote_number, question_id, message, user_id)
        VALUES ('{data_handler.CURRENT_TIME}', {0}, {question_id}, '{new_answer}', {user_id})"""
    cursor.execute(query)


@database_common.connection_handler
def edit_answers_by_id (cursor: RealDictCursor, answer_id: int, new_message: str) -> list:
    query = f"""
        UPDATE answer
        SET message = '{new_message}'
        WHERE id = {answer_id}"""
    cursor.execute(query)


@database_common.connection_handler
def delete_answer_by_id (cursor: RealDictCursor, answer_id: int) -> list:
    query = f"""
        DELETE FROM answer
        WHERE id = {answer_id}"""
    cursor.execute(query)



