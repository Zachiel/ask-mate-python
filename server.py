"""AskMate server route management."""
from flask import Flask, render_template
import data_handler

app = Flask(__name__, static_url_path='/static')


@app.route("/")
def hello():
    """Main page route."""
    headers_question = data_handler.HEADERS_QUESTION
    headers_answer = data_handler.HEADERS_ANSWER
    return render_template('index.html', headers_question=headers_question,
                           headers_answer=headers_answer)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
