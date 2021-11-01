from flask import Flask, render_template, request, url_for, redirect,session
import data_handler

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def display_latest_five_questions():
    latest_five_questions = data_handler.questions_model.display_latest_five_questions()
    search_phrase = request.args.get("search_phrase")

    if search_phrase:
        search_results = data_handler.search_in_questions_and_answers(search_phrase)
        return render_template("index.html", search_results=search_results)

    return render_template("index.html", latest_five_questions=latest_five_questions)




if __name__ == "__main__":
    app.run(
    host="127.0.0.1",
    port=8000,
    debug=True
)
