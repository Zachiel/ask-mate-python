"""AskMate server route management."""
# pylint: disable=no-value-for-parameter, no-member
# pyright: reportGeneralTypeIssues=false
import os
import sys
from typing import Union, Any
import uuid
import re
from flask import Flask, render_template, request, redirect, Response
from flask import session, abort
import data_handler

UPLOAD_FOLDER: str = 'static\\uploads'

app: Flask = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1 * 1000 * 1000
app.secret_key = b'$2b$12$LejxQfNZY8SxvKE8raOr3.tGE2CDymFMqybBCNKPD1R.lFf9Romqa'


def save_image(file) -> Union[str, None]:
    """Save image to server and return file path."""
    if file and data_handler.allowed_file(file.filename):
        filename: str = uuid.uuid4().hex + '.' +\
            file.filename.rsplit('.', 1)[1].lower()
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        filename = None
    file_path: Union[str, None] = os.path.join(app.config['UPLOAD_FOLDER'],
                                                filename) if filename else None
    return file_path


@app.route("/")
def hello() -> str:
    """Main page route."""
    session_user = data_handler.get_id_by_username(session.get('user', default=''))
    logged_in = session.get('logged_in', default=False)
    questions: list[dict[str, str]] = data_handler.get_latest_questions()
    comment_count: dict[str, str] = data_handler.get_answer_count()
    return render_template('pages/index.html',
                            questions=questions,
                            time_passed=data_handler.how_much_time_passed,
                            comment_count=comment_count,
                            to_string=str,
                            session_user=session_user,
                            logged_in=logged_in)


@app.route("/list")
def list_questions() -> str:
    """Main page route."""
    session_user = data_handler.get_id_by_username(session.get('user', default=''))
    logged_in = session.get('logged_in', default=False)
    questions: list[dict[str, str]] = data_handler.get_sorted_questions()
    comment_count: dict[str, str] = data_handler.get_answer_count()
    sort_by: Union[str, None] = request.args.get('order_by')
    order: Union[str, None] = request.args.get('order_direction')
    if sort_by:
        questions: list[dict[str, str]] = data_handler.get_sorted_questions(
                                            sort_by, order)
    return render_template('pages/index.html',
                            questions=questions,
                            time_passed=data_handler.how_much_time_passed,
                            comment_count=comment_count,
                            to_string=str,
                            session_user=session_user,
                            logged_in=logged_in)


@app.route("/question/<question_id>/")
def display_question(question_id) -> str:
    """Specific question page route."""
    session_user = data_handler.get_id_by_username(session.get('user', default=''))
    logged_in = session.get('logged_in', default=False)
    data_handler.increase_question_view_count(question_id)
    question: list[dict[str, str]] = data_handler.get_question_by_id(
                                                                    question_id)
    answers: list[dict[str, str]] = data_handler.get_answers_for_question(
                                                                    question_id)
    answer_ids: list[int] = [row['id'] for row in answers]
    question_comments: list[dict[str, str]] = \
                            data_handler.get_comments_for_question(question_id)
    answer_comments: list[dict[str, str]] = \
                                    data_handler.get_answer_comments(answer_ids)
    tag= data_handler.get_tag_for_question(question_id)
    question_ids_of_current_user = []
    question_of_user = False
    if logged_in:
        question_ids_of_current_user = data_handler.get_question_ids_of_user_id(session_user['id'])
        question_of_user = data_handler.check_if_question_of_user(question_id, question_ids_of_current_user)
    return render_template('pages/display_question.html',
                            question=question[0],
                            answers=answers,
                            question_comments=question_comments,
                            answer_comments=answer_comments,
                            count_answers=len(answers),
                            to_string=str,
                            tag = None if tag is None else tag,
                            question_of_user=question_of_user,
                            session_user=session_user,
                            logged_in=logged_in)


@app.route('/add_question', methods=['GET', 'POST'])
def new_question() -> Union[Response, str]:
    """Adding new question route."""
    session_user = data_handler.get_id_by_username(session.get('user', default=''))
    logged_in = session.get('logged_in', default=False)
    tags = data_handler.get_tags()
    if request.method == "POST":
        title: Union[str, None] = request.form.get("title")
        message: Union[str, None] = request.form.get("message")
        file: Any = request.files['file']
        file_path: Union[str, None] = save_image(file)
        data_handler.add_question_to_database(title, message, file_path)

        tag = request.form.get("tag")
        adding_question = data_handler.get_question_id_from_title(title)
        data_handler.add_tag(adding_question, tag)
        return redirect('/list')
    return render_template('pages/question.html', tags=tags,
    session_user=session_user,
    logged_in=logged_in)


@app.route("/question/<question_id>/edit", methods=['POST','GET'])
def edit_question(question_id) -> Union[Response, str]:
    """Editing specific question route."""
    session_user = data_handler.get_id_by_username(session.get('user', default=''))
    logged_in = session.get('logged_in', default=False)
    question: list[dict[str, str]] = data_handler.get_question_by_id(
                                                            question_id)
    current_tag = data_handler.get_tag_for_question(question_id)
    tags = data_handler.get_tags()
    if request.method == 'POST':
        title: Union[str, None] = request.form.get("title")
        message: Union[str, None] = request.form.get("message")
        file: Any = request.files['file']
        file_path: Union[str, None] = save_image(file)
        tag = request.form.get("tag")
        data_handler.edit_question(question_id, title, message, file_path, tag)
        return redirect('/question/'+question_id)
    return render_template('pages/question.html',
                        question=question[0],
                        to_string=str,
						current_tag=current_tag,
						tags=tags,
                        session_user=session_user,
                        logged_in=logged_in)


@app.route("/question/<question_id>/delete",
            methods=["POST"])
def delete_question(question_id) -> Response:
    """Specific question delete route."""
    data_handler.delete_question(question_id)
    return redirect("/list")


@app.route("/question/<question_id>/vote-up", methods=['POST'])
def vote_question_up(question_id) -> Response:
    """Question upvoting route."""
    data_handler.vote_question_up(question_id)
    return redirect("/list")


@app.route("/question/<question_id>/vote-down", methods=['POST'])
def vote_question_down(question_id) -> Response:
    """Question downvoting route."""
    data_handler.vote_question_down(question_id)
    return redirect("/list")


@app.route("/question/<question_id>/new-answer",
            methods=['GET', 'POST'])
def new_answer(question_id) -> Union[Response, str]:
    """Adding new answer route."""
    session_user = data_handler.get_id_by_username(session.get('user', default=''))
    logged_in = session.get('logged_in', default=False)
    if request.method == "POST":
        message: Union[str, None] = request.form.get("message")
        file: Any = request.files['file']
        file_path: Union[str, None] = save_image(file)
        data_handler.add_answer_to_database(question_id, message, file_path)
        return redirect("/question/"+question_id)
    return render_template('pages/answer.html',
    session_user=session_user,
    logged_in=logged_in)


@app.route("/question/<question_id>/answer/<answer_id>/edit_answer",
            methods=['GET', 'POST'])
def edit_answer(question_id, answer_id) -> Union[Response, str]:
    """Edit existing answer route."""
    session_user = data_handler.get_id_by_username(session.get('user', default=''))
    logged_in = session.get('logged_in', default=False)
    answer: list[dict[str, str]] = data_handler.get_answer_by_id(answer_id)
    if request.method == "POST":
        message: Union[str, None] = request.form.get("message")
        file: Any = request.files['file']
        file_path: Union[str, None] = save_image(file)
        data_handler.edit_answer(question_id, message, file_path)
        return redirect("/question/"+question_id)
    return render_template('pages/answer.html', answer=answer[0],
    session_user=session_user,
    logged_in=logged_in)


@app.route("/question/<question_id>/answer/<answer_id>/delete_answer",
            methods=["POST"])
def delete_answer(question_id, answer_id) -> Response:
    """Specific answer delete route."""
    data_handler.delete_answer(answer_id)
    return redirect("/question/" + question_id)


@app.route("/question/<question_id>/answer/<int:answer_id>/vote-up",
            methods=['POST'])
def vote_answer_up(question_id, answer_id) -> Response:
    """Answer upvoting route."""
    data_handler.vote_answer_up(answer_id)
    return redirect("/question/" + question_id)


@app.route("/question/<question_id>/answer/<int:answer_id>/vote-down",
            methods=['POST'])
def vote_answer_down(question_id, answer_id) -> Response:
    """Answer downvoting route."""
    data_handler.vote_answer_down(answer_id)
    return redirect("/question/" + question_id)


@app.route("/registration",
            methods=['POST'])
def registration_form():
    if request.method == 'POST':
        username = request.form.get('usernameValidation')
        password = request.form.get('validationPassword')
        email = request.form.get('email-validation')
        fname = request.form.get('firstNameValidation')
        lname = request.form.get('lastNameValidation')
        if data_handler.check_exisiting_username(username) == True:
            return 'Username already in use!'
        elif data_handler.check_exisiting_email(email) == True:
            return 'Email already in use!'
        elif not username or not password or not email or not fname or not lname:
            return 'Please fill out the form!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            return 'Username must contain only characters and numbers!'
        elif not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*_=+-]).{8,}$', password):
            return 'Invalid password'
        else:
            hashed_password = data_handler.hash_password(password)
            registrationDate = data_handler.time_now()
            data_handler.register_new_user(username, hashed_password, email, fname, lname, registrationDate)
            return render_template('pages/success.html')
    return redirect('/')


@app.route('/question/<question_id>/accept_answer/<int:answer_id>',
           methods=['POST'])
def accept_answer(question_id, answer_id):
    data_handler.accept_answer_by_id(answer_id)
    return redirect('/question/'+ question_id)

    

@app.route("/all_tags")
def search_through_tags():
    """showing all tags to search through them"""
    session_user = data_handler.get_id_by_username(session.get('user', default=''))
    logged_in = session.get('logged_in', default=False)
    tags = data_handler.get_tags()
    tags_names = []
    for info in tags:
        tags_names.append(info['name'])
    return render_template("/pages/tags_page.html/", tags_names=tags_names,
    session_user=session_user,
    logged_in=logged_in)


@app.route("/question/<question_id>/new-comment",
            methods=["GET", "POST"])
def new_question_comment(question_id) -> None:
    """Add comment to a question route."""
    session_user = data_handler.get_id_by_username(session.get('user', default=''))
    logged_in = session.get('logged_in', default=False)
    if request.method == "POST":
        message: Union[str, None] = request.form.get("message")
        data_handler.add_comment_to_question(question_id, message)
        return redirect("/question/"+question_id)
    return render_template('pages/comment.html',
    session_user=session_user,
    logged_in=logged_in)


@app.route("/question/<question_id>/answer/<answer_id>/new-comment",
            methods=["GET", "POST"])
def new_answer_comment(question_id, answer_id) -> None:
    """Add comment to an answer route."""
    session_user = data_handler.get_id_by_username(session.get('user', default=''))
    logged_in = session.get('logged_in', default=False)
    if request.method == "POST":
        message: Union[str, None] = request.form.get("message")
        data_handler.add_comment_to_answer(answer_id, message)
        return redirect("/question/"+question_id)
    return render_template('pages/comment.html',
    session_user=session_user,
    logged_in=logged_in)


@app.route("/question/<question_id>/comment/<comment_id>/edit-comment",
            methods=["GET", "POST"])
def edit_question_comment(question_id, comment_id) -> None:
    """Edit comment to a question route."""
    session_user = data_handler.get_id_by_username(session.get('user', default=''))
    logged_in = session.get('logged_in', default=False)
    comment: list[dict[str, str]] = data_handler.get_comment_by_id(comment_id)
    if request.method == "POST":
        message: Union[str, None] = request.form.get("message")
        data_handler.edit_comment(comment_id, message)
        return redirect("/question/"+question_id)
    return render_template('pages/comment.html', comment=comment[0],
    session_user=session_user,
    logged_in=logged_in)


@app.route("/question/<question_id>/answer/<answer_id>/comment/<comment_id>/edit-comment",
            methods=["GET", "POST"])
def edit_answer_comment(question_id, answer_id, comment_id) -> None:
    """Edit comment to an answer route."""
    session_user = data_handler.get_id_by_username(session.get('user', default=''))
    logged_in = session.get('logged_in', default=False)
    comment: list[dict[str, str]] = data_handler.get_comment_by_id(comment_id)
    if request.method == "POST":
        message: Union[str, None] = request.form.get("message")
        data_handler.edit_comment(comment_id, message)
        return redirect("/question/"+question_id)
    return render_template('pages/comment.html', comment=comment[0],
    session_user=session_user,
    logged_in=logged_in)


@app.route("/question/<question_id>/comment/<comment_id>/delete-comment",
            methods=["POST"])
def delete_comment(question_id, comment_id) -> None:
    """Delete specific comment route."""
    data_handler.delete_comment(comment_id)
    return redirect("/question/" + question_id)


@app.route("/search",
            methods=["POST"])
def search() -> Response:
    """Search database records route."""
    phrase: str = request.form.get("search")
    records: Union[str, None] = data_handler.search_for_question(phrase)
    return records


@app.route("/tag_page/<tag>")
def tag_page(tag):
    """show list of questions with specific tag"""
    session_user = data_handler.get_id_by_username(session.get('user', default=''))
    logged_in = session.get('logged_in', default=False)
    questions: list[dict[str, str]] = data_handler.get_tagged_questions(tag)
    comment_count: dict[str, str] = data_handler.get_answer_count()
    return render_template("/pages/tag_page.html/",
                            tag=tag,
                            questions=questions,
                            time_passed=data_handler.how_much_time_passed,
                            comment_count=comment_count,
                            to_string=str,
                            session_user=session_user,
                            logged_in=logged_in)


@app.route("/new_tag", methods=['GET', 'POST'])
def new_tag() -> Union[Response, str]:
    """Adding new tag route."""
    session_user = data_handler.get_id_by_username(session.get('user', default=''))
    logged_in = session.get('logged_in', default=False)
    if request.method == "POST":
        tag: Union[str, None] = request.form.get("tag")
        data_handler.add_tag_to_database(tag)
        return redirect("/")
    return render_template('pages/new_tag.html',
    session_user=session_user,
    logged_in=logged_in)


@app.route("/users")
def display_users():
    """Display existing users route."""
    session_user = data_handler.get_id_by_username(session.get('user', default=''))
    logged_in = session.get('logged_in', default=False)
    users = data_handler.get_all_user_stats()
    reputations = []
    for user in users:
        reputations.append(data_handler.get_user_reputation(user['id']))
    return render_template('pages/users.html',
                            users=users,
                            reps=reputations,
                            session_user=session_user,
                            logged_in=logged_in)


@app.route("/user/<user_id>")
def profile_page(user_id):
    """Display user profile route."""
    session_user = data_handler.get_id_by_username(session.get('user', default=''))
    logged_in = session.get('logged_in', default=False)
    user = data_handler.get_user_by_id(user_id)
    reputation = data_handler.get_user_reputation(user_id)
    return render_template("pages/user_profile.html",
                            user=user,
                            rep=reputation,
                            session_user=session_user,
                            logged_in=logged_in)


@app.route('/login',
            methods=['POST', 'GET'])
def page_login():
    correct_user = False
    if request.method == 'POST':
        login = request.form.get("username")
        password = request.form.get("password")
        correct_user = data_handler.check_credentials(login, password)
        if correct_user:
            session.clear()
            session['logged_in'] = True
            session['user'] = login if login else ''
            return redirect('/')
        return abort(401)
    return abort(403)


@app.route('/logout')
def user_logout():
    session.clear()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
