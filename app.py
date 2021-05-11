from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES_KEY = "responses"
app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route("/")
def select_survey():
    """select survey"""

    return render_template("start_page.html", survey=survey)


@app.route("/begin", methods=["POST"])
def start_survey():
    """
    Clear response list
    Redirect to questions
    """

    session[RESPONSES_KEY] = []

    return redirect("/questions/0")


@app.route("/answer", methods=["POST"])
def handle_question():
    """
    append to response list
    redirect to next question or end
    """

    # get response
    choice = request.form['answer']

    # append to reponse list
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    # after each question, check if survey completed
    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/questions/<int:qid>")
def display_question(qid):
    """Display question"""
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        # no responses, redirect
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        # survey complete, redirect to complete
        return redirect("/complete")

    if (len(responses) != qid):
        # question skipped, redirect to correct question
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template(
        "question.html", question_num=qid, question=question)


@app.route("/complete")
def survey_complete():
    """ if survey  is complete, display thank you."""

    return render_template("survey_complete.html")
