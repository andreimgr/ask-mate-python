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




if __name__ == "__main__":
    app.run(
    host="127.0.0.1",
    port=8000,
    debug=True
)
