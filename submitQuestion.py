#!/usr/local/bin/python2.7

'''
Author: Samantha Voigt
submitQuestion.py

TODO: Write a description of the file

'''

import MySQLdb
import dbConnect

def addQuestion(question): 
	'''
	Adds the provided question to the questions table in the given database. 
	'''
	conn = dbConnect.connect()
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	statement = "INSERT INTO questions (question, status) VALUES (%s, 'not-started');"
	curs.execute(statement, (question,))
