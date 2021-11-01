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



