from flask import Flask, render_template, request, redirect, url_for, flash, session
import data_handler
import util
import bonus_questions

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\xec]/'


@app.route("/")
def index():
    if "username" not in session:
        session["username"] = None
        user = None
    else:
        user = data_handler.get_user_by_username(session["username"])
    parameters = {"order_by": "submission_time", "order_direction": "DESC"}
    questions = data_handler.list_latest_questions_by_parameters(parameters)
    return render_template("index.html",
                           questions=questions,
                           header=data_handler.QUESTION_HEADER,
                           username=session["username"],
                           user_id=user)


@app.route("/list")
def list_questions():
    if "username" not in session:
        session["username"] = None
        user = None
    else:
        user = data_handler.get_user_by_username(session["username"])
    parameters = {"order_by": "submission_time", "order_direction": "DESC"}
    questions = data_handler.list_all_questions_by_parameters(parameters)
    return render_template("index.html",
                           questions=questions,
                           header=data_handler.QUESTION_HEADER,
                           username=session["username"],
                           user_id=user)


@app.route("/sort")
def sort_questions():
    if "username" not in session:
        session["username"] = None
        user = None
    else:
        user = data_handler.get_user_by_username(session["username"])
    parameters = request.args.to_dict()
    questions = data_handler.list_latest_questions_by_parameters(parameters)
    return render_template("index.html",
                           questions=questions,
                           header=data_handler.QUESTION_HEADER,
                           username=session["username"],
                           user_id=user)


@app.route("/search")
def search():
    searching_phrase = request.args.get("q")
    questions = util.highlight_search_result(data_handler.search_questions(searching_phrase), searching_phrase)
    answers = util.highlight_search_result(data_handler.search_answers(searching_phrase), searching_phrase)
    return render_template("search/search_result.html",
                           questions=questions,
                           answers=answers,
                           phrase=searching_phrase,
                           question_header=data_handler.SEARCH_HEADER_QUESTION,
                           answer_header=data_handler.SEARCH_HEADER_ANSWER)


@app.route("/question/<id>")
def display(id):
    if "username" not in session:
        session["username"] = None
        user = None
    else:
        user = data_handler.get_user_by_username(session["username"])
    data_handler.count_view_number(id)
    question = data_handler.get_question_by_id(id)
    answer = data_handler.get_answer_by_question_id(id)
    answer_ids = tuple(answer["id"] for answer in data_handler.get_answer_ids_by_question_id(id))
    question_comments = data_handler.get_comments_by_question_id(id)
    answers_comments = data_handler.get_comments_by_answer_id(answer_ids)
    question_tag = data_handler.get_question_tag_by_question_id(id)
    return render_template("display/display_result.html",
                           question=question,
                           answers=answer,
                           question_comments=question_comments,
                           answers_comments=answers_comments,
                           question_tag=question_tag,
                           question_header=data_handler.DISPLAY_QUESTION_HEADER,
                           answer_header=data_handler.ANSWER_HEADER,
                           question_comment_header=data_handler.QUESTION_COMMENT_HEADER,
                           answer_comment_header=data_handler.ANSWER_COMMENT_HEADER,
                           username=session["username"],
                           user_id=user)


@app.route("/add-question", methods=["GET", "POST"])
def add_question():
    if session["username"] == None:
        return redirect(url_for("registration"))
    user = data_handler.get_user_by_username(session["username"])
    if request.method == "POST":
        question = util.save_image(request.form.to_dict(), request.files["image"])
        data_handler.add_question(question, int(user[0]["id"]))
        data_handler.count_questions_plus(session["username"])
        return redirect(url_for("index"))
    return render_template("questions/add_question.html")


@app.route("/question/<id>/new-answer", methods=["GET", "POST"])
def add_answer(id):
    if session["username"] == None:
        return redirect(url_for("registration"))
    user = data_handler.get_user_by_username(session["username"])
    if request.method == "POST":
        answer = util.save_image(request.form.to_dict(), request.files["image"])
        data_handler.add_answer(id, answer, int(user[0]["id"]))
        data_handler.count_answers_plus(session["username"])
        return redirect(url_for("display", id=id))
    return render_template("answers/add_answer.html", id=id)


@app.route("/question/<id>/new-comment", methods=["GET", "POST"])
def add_comment_to_question(id):
    if session["username"] == None:
        return redirect(url_for("registration"))
    user = data_handler.get_user_by_username(session["username"])
    if request.method == "POST":
        comment = request.form.to_dict()
        data_handler.add_comment_to_question(id, comment, int(user[0]["id"]))
        data_handler.count_comments_plus(session["username"])
        return redirect(url_for("display", id=id))
    return render_template("comments/add_comment_to_question.html",
                           id=id)


@app.route("/answer/<id>/new-comment", methods=["GET", "POST"])
def add_comment_to_answer(id):
    if session["username"] == None:
        return redirect(url_for("registration"))
    user = data_handler.get_user_by_username(session["username"])
    if request.method == "POST":
        comment = request.form.to_dict()
        data_handler.add_comment_to_answer(id, comment, int(user[0]["id"]))
        data_handler.count_comments_plus(session["username"])
        return redirect(url_for("display", id=data_handler.get_answer_by_id(id)[0]["question_id"]))
    return render_template("comments/add_comment_to_answer.html",
                           id=id)


@app.route("/question/<id>/new-tag", methods=["GET", "POST"])
def add_tag(id):
    if session["username"] == None:
        return redirect(url_for("registration"))
    tags = data_handler.get_tags()
    if request.method == "POST":
        tag = data_handler.create_tag(request.form.to_dict()["tag"])
        data_handler.add_tag_to_question(id, tag[0]["id"])
        return redirect(url_for("display", id=id))
    return render_template("tags/add_tag.html",
                           id=id,
                           tags=tags)


@app.route("/question/<id>/delete", methods=["GET", "POST"])
def delete_question(id):
    if session["username"] == None:
        return redirect(url_for("registration"))
    question = data_handler.get_question_by_id(id)
    util.delete_image(question)
    data_handler.delete_question(id)
    data_handler.count_questions_minus(session["username"])
    return redirect(url_for("index"))


@app.route("/answer/<id>/delete", methods=["GET", "POST"])
def delete_answer(id):
    if session["username"] == None:
        return redirect(url_for("registration"))
    question_id = data_handler.get_answer_by_id(id)
    answer = data_handler.get_answer_by_id(id)
    util.delete_image(answer)
    data_handler.delete_answer(id)
    data_handler.count_answers_minus(session["username"])
    return redirect(url_for("display", id=question_id[0]["question_id"]))


@app.route("/comments/<id>/delete ", methods=["GET", "POST"])
def delete_comment(id):
    if session["username"] == None:
        return redirect(url_for("registration"))
    comment = data_handler.get_comment_by_id(id)
    if comment[0]["question_id"] is None:
        link = data_handler.get_answer_by_id(comment[0]["answer_id"])
    else:
        link = data_handler.get_comment_by_id(id)
    data_handler.delete_comment(id)
    data_handler.count_comments_minus(session["username"])
    return redirect(url_for("display", id=link[0]["question_id"]))


@app.route("/question/<question_id>/tag/<tag_id>/delete")
def delete_tag(question_id, tag_id):
    if session["username"] == None:
        return redirect(url_for("registration"))
    data_handler.delete_tag_by_tag_id(question_id, tag_id)
    return redirect(url_for("display", id=question_id))


@app.route("/question/<id>/update", methods=["GET", "POST"])
def update_question(id):
    if session["username"] == None:
        return redirect(url_for("registration"))
    question = data_handler.get_question_by_id(id)
    if request.method == "POST":
        new_question = request.form.to_dict()
        data_handler.update_question(id, new_question)
        return redirect(url_for("display", id=id))
    return render_template("questions/update_question.html",
                           question=question[0])


@app.route("/answer/<id>/edit", methods=["GET", "POST"])
def update_answer(id):
    if session["username"] == None:
        return redirect(url_for("registration"))
    answer = data_handler.get_answer_by_id(id)
    if request.method == "POST":
        new_answer = request.form.to_dict()
        data_handler.update_answer(id, new_answer)
        return redirect(url_for("display", id=answer[0]["question_id"]))
    return render_template("answers/update_answers.html",
                           answer=answer[0])


@app.route("/comment/<id>/edit", methods=["GET", "POST"])
def update_comment(id):
    if session["username"] == None:
        return redirect(url_for("registration"))
    comment = data_handler.get_comment_by_id(id)
    if comment[0]["question_id"] is None:
        link = data_handler.get_answer_by_id(comment[0]["answer_id"])
    else:
        link = data_handler.get_comment_by_id(id)
    if request.method == "POST":
        data_handler.count_edit(id)
        comment = request.form.to_dict()
        data_handler.update_comment(id, comment)
        return redirect(url_for("display", id=link[0]["question_id"]))
    return render_template("comments/update_comments.html",
                           comment=comment[0])


@app.route("/question/<id>/vote_up")
def vote_up_question(id):
    if session["username"] == None:
        return redirect(url_for("registration"))
    data_handler.vote_question(id, "+")
    question = data_handler.get_question_by_id(id)
    data_handler.reputation_question(question[0]["user_id"], '+')
    return redirect(url_for("display", id=id))


@app.route("/question/<id>/vote_down")
def vote_down_question(id):
    if session["username"] == None:
        return redirect(url_for("registration"))
    data_handler.vote_question(id, "-")
    question = data_handler.get_question_by_id(id)
    data_handler.reputation_question(question[0]["user_id"], '-')
    return redirect(url_for("display", id=id))


@app.route("/answer/<id>/vote_up")
def vote_up_answer(id):
    if session["username"] == None:
        return redirect(url_for("registration"))
    data_handler.vote_answer(id, "+")
    answer = data_handler.get_answer_by_id(id)
    data_handler.reputation_answer(answer[0]["user_id"], '+')
    return redirect(url_for("display", id=data_handler.get_answer_by_id(id)[0]["question_id"]))


@app.route("/answer/<id>/vote_down")
def vote_down_answer(id):
    if session["username"] == None:
        return redirect(url_for("registration"))
    data_handler.vote_answer(id, "-")
    answer = data_handler.get_answer_by_id(id)
    data_handler.reputation_answer(answer[0]["user_id"], '-')
    return redirect(url_for("display", id=data_handler.get_answer_by_id(id)[0]["question_id"]))


@app.route("/bonus-questions")
def main():
    return render_template('bonus_questions.html', questions=bonus_questions.SAMPLE_QUESTIONS)


@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        password_repeat = request.form["password-repeat"]
        validate_email = data_handler.get_user_by_username(email)
        if password == password_repeat:
            hashed_password = util.hash_password(password)
            if validate_email == []:
                data_handler.add_user(email, hashed_password)
                session["username"] = email
                return redirect(url_for("index"))
            else:
                flash("The email is already taken!", "Error")
        else:
            flash("Your password and confirmation password do not match!", "Error")
    return render_template('registration.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        validate_email = data_handler.get_user_by_username(email)
        if validate_email != []:
            validate_password = util.verify_password(password, validate_email[0]["password_hash"])
            if validate_password:
                session["username"] = email
                return redirect(url_for("index"))
            else:
                flash("Not valid password!")
        else:
            flash("This email is not valid!")
    return render_template('login.html')


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


@app.route("/user/<user_id>")
def user_page(user_id):
    if session["username"] == None:
        return redirect(url_for("registration"))
    user = data_handler.get_user_by_user_id(user_id)
    questions = data_handler.get_user_questions(user[0]["id"])
    answers = data_handler.get_user_answers(user[0]["id"])
    question_comments = data_handler.get_user_question_comments(user[0]["id"])
    answer_comments = data_handler.get_user_answer_comments(user[0]["id"])
    return render_template("users/user.html",
                           user=user,
                           header=data_handler.DISPLAY_USER_HEADER,
                           questions=questions,
                           answers=answers,
                           question_comments=question_comments,
                           answer_comments=answer_comments,
                           )


@app.route("/users")
def list_users():
    if session["username"] == None:
        return redirect(url_for("registration"))
    return render_template('users.html',
                           users=data_handler.get_all_user(),
                           header=data_handler.USERS_HEADER)


@app.route('/accept-answer/<answer_id>/<state>')
def accept_answer(answer_id, state):
    answer = data_handler.get_answer_by_id(answer_id)
    data_handler.change_answer_state(answer_id, state)
    data_handler.reputation_accepted(answer[0]["user_id"], state)
    return redirect(url_for("display", id=data_handler.get_answer_by_id(answer_id)[0]["question_id"]))

@app.route("/tags")
def list_tags():
    return render_template('tag_list.html', tag=data_handler.get_all_tags())

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True,
    )
