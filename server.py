"""AskMate server route management."""
# pylint: disable=no-value-for-parameter, no-member
# pyright: reportGeneralTypeIssues=false
import os
import sys
from typing import Union, Any
import uuid
from flask import Flask, render_template, request, redirect, Response
import data_handler
import re
import hashing

UPLOAD_FOLDER: str = 'static/uploads'

app: Flask = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1 * 1000 * 1000


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
    questions: list[dict[str, str]] = data_handler.get_latest_questions()
    comment_count: dict[str, str] = data_handler.get_comment_count()
    #print(questions, file=sys.stderr)
    return render_template('pages/index.html',
                            questions=questions,
                            time_passed=data_handler.how_much_time_passed,
                            comment_count=comment_count,
                            to_string=str)


@app.route("/list")
def list_questions() -> str:
    """Main page route."""
    questions: list[dict[str, str]] = data_handler.get_sorted_questions()
    comment_count: dict[str, str] = data_handler.get_comment_count()
    sort_by: Union[str, None] = request.args.get('order_by')
    order: Union[str, None] = request.args.get('order_direction')
    if sort_by:
        questions: list[dict[str, str]] = data_handler.get_sorted_questions(
                                            sort_by, order)
    return render_template('pages/index.html',
                            questions=questions,
                            time_passed=data_handler.how_much_time_passed,
                            comment_count=comment_count,
                            to_string=str)


@app.route("/question/<question_id>/")
def display_question(question_id) -> str:
    """Specific question page route."""
    data_handler.increase_view_count(question_id)
    question: list[dict[str, str]] = data_handler.get_question_by_id(
                                                                    question_id)
    answers: list[dict[str, str]] = data_handler.get_answers_for_question(
                                                                    question_id)
    return render_template('pages/display_question.html',
                            question=question[0],
                            answers=answers,
                            count_answers=len(answers))


@app.route("/question/<question_id>/delete", methods=["POST"])
def delete_question(question_id) -> Response:
    """Specific question delete route."""
    data_handler.delete_question(question_id)
    return redirect("/list")


@app.route("/question/<question_id>/<answer_id>/delete_answer",
            methods=["POST"])
def delete_answer(question_id, answer_id) -> Response:
    """Specific answer delete route."""
    data_handler.delete_answer(answer_id)
    return redirect("/question/" + question_id)


@app.route("/question/<question_id>/new-answer", methods=['GET', 'POST'])
def new_answer(question_id) -> Union[Response, str]:
    """Adding new answer route."""
    if request.method == "POST":
        message: Union[str, None] = request.form.get("message")
        data_handler.add_answer_to_database(question_id, message)
        return redirect("/question/"+question_id)
    return render_template('pages/new_answer.html')


@app.route('/add_question', methods=['GET', 'POST'])
def new_question() -> Union[Response, str]:
    """Adding new question route."""
    if request.method == "POST":
        message: Union[str, None] = request.form.get("question")
        title: Union[str, None] = request.form.get("title")
        file: Any = request.files['file']
        file_path: Union[str, None] = save_image(file)
        data_handler.add_question_to_database(title, message, file_path)
        return redirect('/list')
    return render_template('pages/add_question.html')


@app.route("/question/<question_id>/edit", methods=['POST','GET'])
def edit_question(question_id) -> Union[Response, str]:
    """Editing specific question route."""
    question: list[dict[str, str]] = data_handler.get_question_by_id(
                                                            question_id)
    if request.method == 'POST':
        title: Union[str, None] = request.form.get("title")
        message: Union[str, None] = request.form.get("message")
        file: Any = request.files['file']
        file_path: Union[str, None] = save_image(file)
        data_handler.edit_question(question_id, title, message, file_path)
        return redirect('/question/'+question_id)
    return render_template('pages/edit_question.html',
                        question=question[0])


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

#TODO change prints for messages on site f.e alerts or just plain text
@app.route("/registration",
           methods=['POST', 'GET'])
def registration_form():
    if (request.method == 'POST' 
        and 'username' in request.form 
        and 'password' in request.form):
        username = request.form.get('username')
        password = request.form.get('password')
        if data_handler.check_exisiting_username(username) == True:
            print('Account already exists!')
        elif not re.match(r'[A-Za-z0-9]+', username):
            print('Username must contain only characters and numbers!')
            
        #TODO checking if username and password is empty is not working
        elif not username or not password:
            print('Please fill out the form!')
        else:
            hashed_password = hashing.hash_password(password)
            data_handler.register_new_user(username, hashed_password)
            print('You have succesfully registered!')
            return redirect('/list')
    elif request.method == 'POST':
        print('Please fill out the form!')
        
    return render_template('pages/registration.html')
        


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
