'''
Author: Samantha Voigt
index.py

'''

import MySQLdb
import dbConnect

def getQuestions(): 
	'''
	Takes in the current database as a string and a boolean value representing whether or not a SHE is currently logged in. 

	Returns a list (ul) string of all of the questions in the questions table of the database
	If a SHE is logged in, this list features <edit> buttons, otherwise, it is just a simple list
	'''
	conn = dbConnect.connect()
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	statement = "SELECT DATE_FORMAT(ts, '%W %M %d, %Y') as formatted_ts, question, answer, id FROM questions WHERE status='completed' ORDER BY ts DESC;"
	curs.execute(statement)
	questions = []
	while True:
		row = curs.fetchone()
		if row == None: 
			return questions
		row['ts'] = row['formatted_ts'] # rename formatted_ts to be ts
		questions.append(row)

def getQuestionsPaginated(loggedIn, page): 
	'''
	Takes in the current database as a string, a boolean value representing whether or not a SHE is currently logged in, and the question number to start on. 

	Returns a list (ul) string of the questions in the questions table of the database starting from the given start parameter until 10 questions past that. 
	If a SHE is logged in, this list features <edit> buttons, otherwise, it is just a simple list
	'''

	start = (page - 1) * 10 # convert the page value to a "start" value

	conn = dbConnect.connect()
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries

	try: 
		fstart = int(start)
		statement = "SELECT DATE_FORMAT(ts, '%W %M %d, %Y') AS formatted_ts, question, answer, id FROM questions WHERE status='completed' ORDER BY ts DESC LIMIT {start}, 10;".format(start=fstart)
		curs.execute(statement)
		lines = []
		lines.append("<ul class='list-group'>")
		while True:
			row = curs.fetchone()
			if row == None: 
				lines.append("</ul>")
				return "\n".join(lines)
			row['ts'] = row['formatted_ts'] # rename formatted_ts to be ts
			if loggedIn: # add the 'edit' button if a SHE is logged in
				lines.append("<li class='list-group-item'><span class='question'>{question}</span><br><br><span class='answer'>{ans}</span><br><br><a class='btn btn-primary' href='answerQuestions.cgi?questionSubmit=True&q_selection={id}' role='button'>Edit Answer</a><br><span class='timestamp'>Asked on: {ts}</span>".format(ts=row['ts'], question=row['question'], ans=row['answer'], id=row['id']))
			else:
				lines.append("<li class='list-group-item'><span class='question'>{question}</span><br><br><span class='answer'>{ans}</span><br><br><span class='timestamp'>Asked on: {ts}</span>".format(ts=row['ts'], question=row['question'], ans=row['answer']))
	except ValueError: # except for when start isn't something that can be parsed into an int
		return "There was an error"


def getCompletedCount(): 
	'''
	Returns the number of questions in the questions table for purposes of pagination.
	'''

	conn = dbConnect.connect()
	curs = conn.cursor(MySQLdb.cursors.DictCursor)

	statement = "SELECT count(*) AS total FROM questions where status='completed';"
	curs.execute(statement)
	row = curs.fetchone()
	return row['total']