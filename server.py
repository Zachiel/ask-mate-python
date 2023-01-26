"""AskMate server route management."""
# pylint: disable=no-value-for-parameter, no-member
# pyright: reportGeneralTypeIssues=false
import sys
from typing import Union
from flask import Flask, render_template, request, redirect, Response
import data_handler

app: Flask = Flask(__name__, static_url_path='/static')


@app.route("/")
def hello() -> str:
    """Main page route."""
    questions: list[dict[str, str]] = data_handler.get_latest_questions()
    comment_count: dict[str, str] = data_handler.get_comment_count()
    print(questions, file=sys.stderr)
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
        data_handler.add_question_to_database(message=message,
                                            title=title)
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
        data_handler.edit_question(question_id, title, message)
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


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
