
from flask import Flask, url_for, render_template, request, flash
import home, submitQuestion, answerQuestions


app = Flask(__name__)


# ======================= HOME PAGE =============================
@app.route('/')
def index():
	return render_template('index.html', questions=home.getQuestions())


# ======================= SUBMIT PAGE =============================
@app.route('/submit', methods=['GET', 'POST'])
def submit():
	if request.method == 'POST': 
		ques = request.form['question']
		ques = ques.replace('\n', '<br />')
		submitQuestion.addQuestion(ques)
		return render_template('submitQuestion.html', success="Thank you! Your question has been submitted successfully.")
	return render_template('submitQuestion.html')


# ======================= ANSWER PAGE =============================
@app.route('/answer', methods=['GET', 'POST'])
def answer(): 
	if request.method == 'POST': 
		if 'q_selection' in request.form:
			selectedQuestion = answerQuestions.getSelectedQuestion(request.form['q_selection']) # pass in the id
			if selectedQuestion:
				return render_template('answerQuestions.html', selection=selectedQuestion)
			else: 
				return render_template('answerQuestions.html', error="ERROR: couldn't find selected question in the database")
		if 'save' in request.form: # save the answer
			answerQuestions.updateAnswer(request.form['id'], request.form['answer'], "save")
		if 'publish' in request.form: # publish the answer
			answerQuestions.updateAnswer(request.form['id'], request.form['answer'], "publish")
	qs = answerQuestions.getUnpublishedQuestions()
	if qs: # if there are questions to answer, render the template with those questions
		return render_template('answerQuestions.html', questions=qs)
	else: # render the page with an info text
		return render_template('answerQuestions.html', info="There are no questions to answer at this time.")



if __name__ == '__main__':
	app.run(debug=True)


# to allow requests to be treated as such
with app.test_request_context():
	url_for('static', filename='index.html') # for dev





