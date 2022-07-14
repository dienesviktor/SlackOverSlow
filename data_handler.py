from psycopg2 import sql
import connection

QUESTION_HEADER = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image", "user_id"]
DISPLAY_QUESTION_HEADER = ["vote_number", "title", "message", "image"]
ANSWER_HEADER = ["vote_number", "message", "image", "user_id"]
QUESTION_COMMENT_HEADER = ["message", "submission_time", "edited_count", "user_id"]
ANSWER_COMMENT_HEADER = ["answer_id", "message", "submission_time", "edited_count", "user_id"]
SEARCH_HEADER_QUESTION = ["Question", "Title", "Message"]
SEARCH_HEADER_ANSWER = ["Question", "Answer", "Message"]
DISPLAY_USER_HEADER = ["id", "username", "registration_date", "number_of_questions", "number_of_answers", "number_of_comments", "reputation"]
USERS_HEADER = ["username", "registration_date", "number_of_questions", "number_of_answers", "number_of_comments", "reputation"]



@connection.connection_handler
def get_question_by_id(cursor, question_id):
    cursor.execute(sql.SQL("SELECT * \
                            FROM question \
                            WHERE id = {question_id}").format
                   (question_id=sql.Literal(question_id)))
    return cursor.fetchall()


@connection.connection_handler
def get_answer_by_id(cursor, answer_id):
    cursor.execute(sql.SQL("SELECT * \
                            FROM answer \
                            WHERE id = {answer_id}").format
                   (answer_id=sql.Literal(answer_id)))
    return cursor.fetchall()


@connection.connection_handler
def get_answer_by_question_id(cursor, question_id):
    cursor.execute(sql.SQL("SELECT * \
                            FROM answer \
                            WHERE question_id = {question_id} \
                            ORDER BY id").format
                   (question_id=sql.Literal(question_id)))
    return cursor.fetchall()


@connection.connection_handler
def get_answer_ids_by_question_id(cursor, id):
    cursor.execute(sql.SQL("SELECT id \
                            FROM answer \
                            WHERE question_id = {id}").format
                   (id=sql.Literal(id)))
    return cursor.fetchall()


@connection.connection_handler
def get_comment_by_id(cursor, comment_id):
    cursor.execute(sql.SQL("SELECT * \
                            FROM comment \
                            WHERE id = {comment_id}").format
                   (comment_id=sql.Literal(comment_id)))
    return cursor.fetchall()


@connection.connection_handler
def get_comments_by_question_id(cursor, id):
    cursor.execute(sql.SQL("SELECT * \
                            FROM comment \
                            WHERE question_id = {id} \
                            ORDER BY id").format
                   (id=sql.Literal(id)))
    return cursor.fetchall()


@connection.connection_handler
def get_comments_by_answer_id(cursor, answer_ids):
    if len(answer_ids) != 0:
        cursor.execute(sql.SQL("SELECT * \
                                FROM comment \
                                WHERE answer_id IN {answer_ids} \
                                ORDER BY id").format
                       (answer_ids=sql.Literal(answer_ids)))
        return cursor.fetchall()
    else:
        return []


@connection.connection_handler
def get_tags(cursor):
    cursor.execute(sql.SQL("SELECT name FROM tag"))
    return cursor.fetchall()


@connection.connection_handler
def get_question_tag_by_question_id(cursor, question_id):
    cursor.execute(sql.SQL("SELECT id, name \
                            FROM question_tag \
                            LEFT JOIN tag ON question_tag.tag_id = tag.id \
                            WHERE question_tag.question_id = {question_id}").format
                   (question_id=sql.Literal(question_id)))
    return cursor.fetchall()


@connection.connection_handler
def list_latest_questions_by_parameters(cursor, parameters):
    cursor.execute(sql.SQL("SELECT * \
                            FROM question \
                            ORDER BY {order_by} {order_direction} \
                            LIMIT 5").format
                   (order_by=sql.Identifier(parameters["order_by"]),
                    order_direction=sql.SQL(parameters["order_direction"])))
    return cursor.fetchall()


@connection.connection_handler
def list_all_questions_by_parameters(cursor, parameters):
    cursor.execute(sql.SQL("SELECT * \
                            FROM question \
                            ORDER BY {order_by} {order_direction}").format
                   (order_by=sql.Identifier(parameters["order_by"]),
                    order_direction=sql.SQL(parameters["order_direction"])))
    return cursor.fetchall()


@connection.connection_handler
def add_question(cursor, question, user_id):
    cursor.execute(sql.SQL("INSERT INTO question (submission_time, view_number, vote_number, title, message, image, user_id) \
                            VALUES (CURRENT_TIMESTAMP(0), 0, 0, {title}, {message}, {image}, {user_id})").format
                   (title=sql.Literal(question["title"]),
                    message=sql.Literal(question["message"]),
                    image=sql.Literal(question["image"]),
                    user_id=sql.Literal(user_id)))


@connection.connection_handler
def add_answer(cursor, question_id, answer, user_id):
    cursor.execute(sql.SQL("INSERT INTO answer (submission_time, vote_number, question_id, message, image, state, user_id) \
                            VALUES (CURRENT_TIMESTAMP(0), 0, {question_id}, {message}, {image}, False, {user_id})").format
                   (question_id=sql.Literal(question_id),
                    message=sql.Literal(answer["message"]),
                    image=sql.Literal(answer["image"]),
                    user_id=sql.Literal(user_id)))


@connection.connection_handler
def add_comment_to_question(cursor, answer_id, comment, user_id):
    cursor.execute(sql.SQL("INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count, user_id) \
                            VALUES ({question_id}, {answer_id}, {message}, CURRENT_TIMESTAMP(0), 0, {user_id})").format
                   (answer_id=sql.Literal(None),
                    question_id=sql.Literal(answer_id),
                    message=sql.Literal(comment["message"]),
                    user_id=sql.Literal(user_id)))



@connection.connection_handler
def add_comment_to_answer(cursor, answer_id, comment, user_id):
    cursor.execute(sql.SQL("INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count, user_id) \
                            VALUES ({question_id}, {answer_id}, {message}, CURRENT_TIMESTAMP(0), 0, {user_id})").format
                   (answer_id=sql.Literal(answer_id),
                    question_id=sql.Literal(None),
                    message=sql.Literal(comment["message"]),
                    user_id=sql.Literal(user_id)))


@connection.connection_handler
def create_tag(cursor, new_tag):
    cursor.execute(sql.SQL("INSERT INTO tag (name) VALUES ({new_tag}) \
                            ON CONFLICT (name) DO NOTHING").format
                   (new_tag=sql.Literal(new_tag)))
    cursor.execute(sql.SQL("SELECT id FROM tag \
                            WHERE name = {new_tag}").format
                   (new_tag=sql.Literal(new_tag)))
    return cursor.fetchall()


@connection.connection_handler
def add_tag_to_question(cursor, question_id, tag_id):
    cursor.execute(sql.SQL("INSERT INTO question_tag (question_id, tag_id) \
                            VALUES ({question_id}, {tag_id}) \
                            ON CONFLICT (question_id, tag_id) DO NOTHING").format
                   (tag_id=sql.Literal(tag_id),
                    question_id=sql.Literal(question_id)))


@connection.connection_handler
def delete_question(cursor, question_id):
    cursor.execute(sql.SQL("DELETE FROM question \
                            WHERE id = {question_id}").format
                   (question_id=sql.Literal(question_id)))


@connection.connection_handler
def delete_answer(cursor, answer_id):
    cursor.execute(sql.SQL("DELETE FROM answer \
                            WHERE id = {answer_id}").format
                   (answer_id=sql.Literal(answer_id)))


@connection.connection_handler
def delete_comment(cursor, comment_id):
    cursor.execute(sql.SQL("DELETE FROM comment \
                            WHERE id = {comment_id}").format
                   (comment_id=sql.Literal(comment_id)))


@connection.connection_handler
def delete_tag_by_tag_id(cursor, question_id, tag_id):
    cursor.execute(sql.SQL("DELETE FROM question_tag \
                            WHERE question_id = {question_id} AND tag_id = {tag_id}").format
                   (question_id=sql.Literal(question_id),
                    tag_id=sql.Literal(tag_id)))


@connection.connection_handler
def update_question(cursor, question_id, question):
    cursor.execute(sql.SQL("UPDATE question \
                            SET message = {message}, title = {title} \
                            WHERE id = {question_id}").format
                   (message=sql.Literal(question["message"]),
                    title=sql.Literal(question["title"]),
                    question_id=sql.Literal(question_id)))


@connection.connection_handler
def update_answer(cursor, answer_id, answer):
    cursor.execute(sql.SQL("UPDATE answer \
                            SET message = {message} \
                            WHERE id = {answer_id}").format
                   (answer_id=sql.Literal(answer_id),
                    message=sql.Literal(answer["message"])))


@connection.connection_handler
def update_comment(cursor, comment_id, comment):
    cursor.execute(sql.SQL("UPDATE comment \
                            SET message = {message}, submission_time = CURRENT_TIMESTAMP(0) \
                            WHERE id = {comment_id}").format
                   (message=sql.Literal(comment["message"]),
                    comment_id=sql.Literal(comment_id)))


@connection.connection_handler
def vote_question(cursor, question_id, vote):
    cursor.execute(sql.SQL("UPDATE question \
                            SET vote_number = \
                            CASE WHEN {vote} = '+' \
                            THEN vote_number + 1 \
                            ELSE vote_number - 1 END \
                            WHERE id = {question_id}").format
                   (question_id=sql.Literal(question_id),
                    vote=sql.Literal(vote)))


@connection.connection_handler
def vote_answer(cursor, answer_id, vote):
    cursor.execute(sql.SQL("UPDATE answer \
                            SET vote_number = \
                            CASE WHEN {vote} = '+' \
                            THEN vote_number + 1 \
                            ELSE vote_number - 1 END \
                            WHERE id = {answer_id}").format
                   (answer_id=sql.Literal(answer_id),
                    vote=sql.Literal(vote)))


@connection.connection_handler
def search_questions(cursor, search_phrase):
    cursor.execute(sql.SQL("SELECT DISTINCT question.id, question.title, question.message \
                            FROM question \
                            LEFT JOIN answer ON question.id = answer.question_id \
                            WHERE question.message ILIKE {search_phrase} OR question.title ILIKE {search_phrase} \
                            ORDER BY question.id").format
                   (search_phrase=sql.Literal(f"%{search_phrase}%")))
    return cursor.fetchall()


@connection.connection_handler
def search_answers(cursor, search_phrase):
    cursor.execute(sql.SQL("SELECT answer.question_id, answer.id, answer.message \
                            FROM question \
                            LEFT JOIN answer ON question.id = answer.question_id \
                            WHERE answer.message ILIKE {search_phrase} \
                            ORDER BY question.id").format
                   (search_phrase=sql.Literal(f"%{search_phrase}%")))
    return cursor.fetchall()


@connection.connection_handler
def count_view_number(cursor, question_id):
    cursor.execute(sql.SQL("UPDATE question \
                            SET view_number = view_number + 1 \
                            WHERE id = {question_id}").format
                   (question_id=sql.Literal(question_id)))


@connection.connection_handler
def count_edit(cursor, comment_id):
    cursor.execute(sql.SQL("UPDATE comment \
                            SET edited_count = edited_count + 1 \
                            WHERE id = {comment_id}").format
                   (comment_id=sql.Literal(comment_id)))


@connection.connection_handler
def get_user_by_user_id(cursor, user_id):
    cursor.execute(sql.SQL("SELECT * \
                            FROM users \
                            WHERE id = {user_id}").format
                   (user_id=sql.Literal(user_id)))
    return cursor.fetchall()


@connection.connection_handler
def get_user_by_username(cursor, email):
    cursor.execute(sql.SQL("SELECT * \
                            FROM users \
                            WHERE username = {email}").format
                   (email=sql.Literal(email)))
    return cursor.fetchall()


@connection.connection_handler
def add_user(cursor, email, password):
    cursor.execute(sql.SQL("INSERT INTO users (username, password_hash, registration_date, number_of_questions, number_of_answers, number_of_comments, reputation) \
                            VALUES ({email}, {password}, CURRENT_TIMESTAMP(0), 0, 0, 0, 0)").format
                   (email=sql.Literal(email),
                    password=sql.Literal(password)))


@connection.connection_handler
def get_user_questions(cursor, user_id):
    cursor.execute(sql.SQL("SELECT id, title, message \
                            FROM question \
                            WHERE user_id = {user_id}").format
                   (user_id=sql.Literal(user_id)))
    return cursor.fetchall()


@connection.connection_handler
def get_user_answers(cursor, user_id):
    cursor.execute(sql.SQL("SELECT question_id, message \
                            FROM answer \
                            WHERE user_id = {user_id}").format
                   (user_id=sql.Literal(user_id)))
    return cursor.fetchall()


@connection.connection_handler
def get_user_question_comments(cursor, user_id):
    cursor.execute(sql.SQL("SELECT question_id, message \
                            FROM comment \
                            WHERE user_id = {user_id} AND question_id != {notvalid}").format
                   (user_id=sql.Literal(user_id),
                    notvalid=sql.Literal(0)))
    return cursor.fetchall()


@connection.connection_handler
def get_user_answer_comments(cursor, user_id):
    cursor.execute(sql.SQL("SELECT answer.question_id, comment.message \
                                FROM comment \
                                JOIN answer ON comment.answer_id = answer.id \
                                WHERE comment.user_id = {user_id} AND comment.answer_id != {notvalid}").format
                   (user_id=sql.Literal(user_id),
                    notvalid=sql.Literal(0)))
    return cursor.fetchall()

  
@connection.connection_handler
def get_all_user(cursor):
    cursor.execute(sql.SQL("SELECT id, username, registration_date, number_of_questions, number_of_answers, number_of_comments, reputation  \
                            FROM users"))
    return cursor.fetchall()


@connection.connection_handler
def count_questions_plus(cursor, email):
    cursor.execute(sql.SQL("UPDATE users \
                            SET number_of_questions = number_of_questions + 1 \
                            WHERE username = {email}").format
                   (email=sql.Literal(email)))

@connection.connection_handler
def count_questions_minus(cursor, email):
    cursor.execute(sql.SQL("UPDATE users \
                            SET number_of_questions = number_of_questions - 1 \
                            WHERE username = {email}").format
                   (email=sql.Literal(email)))


@connection.connection_handler
def count_answers_plus(cursor, email):
    cursor.execute(sql.SQL("UPDATE users \
                            SET number_of_answers = number_of_answers + 1 \
                            WHERE username = {email}").format
                   (email=sql.Literal(email)))

@connection.connection_handler
def count_answers_minus(cursor, email):
    cursor.execute(sql.SQL("UPDATE users \
                            SET number_of_answers = number_of_answers - 1 \
                            WHERE username = {email}").format
                   (email=sql.Literal(email)))


@connection.connection_handler
def count_comments_plus(cursor, email):
    cursor.execute(sql.SQL("UPDATE users \
                            SET number_of_comments = number_of_comments + 1 \
                            WHERE username = {email}").format
                   (email=sql.Literal(email)))


@connection.connection_handler
def count_comments_minus(cursor, email):
    cursor.execute(sql.SQL("UPDATE users \
                            SET number_of_comments = number_of_comments - 1 \
                            WHERE username = {email}").format
                   (email=sql.Literal(email)))


@connection.connection_handler
def reputation_question(cursor, user_id, vote):
    cursor.execute(sql.SQL("UPDATE users \
                            SET reputation = \
                            CASE WHEN {vote} = '+' \
                            THEN users.reputation + 5 \
                            ELSE users.reputation - 2 END \
                            WHERE id = {user_id}").format
                   (user_id=sql.Literal(user_id),
                    vote=sql.Literal(vote)))


@connection.connection_handler
def reputation_answer(cursor, user_id, vote):
    cursor.execute(sql.SQL("UPDATE users \
                            SET reputation = \
                            CASE WHEN {vote} = '+' \
                            THEN users.reputation + 10 \
                            ELSE users.reputation - 2 END \
                            WHERE id = {user_id}").format
                   (user_id=sql.Literal(user_id),
                    vote=sql.Literal(vote)))


@connection.connection_handler
def reputation_accepted(cursor, user_id, state):
    cursor.execute(sql.SQL("UPDATE users \
                            SET reputation = reputation + 15\
                            WHERE id = {user_id} AND {state} = True").format
                   (user_id=sql.Literal(user_id),
                    state=sql.Literal(state)))


@connection.connection_handler
def change_answer_state(cursor, answer_id, state):
    cursor.execute(sql.SQL("UPDATE answer \
                            SET state = \
                            CASE WHEN {state} THEN True \
                            ELSE False END \
                            WHERE id = {answer_id}").format
                   (answer_id=sql.Literal(answer_id),
                    state=sql.Literal(state)))


@connection.connection_handler
def get_all_tags(cursor):
    cursor.execute(sql.SQL("SELECT tag.name, COUNT(question_tag.question_id) as number \
                            FROM tag \
                            JOIN question_tag ON question_tag.tag_id = tag.id \
                            GROUP BY tag.name"))
    return cursor.fetchall()
