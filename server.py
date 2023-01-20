"""AskMate server route management."""
from flask import Flask, render_template, request, redirect
import data_handler
from datetime import datetime

app = Flask(__name__, static_url_path='/static')

HEADERS_QUESTION = data_handler.HEADERS_QUESTION
HEADERS_ANSWER = data_handler.HEADERS_ANSWER

@app.route("/")
@app.route("/list", methods=['GET'])
def hello():
    """Main page route."""
    questions = data_handler.get_data('question')
    answers = data_handler.get_data('answer')
    comment_count = data_handler.count_comments()
    sort_by, order = (request.args.get('order_by'),
                    request.args.get('order_direction'))
    order = 'DESC' if order == 'descending' else 'ASC'
    if sort_by:
        questions = data_handler.get_data('question',
                                        sort_by, order)
    return render_template('index.html', headers_question=HEADERS_QUESTION,
                           headers_answer=HEADERS_ANSWER,
                           questions=questions,
                           time_passed=data_handler.how_much_time_passed,
                           comment_count=comment_count)


@app.route("/question/<question_id>/")
def display_question(question_id):
    
    answers = data_handler.get_data('answer')
    question_to_send = data_handler.get_question_by_id(
        question_id)
    answers_send_list = []
    for answer in answers:
        if answer['question_id'] == int(question_id):
            answers_send_list.append(answer)
    return render_template(
        'display_question.html',
        question=question_to_send,
        answers=answers_send_list,
        count_answers=len(answers_send_list))


@app.route("/question/<question_id>/delete", methods=["POST"])
def delete_question(question_id):
    data_handler.delete_data(mode = 'question', 
                             given_question_id = question_id)
    return redirect("/list")

@app.route("/question/<question_id>/<aid>/delete_answer", methods=["POST"])
def delete_answer(question_id, aid):
    data_handler.delete_data(mode='answer', 
                            answer_id =aid)
    return redirect("/question/" + question_id)


@app.route("/question/<question_id>/new-answer", methods=['POST', 'GET'])
def new_answer(question_id):
    # The page has a POST form with a form field called message
    # Posting an answer redirects to the question detail page
    if request.method == "POST":
        message = request.form.get("message")
        data_handler.add_data_to_file(question_id=question_id,
                                      mode='answer',
                                      message=message)
        return redirect("/question/"+question_id)
    return render_template('new_answer.html')


@app.route('/add_question', methods=['GET', 'POST'])
def add_new_question():
    if request.method == "GET":
        return render_template('/add_question.html')
    else:
        message = request.form.get("question")
        title = request.form.get("title")
        data_handler.add_data_to_file(mode='question',
                                      message=message,
                                      title=title)
        return redirect('/list')


@app.route("/question/<question_id>/edit", methods=['POST','GET'])
def edit_question(question_id):
    question = data_handler.get_question_by_id(question_id)

    if request.method == 'POST':
        question['title'] = request.form.get("title")
        question['message'] = request.form.get("msg")
        data_handler.delete_question_from_file_by_id('sample_data/question.csv',
                                                     question_id)
        data_handler.write_data_to_file(HEADERS_QUESTION,
                                        data_handler.QUESTION_PATH,
                                        question)
        return redirect('/question/'+question_id)

    return render_template('edit_question.html',
                        question=question)


@app.route("/question/<question_id>/vote-up", methods=['POST'])
def vote_question_up(question_id):
    data_handler.voting_questions(question_id, 'up')
    return redirect("/list")


@app.route("/question/<question_id>/vote-down", methods=['POST'])
def vote_question_down(question_id):
    data_handler.voting_questions(question_id, 'down')
    return redirect("/list")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
