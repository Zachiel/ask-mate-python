"""AskMate server route management."""
# pylint: disable=no-value-for-parameter, no-member
# pyright: reportGeneralTypeIssues=false
from typing import Union
from flask import Flask, render_template, request, redirect, Response
import data_handler

app: Flask = Flask(__name__, static_url_path='/static')

HEADERS_QUESTION: list[str] = data_handler.HEADERS_QUESTION
HEADERS_ANSWER: list[str] = data_handler.HEADERS_ANSWER


@app.route("/")
def hello() -> str:
    """Main page route."""
    questions: list[dict[str, str]] = data_handler.get_latest_questions()
    comment_count: dict[str, str] = data_handler.count_comments()
    return render_template('pages/index.html',
                            headers_question=HEADERS_QUESTION,
                            headers_answer=HEADERS_ANSWER,
                            questions=questions,
                            time_passed=data_handler.how_much_time_passed,
                            comment_count=comment_count)


@app.route("/list")
def list_questions() -> str:
    """Main page route."""
    questions: list[dict[str, str]] = data_handler.get_sorted_questions()
    comment_count: dict[str, str] = data_handler.count_comments()
    sort_by: Union[str, None] = request.args.get('order_direction')
    order: Union[str, None] = ('DESC'
                                if request.args.get('order_by') == 'descending'
                                else 'ASC')
    if sort_by:
        questions: list[dict[str, str]] = data_handler.get_sorted_questions(
                                            sort_by, order)
    return render_template('pages/index.html',
                            headers_question=HEADERS_QUESTION,
                            headers_answer=HEADERS_ANSWER,
                            questions=questions,
                            time_passed=data_handler.how_much_time_passed,
                            comment_count=comment_count)



@app.route("/question/<question_id>")
def display_question(question_id) -> str:
    """Specific question page route."""
    question: list[dict[str, str]] = data_handler.get_question_by_id(
                                                                    question_id)
    answers: list[dict[str, str]] = data_handler.get_answers_for_question(
                                                                    question_id)
    return render_template('pages/display_question.html',
                            question=question,
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
        data_handler.add_answer_to_database(question_id=question_id,
                                            message=message)
        return redirect("/question/"+question_id)
    return render_template('pages/new_answer.html')


@app.route('/add_question', methods=['GET', 'POST'])
def new_question() -> Union[Response, str]:
    """Adding new question route."""
    if request.method == "POST":
        message: Union[str, None] = request.form.get("question")
        title: Union[str, None] = request.form.get("title")
        data_handler.add_data_to_file(mode='question',
                                        message=message,
                                        title=title)
        return redirect('/list')
    return render_template('pages/add_question.html')


@app.route("/question/<question_id>/edit", methods=['POST','GET'])
def edit_question(question_id) -> Union[Response, str]:
    """Editing specific question route."""
    question: list[dict[str, str]] = data_handler.get_question_by_id(
                                                            question_id)
    if request.method == 'POST':
        new_title: Union[str, None] = request.form.get("title")
        new_message: Union[str, None] = request.form.get("message")
        data_handler.edit_question(mode='question',
                                    title = new_title,
                                    message = new_message,
                                    given_question_id=question_id)
        return redirect('/question/'+question_id)
    return render_template('pages/edit_question.html',
                        question=question)


@app.route("/question/<question_id>/vote-up", methods=['POST'])
def vote_question_up(question_id) -> Response:
    """Question upvoting route."""
    data_handler.voting_questions(question_id, 'up')
    return redirect("/list")


@app.route("/question/<question_id>/vote-down", methods=['POST'])
def vote_question_down(question_id) -> Response:
    """Question downvoting route."""
    data_handler.voting_questions(question_id, 'down')
    return redirect("/list")


@app.route("/question/<question_id>/answer/<int:answer_id>/vote-up",
            methods=['POST'])
def vote_answer_up(question_id, answer_id) -> Response:
    """Answer upvoting route."""
    data_handler.voting_answer(answer_id, mode='up')
    return redirect("/question/" + question_id)


@app.route("/question/<question_id>/answer/<int:answer_id>/vote-down",
            methods=['POST'])
def vote_answer_down(question_id, answer_id) -> Response:
    """Answer downvoting route."""
    data_handler.voting_answer(answer_id, mode='down')
    return redirect("/question/" + question_id)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
