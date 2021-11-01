import database_common
import data_handler
from psycopg2 import sql
from psycopg2.extras import RealDictCursor


@database_common.connection_handler
def display_questions (cursor: RealDictCursor) -> list:
    query = """
        SELECT question.id AS question_id, question.submission_time AS question_submission_time, question.title AS question_title, users.username AS username
        FROM question
        JOIN users
        ON question.user_id = users.id
        ORDER by submission_time DESC"""
    cursor.execute(query)
    fetch = cursor.fetchall()
    questions = []

    for row in fetch:
        questions.append(dict(row))
    return questions


@database_common.connection_handler
def display_question_by_id (cursor: RealDictCursor, question_id: int) -> list:
    query = f"""
        SELECT *
        FROM question
        WHERE id = {question_id}"""
    cursor.execute(query)
    fetch = cursor.fetchall()

    question_by_id = []

    for row in fetch:
        question_by_id.append(dict(row))

    return question_by_id


@database_common.connection_handler
def add_new_question (cursor: RealDictCursor, new_question_title: str, new_question_message: str, user_id: int) -> list:
    query = f"""
        INSERT INTO question (submission_time, view_number, vote_number, title, message, user_id)
        VALUES ('{data_handler.CURRENT_TIME}', {0}, {0}, '{new_question_title}', '{new_question_message}',{user_id})"""
    cursor.execute(query)


@database_common.connection_handler
def delete_question_by_id (cursor: RealDictCursor, question_id: int) -> list:
    query = f"""
        DELETE FROM question
        WHERE id = {question_id}"""
    cursor.execute(query)


@database_common.connection_handler
def edit_question_by_id (cursor: RealDictCursor, question_id: int, new_title: str, new_message: str) -> list:
    query = f"""
        UPDATE question
        SET title = '{new_title}', message = '{new_message}'
        WHERE id = {question_id}"""
    cursor.execute(query)


@database_common.connection_handler
def sort_questions (cursor: RealDictCursor, order_by: str, sort_direction: str) -> list:
    query = f"""
        SELECT question.id AS question_id, question.submission_time AS question_submission_time, question.title AS question_title, users.username AS username
        FROM question
        JOIN users
        ON question.user_id = users.id
        ORDER BY {order_by} {sort_direction}"""
    cursor.execute(query)   
    fetch = cursor.fetchall()

    sorted_questions = []

    for row in fetch:
        sorted_questions.append(dict(row))

    return sorted_questions 


@database_common.connection_handler
def display_latest_five_questions (cursor: RealDictCursor) -> list:
    query = """
        SELECT question.id AS question_id, question.submission_time AS question_submission_time, question.title AS question_title, users.username AS username
        FROM question
        JOIN users
        ON question.user_id = users.id
        ORDER BY submission_time
        DESC LIMIT 5"""
    cursor.execute(query)
    fetch = cursor.fetchall()

    latest_five_questions = []

    for question in fetch:
        latest_five_questions.append(dict(question))

    return latest_five_questions


@database_common.connection_handler
def get_question_id_from_answer (cursor: RealDictCursor, answer_id) -> list:
    query = f"""
        SELECT question_id
        FROM answer
        WHERE id = {answer_id}"""
    cursor.execute(query)
    fetch = cursor.fetchall()

    for answer in fetch:
        question_id = answer["question_id"]

    return question_id

@database_common.connection_handler
def getVotes (cursor: RealDictCursor, answer_id) -> list:
    query = f"""
    SELECT vote_number
    FROM answer
    WHERE 
    id = {answer_id}
    LIMIT 1;
    """
    cursor.execute(query)
    
    fetch = dict(cursor.fetchone())

    return fetch["vote_number"]

@database_common.connection_handler
def modifyVote (cursor: RealDictCursor, tableToBeQueried, item_id, voteModifier) -> list:
    query = f"""
    UPDATE {tableToBeQueried}
    SET vote_number = vote_number + {voteModifier}
    WHERE
    id = {item_id};
    """
    cursor.execute(query)


