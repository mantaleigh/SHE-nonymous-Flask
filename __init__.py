
from flask import Flask, url_for, render_template, request, flash
import home, submitQuestion


app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html', questions=home.getQuestions())

@app.route('/submit', methods=['GET', 'POST'])
def submit():
	if request.method == 'POST': 
		ques = request.form['question']
		ques = ques.replace('\n', '<br />')
		submitQuestion.addQuestion(ques)
		return render_template('submitQuestion.html', success="Thank you! Your question has been submitted successfully.")
	return render_template('submitQuestion.html')

@app.route('/answer', methods=['GET', 'POST'])
def answer(): 
	return render_template('answerQuestions.html')

if __name__ == '__main__':
	app.run(debug=True)

# to allow requests to be treated as such
with app.test_request_context():
	url_for('static', filename='index.html') # for dev