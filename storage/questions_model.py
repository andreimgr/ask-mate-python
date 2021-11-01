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



