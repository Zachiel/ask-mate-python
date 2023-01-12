"""AskMate server route management."""
from flask import Flask, render_template, request
import data_handler

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


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
