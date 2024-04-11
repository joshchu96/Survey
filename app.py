from flask import Flask,render_template, redirect, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey 

app= Flask(__name__) #flask can find this file
app.config['SECRET_KEY']= "very_secret_key"

#create the debugger toolbar
toolbar= DebugToolbarExtension(app)
responses =[]


@app.route("/")
def show_survey_intro():
    return render_template('start.html', survey=satisfaction_survey)

@app.route("/begin-survey", methods=["POST"])
def begin_survey():
    return redirect("/questions/0")

@app.route("/questions/<int:qindex>")
def show_question(qindex):

    if (responses) is None:
        return redirect("/")

    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/finished')
    
    if len(responses) != qindex:
        flash(f"This is not the right question number you should be on {qindex}")

    question = satisfaction_survey.questions[qindex]
    return render_template("questions.html", q_num = qindex, question=question)



@app.route("/answers", methods=["POST"])
def handle_answers():
   
    choice = request.form['answer']
    #add choice to the list for responses
    responses.append(choice)

    return redirect(f"/questions/{len(responses)}")

@app.route('/finished')
def done():

    return render_template("finished.html")