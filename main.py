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


@app.route('/question/<int:question_id>/delete')
def delete_question(question_id):
    question_user_id = data_handler.users_model.get_username_by_question_id(question_id)

    if "username" in session and session["username"] == question_user_id:
        data_handler.questions_model.delete_question_by_id(question_id)
        return redirect(url_for('display_questions'))
    return render_template("not-allowed.html")


@app.route('/question/<int:question_id>/edit', methods=["GET","POST"])
def edit_question(question_id):
    question_user_id = data_handler.users_model.get_username_by_question_id(question_id)
  
    if "username" in session and session["username"] == question_user_id:

        if request.method == "POST":
            form_input = dict(request.form)
            updated_question_title = form_input["updated_question_title"]
            updated_question_message = form_input["updated_question_message"]

            data_handler.questions_model.edit_question_by_id(question_id, updated_question_title, updated_question_message)

            return redirect (url_for ('display_question_by_id',question_id=question_id))

        question_details = data_handler.questions_model.display_question_by_id(question_id)
        
        return render_template(
            'question/edit-question.html', 
            question_details=question_details)

    return render_template("not-allowed.html")


@app.route('/question/<int:question_id>/new-answer', methods=["GET","POST"])
def add_new_answer(question_id):
    question_user_id = data_handler.users_model.get_username_by_question_id(question_id)

    if "username" in session and session["username"] == question_user_id:
        user_id = data_handler.users_model.get_id_for_user(session['username'])
        
        if request.method == "POST":
            form_input = dict(request.form)
            new_answer_message = form_input["answer_message"]

            data_handler.answers_model.add_new_answer(question_id, new_answer_message, user_id)

            return redirect(url_for(
                'display_question_by_id', 
                question_id=question_id))

        return render_template(
            'answer/add-answer.html', 
            question_id=question_id)

    return "In order to add a new question, you have to be logged in"


@app.route('/answer/<int:answer_id>/edit', methods=["GET","POST"])
def edit_answer(answer_id):
    answer_user_id = data_handler.users_model.get_username_by_answer_id(answer_id)

    if "username" in session and session["username"] == answer_user_id:
        answer_details = data_handler.answers_model.display_answer_by_id(answer_id)
        
        for answer in answer_details:
            answer_id = answer["id"]
            answer_message = answer["message"]

        if request.method == "POST":
            form_input = dict(request.form)
            updated_answer_message = form_input["updated_answer_message"]

            data_handler.answers_model.edit_answers_by_id(answer_id, updated_answer_message)
            question_id = data_handler.answers_model.get_question_id_from_answer(answer_id)

            return redirect(url_for("display_question_by_id", question_id=question_id))

        return render_template(
                "answer/edit-answer.html",
                answer_id=answer_id,
                answer_message=answer_message)

    return render_template("not-allowed.html")


@app.route('/answer/<int:answer_id>/delete')
def delete_answer(answer_id):
    answer_user_id = data_handler.users_model.get_username_by_answer_id(answer_id)

    if "username" in session and session["username"] == answer_user_id:
        question_id = data_handler.questions_model.get_question_id_from_answer(answer_id)
        data_handler.answers_model.delete_answer_by_id(answer_id)

        return redirect(url_for("display_question_by_id", question_id=question_id))
    return render_template("not-allowed.html")



@app.route('/question/<int:question_id>/add-comment', methods=["GET","POST"])
def add_comment_to_question(question_id):
    if "username" in session:
        user_id = data_handler.users_model.get_id_for_user(session['username'])

        if request.method == "POST":
            form_input = dict(request.form)
            question_comment = form_input["comment_message"]

            data_handler.comments_model.add_comment_to_question(question_id,question_comment,user_id)
            
            return redirect(url_for("display_question_by_id", question_id=question_id))

        return render_template("comment/add-comment.html")


@app.route('/answer/<int:answer_id>/add-comment', methods=["GET","POST"])
def add_comment_to_answer(answer_id):
    if "username" in session:
        user_id = data_handler.users_model.get_id_for_user(session['username'])

        if request.method == "POST":
            form_input = dict(request.form)
            answer_comment = form_input["comment_message"]

            data_handler.comments_model.add_comment_to_answer(answer_id, answer_comment, user_id)
            question_id = data_handler.answers_model.get_question_id_from_answer(answer_id)

            return redirect(url_for(
                    "display_question_by_id", 
                    question_id=question_id))
        return render_template("comment/add-comment.html")



@app.route('/users')
def display_users():
    if "username" in session:
        user_list = data_handler.users_model.display_users()


        return render_template(
            "users/users.html", 
            user_list = user_list)


@app.route('/users/<int:user_id>')
def display_user_details(user_id):
    if "username" in session:
        user_questions = data_handler.users_model.get_user_questions(user_id)
        user_questions_count = data_handler.users_model.user_questions_count(user_id)

        user_answers = data_handler.users_model.get_user_answers(user_id)
        user_answers_count = data_handler.users_model.user_answers_count(user_id)

        user_info = data_handler.users_model.get_user_info(user_id)

        return render_template(
            "users/user-details.html",
            user_questions=user_questions,
            user_answers=user_answers,
            user_info=user_info,
            user_questions_count=user_questions_count,
            user_answers_count=user_answers_count)


@app.route('/question/<int:question_id>/upvote', methods=["GET"])
def upvoteQuestion(question_id):
    
    if "username" in session:
        

        currentUserId = data_handler.users_model.get_id_for_user(session['username'])
        currentVote = data_handler.getVoteType("voted_questions",question_id,currentUserId)
        targetUserId = data_handler.getTargetUserId("question",question_id)

        if currentVote == 0:
            data_handler.questions_model.modifyVote("question",question_id,1)
            data_handler.users_model.modifyReputation(targetUserId,5)
            data_handler.addTopicResponseRecord("voted_questions",targetUserId,question_id,1)
        elif currentVote == -1:
            data_handler.questions_model.modifyVote("question",question_id,1)
            data_handler.users_model.modifyReputation(targetUserId,5)
            data_handler.addTopicResponseRecord("voted_questions",targetUserId,question_id,1)

        
    return redirect(f"/question/{question_id}")


@app.route('/answer/<int:answer_id>/upvote', methods=["GET"])
def upvoteAnswer(answer_id):
    question_id = data_handler.answers_model.get_question_id_from_answer(answer_id)
    if "username" in session:
        currentUserId = data_handler.users_model.get_id_for_user(session['username'])
        currentVote = data_handler.getVoteType("voted_answers",answer_id,currentUserId)
        targetUserId = data_handler.getTargetUserId("answer",answer_id)

        if currentVote == 0:
            data_handler.answers_model.modifyVote("answer",answer_id,1)
            data_handler.users_model.modifyReputation(currentUserId,2)
            data_handler.addTopicResponseRecord("voted_answers",targetUserId,answer_id,1)
            
        elif currentVote == -1:
            data_handler.answers_model.modifyVote("answer",answer_id,1)
            data_handler.users_model.modifyReputation(currentUserId,2)
            data_handler.addTopicResponseRecord("voted_answers",targetUserId,answer_id,1)
        
        
    return redirect(f"/question/{question_id}")


@app.route('/answer/<int:answer_id>/downvote', methods=["GET"])
def downvoteAnswer(answer_id):
    question_id = data_handler.answers_model.get_question_id_from_answer(answer_id)
    if "username" in session:
        currentUserId = data_handler.users_model.get_id_for_user(session['username'])
        currentVote = data_handler.getVoteType("voted_answers",answer_id,currentUserId)
        targetUserId = data_handler.getTargetUserId("answer",answer_id)

        if currentVote == 1:
            data_handler.questions_model.modifyVote("answer",answer_id,-1)
            data_handler.users_model.modifyReputation(targetUserId,2)
            data_handler.addTopicResponseRecord("voted_answers",targetUserId,answer_id,-1)
        elif currentVote == 0:
            data_handler.questions_model.modifyVote("answer",answer_id,-1)
            data_handler.users_model.modifyReputation(targetUserId,-2)
            data_handler.addTopicResponseRecord("voted_answers",targetUserId,answer_id,-1)
          
    return redirect(f"/question/{question_id}")


@app.route('/question/<int:question_id>/downvote', methods=["GET"])
def downvoteQuestion(question_id):
    if "username" in session:
        currentUserId = data_handler.users_model.get_id_for_user(session['username'])
        currentVote = data_handler.getVoteType("voted_questions",question_id,currentUserId)
        targetUserId = data_handler.getTargetUserId("question",question_id)

        if currentVote == 1:
            data_handler.questions_model.modifyVote("question",question_id,-1)
            data_handler.users_model.modifyReputation(targetUserId,-2)
            data_handler.addTopicResponseRecord("voted_questions",targetUserId,question_id,-1)
        elif currentVote == 0:
            data_handler.questions_model.modifyVote("question",question_id,-1)
            data_handler.users_model.modifyReputation(targetUserId,-2)
            data_handler.addTopicResponseRecord("voted_questions",targetUserId,question_id,-1)

        
    return redirect(f"/question/{question_id}")


if __name__ == "__main__":
    app.run(
    host="127.0.0.1",
    port=8000,
    debug=True
)
