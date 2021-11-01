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


@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "POST":
        form_input = dict(request.form)
        username = form_input["username"]
        password = data_handler.hash_password(form_input["password"])
        

        data_handler.register_user(username, password)
        
        return redirect(url_for("display_questions"))

    return render_template("register.html")


@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        session["username"] = request.form["username"]
        password = request.form["password"]

        check_login = data_handler.check_login(session["username"], password)

        if check_login is True:
            return redirect(url_for("display_questions"))
        return render_template("login.html", check_login=check_login)
    
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("display_questions"))
    

@app.route('/list')
def display_questions():
    questions = data_handler.questions_model.display_questions()

    sort_by = request.args.get("sort_by")
    sort_order = request.args.get("sort_order")

    if sort_by or sort_order:
        sorted_questions = data_handler.questions_model.sort_questions(sort_by, sort_order)

        return render_template(
            'question/list-questions.html',
            sorted_questions=sorted_questions)

    if "username" in session:
        return render_template("question/list-questions.html", questions=questions)

    return render_template(
        'question/list-questions.html', 
        questions=questions)


@app.route('/question/<int:question_id>/', methods=["GET","POST"])
def display_question_by_id(question_id):
    questions = data_handler.questions_model.display_question_by_id(question_id)
    answers_by_question_id = data_handler.answers_model.display_answers_by_question_id(question_id)
 
    comments_for_questions = data_handler.comments_model.display_comments_by_question_id(question_id)

    question_posted_by = data_handler.users_model.get_username_by_question_id(question_id)

    questionVoteNumber = data_handler.questions_model.getVotes(question_id)


    return render_template(
        "question/question.html", 
        questions=questions,
        question_posted_by=question_posted_by,
        answers_by_question_id=answers_by_question_id,
        comments_for_questions=comments_for_questions)

@app.route('/add-question', methods=["GET","POST"])
def add_new_question():

    if "username" in session:
        user_id = data_handler.users_model.get_id_for_user(session['username'])

        if request.method == "POST":
            form_input = dict(request.form)
            new_question_title = form_input["question_title"]
            new_question_message = form_input["question_message"]
            new_question_id = int(data_handler.get_future_question_id()) + 1

            data_handler.questions_model.add_new_question(new_question_title, new_question_message, user_id)
            return redirect(url_for("display_question_by_id", question_id=new_question_id))

        return render_template('question/add-question.html')

    return "In order to add a new question, you have to be logged in"





if __name__ == "__main__":
    app.run(
    host="127.0.0.1",
    port=8000,
    debug=True
)
