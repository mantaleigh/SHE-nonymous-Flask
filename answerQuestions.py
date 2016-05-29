#!/usr/local/bin/python2.7

'''
Author: Samantha Voigt
answerQuestions.py

TODO: Write a description of the file

TODO: Color in-progress and not-started questions differently
TODO: Count number of unanswered questions and display


'''

import MySQLdb
import dbConnect


def getUnpublishedQuestions(): 
	'''
		Returns a list of the questions if there are questions to answer, otherwise returns False.
	'''
	conn = dbConnect.connect()
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	statement = "SELECT DATE_FORMAT(ts, '%W %M %d, %Y') as formatted_ts, question, answer, status, id FROM questions WHERE status='not-started' OR status='in-progress' ORDER BY ts DESC;"
	curs.execute(statement)

	questions = []
	count = 0
	while True:
		row = curs.fetchone()
		if row == None: 
			if count > 0: # there were questions to answer
				return questions
			else: 
				return False
		count+=1
		row['ts'] = row['formatted_ts'] # rename formatted_ts to be ts
		questions.append(row)

def getSelectedQuestion(id): 
	'''
		Returns False if the question with the requested id does not exist in the database, returns the question's row otherwise.
	'''

	conn = dbConnect.connect()
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	statement = "SELECT * FROM questions WHERE id=%s"
	curs.execute(statement, id)
	row = curs.fetchone()
	if row: # only one result
		return row
	else: 
		return False # shouldn't happen


def updateAnswer(q_id, answer, update_type): 
	'''
	Adds the provided question to the questions table in the given database. 
	'''
	conn = dbConnect.connect()
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	statement = "SELECT * FROM questions WHERE id=%s"
	curs.execute(statement, (q_id,))
	row = curs.fetchone() # only one result
	timestamp = row['ts']
	# timestamp automatically changes on update - so you have to replace it with the old value
	if update_type == 'publish':
		statement = "update questions set status='completed', answer=%s, ts=%s where id=%s"
		# change the status to completed
	if update_type == 'save': 
		statement = "update questions set status='in-progress', answer=%s, ts=%s where id=%s"
		# change the status to in-progress
	curs.execute(statement, (answer, timestamp, q_id))

