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



