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



