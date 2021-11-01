import database_common
import data_handler
from psycopg2 import sql
from psycopg2.extras import RealDictCursor


@database_common.connection_handler
def display_comments_by_question_id(cursor: RealDictCursor, question_id) -> list:
    query = f"""
        SELECT comment.question_id,
        comment.submission_time AS comment_submission_time,
        comment.message AS comment_message,
        users.username AS username
        FROM comment
        JOIN users
        ON comment.user_id = users.id
        WHERE comment.question_id = {question_id}"""
    
    cursor.execute(query)
    fetch = cursor.fetchall()

    comments_by_question = []

    for comment in fetch:
        comments_by_question.append(dict(comment))

    return comments_by_question


@database_common.connection_handler
def add_comment_to_question (cursor: RealDictCursor, question_id: int, message: str, user_id: int) -> list:
    query = f"""
        INSERT INTO comment (question_id, message, submission_time, user_id)
        VALUES ({question_id}, '{message}', '{data_handler.CURRENT_TIME}',{user_id})"""
    cursor.execute(query)


@database_common.connection_handler
def add_comment_to_answer (cursor: RealDictCursor, answer_id: int, message: str, user_id: int) -> list:
    query = f"""
        INSERT INTO comment (answer_id, message, submission_time, user_id)
        VALUES ({answer_id}, '{message}', '{data_handler.CURRENT_TIME}', {user_id})"""
    cursor.execute(query)


@database_common.connection_handler
def display_comments_for_answer (cursor: RealDictCursor, answer_id):
    query = f"""
        select comment.id AS comment_id,
        comment.message AS comment_message,
        comment.submission_time AS comment_submission_time,
        comment.answer_id AS comment_answer_id,
        answer.id AS answer_id,
        answer.message AS answer_message
        from comment
        join answer
        on comment.answer_id = answer.id"""

    cursor.execute(query)
    fetch = cursor.fetchall()

    comments_by_answer = []

    for comment in fetch:
        comments_by_answer.append(dict(comment))

    return comments_by_answer


@database_common.connection_handler
def update_comment_by_id (cursor: RealDictCursor, comment_id: int, new_message: str) -> list:
    query = f"""
        UPDATE comment
        SET message = '{new_message}', submission_time = '{data_handler.CURRENT_TIME}'
        WHERE id = {comment_id}"""
    cursor.execute(query)



