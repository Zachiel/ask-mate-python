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
    questions = data_handler.get_data_from_file(
        'sample_data/question.csv')
    questions = data_handler.sorter(questions)
    answers = data_handler.get_data_from_file(
        'sample_data/answer.csv')
    comment_count = data_handler.count_comments()
    sort_by, order = (request.args.get('order_by'),
                    request.args.get('order_direction'))
    if sort_by:
        questions = data_handler.sorter(questions,
                                        sort_by, order)
    return render_template('index.html', headers_question=HEADERS_QUESTION,
                           headers_answer=HEADERS_ANSWER,
                           questions=questions,
                           time_passed=data_handler.how_much_time_passed,
                           comment_count=comment_count)

@app.route("/question/<question_id>/")
def question(question_id):
    questions = data_handler.get_data_from_file(
        'sample_data/question.csv')
    answers = data_handler.get_data_from_file(
        'sample_data/answer.csv')
    question_send = ''
    answers_send_list = []
    for question in questions:
        if question['id'] == question_id:
            question_send = question
            break
        else:
            continue
    for answer in answers:
        if answer['question_id'] == question_id:
            answers_send_list.append(answer)
    return render_template('display_question.html', question=question_send, answers=answers_send_list)

@app.route("/question/<question_id>/delete", methods=["POST"])
def delete_question(question_id):
    data_handler.delete_question_from_file_by_id(
        'sample_data/question.csv', question_id)
    data_handler.delete_answers_for_question_id(
        'sample_data/answer.csv', question_id)
    return redirect("/list")

@app.route("/question/<question_id>/new-answer", methods=['POST', 'GET'])
def new_answer(question_id):
    # The page has a POST form with a form field called message
    # Posting an answer redirects to the question detail page
    if request.method == "POST":
        new_answer = {}
        new_answer['id'] = data_handler.generate_id()
        
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        without_ms = int(timestamp)
        new_answer['submission_time'] = without_ms
        
        new_answer['vote_number'] = '0'
        new_answer['question_id'] = question_id
        new_answer['message'] = request.form.get("message")
        
        data_handler.write_data_to_file(HEADERS_ANSWER, data_handler.ANSWER_PATH, new_answer)
        return redirect("/question/"+question_id)
    return render_template('new_answer.html')

@app.route('/add_question', methods=['GET', 'POST'])
def add_new_question():
    if request.method == "GET":
        return render_template('/add_question.html')
    else:
        new_question = {}

        new_question['id'] = data_handler.generate_id()
        new_question['submission_time'] = data_handler.time_now()
        new_question['view_number'] = '0'
        new_question['vote_number'] = '0'
        new_question['title'] = request.form.get("title")
        new_question['message'] = request.form.get("question")

        data_handler.write_data_to_file(data_handler.HEADERS_QUESTION, data_handler.QUESTION_PATH, new_question)
        return redirect('/list')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
