"""AskMate server route management."""
from flask import Flask, render_template
import data_handler

app = Flask(__name__, static_url_path='/static')


@app.route("/")
@app.route("/list")
def hello():
    """Main page route."""
    questions = data_handler.get_data_from_file('sample_data/question.csv')
    headers_question = data_handler.HEADERS_QUESTION
    headers_answer = data_handler.HEADERS_ANSWER
    return render_template('index.html', headers_question=headers_question,
                           headers_answer=headers_answer,
                           questions=questions)

@app.route("/question/<question_id>")
def question(question_id):
    return 'hello'


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
