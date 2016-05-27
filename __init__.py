from flask import Flask, url_for, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', rightLinks="<li>none rn", message="", allQuestions="<p>Test questions!</p>", pagerButtons="")

@app.route('/hello')
def hello():
    return 'Hello World'

if __name__ == '__main__':
    app.run(debug=True)

# to allow requests to be treated as such
with app.test_request_context():
	url_for('static', filename='index.html') # for dev